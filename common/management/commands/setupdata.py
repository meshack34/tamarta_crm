import os
from secrets import token_urlsafe

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Migrate and populate database with initial data"

    def handle(self, *args, **options):
        User = get_user_model()

        if not settings.TESTING:
            call_command('migrate', verbosity=1)

        # Load fixtures
        call_command(
            'loaddata',
            'country.json',
            'currency.json',
            'groups.json',
            'resolution.json',
            'department.json',
            'deal_stage.json',
            'projectstage.json',
            'taskstage.json',
            'client_type.json',
            'closing_reason.json',
            'industry.json',
            'lead_source.json',
            'publicemaildomain.json',
            'help_en.json',
            'sites.json',
            'reminders.json',
            'massmailsettings.json',
            verbosity=1
        )

        # Create superuser if not exists
        if not settings.TESTING:
            username = 'IamSUPER'
            email = 'super@example.com'
            pas = token_urlsafe(6)

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=pas
                )
                print(
                    "\n✅ SUPERUSER created successfully!\n",
                    f" USERNAME: {username}\n",
                    f" PASSWORD: {pas}\n",
                    f" EMAIL: {email}\n"
                )
            else:
                print(f"\n⚠️ Superuser '{username}' already exists — skipping creation.\n")
