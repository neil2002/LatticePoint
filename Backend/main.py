from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import os
import re
import google.generativeai as genai
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from dotenv import load_dotenv

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

async def analyze_prompt_intent(prompt: str) -> Dict:
    """Determine whether the prompt is requesting data transformation or visualization."""
    print(f"Analyzing prompt intent for: {prompt}")

    response_format = {
    "intent": "visualization",
    "reason": "Prompt explicitly requests a chart/graph visualization",
    "visualization_type": "bar",
    "transformation_type": None
}

    input_text = f"""Analyze the following prompt and determine if it's requesting data transformation or visualization:

Prompt: {prompt}

Provide a JSON response with:
1. intent: Either 'visualization' or 'transformation'
2. reason: Brief explanation of why this classification was chosen
3. visualization_type: If intent is 'visualization', specify the chart type ('bar', 'line', 'pie', 'scatter', 'area'), else None
4. transformation_type: If intent is 'transformation', specify the operation type ('aggregate', 'filter', 'join', 'compute'), else None
5. Do not null instead use None, because python does not have null

Example response format:
{response_format}

Provide only the JSON response, no explanations."""

    try:
        response = await model.generate_content_async(
            input_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                top_k=40,
            )
        )
        print(f"Intent analysis response: {response.text}")
        json = re.search(r"```json\n(.*?)\n```", response.text, re.DOTALL)
        json = json.group(1) if json else response.text
        print(json)
        return eval(json)
    except Exception as e:
        print(f"Error analyzing prompt intent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing prompt intent: {str(e)}")

async def get_chart_config(prompt: str, columns: List[str]) -> Dict:
    """Generate chart configuration based on natural language prompt."""
    print(f"Generating chart config for prompt: {prompt} with columns: {columns}")
    response_format = {
    "chart_type": "bar",
    "x_axis": "date",
    "y_axis": "sales",
    "aggregation": "sum",
    "title": "Total Sales by Date"
}
    input_text = f"""Based on the following prompt, determine the appropriate chart configuration:

Prompt: {prompt}

Available columns: {', '.join(columns)}

Generate a JSON configuration with:
1. chart_type: 'bar', 'line', 'pie', 'scatter', or 'area'
2. x_axis: column name for x-axis
3. y_axis: column name for y-axis
4. aggregation: 'sum', 'average', 'count', or 'none'
5. title: chart title

Example response format:
{response_format}

Provide only the JSON configuration, no explanations."""

    try:
        response = await model.generate_content_async(
            input_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95,
                top_k=40,
            )
        )
        print(f"Chart config response: {response.text}")
        json = re.search(r"```json\n(.*?)\n```", response.text, re.DOTALL)
        json = json.group(1) if json else response.text
        print(json)
        return eval(json)
    except Exception as e:
        print(f"Error generating chart configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating chart configuration: {str(e)}")

async def get_transformation_code(prompt: str, columns: List[str]) -> str:
    """Generate PySpark transformation code based on prompt."""
    print(f"Generating transformation code for prompt: {prompt} with columns: {columns}")

    columns_context = "Available columns: " + ", ".join(columns)
    input_text = f"""Write Python code to perform the following PySpark DataFrame transformation:

{prompt}

Available columns: {columns_context}

Requirements:
1. Use PySpark DataFrame operations (pyspark.sql.functions as F)
2. Handle missing values appropriately
3. Store result in 'transformed_df'
4. Return a Spark DataFrame
5. Use proper type conversions if needed

Available imports:
- from pyspark.sql import functions as F
- from pyspark.sql.types import *
- datetime

Example format:
```python
transformed_df = df.withColumn('new_column', F.col('column1') * F.col('column2'))
transformed_df = transformed_df.na.fill(0)  # Handle nulls
```

Provide only the code, no explanations."""

    try:
        response = await model.generate_content_async(
            input_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                top_p=0.95,
                top_k=40,
            )
        )
        print(f"Transformation code response: {response.text}")
        code_match = re.search(r"```python\n(.*?)\n```", response.text, re.DOTALL)
        code = code_match.group(1) if code_match else response.text
        print(f"Extracted transformation code: {code}")
        return code
    except Exception as e:
        print(f"Error generating transformation code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating transformation code: {str(e)}")

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
        
        # print(f"Final response: {response}")
        return response
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Temporary file removed: {temp_path}")
