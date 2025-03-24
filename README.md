
# 🚀 AI-Powered Email Response Agent 🌟

## ✨ Overview
Welcome to the **AI-Powered Email Response Agent**! This is a 🔥 FastAPI-based app that automates email replies with the power of AI! Using Hugging Face’s `zephyr-7b-beta` model via `InferenceClient`, it crafts professional responses, integrates with Gmail 📧 (IMAP + SMTP), and stores everything in MongoDB Atlas ☁️. Plus, it comes with a slick REST API for manual control and feedback. Watch it blast off every 60 seconds to check your inbox and respond like a pro! 🚀

Built with a modular, production-ready vibe—complete with logging 📜, error handling ⚡, and background task magic ✨.

---

## 🌟 Features
- **📥 Auto Email Magic**: Scans your Gmail inbox every minute for unread emails, generates AI replies, and sends them back—boom! 💥
- **🧠 AI Smarts**: Powered by Hugging Face’s `zephyr-7b-beta` for top-notch customer support responses.
- **💾 Data Vault**: Stores email details and responses in MongoDB Atlas with unique IDs.
- **🌐 REST API**:
  - `POST /generate-response`: Fire off a custom email reply! 📤
  - `GET /responses/{response_id}`: Peek at a stored response. 👀
  - `POST /feedback`: Rate and comment on replies. ⭐
  - `GET /`: Check if the engine’s running! ✅
- **📝 Logging**: Every move is logged in `app.log` for easy tracking.
- **🛡️ Error Proof**: Retry logic keeps MongoDB and email sending rock-solid.

---

## 🛠️ Requirements
### Software
- **Python**: 3.9+ 🐍
- **Conda**: For environment awesomeness (optional) 🌍
- **Git**: If you’re cloning this bad boy (optional) 🌿

### Services
- **Gmail**: 
  - Enable IMAP in settings. 📬
  - Grab an [App Password](https://support.google.com/accounts/answer/185833) if 2FA’s on. 🔑
- **Hugging Face**: 
  - Snag an API key from [Hugging Face](https://huggingface.co/settings/tokens). 🤗
  - Ensure access to `HuggingFaceH4/zephyr-7b-beta`. 🚀
- **MongoDB Atlas**: 
  - Set up a cluster and get your URI. ☁️
  - Whitelist your IP for access. 🔐

### Dependencies
Check `requirements.txt`:
fastapi==0.95.1
pydantic==1.10.14
huggingface-hub==0.23.4
langchain==0.0.154
pymongo==4.3.3
python-dotenv==1.0.0
uvicorn==0.21.1
aiohttp==3.8.4


## 🚀 Setup
1. **Clone It**:
   ```bash
   git clone <repo-url>
   cd email_response_agent
Create Your Space: With Conda:

conda create -n emailresponse python=3.9
conda activate emailresponse
Or venv:

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
Load the Arsenal:

pip install -r requirements.txt
Set the Controls: Create a .env file:

EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
HUGGINGFACE_API_KEY=your-hf-api-key
COMPANY_NAME=Tech Innovators Inc
AGENT_NAME=support team
MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/?retryWrites=true&w=majority
Launch!:

uvicorn main:app --reload
Liftoff at http://127.0.0.1:8000! 🌍
🎉 Usage
Auto Mode
Watches your inbox every 60s, responds with AI flair, and logs it all! ⚡

API Fun
Root Check:

GET http://127.0.0.1:8000/
Response: {"status": "Email Response Agent v5.0 with MongoDB Atlas and Feedback is running"} ✅
Generate a Reply:

POST http://127.0.0.1:8000/generate-response
Content-Type: application/json
{"subject": "Test", "email_body": "Hi there!", "sender_email": "test@example.com"}
Response: {"status": "Response generated successfully", "response_id": "<id>"} 🚀
Fetch a Response:

GET http://127.0.0.1:8000/responses/<response_id>
Response: Your stored email data! 📜
Give Feedback:

POST http://127.0.0.1:8000/feedback
Content-Type: application/json
{"response_id": "<id>", "rating": 4, "comment": "Great job!"}
Response: {"message": "Feedback submitted successfully"} ⭐
🌌 MongoDB Schema
json

Collapse

Wrap

Copy
{
    "_id": "67e17c8d827c73718d713e21",
    "subject": "inquiry about product availability",
    "email_body": "Is the XYZ product available?",
    "sender_email": "ksaikiranXXX@gmail.com",
    "ai_response": "Hello, thanks for asking about XYZ...",
    "response_time": 2.54,
    "accuracy": 4,
    "timestamp": "2025-03-24T15:38:51Z",
    "feedback": null,
    "email_sent": true
}
📜 Logs in Action
See the magic happen in app.log:

2025-03-24 21:08:51,000 - src.utils.logging - INFO - Processing email from sai kiran <ksaikiran129@gmail.com> with subject: inquiry about product availability
2025-03-24 21:08:53,536 - src.utils.logging - INFO - AI response generated in 2.54s
2025-03-24 21:08:57,965 - src.utils.logging - INFO - Response sent to sai kiran <ksaikiran129@gmail.com>
Every step is tracked for your cosmic journey! 🌠

💡 Tips & Tricks
Bounces Beware: It replies to everything—even mailer-daemon bounce emails! Add a filter in email_service.py to skip those if you want. 🚫
Speed Boost: AI responses take 2-7 seconds—pretty zippy for intergalactic support! ⚡
Lock It Down: Keep .env safe—don’t let it blast off to GitHub! 🔒
🛠️ Troubleshooting
📧 Email Woes: Double-check EMAIL_ADDRESS and EMAIL_PASSWORD. Ensure IMAP’s on in Gmail settings.
☁️ MongoDB Hiccups: Verify MONGO_URI and your IP’s whitelisted in Atlas.
🤗 AI Glitches: Confirm your Hugging Face API key and model access.
🔍 Logs Are Your Friend: Peek at app.log for clues when things go sideways.
🌍 Contributing
Got a stellar idea? Fork this repo, tweak it, and send a pull request! Add filters, supercharge the AI, or share your feedback—let’s make it out-of-this-world! 🌌

⚖️ License
This project’s a free-for-all for learning and fun! No license attached—use it wisely. For commercial missions, check Hugging Face and MongoDB Atlas terms. 🚀
