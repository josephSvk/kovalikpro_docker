from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a new user"

    def handle(self, *args, **kwargs):
        email = input("Please enter the user's email: ")
        password = input("Please enter the user's password: ")

        userser = get_user_model()

        try:
            if not userser.objects.filter(email=email).exists():
                user = userser.objects.create_user(email=email, password=password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created new user: {email}"),
                )
            else:
                self.stdout.write(
                    self.style.ERROR("A user with that email already exists."),
                )
        except FieldError as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
