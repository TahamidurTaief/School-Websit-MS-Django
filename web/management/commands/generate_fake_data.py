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

        # Create Departments
        departments = [
            ('বিজ্ঞান', 'Science', 'fas fa-flask'),
            ('বাণিজ্য', 'Commerce', 'fas fa-chart-line'),
            ('মানবিক', 'Humanities', 'fas fa-book-reader'),
            ('কম্পিউটার বিজ্ঞান', 'Computer Science', 'fas fa-laptop-code'),
            ('ইলেকট্রিক্যাল', 'Electrical Engineering', 'fas fa-bolt')
        ]
        
        for name_bn, name_en, icon in departments:
            Department.objects.create(
                name=name_bn,
                name_en=name_en,
                icon=icon,
                description=fake.paragraph()
            )

        # Create Classes
        classes = [
            ('ষষ্ঠ শ্রেণী', 'Class Six', 6),
            ('সপ্তম শ্রেণী', 'Class Seven', 7),
            ('অষ্টম শ্রেণী', 'Class Eight', 8),
            ('নবম শ্রেণী', 'Class Nine', 9),
            ('দশম শ্রেণী', 'Class Ten', 10),
            ('একাদশ শ্রেণী', 'Class Eleven', 11),
            ('দ্বাদশ শ্রেণী', 'Class Twelve', 12),
        ]
        
        for name_bn, name_en, value in classes:
            Class.objects.create(
                name=name_bn,
                name_en=name_en,
                numeric_value=value,
                description=fake.paragraph()
            )

        # Create Teachers
        positions = ['প্রধান শিক্ষক', 'সহকারী শিক্ষক', 'বিজ্ঞান শিক্ষক', 'ইংরেজি শিক্ষক', 'গণিত শিক্ষক']
        for _ in range(10):
            Teacher.objects.create(
                name=fake.name(),
                position=random.choice(positions),
                education=f'এমএসসি, {fake.word()}',
                specialization=fake.word(),
                experience=fake.paragraph(),
                email=fake.email(),
                phone=fake.phone_number(),
                is_special_officer=random.choice([True, False])
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
