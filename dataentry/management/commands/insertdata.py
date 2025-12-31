from django.core.management.base import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help = "insert data into the database"

    def handle(self, *args, **kwargs):
        dataset = [
            {"roll_no": "101", "name": "John", "age": 20},
            {"roll_no": "102", "name": "Jane", "age": 22},
            {"roll_no": "103", "name": "Jack", "age": 21},
            {"roll_no": "104", "name": "Jill", "age": 23},
            {"roll_no": "105", "name": "Joe", "age": 24},
            {"roll_no": "106", "name": "Jenny", "age": 25},
            {"roll_no": "107", "name": "Jim", "age": 26},
            {"roll_no": "108", "name": "Julia", "age": 27},
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(
                    roll_no=data['roll_no'], name=data['name'], age=data['age'])

            else:
                self.stdout.write(self.style.WARNING(
                    f"Student with roll no {roll_no} already exists"))
        self.stdout.write(self.style.SUCCESS('data inserted successfully'))
# I would like to add data to the database using custom commands
