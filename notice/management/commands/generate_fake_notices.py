import os
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from notice.models import Notice, NoticeType
from web.models import Class, Department
import random

class Command(BaseCommand):
    help = 'Generates fake notices for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('--num_notices', type=int, default=10, help='The number of fake notices to create.')

    def handle(self, *args, **kwargs):
        fake = Faker('bn_BD') # Use Bengali locale for Faker
        num_notices = kwargs['num_notices']

        self.stdout.write("Creating Notice Types...")
        notice_types = [
            NoticeType.objects.get_or_create(name='প্রশাসনিক নোটিশ', slug='administration-notice')[0],
            NoticeType.objects.get_or_create(name='স্কুল/কলেজ নোটিশ', slug='school-college-notice')[0],
            NoticeType.objects.get_or_create(name='শিক্ষার্থী নোটিশ', slug='student-notice')[0],
            NoticeType.objects.get_or_create(name='শিক্ষক নোটিশ', slug='teacher-notice')[0],
            NoticeType.objects.get_or_create(name='শ্রেণিভিত্তিক নোটিশ', slug='class-based-notice')[0],
            NoticeType.objects.get_or_create(name='বিভাগভিত্তিক নোটিশ', slug='department-based-notice')[0],
        ]
        self.stdout.write(self.style.SUCCESS("Notice Types created/fetched."))

        self.stdout.write("Fetching existing Classes and Departments...")
        classes = list(Class.objects.all())
        departments = list(Department.objects.all())

        if not classes:
            self.stdout.write(self.style.WARNING("No Class objects found. Please create some classes first."))
        if not departments:
            self.stdout.write(self.style.WARNING("No Department objects found. Please create some departments first."))

        self.stdout.write(f"Generating {num_notices} fake notices...")
        for i in range(num_notices):
            title = fake.sentence(nb_words=5)
            short_description = fake.paragraph(nb_sentences=2)
            notice_type = random.choice(notice_types)
            
            class_name = None
            department = None

            # Assign class or department based on notice type
            if notice_type.slug == 'class-based-notice' and classes:
                class_name = random.choice(classes)
            elif notice_type.slug == 'department-based-notice' and departments:
                department = random.choice(departments)

            # Create a dummy PDF file for upload
            dummy_file_path = os.path.join(os.path.dirname(__file__), 'dummy_notice.pdf')
            with open(dummy_file_path, 'wb') as f:
                f.write(b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</ProcSet[/PDF/Text]/Font<</F1 5 0 R>>>>/Contents 4 0 R>>endobj 4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Fake Notice Content) Tj ET\nendstream 5 0 obj<</Type/Font/Subtype/Type1/Name/F1/BaseFont/Helvetica/Encoding/MacRomanEncoding>>endobj\nxref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000253 00000 n\n0000000320 00000 n\ntrailer<</Size 6/Root 1 0 R>>startxref\n460\n%%EOF')

            with open(dummy_file_path, 'rb') as f:
                notice_obj = Notice.objects.create(
                    title=title,
                    short_description=short_description,
                    notice_type=notice_type,
                    class_name=class_name,
                    department=department,
                    file=File(f, name=f'notice_{i}.pdf')
                )
            os.remove(dummy_file_path) # Clean up dummy file

            self.stdout.write(f"Created notice: {notice_obj.title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_notices} fake notices."))
