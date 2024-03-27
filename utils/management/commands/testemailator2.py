import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from utils.services.generate_random_quote_v1 import generate_random_quote_v1
from utils.services.generate_random_quote_v4 import generate_random_quote_v4
from utils.services.generate_random_quote_v5 import generate_random_quote_v5

logger = logging.getLogger("utils.management.commands.emailator2")


class Command(BaseCommand):
    help = "Send an email with a random quote, translated to the specified language."

    def add_arguments(self, parser):
        parser.add_argument(
            "--lang",
            type=str,
            default="en",
            help="Language code for translation.",
        )

    def handle(self, *args, **options):
        language = options["lang"]
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
            except (ValueError, KeyError) as e:
                self.stdout.write(
                    self.style.ERROR(f"Error using {generate_quote.__name__}: {e}"),
                )
        if quote and quote.strip():
            try:
                subject = "Your Daily Quote"
                message = quote
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = ["20kovalik20@gmail.com"]
                send_mail(subject, message, email_from, recipient_list)
                self.stdout.write(
                    self.style.SUCCESS("Successfully sent the quote email."),
                )
            except (ValueError, KeyError) as e:
                self.stdout.write(self.style.ERROR(f"Error sendmail: {e}"))
        else:
            logger.error("The quote is empty. Email will not be sent.")
            self.stdout.write(
                self.style.WARNING("The quote is empty. Email will not be sent."),
            )
