#!/usr/bin/env python
"""
Standalone script to add fake faculty data to the Django database
Run this after setting up Django environment
"""

import os
import sys
import django
import random

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolProject.settings')
django.setup()

from web.models import FacultyMember

def create_fake_faculty_data(count=25):
    """Create fake faculty members"""
    
    # Bengali names and positions
    bengali_names = [
        'ড. মোহাম্মদ আবুল কাসেম', 'প্রফেসর নূরুল ইসলাম', 'ড. ফাতেমা খাতুন',
        'মোহাম্মদ আব্দুর রহমান', 'নাসিরুদ্দিন আহমেদ', 'রাশিদা বেগম',
        'ড. আব্দুল মান্নান', 'শামসুন্নাহার বেগম', 'মোহাম্মদ আলী',
        'জাহানারা খাতুন', 'ড. মোস্তফা করিম', 'রোকেয়া সুলতানা',
        'আব্দুল জলিল', 'ফরিদা পারভীন', 'মোহাম্মদ হাসান',
        'সালমা আক্তার', 'ড. আনিসুর রহমান', 'নাসিমা বেগম',
        'মোহাম্মদ ইউসুফ', 'রাবেয়া খাতুন', 'আশরাফুল আলম',
        'মরিয়ম আক্তার', 'ড. শফিকুল ইসলাম', 'হালিমা খাতুন',
        'নজরুল ইসলাম', 'তাহমিনা বেগম', 'মোহাম্মদ সালাম',
        'জেসমিন আরা', 'ড. রফিকুল ইসলাম', 'নূরজাহান বেগম',
        'আব্দুস সাত্তার', 'রহিমা খাতুন', 'মোহাম্মদ করিম',
        'সাকিনা বেগম', 'আব্দুল গনি', 'ফাতেমা আক্তার'
    ]

    teacher_positions = [
        'প্রধান শিক্ষক', 'সহকারী প্রধান শিক্ষক', 'বাংলা বিষয়ের শিক্ষক',
        'ইংরেজি বিষয়ের শিক্ষক', 'গণিত বিষয়ের শিক্ষক', 'বিজ্ঞান বিষয়ের শিক্ষক',
        'সামাজিক বিজ্ঞান বিষয়ের শিক্ষক', 'ইসলাম শিক্ষা বিষয়ের শিক্ষক',
        'শারীরিক শিক্ষা বিষয়ের শিক্ষক', 'কৃষি শিক্ষা বিষয়ের শিক্ষক',
        'গার্হস্থ্য বিজ্ঞান বিষয়ের শিক্ষক', 'কম্পিউটার বিষয়ের শিক্ষক'
    ]

    management_positions = [
        'সভাপতি', 'সহ-সভাপতি', 'সাধারণ সম্পাদক', 'কোষাধ্যক্ষ',
        'সদস্য', 'উপদেষ্টা সদস্য', 'নির্বাহী সদস্য'
    ]

    admin_positions = [
        'প্রশাসনিক কর্মকর্তা', 'সহকারী প্রশাসনিক কর্মকর্তা', 'হিসাবরক্ষক',
        'অফিস সহায়ক', 'তথ্য প্রযুক্তি কর্মকর্তা', 'গ্রন্থাগারিক'
    ]

    staff_positions = [
        'নিরাপত্তা প্রহরী', 'পরিচ্ছন্নতাকর্মী', 'আয়া', 'মালী',
        'চালক', 'রান্নার কাজে নিয়োজিত', 'ইলেকট্রিশিয়ান', 'প্লাম্বার'
    ]

    departments = [
        'বাংলা বিভাগ', 'ইংরেজি বিভাগ', 'গণিত বিভাগ', 'বিজ্ঞান বিভাগ',
        'সামাজিক বিজ্ঞান বিভাগ', 'ইসলাম শিক্ষা বিভাগ', 'শারীরিক শিক্ষা বিভাগ',
        'কৃষি শিক্ষা বিভাগ', 'গার্হস্থ্য বিজ্ঞান বিভাগ', 'কম্পিউটার বিভাগ',
        'প্রশাসন বিভাগ', 'হিসাব বিভাগ'
    ]

    education_levels = [
        'স্নাতকোত্তর (বাংলা)', 'স্নাতকোত্তর (ইংরেজি)', 'স্নাতকোত্তর (গণিত)',
        'স্নাতকোত্তর (পদার্থবিজ্ঞান)', 'স্নাতকোত্তর (রসায়ন)', 'স্নাতকোত্তর (জীববিজ্ঞান)',
        'স্নাতকোত্তর (ভূগোল)', 'স্নাতকোত্তর (ইতিহাস)', 'স্নাতকোত্তর (ইসলামিক স্টাডিজ)',
        'স্নাতকোত্তর (শারীরিক শিক্ষা)', 'স্নাতকোত্তর (কৃষি)', 'স্নাতকোত্তর (গার্হস্থ্য বিজ্ঞান)',
        'স্নাতকোত্তর (কম্পিউটার সায়েন্স)', 'বি.এড', 'এম.এড', 'পিএইচডি'
    ]

    categories = ['teacher', 'management', 'administration', 'staff']
    category_weights = [0.5, 0.2, 0.2, 0.1]  # 50% teachers, 20% management, 20% admin, 10% staff

    created_count = 0
    order_counter = 1

    print(f"Creating {count} fake faculty members...")

    for i in range(count):
        # Choose category based on weights
        category = random.choices(categories, weights=category_weights)[0]
        
        # Choose appropriate position based on category
        if category == 'teacher':
            position = random.choice(teacher_positions)
        elif category == 'management':
            position = random.choice(management_positions)
        elif category == 'administration':
            position = random.choice(admin_positions)
        else:  # staff
            position = random.choice(staff_positions)

        # Choose a name
        name = random.choice(bengali_names)
        
        # Generate other fields
        department = random.choice(departments) if random.choice([True, False]) else ''
        education = random.choice(education_levels) if random.choice([True, False]) else ''
        experience = f"{random.randint(1, 25)}" if random.choice([True, False]) else ''
        
        # Generate email (some faculty may not have email)
        email = ''
        if random.choice([True, False, False]):  # 33% chance of having email
            base_names = ['admin', 'teacher', 'faculty', 'staff', 'contact']
            email = f"{random.choice(base_names)}{random.randint(1, 999)}@school.edu.bd"
        
        # Generate phone (some faculty may not have phone)
        phone = ''
        if random.choice([True, False]):  # 50% chance of having phone
            phone = f"01{random.randint(1, 9)}{random.randint(10000000, 99999999)}"

        try:
            faculty_member = FacultyMember.objects.create(
                category=category,
                name=name,
                position=position,
                department=department,
                education=education,
                experience=experience,
                email=email,
                phone=phone,
                is_active=True,
                order=order_counter
            )
            created_count += 1
            order_counter += 1
            
            print(f'✓ Created {category}: {name} - {position}')
            
        except Exception as e:
            print(f'✗ Error creating faculty member: {e}')

    print(f'\n🎉 Successfully created {created_count} faculty members!')
    
    # Show summary by category
    print("\n📊 Summary by category:")
    for category in categories:
        count_in_category = FacultyMember.objects.filter(category=category).count()
        category_display = dict(FacultyMember.CATEGORY_CHOICES)[category]
        print(f'   {category_display}: {count_in_category} members')

if __name__ == '__main__':
    # Check if faculty members already exist
    existing_count = FacultyMember.objects.count()
    if existing_count > 0:
        response = input(f"There are already {existing_count} faculty members. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            sys.exit()
    
    # Get count from command line argument or use default
    count = 25
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Invalid count argument. Using default count of 25.")
    
    create_fake_faculty_data(count)
