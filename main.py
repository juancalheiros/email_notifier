import smtplib
import logging

from os import getenv
from base64 import b64decode
from email.message import EmailMessage
from json import loads as json_loads
from typing import Optional, List, Dict


logging.basicConfig(
    level=getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def decode_pubsub_message(event: Optional[dict]) -> str:
    if not event or "data" not in event:
        return "[]"
    return b64decode(event["data"]).decode("utf-8")


def format_job_text(job: Dict) -> str:
    title = job.get("job_title", "Sem título")
    company = job.get("company", "N/A")
    location = "Remoto" if job.get("job_is_remote") else job.get("job_location", "N/A")

    apply_link = job.get("job_apply_link") or job.get("job_google_link")
    description = job.get("description", "")[:300].strip()

    return (
        f"📌 {title}\n"
        f"🏢 Empresa: {company}\n"
        f"📍 Local: {location}\n\n"
        f"📝 Resumo:\n{description}...\n\n"
        f"🔗 Candidatar-se:\n{apply_link}\n"
    )


def format_search_text(search: Dict) -> str:
    keywords = search.get("keywords", "Busca")
    jobs = search.get("jobs", [])

    if not jobs:
        return f"\n🔍 {keywords}\nNenhuma vaga encontrada.\n"

    jobs_text = "\n".join(
        f"{i+1}) {format_job_text(job)}"
        for i, job in enumerate(jobs)
    )

    return f"\n🔍 {keywords}\n\n{jobs_text}"


def build_email(user: Dict) -> EmailMessage:
    email_to = user.get("email")
    searches = user.get("searches", [])

    if not email_to:
        raise ValueError("User without email")

    body = "\n".join(format_search_text(search) for search in searches)

    msg = EmailMessage()
    msg["Subject"] = "📬 Novas vagas encontradas"
    msg["From"] = getenv("EMAIL_FROM")
    msg["To"] = email_to

    msg.set_content(
        f"""
            Olá!

            Encontramos novas vagas com base nas suas buscas:

            {body}

            —
            Job Search Bot 🚀
            """
    )
    return msg


def send_email(msg: EmailMessage) -> None:
    SMTP_HOST = getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(getenv("SMTP_PORT", 465))
    email_from = getenv("EMAIL_FROM")
    email_password = getenv("EMAIL_PASSWORD")

    if not email_from or not email_password:
        raise RuntimeError("EMAIL_FROM ou EMAIL_PASSWORD não configurados")

    logging.info(f"Enviando email para {msg['To']}")

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(email_from, email_password)
        smtp.send_message(msg)

    logging.info("Email enviado com sucesso.")


def main(event=None, context=None) -> None:
    message = decode_pubsub_message(event)
    users: List[Dict] = json_loads(message)

    if not users:
        logging.warning("Payload vazio recebido.")
        return

    for user in users:
        try:
            email = build_email(user)
            send_email(email)
        except Exception as e:
            logging.error(f"Erro ao processar usuário {user.get('email')}: {e}")


if __name__ == "__main__":
    main()
