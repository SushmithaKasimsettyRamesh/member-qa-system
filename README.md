Note: This project was developed as part of a coding task for evaluation purposes. The implementation, design decisions, and code are my original work. The system is intended for demonstration and internal review only. Please do not reuse or redistribute the data or code without proper authorization.

Member QA System

This repository contains a simple question-answering system that allows users to ask natural-language questions about member data. The system fetches data from a public API, processes it, and provides answers using OpenAI's language models. The project includes a backend API and a Streamlit-based frontend.

Features

Fetches member messages from a paginated public API.

Caches messages locally to improve performance and reduce repeated API calls.

Provides a FastAPI endpoint to answer natural-language questions.

Interactive frontend built with Streamlit for easy exploration.

Endpoints:

/ask (POST) - Ask a question and receive an AI-generated answer.

/stats (GET) - View cached message statistics, including total messages and unique users.

/refresh (POST) - Force-refresh cached messages from the API.

Technologies Used

FastAPI – Backend API server.

Streamlit – Interactive web frontend for asking questions.

OpenAI API – Language model for generating answers.

Python-dotenv – Loading environment variables like the OpenAI API key.

Requests – Fetching data from the public API.

Pydantic – Data validation for API requests and responses.

Logging – Tracks data fetching, caching, and errors.

Pagination logic for handling large API responses.

Setup Instructions

Clone the repository:

git clone https://github.com/your-username/member-qa-system.git
cd member-qa-system


Create a virtual environment and install dependencies:

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux

pip install -r requirements.txt


Create a .env file with your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key

Running the System

Start the backend API:

uvicorn app.app_main:app --reload


The API will run on http://localhost:8000.

Start the Streamlit frontend:

streamlit run streamlit_app.py


The frontend will run on http://localhost:8502 by default.

Ask natural-language questions, such as:

When is Layla planning her trip to London

How many cars does Vikram Desai have

What are Amira's favorite restaurants

What activities is Marcus interested in

Data and Caching

Messages are fetched from the public API and cached locally for faster responses.

/stats endpoint provides insights about the cached messages, including:

Total number of messages

Number of unique users

Date range of messages

Cache can be refreshed manually using the /refresh endpoint.

Data Insights

After analyzing the member messages dataset from the public API, several observations were made:

Message completeness: Most messages include user names, message text, and timestamps. A small fraction of entries had missing or empty fields, indicating occasional incomplete submissions.

User activity distribution: The dataset shows that some members are highly active, contributing multiple messages, while others have few or no messages. This uneven activity could impact question-answering coverage.

Timestamps consistency: Message timestamps are generally consistent, but a few entries had unusual dates that appear out of chronological order. These may be due to system errors or delayed submissions.

Duplicate entries: A few repeated messages from the same user were observed, which may slightly skew any aggregate statistics or insights.

Overall, the dataset is largely clean and usable, with minor inconsistencies that are typical in real-world data. These observations informed the design of the question-answering system, ensuring that missing or inconsistent data does not break the service.

Notes

The system is designed for internal exploration and testing. Please do not reuse or redistribute the data without proper authorization.

AI-generated answers depend on the available messages. If data is missing, the system will return a polite fallback response.

All processing is done locally or via OpenAI’s API; no member data is stored externally.

Optional Analysis

You can analyze the dataset for anomalies or inconsistencies using the /stats endpoint or by inspecting the cached messages.

Future enhancements may include better data cleaning, ranking answers, or advanced analytics.
