Member QA System

Note: This project was developed as part of a coding task for evaluation purposes. The implementation, design decisions, and code are my original work. The system is intended for demonstration and internal review only. Please do not reuse or redistribute the data or code without proper authorization.

Overview

This repository contains a question-answering system that allows users to ask natural-language questions about member data. The system fetches data from a public API, processes it, and provides answers using OpenAI's language models. It includes a backend API and a Streamlit frontend for interactive use.

Features

Fetches member messages from a paginated public API.

Caches messages locally to improve performance and reduce repeated API calls.

Provides a FastAPI endpoint to answer natural-language questions.

Interactive frontend built with Streamlit for easy exploration.

Endpoints:

/ask (POST) – Ask a question and receive an AI-generated answer.

/stats (GET) – View cached message statistics, including total messages and unique users.

/refresh (POST) – Force-refresh cached messages from the API.

Technologies Used

FastAPI – Backend API server.

Streamlit – Interactive frontend for question answering.

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
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt


Create a .env file with your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key

Running the System

Start the backend API:

uvicorn app.app_main:app --reload


The API will run on http://localhost:8000
.

Start the Streamlit frontend:

streamlit run streamlit_app.py


The frontend will run on http://localhost:8502
 by default.

Ask natural-language questions such as:

When is Layla planning her trip to London

How many cars does Vikram Desai have

What are Amira's favorite restaurants

What activities is Marcus interested in

Data and Caching

Messages are fetched from the public API and cached locally for faster responses.

The /stats endpoint provides insights about the cached messages, including total messages, unique users, and date range.

Cache can be refreshed manually using the /refresh endpoint.

Data Insights

Analysis of the member messages dataset revealed:

Message completeness: Most messages include user names, text, and timestamps, with occasional missing fields.

User activity distribution: Some members are highly active, while others have few messages.

Timestamp consistency: Mostly consistent, with a few out-of-order entries.

Duplicate entries: A few repeated messages exist, slightly affecting statistics.

The dataset is largely clean and usable, with minor inconsistencies typical in real-world data. These insights informed caching and question-answering logic.

Design Notes / Approach

Data fetching: Implemented a paginated API fetcher with caching to minimize repeated API calls and reduce latency.

Question-answering engine: Uses OpenAI’s language models to process member messages and generate answers.

Context formatting: Messages are formatted into a readable text block to provide context for AI inference.

FastAPI backend: Handles /ask, /stats, and /refresh endpoints for reliable service.

Streamlit frontend: Provides an interactive interface for exploring the system without coding.

Error handling: Includes graceful fallbacks when messages are missing or the API is unavailable.

Alternative approaches considered:

Storing messages in a database for more advanced queries.

Using embeddings or semantic search for more accurate question-answering.

Ranking multiple candidate answers for improved relevance.

Notes

Designed for internal exploration and testing; do not reuse data or code without authorization.

AI answers depend on cached messages; missing data may result in fallback responses.

All processing occurs locally or via OpenAI’s API; no member data is stored externally.

Optional Analysis

Dataset anomalies and statistics can be explored via /stats or by inspecting cached messages.

Future improvements could include advanced analytics, better data cleaning, and answer ranking.
