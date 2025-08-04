#!/usr/bin/env python
"""
Script to check and display current faculty data
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolProject.settings')
django.setup()

from web.models import FacultyMember, Teacher

def display_faculty_data():
    """Display current faculty data"""
    
    print("🎓 CURRENT FACULTY DATA SUMMARY")
    print("=" * 50)
    
    # FacultyMember model data
    print("\n📊 NEW FACULTY MEMBER MODEL:")
    faculty_count = FacultyMember.objects.count()
    print(f"Total Faculty Members: {faculty_count}")
    
    if faculty_count > 0:
        for category, label in FacultyMember.CATEGORY_CHOICES:
            count = FacultyMember.objects.filter(category=category).count()
            print(f"  {label}: {count}")
            
        print("\n📝 Recent Faculty Members:")
        recent_faculty = FacultyMember.objects.all()[:10]
        for faculty in recent_faculty:
            print(f"  • {faculty.name} - {faculty.position} ({faculty.get_category_display()})")
    
    # Teacher model data
    print(f"\n📊 OLD TEACHER MODEL:")
    teacher_count = Teacher.objects.count()
    print(f"Total Teachers: {teacher_count}")
    
    if teacher_count > 0:
        for category, label in Teacher.CATEGORY_CHOICES:
            count = Teacher.objects.filter(category=category).count()
            print(f"  {label}: {count}")

def check_template_readiness():
    """Check if we have data for all template sections"""
    print("\n🔍 TEMPLATE READINESS CHECK:")
    print("=" * 50)
    
    # Check FacultyMember categories
    categories_needed = ['teacher', 'management', 'administration', 'staff']
    for category in categories_needed:
        count = FacultyMember.objects.filter(category=category, is_active=True).count()
        status = "✅" if count > 0 else "❌"
        category_display = dict(FacultyMember.CATEGORY_CHOICES)[category]
        print(f"{status} {category_display}: {count} active members")
    
    print("\n📋 SUGGESTED ACTIONS:")
    if FacultyMember.objects.filter(category='teacher', is_active=True).count() < 5:
        print("• Add more teachers to populate the শিক্ষক বৃন্দ section")
    
    if FacultyMember.objects.filter(category='management', is_active=True).count() < 3:
        print("• Add more management members to populate the পরিচালনা পর্ষদ section")
    
    if FacultyMember.objects.filter(category='administration', is_active=True).count() < 2:
        print("• Add more admin officers to populate the প্রশাসনিক কর্মকর্তা section")
    
    if FacultyMember.objects.filter(category='staff', is_active=True).count() < 2:
        print("• Add more staff to populate the কর্মচারি বৃন্দ section")

def show_admin_urls():
    """Show useful admin URLs"""
    print("\n🔗 ADMIN PANEL LINKS:")
    print("=" * 50)
    print("To manage faculty data, visit these admin URLs:")
    print("• Faculty Members: http://localhost:8000/admin/web/facultymember/")
    print("• Teachers (Old): http://localhost:8000/admin/web/teacher/")
    print("• Add Faculty Member: http://localhost:8000/admin/web/facultymember/add/")

if __name__ == '__main__':
    display_faculty_data()
    check_template_readiness()
    show_admin_urls()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Visit the Django admin panel to manage faculty data")
    print("2. Start the development server: python manage.py runserver")
    print("3. Visit the administration page to see the new card design")
    print("4. Add faculty photos through the admin panel for better appearance")
