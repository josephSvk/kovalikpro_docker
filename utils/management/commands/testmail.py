from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sends a test email."

    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            type=str,
            help="The email address to send a test email to.",
        )

    def handle(self, *args, **options):
        email_address = options["email"]

        email = EmailMessage(
            subject="Test Email",
            body="This is a test email sent from Django.",
            from_email="kovalikpro@gmail.com",
            to=[email_address],
        )

        # Optionally log the email body and headers here before sending
        self.stdout.write(f"Sending email to: {email_address}")
        self.stdout.write(f"Email subject: {email.subject}")
        self.stdout.write(f"Email body: {email.body}")
        self.stdout.write(f"From: {email.from_email}")
        self.stdout.write(f"To: {email.to}")

        # Send the email
        email.send()

        self.stdout.write(self.style.SUCCESS("Email sent successfully!"))
