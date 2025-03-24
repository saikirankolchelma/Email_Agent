from langchain.prompts import PromptTemplate  # Use PromptTemplate instead of ChatPromptTemplate
from huggingface_hub import InferenceClient
from src.config.settings import settings
from src.utils.logging import logger
import time

class AIService:
    def __init__(self):
        self.client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=settings.HUGGINGFACE_API_KEY)
        self.prompt = PromptTemplate(
            input_variables=["company", "email_body", "agent_name"],
            template="""
            You are a customer support agent for {company}.
            Generate a response that:
            1. Acknowledges the customer's query: {email_body}
            2. Provides a helpful and professional answer
            3. Offers further assistance if needed

            Email content:
            ---
            {email_body}
            ---
            Sign the response as:
            Best regards,
            {agent_name}
            Customer Support Team
            {company}
            """
        )
        logger.info("Hugging Face client initialized successfully")

    def generate_response(self, email_body: str) -> tuple[str, float]:
        logger.info("Generating AI response")
        try:
            start_time = time.time()
            formatted_prompt = self.prompt.format(
                email_body=email_body,
                company=settings.COMPANY_NAME,
                agent_name=settings.AGENT_NAME
            )
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": formatted_prompt}],
                max_tokens=256,
                temperature=0.7
            )
            ai_response = response.choices[0].message.content
            response_time = round(time.time() - start_time, 2)
            logger.info(f"AI response generated in {response_time}s")
            return ai_response, response_time
        except Exception as e:
            logger.error(f"AI response generation failed: {str(e)}")
            raise

ai_service = AIService()