from getpass import getpass
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Create one named practice staff account. Run privately for each person."

    def add_arguments(self, parser):
        parser.add_argument("username", choices=["aswathy","rahul"])

    @transaction.atomic
    def handle(self, username, **options):
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise CommandError("Account already exists. Use changepassword to reset it.")
        user = User(username=username, is_staff=True)
        password = getpass("New password: ")
        validate_password(password,user)
        if password != getpass("Repeat password: "):
            raise CommandError("Passwords did not match.")
        user.set_password(password)
        user.save()
        user.user_permissions.set(Permission.objects.filter(content_type__app_label="appointments", codename__in=["view_appointment","add_appointment","change_appointment"]))
        self.stdout.write(f"Created {username}.")
