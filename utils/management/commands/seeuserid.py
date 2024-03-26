from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lists all users and allows deleting a user by ID"

    def handle(self, *args, **kwargs):
        user = get_user_model()
        users = user.objects.all()
        self.stdout.write("Current users:")
        for user in users:
            self.stdout.write(
                f"ID: {user.id}, Email: {user.email}, Active: {user.is_active}",
            )

        user_id = input(
            "Enter the ID of the user you wish to delete (or 'exit' to cancel): ",
        )
        if user_id.lower() == "exit":
            self.stdout.write("Operation cancelled.")
            return

        try:
            user_id = int(user_id)
            user = user.objects.get(id=user_id)
            user.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"User with ID {user_id} has been successfully deleted.",
                ),
            )
        except user.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("User with the given ID does not exist."),
            )
        except ValueError:
            self.stdout.write(
                self.style.ERROR("Invalid input. Please enter a valid numeric ID."),
            )
