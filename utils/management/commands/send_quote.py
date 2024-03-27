# /utils/management/commands/send_quote.py

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from utils.services.send_quote_emails import send_quote_email


class Command(BaseCommand):
    help = "Send quote emails to all users with an active subscription."

    def handle(self, *args, **options):
        users_with_subscription = get_user_model().objects.filter(
            quote_subscriptions__subscribed=True,
        )

        for user in users_with_subscription:
            if user.email:  # Predpokladáme, že používateľ má nastavenú e-mailovú adresu
                send_quote_email(user.email)
