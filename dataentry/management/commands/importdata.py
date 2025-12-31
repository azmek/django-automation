from django.core.management.base import BaseCommand, CommandError
from dataentry.models import Student
from django.apps import apps
import csv

# Proposed command - uv run manage.py importdata file_path model_name


class Command(BaseCommand):
    help = "Imports data from a CSV file to the database"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        model = None
        # Search for the model across all installed apps
        for app_config in apps.get_app_configs():
            # search for the model in the app
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue  # continue to the next app if the model is not found

        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app')

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(
            'data imported from csv successfully'))
