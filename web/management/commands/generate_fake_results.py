import os
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from web.models import Result, Class, Department
import random

class Command(BaseCommand):
    help = 'Generates fake results for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('--num_results', type=int, default=10, help='The number of fake results to create.')

    def handle(self, *args, **kwargs):
        fake = Faker('bn_BD') # Use Bengali locale for Faker
        num_results = kwargs['num_results']

        self.stdout.write("Fetching existing Classes and Departments...")
        classes = list(Class.objects.all())
        departments = list(Department.objects.all())

        if not classes:
            self.stdout.write(self.style.WARNING("No Class objects found. Please create some classes first."))
        if not departments:
            self.stdout.write(self.style.WARNING("No Department objects found. Please create some departments first."))

        self.stdout.write(f"Generating {num_results} fake results...")
        for i in range(num_results):
            title = fake.sentence(nb_words=5)
            
            class_name = None
            department = None

            # Assign class or department randomly
            if classes and departments:
                if random.random() > 0.5: # 50% chance to assign class
                    class_name = random.choice(classes)
                else: # 50% chance to assign department
                    department = random.choice(departments)
            elif classes: # Only classes available
                class_name = random.choice(classes)
            elif departments: # Only departments available
                department = random.choice(departments)

            # Create a dummy PDF file for upload
            dummy_file_path = os.path.join(os.path.dirname(__file__), 'dummy_result.pdf')
            with open(dummy_file_path, 'wb') as f:
                f.write(b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</ProcSet[/PDF/Text]/Font<</F1 5 0 R>>>>/Contents 4 0 R>>endobj 4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Fake Result Content) Tj ET\nendstream 5 0 obj<</Type/Font/Subtype/Type1/Name/F1/BaseFont/Helvetica/Encoding/MacRomanEncoding>>endobj\nxref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000253 00000 n\n0000000320 00000 n\ntrailer<</Size 6/Root 1 0 R>>startxref\n460\n%%EOF')

            with open(dummy_file_path, 'rb') as f:
                result_obj = Result.objects.create(
                    title=title,
                    class_name=class_name,
                    department=department,
                    file=File(f, name=f'result_{i}.pdf')
                )
            os.remove(dummy_file_path) # Clean up dummy file

            self.stdout.write(f"Created result: {result_obj.title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_results} fake results."))