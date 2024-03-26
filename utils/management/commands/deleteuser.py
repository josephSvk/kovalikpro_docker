from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes a user account based on the provided email"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="The email of the user to delete")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        user = get_user_model()

        try:
            user = user.objects.get(email=email)
            user.delete()
            self.stdout.write(
                self.style.SUCCESS(f"User with email {email} has been deleted."),
            )
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.ERROR("User with the given email does not exist."),
            )
        except Exception(ValueError, KeyError) as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e!s}"))
