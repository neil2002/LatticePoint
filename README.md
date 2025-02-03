# Datafy AI Data Analysis Dashboard

A sophisticated web application that combines data processing, analysis, and visualization capabilities with an intuitive dashboard builder interface. Built with Vue.js and FastAPI, this platform enables users to create custom visualizations and perform complex analyses through a user-friendly interface.

## Project Overview

This application enables users to:
- Create custom data visualizations through a drag-and-drop interface
- Process and analyze data through natural language queries
- Build sophisticated dashboards without writing code
- Perform complex analyses through PySpark integration
- Access AI-powered insights through Ollama integration

## Demo Video

Watch our demo video to see the application in action:


<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>



## Workflow

![Interactive Data Analysis Workflow](./workflow.png)

## Dashboard Builder

The Dashboard Builder provides:
- Drag-and-drop interface for creating custom dashboards
- Multiple chart types and visualization options
- Real-time data updates and previews
- Customizable layouts and settings
- Interactive data filtering
- Save and share functionality
- Version history management

### Using the Dashboard Builder

1. Access the dashboard builder interface
2. Start with a blank canvas
3. Add visualization components through drag-and-drop
4. Configure data sources and chart settings
5. Use natural language queries for data processing
6. Save and share your dashboard configurations

## Technologies Used

### Frontend
- Vue.js 3.5 for the user interface
- Pinia for state management
- Vue Router for navigation
- Chart.js for interactive data visualization
- Tailwind CSS with DaisyUI for styling

### Backend
- FastAPI for the REST API implementation
- PySpark for distributed data processing
- Ollama for local AI model integration
- Python 3.8+ for backend services

## Prerequisites

- Node.js (version 18.0.0 or higher)
- Python (version 3.8 or higher)
- Java Runtime Environment (JRE) for PySpark
- Ollama installation

## Installation

### Frontend Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd [project-directory]
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

### Backend Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### Ollama Setup

1. Install Ollama:

For Unix-based systems:
```bash
curl https://ollama.ai/install.sh | sh
```

For Windows:
Download and install from https://ollama.ai/download

2. Pull required model:
```bash
ollama pull deepseek-r1:8b
```

## API Structure

The backend API provides these key endpoints:
- `/process` - Handles data processing requests
- `/analyze` - Manages analysis operations
- `/dashboard` - Controls dashboard configurations

## Development

For building production assets:
```bash
npm run build
```

For running tests:
```bash
npm run test
```

## Contributing

We welcome contributions to improve the platform. Please review our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License.

## Support

For technical support or questions, please create an issue in the GitHub repository. Our team actively monitors and responds to reported issues.
