from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from web.models import InformationService, InformationSlider, FacilityInfo, FacultyInfo
import random

fake = Faker(['bn_BD', 'en_US'])

class Command(BaseCommand):
    help = 'Generate sample data for Information Service Center'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating Information Service data...')
        
        # Create Information Service content
        info_service = InformationService.objects.create(
            title='আমাদের প্রতিষ্ঠানের তথ্য সেবা কেন্দ্র',
            description='আমাদের প্রতিষ্ঠানের সকল গুরুত্বপূর্ণ তথ্য এবং সুবিধা সম্পর্কে জানতে এই পৃষ্ঠাটি দেখুন। আমরা আমাদের শিক্ষার্থীদের সর্বোচ্চ মানের শিক্ষা প্রদানের জন্য আধুনিক সুযোগ-সুবিধা নিশ্চিত করেছি।',
            is_active=True
        )
        
        # Create slider images
        slider_data = [
            {
                'title': 'আমাদের মূল ভবন',
                'description': 'আধুনিক স্থাপত্যশৈলীতে নির্মিত আমাদের মূল ভবন',
                'order': 1
            },
            {
                'title': 'কম্পিউটার ল্যাব',
                'description': 'আধুনিক কম্পিউটার ল্যাবরেটরি',
                'order': 2
            },
            {
                'title': 'লাইব্রেরি',
                'description': 'সমৃদ্ধ লাইব্রেরি সুবিধা',
                'order': 3
            },
            {
                'title': 'খেলার মাঠ',
                'description': 'বিস্তৃত খেলার মাঠ',
                'order': 4
            },
            {
                'title': 'মাল্টিমিডিয়া ক্লাসরুম',
                'description': 'আধুনিক মাল্টিমিডিয়া ক্লাসরুম',
                'order': 5
            }
        ]
        
        for slider in slider_data:
            InformationSlider.objects.create(
                title=slider['title'],
                description=slider['description'],
                order=slider['order'],
                is_active=True
            )
        
        # Create facility information
        facilities_data = [
            {
                'facility_type': 'classroom',
                'title': 'মোট কক্ষ সংখ্যা',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ৩০টি আধুনিক ক্লাসরুম রয়েছে। প্রতিটি কক্ষে পর্যাপ্ত আলো-বাতাসের ব্যবস্থা রয়েছে।',
                'icon': 'fas fa-chalkboard-teacher',
                'count': 30,
                'unit': 'টি',
                'order': 1
            },
            {
                'facility_type': 'computer',
                'title': 'কম্পিউটার সংখ্যা',
                'description': 'আমাদের কম্পিউটার ল্যাবে মোট ৫০টি আধুনিক কম্পিউটার রয়েছে। সব কম্পিউটারে ইন্টারনেট সংযোগ রয়েছে।',
                'icon': 'fas fa-laptop',
                'count': 50,
                'unit': 'টি',
                'order': 2
            },
            {
                'facility_type': 'seats',
                'title': 'মোট আসন সংখ্যা',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ১২০০ জন শিক্ষার্থীর জন্য আসন ব্যবস্থা রয়েছে।',
                'icon': 'fas fa-chair',
                'count': 1200,
                'unit': 'জন',
                'order': 3
            },
            {
                'facility_type': 'multimedia',
                'title': 'মাল্টিমিডিয়া ক্লাসরুম',
                'description': 'আমাদের প্রতিষ্ঠানে ১০টি মাল্টিমিডিয়া ক্লাসরুম রয়েছে। প্রতিটি কক্ষে প্রজেক্টর এবং সাউন্ড সিস্টেম রয়েছে।',
                'icon': 'fas fa-tv',
                'count': 10,
                'unit': 'টি',
                'order': 4
            },
            {
                'facility_type': 'transport',
                'title': 'যানবাহন সংখ্যা',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ৫টি বাস রয়েছে যা শিক্ষার্থীদের পরিবহন সেবা প্রদান করে।',
                'icon': 'fas fa-bus',
                'count': 5,
                'unit': 'টি',
                'order': 5
            },
            {
                'facility_type': 'classroom',
                'title': 'বিজ্ঞান ল্যাব',
                'description': 'আমাদের প্রতিষ্ঠানে ৩টি আধুনিক বিজ্ঞান ল্যাবরেটরি রয়েছে।',
                'icon': 'fas fa-flask',
                'count': 3,
                'unit': 'টি',
                'order': 6
            },
            {
                'facility_type': 'computer',
                'title': 'প্রিন্টার সংখ্যা',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ৮টি প্রিন্টার রয়েছে।',
                'icon': 'fas fa-print',
                'count': 8,
                'unit': 'টি',
                'order': 7
            },
            {
                'facility_type': 'seats',
                'title': 'শিক্ষক আসন',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ৬০ জন শিক্ষকের জন্য আসন ব্যবস্থা রয়েছে।',
                'icon': 'fas fa-user-tie',
                'count': 60,
                'unit': 'জন',
                'order': 8
            },
            {
                'facility_type': 'multimedia',
                'title': 'অডিটোরিয়াম',
                'description': 'আমাদের প্রতিষ্ঠানে একটি আধুনিক অডিটোরিয়াম রয়েছে যেখানে ৫০০ জন দর্শক বসতে পারে।',
                'icon': 'fas fa-theater-masks',
                'count': 1,
                'unit': 'টি',
                'order': 9
            },
            {
                'facility_type': 'transport',
                'title': 'পার্কিং স্পেস',
                'description': 'আমাদের প্রতিষ্ঠানে মোট ১০০টি গাড়ির জন্য পার্কিং স্পেস রয়েছে।',
                'icon': 'fas fa-parking',
                'count': 100,
                'unit': 'টি',
                'order': 10
            }
        ]
        
        for facility in facilities_data:
            FacilityInfo.objects.create(
                facility_type=facility['facility_type'],
                title=facility['title'],
                description=facility['description'],
                icon=facility['icon'],
                count=facility['count'],
                unit=facility['unit'],
                order=facility['order'],
                is_active=True
            )
        
        # Create faculty information
        faculty_data = [
            {
                'name': 'ড. মোহাম্মদ আলী',
                'position': 'প্রধান শিক্ষক',
                'department': 'বিজ্ঞান বিভাগ',
                'education': 'পিএইচডি, পদার্থবিজ্ঞান',
                'experience': '১৫',
                'email': 'principal@schoolproject.edu.bd',
                'phone': '+880 1234-567890',
                'order': 1
            },
            {
                'name': 'জনাব রফিকুল ইসলাম',
                'position': 'সহকারী প্রধান শিক্ষক',
                'department': 'বাণিজ্য বিভাগ',
                'education': 'এমবিএ, ব্যবস্থাপনা',
                'experience': '১২',
                'email': 'rafiqul@schoolproject.edu.bd',
                'phone': '+880 1234-567891',
                'order': 2
            },
            {
                'name': 'জনাবা ফারজানা আক্তার',
                'position': 'সহকারী শিক্ষিকা',
                'department': 'মানবিক বিভাগ',
                'education': 'এমএ, বাংলা সাহিত্য',
                'experience': '১০',
                'email': 'farzana@schoolproject.edu.bd',
                'phone': '+880 1234-567892',
                'order': 3
            },
            {
                'name': 'জনাব কামাল হোসেন',
                'position': 'সহকারী শিক্ষক',
                'department': 'কম্পিউটার বিজ্ঞান',
                'education': 'এমএসসি, কম্পিউটার বিজ্ঞান',
                'experience': '৮',
                'email': 'kamal@schoolproject.edu.bd',
                'phone': '+880 1234-567893',
                'order': 4
            },
            {
                'name': 'জনাবা নাসরিন সুলতানা',
                'position': 'সহকারী শিক্ষিকা',
                'department': 'ইংরেজি বিভাগ',
                'education': 'এমএ, ইংরেজি সাহিত্য',
                'experience': '৯',
                'email': 'nasrin@schoolproject.edu.bd',
                'phone': '+880 1234-567894',
                'order': 5
            },
            {
                'name': 'জনাব মাহমুদুল হাসান',
                'position': 'সহকারী শিক্ষক',
                'department': 'গণিত বিভাগ',
                'education': 'এমএসসি, গণিত',
                'experience': '১১',
                'email': 'mahmudul@schoolproject.edu.bd',
                'phone': '+880 1234-567895',
                'order': 6
            }
        ]
        
        for faculty in faculty_data:
            FacultyInfo.objects.create(
                name=faculty['name'],
                position=faculty['position'],
                department=faculty['department'],
                education=faculty['education'],
                experience=faculty['experience'],
                email=faculty['email'],
                phone=faculty['phone'],
                order=faculty['order'],
                is_active=True
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created Information Service data:\n'
                f'- 1 Information Service content\n'
                f'- {len(slider_data)} Slider images\n'
                f'- {len(facilities_data)} Facility information items\n'
                f'- {len(faculty_data)} Faculty information items'
            )
        ) 