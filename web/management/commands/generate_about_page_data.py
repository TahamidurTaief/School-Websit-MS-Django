from django.core.management.base import BaseCommand
from web.models import (
    AboutPage, SchoolHistory, SchoolBriefInfo, AboutPrincipalMessage,
    SchoolApproval, SchoolBranch, SchoolRecognition, SchoolAims,
    AimPoint, AboutNewsItem, AboutLink
)

class Command(BaseCommand):
    help = 'Generate initial data for about page'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating about page data...')
        
        # Create About Page
        about_page, created = AboutPage.objects.get_or_create(
            title='আমাদের সম্পর্কে (About Us)',
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(f'Created AboutPage: {about_page.title}')
        
        # Create School History
        history, created = SchoolHistory.objects.get_or_create(
            title='প্রতিষ্ঠানের ইতিহাস',
            defaults={
                'content': '''আমাদের স্কুল ১৯৮০ সালে প্রতিষ্ঠিত হয়েছিল। প্রতিষ্ঠানটি প্রথমে একটি ছোট ভবনে শুরু হয়েছিল মাত্র ৫০ জন শিক্ষার্থী নিয়ে। বর্তমানে আমাদের প্রতিষ্ঠানে ১০০০+ শিক্ষার্থী অধ্যয়নরত। গত ৪০+ বছরে আমাদের প্রতিষ্ঠান অনেক চড়াই-উতরাই পেরিয়ে আজ একটি সম্মানজনক অবস্থানে পৌঁছেছে। আমাদের প্রাক্তন শিক্ষার্থীরা দেশের বিভিন্ন গুরুত্বপূর্ণ পদে অধিষ্ঠিত আছেন এবং সমাজের উন্নয়নে অবদান রাখছেন।

আমাদের প্রতিষ্ঠানের ইতিহাসে অনেক উল্লেখযোগ্য ঘটনা রয়েছে। ১৯৮৫ সালে প্রথমবারের মতো আমাদের প্রতিষ্ঠান থেকে ১০০% পাসের হার অর্জন করা হয়। ১৯৯০ সালে বিজ্ঞান বিভাগ চালু করা হয়। ২০০০ সালে কম্পিউটার ল্যাব স্থাপন করা হয়। ২০১০ সালে নতুন ভবন নির্মাণ করা হয়। ২০২০ সালে অনলাইন শিক্ষা কার্যক্রম শুরু করা হয়।

আমাদের প্রতিষ্ঠানের সাফল্যের পিছনে রয়েছে দক্ষ শিক্ষক-শিক্ষিকা, আন্তরিক প্রশাসন এবং সহযোগী অভিভাবকদের অবদান। আমরা ভবিষ্যতেও এই সাফল্য ধরে রাখার জন্য নিরলসভাবে কাজ করে যাচ্ছি।''',
                'is_active': True,
                'order': 1
            }
        )
        if created:
            self.stdout.write(f'Created SchoolHistory: {history.title}')
        
        # Create Brief Info
        brief_info, created = SchoolBriefInfo.objects.get_or_create(
            title='সংক্ষিপ্ত তথ্য',
            defaults={
                'description': 'আমাদের প্রতিষ্ঠানে অভিজ্ঞ শিক্ষক-শিক্ষিকা দ্বারা পরিচালিত বিভিন্ন বিভাগ রয়েছে। আধুনিক সুযোগ-সুবিধা সম্পন্ন ক্লাসরুম, ল্যাবরেটরি, লাইব্রেরি এবং খেলার মাঠ রয়েছে। আমাদের প্রতিষ্ঠানে আধুনিক প্রযুক্তি ব্যবহার করে শিক্ষা প্রদান করা হয়।',
                'teachers_count': '৫০+',
                'departments_count': '৫',
                'classrooms_count': '৩০+',
                'students_count': '১০০০+',
                'is_active': True,
                'order': 2
            }
        )
        if created:
            self.stdout.write(f'Created SchoolBriefInfo: {brief_info.title}')
        
        # Create Principal Message
        principal_message, created = AboutPrincipalMessage.objects.get_or_create(
            title='অধ্যক্ষের বাণী',
            defaults={
                'name': 'প্রফেসর মোঃ আবদুল করিম',
                'message': '''প্রিয় শিক্ষার্থীরা,

জ্ঞান অর্জনের জন্য অধ্যবসায়, সততা ও নিষ্ঠার বিকল্প নেই। তোমাদের প্রতিটি দিন হোক নতুন কিছু শেখার এবং নিজেকে গড়ে তোলার। আমাদের প্রতিষ্ঠান তোমাদের স্বপ্নপূরণের সহযাত্রী।

শিক্ষা শুধু ডিগ্রি নয়, এটি মানবিক মূল্যবোধ, নৈতিকতা ও নেতৃত্বের শিক্ষা। তোমরা দেশ ও জাতির গর্ব হয়ে উঠো, এই কামনা করি।

আমাদের প্রতিষ্ঠানের লক্ষ্য হল তোমাদেরকে শুধু একাডেমিকভাবে দক্ষ নয়, বরং একজন ভালো মানুষ হিসেবে গড়ে তোলা। আমরা চাই তোমরা দেশের সুনাগরিক হয়ে দেশের উন্নয়নে অবদান রাখো।

ধন্যবাদ।''',
                'is_active': True,
                'order': 3
            }
        )
        if created:
            self.stdout.write(f'Created AboutPrincipalMessage: {principal_message.title}')
        
        # Create School Approval
        approval, created = SchoolApproval.objects.get_or_create(
            title='অনুমোদন',
            defaults={
                'content': 'আমাদের প্রতিষ্ঠানটি শিক্ষা মন্ত্রণালয় কর্তৃক অনুমোদিত এবং বাংলাদেশ শিক্ষা বোর্ড দ্বারা স্বীকৃত। আমাদের প্রতিষ্ঠানের সকল শাখা সরকারি নিয়ম অনুযায়ী পরিচালিত হয়। আমরা জাতীয় শিক্ষাক্রম অনুসরণ করি এবং সরকারি নির্দেশনা মেনে চলি।',
                'is_active': True,
                'order': 4
            }
        )
        if created:
            self.stdout.write(f'Created SchoolApproval: {approval.title}')
        
        # Create School Branches
        branches_data = [
            {
                'name': 'প্রধান শাখা',
                'location': 'মিরপুর, ঢাকা',
                'established_year': '১৯৮০',
                'order': 1
            },
            {
                'name': 'দ্বিতীয় শাখা',
                'location': 'উত্তরা, ঢাকা',
                'established_year': '২০০৫',
                'order': 2
            }
        ]
        
        for branch_data in branches_data:
            branch, created = SchoolBranch.objects.get_or_create(
                name=branch_data['name'],
                defaults={
                    'location': branch_data['location'],
                    'established_year': branch_data['established_year'],
                    'is_active': True,
                    'order': branch_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created SchoolBranch: {branch.name}')
        
        # Create School Recognition
        recognition, created = SchoolRecognition.objects.get_or_create(
            title='স্বীকৃতি',
            defaults={
                'content': 'আমাদের প্রতিষ্ঠান বিভিন্ন জাতীয় ও আন্তর্জাতিক পুরস্কার অর্জন করেছে। আমরা শিক্ষা মন্ত্রণালয় থেকে "সেরা শিক্ষা প্রতিষ্ঠান" হিসেবে স্বীকৃতি পেয়েছি। আমাদের প্রতিষ্ঠান বাংলাদেশ শিক্ষা বোর্ড থেকে "এ+ গ্রেড" পেয়েছে। আমরা বিভিন্ন আন্তর্জাতিক সংস্থা থেকে স্বীকৃতি পেয়েছি।',
                'document_title': 'সেরা শিক্ষা প্রতিষ্ঠান স্বীকৃতি দলিল',
                'is_active': True,
                'order': 5
            }
        )
        if created:
            self.stdout.write(f'Created SchoolRecognition: {recognition.title}')
        
        # Create School Aims
        aims, created = SchoolAims.objects.get_or_create(
            title='লক্ষ্য ও উদ্দেশ্য',
            defaults={
                'content': 'আমাদের প্রতিষ্ঠানের মূল লক্ষ্য হল শিক্ষার্থীদের মেধা ও মননের সর্বাঙ্গীণ বিকাশ সাধন করা। আমরা চাই আমাদের শিক্ষার্থীরা শুধু একাডেমিক জ্ঞান নয়, বরং নৈতিক মূল্যবোধ, সামাজিক দায়বদ্ধতা এবং নেতৃত্বের গুণাবলী অর্জন করুক।',
                'is_active': True,
                'order': 6
            }
        )
        if created:
            self.stdout.write(f'Created SchoolAims: {aims.title}')
        
        # Create Aim Points
        aim_points_data = [
            'উচ্চমানের শিক্ষা প্রদান',
            'নৈতিক মূল্যবোধ গঠন',
            'সৃজনশীলতা ও উদ্ভাবনী চিন্তার বিকাশ',
            'দেশপ্রেম ও সামাজিক দায়বদ্ধতা সৃষ্টি',
            'আধুনিক প্রযুক্তি ব্যবহারে দক্ষতা অর্জন',
            'শারীরিক ও মানসিক স্বাস্থ্যের উন্নয়ন',
            'সাংস্কৃতিক চেতনার বিকাশ',
            'পরিবেশ সচেতনতা সৃষ্টি'
        ]
        
        for i, point_text in enumerate(aim_points_data, 1):
            point, created = AimPoint.objects.get_or_create(
                aim=aims,
                point=point_text,
                defaults={
                    'is_active': True,
                    'order': i
                }
            )
            if created:
                self.stdout.write(f'Created AimPoint: {point.point}')
        
        # Create News Items
        news_data = [
            {
                'title': 'বার্ষিক ক্রীড়া প্রতিযোগিতা ২০২৩',
                'date': '১০ ডিসেম্বর, ২০২৩',
                'link': '#',
                'order': 1
            },
            {
                'title': 'বিজ্ঞান মেলা আয়োজন',
                'date': '১৪ নভেম্বর, ২০২৩',
                'link': '#',
                'order': 2
            },
            {
                'title': 'শিক্ষক নিয়োগ বিজ্ঞপ্তি',
                'date': '০৫ অক্টোবর, ২০২৩',
                'link': '#',
                'order': 3
            },
            {
                'title': 'মিড টার্ম পরীক্ষার সময়সূচী',
                'date': '২০ সেপ্টেম্বর, ২০২৩',
                'link': '#',
                'order': 4
            },
            {
                'title': 'শিক্ষা সফরের আয়োজন',
                'date': '১৫ আগস্ট, ২০২৩',
                'link': '#',
                'order': 5
            }
        ]
        
        for news_item_data in news_data:
            news_item, created = AboutNewsItem.objects.get_or_create(
                title=news_item_data['title'],
                defaults={
                    'date': news_item_data['date'],
                    'link': news_item_data['link'],
                    'is_active': True,
                    'order': news_item_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created AboutNewsItem: {news_item.title}')
        
        # Create Important Links
        links_data = [
            {
                'title': 'শিক্ষা মন্ত্রণালয়',
                'url': 'https://moedu.gov.bd/',
                'order': 1
            },
            {
                'title': 'বাংলাদেশ শিক্ষা বোর্ড',
                'url': 'https://www.educationboard.gov.bd/',
                'order': 2
            },
            {
                'title': 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড',
                'url': 'http://www.nctb.gov.bd/',
                'order': 3
            },
            {
                'title': 'বাংলাদেশ সরকারি তথ্য',
                'url': 'https://www.gov.bd/',
                'order': 4
            },
            {
                'title': 'শিক্ষা অধিদপ্তর',
                'url': 'http://www.dshe.gov.bd/',
                'order': 5
            }
        ]
        
        for link_data in links_data:
            link, created = AboutLink.objects.get_or_create(
                title=link_data['title'],
                defaults={
                    'url': link_data['url'],
                    'is_active': True,
                    'order': link_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created AboutLink: {link.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully generated about page data!')) 