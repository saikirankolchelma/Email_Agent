import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    IMAP_SERVER: str = "imap.gmail.com"
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "your_mail")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "your_app_pasword")
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Tech Innovators Inc")
    AGENT_NAME: str = os.getenv("AGENT_NAME", "support team")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "your_huggingkey")
    MONGO_URI: str = os.getenv("MONGO_URI")
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5

settings = Settings()

if not settings.EMAIL_PASSWORD or not settings.HUGGINGFACE_API_KEY:
    raise ValueError("Missing critical environment variables: EMAIL_PASSWORD or HUGGINGFACE_API_KEY")