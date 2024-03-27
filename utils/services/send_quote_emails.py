# /utils/services/send_quote_emails.py
import logging

from django.conf import settings
from django.core.mail import send_mail

from .generate_random_quote_v1 import generate_random_quote_v1
from .generate_random_quote_v4 import generate_random_quote_v4
from .generate_random_quote_v5 import generate_random_quote_v5

logger = logging.getLogger("utils.services.send_quote_emails")


def send_quote_email(email_address, language="sk"):
    quote_functions = (
        [
            generate_random_quote_v1,
        ]
        * 2
        + [
            generate_random_quote_v4,
        ]
        + [generate_random_quote_v5]
    )
    for generate_quote in quote_functions:
        quote = generate_quote(language)
        try:
            quote = generate_quote(language)
            if quote:
                break
        except (ValueError, KeyError):
            logger.exception("Error using ")

    if quote and quote.strip():
        try:
            subject = "Your Daily Quote"
            message = quote
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email_address]
            send_mail(
                subject,
                message,
                email_from,
                recipient_list,
            )
            logger.info("Successfully sent the quote email.")
        except (ValueError, KeyError):
            logger.exception("Error sending mail")
    else:
        logger.error("The quote is empty. Email will not be sent.")
