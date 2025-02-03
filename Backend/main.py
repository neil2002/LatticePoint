from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from scipy import stats
import os
import re
import google.generativeai as genai
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import *
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
from dotenv import load_dotenv
from agents import analyze_prompt_intent, get_chart_config, get_transformation_code, get_statistical_code

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini and Spark
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
spark = SparkSession.builder.appName("DataTransformation").getOrCreate()

class ChartConfig(BaseModel):
    x_axis: str
    y_axis: str
    aggregation: str
    chart_type: str
    title: str

def process_chart_data(data: List[Dict], config: Dict) -> Dict:
    """Process data according to chart configuration."""
    print(f"Processing chart data with config: {config}")
    df = pd.DataFrame(data)
    
    # Apply aggregation if specified
    if config['aggregation'] != 'none':
        if config['aggregation'] == 'sum':
            df = df.groupby(config['x_axis'])[config['y_axis']].sum().reset_index()
        elif config['aggregation'] == 'average':
            df = df.groupby(config['x_axis'])[config['y_axis']].mean().reset_index()
        elif config['aggregation'] == 'count':
            df = df.groupby(config['x_axis'])[config['y_axis']].count().reset_index()
    
    print(f"Aggregated data: {df}")
    chart_config = {
        'type': config['chart_type'],
        'data': {
            'labels': df[config['x_axis']].tolist(),
            'datasets': [{
                'label': config['y_axis'],
                'data': df[config['y_axis']].tolist(),
                'backgroundColor': [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                ],
                'borderColor': '#36A2EB',
                'fill': 'true' #config['chart_type'] == 'area'
            }]
        },
        'options': {
            'responsive': 'true',
            'plugins': {
                'title': {
                    'display': 'true',
                    'text': config['title']
                },
                'legend': {
                    'display': 'true'
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': 'true',
                    'title': {
                        'display': 'true',
                        'text': config['y_axis']
                    }
                },
                'x': {
                    'title': {
                        'display': 'true',
                        'text': config['x_axis']
                    }
                }
            }
        }
    }
    
    print(f"Chart configuration generated: {chart_config}")
    return chart_config

def execute_transformation(code: str, df) -> pd.DataFrame:
    """Execute PySpark transformation code."""
    print(f"Executing transformation code:\n{code}")
    try:
        # Create a restricted global environment
        allowed_globals = {
            'spark': spark,
            'F': F,
            'df': df,
            'datetime': datetime
        }
        
        # Execute the code
        exec(code, allowed_globals)
        transformed_df = allowed_globals.get('transformed_df')
        
        if transformed_df is None:
            raise ValueError("Transformation did not produce a result")
        
        print("Transformation successful, resulting DataFrame:")
        transformed_df.show()  # Fix log output
        return transformed_df.toPandas()
    except Exception as e:
        print(f"Error executing transformation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing transformation: {str(e)}")

@app.post("/process")
async def process_data(file: UploadFile = File(...), prompt: str = Form(...)):
    try:
        print(f"Received file: {file.filename} and prompt: {prompt}")
        # Read the file into a Spark DataFrame
        extension = os.path.splitext(file.filename)[-1].lower()
        temp_path = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
        
        with open(temp_path, "wb+") as f:
            f.write(file.file.read())
        
        print(f"Temporary file saved at: {temp_path}")
        
        if extension == '.csv':
            df = spark.read.csv(temp_path, header=True, inferSchema=True)
        elif extension in ['.xlsx', '.xls']:
            pandas_df = pd.read_excel(temp_path)
            df = spark.createDataFrame(pandas_df)
        elif extension == '.json':
            df = spark.read.json(temp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        print(f"Loaded DataFrame with columns: {df.columns}")
        # Clean column names
        for old_col in df.columns:
            new_col = re.sub(r'[^\w\s]', '', old_col).strip().lower().replace(' ', '_')
            df = df.withColumnRenamed(old_col, new_col)
        
        print(f"Cleaned DataFrame columns: {df.columns}")
        # Analyze prompt intent
        intent_analysis = await analyze_prompt_intent(prompt)
        print(f"Intent analysis result: {intent_analysis['intent']}")
        columns = df.columns
        
        if intent_analysis['intent'] == 'visualization':
            # Generate and process visualization
            chart_config = await get_chart_config(prompt, columns)
            pandas_df = df.toPandas()
            visualization = process_chart_data(pandas_df.to_dict('records'), chart_config)
            
            response = {
                "type": "visualization",
                "data": pandas_df.to_dict('records'),
                "visualization": visualization,
                "config": chart_config
            }
        elif intent_analysis['intent'] == 'statistical':
            # Generate and execute statistical analysis code
            statistical_code = await get_statistical_code(prompt, columns)
            
            # Create a restricted global environment
            allowed_globals = {
                'spark': spark,
                'F': F,
                'df': df,
                'np': np,
                'stats': stats,
                'VectorAssembler': VectorAssembler,
                'Correlation': Correlation
            }
            
            # Execute the code
            exec(statistical_code, allowed_globals)
            stat_df = allowed_globals.get('stat_df')
            
            if stat_df is None:
                raise ValueError("Statistical analysis did not produce a result")
            
            # Convert to pandas for response
            result_df = stat_df.toPandas()
            
            response = {
                "type": "statistical",
                "data": result_df.to_dict('records'),
                "statistical_type": intent_analysis['statistical_type']
            }
        else:
            # Generate and execute transformation
            transformation_code = await get_transformation_code(prompt, columns)
            transformed_df = execute_transformation(transformation_code, df)
            
            response = {
                "type": "transformation",
                "data": transformed_df.to_dict('records'),
                "columns": transformed_df.columns.tolist(),
                "rows": len(transformed_df)
            }
        
        return response
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Temporary file removed: {temp_path}")
