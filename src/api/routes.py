from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.models.schemas import EmailQuery, Feedback
from src.core.email_service import email_service
from src.core.ai_service import ai_service
from src.db.mongodb import mongo_db
from src.utils.logging import logger

router = APIRouter()

def process_email(subject: str, email_body: str, sender_email: str):
    ai_response, response_time = ai_service.generate_response(email_body)
    response_data = {
        "subject": subject,
        "email_body": email_body,
        "sender_email": sender_email,
        "ai_response": ai_response,
        "response_time": response_time,
        "accuracy": 4,  # TODO: Add dynamic accuracy
        "feedback": None,
        "email_sent": False
    }
    response_id = mongo_db.insert_response(response_data)
    email_service.send_email(subject, ai_response, sender_email)
    mongo_db.update_response(response_id, {"email_sent": True})
    logger.info(f"Processed email from {sender_email} with ID: {response_id}")

@router.on_event("startup")
async def schedule_email_checks():
    import asyncio
    async def check_emails_periodically():
        while True:
            logger.info("Starting email check cycle")
            email_service.process_incoming_emails(process_email)
            await asyncio.sleep(60)
    asyncio.create_task(check_emails_periodically())
    logger.info("Email check scheduler started")

@router.post("/generate-response")
async def generate_response(query: EmailQuery, background_tasks: BackgroundTasks):
    logger.info(f"Received manual request from {query.sender_email}")
    try:
        ai_response, response_time = ai_service.generate_response(query.email_body)
        response_data = {
            "subject": query.subject,
            "email_body": query.email_body,
            "sender_email": query.sender_email,
            "ai_response": ai_response,
            "response_time": response_time,
            "accuracy": 4,  # TODO: Add dynamic accuracy
            "feedback": None,
            "email_sent": False
        }
        response_id = mongo_db.insert_response(response_data)
        background_tasks.add_task(email_service.send_email, query.subject, ai_response, query.sender_email)
        background_tasks.add_task(mongo_db.update_response, response_id, {"email_sent": True})
        return {"status": "Response generated successfully", "response_id": response_id}
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/responses/{response_id}")
async def get_response(response_id: str):
    logger.info(f"Fetching response with ID: {response_id}")
    response = mongo_db.find_response(response_id)
    if response:
        logger.info(f"Retrieved response with ID: {response_id}")
        return response
    logger.warning(f"Response not found for ID: {response_id}")
    raise HTTPException(status_code=404, detail="Response not found")

@router.post("/feedback")
async def submit_feedback(feedback: Feedback):
    logger.info(f"Submitting feedback for ID: {feedback.response_id}")
    update_data = {
        "feedback": {"rating": feedback.rating, "comment": feedback.comment},
        "accuracy": feedback.rating
    }
    result = mongo_db.update_response(feedback.response_id, update_data)
    if result:
        logger.info(f"Feedback submitted for ID: {feedback.response_id}")
        return {"message": "Feedback submitted successfully"}
    logger.warning(f"Response not found for feedback ID: {feedback.response_id}")
    raise HTTPException(status_code=404, detail="Response not found")

@router.get("/")
async def root():
    return {"status": "Email Response Agent v5.0 with MongoDB Atlas and Feedback is running"}