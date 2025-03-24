from pydantic import BaseModel
from typing import Optional

class EmailQuery(BaseModel):
    subject: str
    email_body: str
    sender_email: str

class Feedback(BaseModel):
    response_id: str
    rating: int
    comment: Optional[str] = None