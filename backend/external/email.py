from typing import Any
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from backend.core.config import config as cfg
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

EMAIL_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template"

template_environ = Environment(
    loader=FileSystemLoader(EMAIL_TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml", "py"]),
)

mail = ConnectionConfig(
    MAIL_USERNAME="marvelousanyatonwu4@gmail.com",
    MAIL_PASSWORD=cfg.MAIL_PASSWORD,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="marvelousanyatonwu4@gmail.com",
    MAIL_FROM_NAME="Velmio",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def render_email_template(template_name: str, context: dict[str, Any]) -> str:
    template = template_environ.get_template(template_name)
    return template.render(**context)


async def send_email(
    subject: str,
    recipients: list[str],
    template_name: str,
    context: dict[str, Any] | None = None,
):
    body = render_email_template(template_name, context)

    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype=MessageType.html
    )

    fm = FastMail(mail)

    await fm.send_message(message)
