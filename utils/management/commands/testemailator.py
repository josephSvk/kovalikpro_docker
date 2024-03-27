from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from kovalikpro_docker.utils.services.generate_random_quote_v1 import (
    generate_random_quote_v4,
)


class Command(BaseCommand):
    help = "Send an email with a random quote, translated to the specified language."

    def add_arguments(self, parser):
        # Přidání argumentu pro jazyk
        parser.add_argument(
            "--lang",
            type=str,
            default="en",
            help="Language code for translation.",
        )

    def handle(self, *args, **options):
        language = options["lang"]
        quote = generate_random_quote_v4(language)
        subject = "Your Daily Quote"
        message = quote
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["20kovalik20@gmail.com"]  # Zde vložte adresu příjemce
        send_mail(subject, message, email_from, recipient_list)
        self.stdout.write(self.style.SUCCESS("Successfully sent the quote email."))
