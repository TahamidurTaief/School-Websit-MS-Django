#!/usr/bin/env python
"""
Script to add fake data to Teacher model (for backward compatibility)
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

from web.models import Teacher

def create_fake_teacher_data(count=10):
    """Create fake teachers in the old Teacher model"""
    
    bengali_names = [
        'আবুল হাসান', 'রাশিদা খাতুন', 'মোহাম্মদ জামিল',
        'ফাতেমা বেগম', 'নূরুল আমিন', 'সালেহা খাতুন',
        'কামরুল হাসান', 'রোকেয়া আক্তার', 'আব্দুর রশিদ',
        'নাসিরা বেগম', 'শামীম আহমেদ', 'তাসলিমা আক্তার',
        'মতিউর রহমান', 'সুফিয়া খাতুন', 'ইউসুফ আলী'
    ]
    
    positions = [
        'সহকারী শিক্ষক (বাংলা)', 'সহকারী শিক্ষক (ইংরেজি)', 
        'সহকারী শিক্ষক (গণিত)', 'সহকারী শিক্ষক (বিজ্ঞান)',
        'প্রভাষক', 'সিনিয়র শিক্ষক', 'জুনিয়র শিক্ষক'
    ]
    
    categories = ['teacher', 'special_officer', 'management_board']
    
    education_levels = [
        'স্নাতক (বাংলা)', 'স্নাতক (ইংরেজি)', 'স্নাতক (গণিত)',
        'স্নাতকোত্তর (বাংলা)', 'স্নাতকোত্তর (ইংরেজি)', 'বি.এড'
    ]
    
    created_count = 0
    
    print(f"Creating {count} fake teachers in Teacher model...")
    
    for i in range(count):
        name = random.choice(bengali_names)
        position = random.choice(positions)
        category = random.choice(categories)
        education = random.choice(education_levels) if random.choice([True, False]) else ''
        experience = f"শিক্ষকতায় {random.randint(1, 20)} বছরের অভিজ্ঞতা" if random.choice([True, False]) else ''
        
        # Generate email and phone
        email = f"teacher{random.randint(1, 999)}@school.edu.bd" if random.choice([True, False]) else ''
        phone = f"01{random.randint(1, 9)}{random.randint(10000000, 99999999)}" if random.choice([True, False]) else ''
        
        try:
            teacher = Teacher.objects.create(
                category=category,
                name=name,
                position=position,
                education=education,
                experience=experience,
                email=email,
                phone=phone,
                is_special_officer=(category == 'special_officer')
            )
            created_count += 1
            print(f'✓ Created {category}: {name} - {position}')
            
        except Exception as e:
            print(f'✗ Error creating teacher: {e}')
    
    print(f'\n🎉 Successfully created {created_count} teachers!')
    
    # Show summary by category
    print("\n📊 Summary by category:")
    for category in ['teacher', 'special_officer', 'management_board', 'administration', 'kormochari']:
        count_in_category = Teacher.objects.filter(category=category).count()
        print(f'   {category}: {count_in_category} members')

if __name__ == '__main__':
    count = 10
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Invalid count argument. Using default count of 10.")
    
    create_fake_teacher_data(count)
