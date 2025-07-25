from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from web.models import (
    SchoolInfo, Department, Class, Teacher,
    Student, Notice, Gallery, PrincipalMessage
)
import random
from django.core.files import File
from pathlib import Path
import os

fake = Faker(['bn_BD', 'en_US'])

class Command(BaseCommand):
    help = 'Generate fake data for the school website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating fake data...')
        
        # Create SchoolInfo
        school = SchoolInfo.objects.create(
            name='বাংলাদেশ মডেল স্কুল এন্ড কলেজ',
            address='মিরপুর-২, ঢাকা-১২১৬',
            email='info@schoolproject.edu.bd',
            phone='+880 1234-567890',
            established_year='1980',
            description='আমাদের প্রতিষ্ঠানটি দেশের অন্যতম সেরা শিক্ষা প্রতিষ্ঠান।',
            history='১৯৮০ সালে প্রতিষ্ঠিত এই প্রতিষ্ঠানটি দীর্ঘ সময় ধরে শিক্ষা সেবা প্রদান করে আসছে।',
            vision='উন্নত জাতি গঠনে শিক্ষার মানোন্নয়ন।',
            mission='শিক্ষার্থীদের সর্বাঙ্গীণ বিকাশ সাধন।'
        )

        # Create Departments (use get_or_create to avoid slug conflict)
        departments = [
            ('বিজ্ঞান', 'Science', 'fas fa-flask'),
            ('বাণিজ্য', 'Commerce', 'fas fa-chart-line'),
            ('মানবিক', 'Humanities', 'fas fa-book-reader'),
            ('কম্পিউটার বিজ্ঞান', 'Computer Science', 'fas fa-laptop-code'),
            ('ইলেকট্রিক্যাল', 'Electrical Engineering', 'fas fa-bolt')
        ]
        department_objs = []
        for name_bn, name_en, icon in departments:
            dept, _ = Department.objects.get_or_create(
                name=name_bn,
                name_en=name_en,
                icon=icon,
                defaults={'description': fake.paragraph()}
            )
            department_objs.append(dept)

        # Create Classes (use get_or_create)
        classes = [
            ('ষষ্ঠ শ্রেণী', 'Class Six', 6),
            ('সপ্তম শ্রেণী', 'Class Seven', 7),
            ('অষ্টম শ্রেণী', 'Class Eight', 8),
            ('নবম শ্রেণী', 'Class Nine', 9),
            ('দশম শ্রেণী', 'Class Ten', 10),
            ('একাদশ শ্রেণী', 'Class Eleven', 11),
            ('দ্বাদশ শ্রেণী', 'Class Twelve', 12),
        ]
        class_objs = []
        for name_bn, name_en, value in classes:
            cls, _ = Class.objects.get_or_create(
                name=name_bn,
                name_en=name_en,
                numeric_value=value,
                defaults={'description': fake.paragraph()}
            )
            class_objs.append(cls)

        # Only clear Teacher objects
        Teacher.objects.all().delete()
        image_pool = [
            f'img/administration/{i}.jpeg' for i in range(1, 11)
        ] + [
            'img/administration/9.jpg'
        ]
        # Special Officers
        special_officer_positions = [
            'প্রধান অভিযোগ গ্রহণকারী কর্মকর্তা',
            'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
            'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
            'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
        ]
        for i, position in enumerate(special_officer_positions):
            Teacher.objects.create(
                category='special_officer',
                name=fake.name(),
                position=position,
                photo=random.choice(image_pool),
                facebook='https://facebook.com/',
                twitter='https://twitter.com/',
                linkedin='https://linkedin.com/',
                is_special_officer=True
            )
        # Teachers
        teacher_positions = [
            'প্রধান শিক্ষক', 'সহকারী শিক্ষক', 'সহকারী শিক্ষিকা', 'সহকারী শিক্ষক',
            'সহকারী শিক্ষিকা', 'সহকারী শিক্ষক', 'সহকারী শিক্ষিকা', 'সহকারী শিক্ষক',
            'সহকারী শিক্ষিকা', 'সহকারী শিক্ষক'
        ]
        for i, position in enumerate(teacher_positions):
            Teacher.objects.create(
                category='teacher',
                name=fake.name(),
                position=position,
                photo=random.choice(image_pool),
                facebook='https://facebook.com/',
                twitter='https://twitter.com/',
                linkedin='https://linkedin.com/',
                is_special_officer=False
            )
        # Management Board
        management_board_positions = [
            'সভাপতি', 'সহ-সভাপতি', 'সদস্য', 'সদস্য'
        ]
        for i, position in enumerate(management_board_positions):
            Teacher.objects.create(
                category='management_board',
                name=fake.name(),
                position=position,
                photo=random.choice(image_pool),
                facebook='https://facebook.com/',
                twitter='https://twitter.com/',
                linkedin='https://linkedin.com/',
                is_special_officer=False
            )

        # Create Students
        classes = Class.objects.all()
        departments = Department.objects.all()
        
        for _ in range(50):
            class_obj = random.choice(classes)
            department_obj = random.choice(departments) if class_obj.numeric_value > 8 else None
            
            Student.objects.create(
                name=fake.name(),
                roll_number=str(random.randint(1, 100)),
                registration_number=f'202{random.randint(1000, 9999)}',
                class_name=class_obj,
                department=department_obj,
                guardian_name=fake.name(),
                guardian_phone=fake.phone_number(),
                address=fake.address()
            )

        # Create Notices
        notice_types = ['notice', 'result', 'admission', 'routine']
        for _ in range(20):
            Notice.objects.create(
                title=fake.sentence(),
                type=random.choice(notice_types),
                date=fake.date_this_year(),
                is_active=random.choice([True, False])
            )

        # Create Gallery Items
        categories = ['school', 'event', 'student', 'teacher']
        for _ in range(10):
            Gallery.objects.create(
                title=fake.sentence(),
                category=random.choice(categories),
                description=fake.paragraph(),
                is_slider=random.choice([True, False])
            )

        # Create Principal Message
        PrincipalMessage.objects.create(
            name='প্রফেসর ড. মোহাম্মদ আলী',
            message='\n'.join(fake.paragraphs(3)),
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))
