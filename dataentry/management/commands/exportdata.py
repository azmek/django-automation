import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import datetime
# Proposed command = uv run manage.py exportdata model_name


class Command(BaseCommand):
    help = "Export data from the database to a CSV file"
    # fetch data from the database

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()
        model = None

        for app_config in apps.get_app_configs():

            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model {model_name} not found")
            return

        data = model.objects.all()

        # generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # Define the csv file name/path
        file_path = f'Exported_{model_name}_data_{timestamp}.csv'
        # open the csv file and write the data to it
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # write the header
            writer.writerow([field.name for field in model._meta.get_fields()])
            # write the data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name)
                                for field in model._meta.get_fields()])
        # print the success message
        self.stdout.write(self.style.SUCCESS('Data exported successfully'))
