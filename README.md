# AI-Powered Data Analysis and Visualization Tool

This project consists of a Vue.js frontend and FastAPI backend that enables users to analyze and visualize data using natural language prompts powered by Google's Gemini AI.

## Project Structure

src/
├── Frontend/ # Vue.js frontend application
└── Backend/   # FastAPI backend service

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm/yarn
- Java Runtime Environment (JRE) for Apache Spark

## Backend Setup

1. Navigate to the Backend directory:
```sh
cd Backend
```
2. Create a virtual environment:
```sh
python -m venv venv
```
3. Activate the virtual environment:
```sh
venv\Scripts\activate
```
4. Install dependencies
```sh
pip install -r requirements.txt
```
5. Create a [`.env` file](./Backend/.env) in the Backend directory:
```markdown
GOOGLE_API_KEY=your_gemini_api_key_here
```
6. Start a Backend Server:
```sh
uvicorn main:app --reload --port 8000
```
The backend will be available at http://localhost:8000

## Frontend Setup

1. Navigate to the Frontend directory:
```sh
cd Frontend
```
2. Install Dependencies:
```sh
npm install
```
3. Start the development server:
```sh
npm run dev
```
The frontend will be available at http://localhost:5173

<!-- Features
File Upload Support:

CSV
Excel (.xlsx, .xls)
JSON
Data Analysis:

Natural language queries for data transformation
PySpark-powered data processing
Automated visualization generation
Visualization Types:

Bar charts
Line charts
Pie charts
Scatter plots
Area charts
Usage
Open http://localhost:5173 in your browser
Upload a data file (CSV/Excel/JSON)
Enter a natural language prompt describing your analysis needs
View the automatically generated visualization or transformed data
Example Prompts
"Show me a bar chart of sales by region"
"Calculate the average revenue by product category"
"Create a line chart showing monthly trends"
"Show me the top 10 customers by revenue"
Technology Stack
Frontend
Vue.js 3
Chart.js
Tailwind CSS
DaisyUI
Vite
Backend
FastAPI
PySpark
Pandas
Google Gemini AI
Python-dotenv
Development
Building for Production
Frontend:

Backend:

Troubleshooting
If you encounter CORS issues:

Ensure the backend CORS settings match your frontend URL
Check if the backend is running on port 8000
File upload issues:

Verify file format is supported
Check file size limits
Visualization not rendering:

Check browser console for errors
Verify data format matches expected schema
License
MIT License

Contributing
Fork the repository
Create your feature branch
Commit your changes
Push to the branch
Create a new Pull Request -->