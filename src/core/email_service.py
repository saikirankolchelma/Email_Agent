import smtplib
import imaplib
from email import message_from_bytes
from email.mime.text import MIMEText
from src.config.settings import settings
from src.utils.logging import logger

class EmailService:
    def __init__(self):
        self.processed_emails = set()

    def send_email(self, subject: str, body: str, recipient: str) -> bool:
        logger.info(f"Attempting to send email to {recipient}")
        try:
            msg = MIMEText(body)
            msg['Subject'] = f"Re: {subject}"
            msg['From'] = f"{settings.AGENT_NAME} <{settings.EMAIL_ADDRESS}>"
            msg['To'] = recipient
            
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                server.sendmail(settings.EMAIL_ADDRESS, [recipient], msg.as_string())
            logger.info(f"Response sent to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {str(e)}")
            raise

    def process_incoming_emails(self, generate_response_callback):
        logger.info("Processing incoming emails")
        try:
            mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
            mail.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            logger.info("Logged into IMAP server successfully")
            mail.select("inbox")
            
            status, messages = mail.search(None, 'UNSEEN')
            if status != "OK" or not messages[0]:
                logger.info("No unseen emails found")
                return
            
            for num in messages[0].split():
                try:
                    logger.info(f"Fetching email {num}")
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    email_msg = message_from_bytes(msg_data[0][1])
                    
                    message_id = email_msg["Message-ID"]
                    if message_id in self.processed_emails:
                        logger.info(f"Skipping already processed email: {message_id}")
                        continue
                    self.processed_emails.add(message_id)
                    
                    body = self._extract_body(email_msg)
                    sender_email = email_msg["From"]
                    subject = email_msg["Subject"] or "No Subject"
                    logger.info(f"Processing email from {sender_email} with subject: {subject}")
                    
                    generate_response_callback(subject, body, sender_email)
                except Exception as e:
                    logger.error(f"Failed to process email {num}: {str(e)}")
        except Exception as e:
            logger.error(f"Email processing error: {str(e)}")
        finally:
            try:
                mail.logout()
                logger.info("Logged out of IMAP server")
            except:
                pass

    def _extract_body(self, email_msg) -> str:
        body = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                content_type = part.get_content_type()
                if content_type in ["text/plain", "text/html"]:
                    body_content = part.get_payload(decode=True).decode(errors='ignore')
                    body = body_content.replace("=", "").replace("=20", " ")
                    break
        else:
            body = email_msg.get_payload(decode=True).decode(errors='ignore')
            body = body.replace("=", "").replace("=20", " ")
        return body.strip()

email_service = EmailService()