import smtplib
import logging

from os import getenv
from base64 import b64decode
from email.message import EmailMessage
from json import loads as json_loads
from typing import Optional


logging.basicConfig(
    level=getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def decode_pubsub_message(event: Optional[dict]) -> str:
    if not event or "data" not in event:
        return "[]"
    return b64decode(event["data"]).decode("utf-8")


def format_job_text(job: dict) -> str:
    title = job.get("job_title", "Sem título")
    company = job.get("company", "N/A")
    location = "Remoto" if job.get("job_is_remote") else job.get("job_location", "N/A")

    apply_link = job.get("job_apply_link")
    google_link = job.get("job_google_link")

    description = job.get("description", "")[:250].strip()

    return f"""
        📌 {title}
        🏢 Empresa: {company}
        📍 Local: {location}

        📝 Resumo:
        {description}...

        🔗 Candidatar-se:
        {apply_link or google_link}
    """

def format_jobs_text(jobs: list[dict]) -> str:
    return "\n\n" + "\n".join(f"{i+1}) {format_job_text(job)}" for i, job in enumerate(jobs))

def build_email(message: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "Job Processing Summary"
    msg["From"] = getenv("EMAIL_FROM")
    msg["To"] = getenv("EMAIL_TO")

    msg.set_content(
        f"""
        O job de busca de vagas foi executado com sucesso.

        {format_jobs_text(json_loads(message))}

        — Cloud Run Job bot
        """
    )
    return msg


def send_email(msg: EmailMessage) -> None:
    SMTP_HOST = getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = getenv("SMTP_PORT", 465)
    email_from = getenv("EMAIL_FROM")
    email_password = getenv("EMAIL_PASSWORD")
    
    logging.info(f"Send email to {msg.get('To')} from {SMTP_HOST}:{SMTP_PORT}....")
    if not email_from or not email_password or not msg.get('To'):
        logging.error("EMAIL_FROM or EMAIL_PASSWORD or EMAIL_TO not defined in environment variables.")
        raise RuntimeError("EMAIL_FROM or EMAIL_PASSWORD or EMAIL_TO not defined in environment variables.")

    logging.info("Connecting to SMTP server...")
    logging.debug(f"Message content: {msg.get_content()}")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(email_from, email_password)
        smtp.send_message(msg)
        
        logging.info("Email sent successfully.")

def main(event=None, context=None) -> None:
    message = decode_pubsub_message(event)
    email = build_email(message)
    send_email(email)

if __name__ == "__main__":
    main()
