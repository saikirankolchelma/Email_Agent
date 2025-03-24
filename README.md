<<<<<<< HEAD
# AI-Powered Email Response Agent

## Overview
A FastAPI-based system that automates email responses using Hugging Face LLM and LangChain, with MongoDB for data storage.

## Setup
1. Clone the repository: `git clone <repo-link>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` (see `.env.example`)
4. Run the app: `uvicorn main:app --reload`

## Requirements
- Python 3.9+
- MongoDB Atlas account
- Hugging Face API key
- Gmail account with app password

## Usage
- **POST /generate-response**: Submit an email query.
- **GET /responses/{response_id}**: Retrieve a response.
- **POST /feedback**: Submit feedback.
- **GET /stats**: View response stats (optional).

## MongoDB Schema
- `_id`: ObjectId
- `subject`: str
- `email_body`: str
- `sender_email`: str
- `ai_response`: str
- `response_time`: float
- `accuracy`: int (1-5)
- `timestamp`: datetime
- `feedback`: { "rating": int, "comment": str } | null
- `email_sent`: bool

## Demo Video
[Link to video]

## Notes
- Emails are checked every 60 seconds from the inbox.
- Feedback updates the accuracy score.
=======
# Email_response_Agent
>>>>>>> 5c51b0dbc088906c56fdc5517cc29aaa8a2e1506
