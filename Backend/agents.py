import os
import re
import json
import aiohttp
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"  # or any other model you have pulled in Ollama

async def _get_ollama_response(prompt: str) -> str:
    """Helper function to get response from Ollama"""
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        try:
            async with session.post(OLLAMA_URL, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('response', '')
                else:
                    raise HTTPException(status_code=response.status, detail="Ollama API error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling Ollama: {str(e)}")

async def analyze_prompt_intent(prompt: str) -> dict:
    """Determine whether the prompt is requesting data transformation, visualization, or statistical analysis."""
    response_format = {
        "intent": "statistical",
        "reason": "Prompt requests statistical analysis",
        "visualization_type": None,
        "transformation_type": None,
        "statistical_type": "correlation"
    }

    input_text = f"""Analyze the following prompt and determine if it's requesting data transformation, visualization, or statistical analysis:

Prompt: {prompt}

Provide a JSON response with:
1. intent: Either 'visualization', 'transformation', or 'statistical'
2. reason: Brief explanation of why this classification was chosen
3. visualization_type: If intent is 'visualization', specify the chart type ('bar', 'line', 'pie', 'scatter', 'area'), else None
4. transformation_type: If intent is 'transformation', specify the operation type ('aggregate', 'filter', 'join', 'compute'), else None
5. statistical_type: If intent is 'statistical', specify the test type ('correlation', 'ttest', 'ztest', 'chi_square'), else None

Example format:
{response_format}"""

    try:
        response = await _get_ollama_response(input_text)
        # Extract JSON from the response
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise HTTPException(status_code=500, detail="Could not parse JSON from response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing prompt intent: {str(e)}")

async def get_chart_config(prompt: str, columns: list) -> dict:
    """Generate chart configuration based on natural language prompt."""
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

Example format:
{response_format}"""

    try:
        response = await _get_ollama_response(input_text)
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise HTTPException(status_code=500, detail="Could not parse JSON from response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart configuration: {str(e)}")

async def get_transformation_code(prompt: str, columns: list) -> str:
    """Generate PySpark transformation code based on prompt."""
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
        response = await _get_ollama_response(input_text)
        code_match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
        code = code_match.group(1) if code_match else response
        return code
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating transformation code: {str(e)}")

async def get_statistical_code(prompt: str, columns: list) -> str:
    """Generate PySpark code for statistical analysis based on prompt."""
    input_text = f"""Write PySpark code to perform the following statistical analysis:

{prompt}

Available columns: {', '.join(columns)}

Requirements:
1. Use PySpark SQL functions (pyspark.sql.functions as F)
2. Include proper statistical computations
3. Store result in 'stat_df'
4. Return both the statistical results and any relevant metrics
5. Handle null values appropriately
6. Include interpretation of results

Available imports:
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
import numpy as np
from scipy import stats

Example formats:

For correlation:
```python
# Create vector of features
assembler = VectorAssembler(inputCols=['col1', 'col2'], outputCol='features')
df_vector = assembler.transform(df)
# Calculate correlation
correlation = Correlation.corr(df_vector, 'features').collect()[0][0]
stat_df = spark.createDataFrame([(correlation.toArray().tolist())], ['correlation_matrix'])
```

For t-test:
```python
# Calculate t-test using pandas
pandas_df = df.select('group1', 'group2').toPandas()
t_stat, p_value = stats.ttest_ind(pandas_df['group1'], pandas_df['group2'])
stat_df = spark.createDataFrame([(float(t_stat), float(p_value))], ['t_statistic', 'p_value'])
```

Provide only the code, no explanations."""

    try:
        response = await _get_ollama_response(input_text)
        code_match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
        code = code_match.group(1) if code_match else response
        return code
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating statistical code: {str(e)}")
