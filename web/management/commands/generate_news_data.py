from django.core.management.base import BaseCommand
from web.models import News, NewsLink
from faker import Faker

fake = Faker('bn_BD')

class Command(BaseCommand):
    help = 'Generate demo news data and news links section for the home page'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating demo news data...')
        
        # Create NewsLink section
        news_links_section, created = NewsLink.objects.get_or_create(
            title='সংবাদ/প্রয়োজনীয় লিংক',
            defaults={'is_active': True}
        )
        
        if created:
            self.stdout.write(f'Created NewsLink section: {news_links_section.title}')
        else:
            self.stdout.write(f'NewsLink section already exists: {news_links_section.title}')
        
        # Create sample news items
        news_data = [
            {
                'title': 'বিদ্যালয়ে বার্ষিক ক্রীড়া প্রতিযোগিতা অনুষ্ঠিত',
                'description': 'আগামী মাসে আমাদের বিদ্যালয়ে বার্ষিক ক্রীড়া প্রতিযোগিতা অনুষ্ঠিত হবে। সকল শিক্ষার্থীদের অংশগ্রহণ বাধ্যতামূলক।',
                'link': 'https://example.com/sports-competition',
                'order': 1
            },
            {
                'title': 'নতুন কম্পিউটার ল্যাব উদ্বোধন',
                'description': 'আজ আমাদের বিদ্যালয়ে নতুন কম্পিউটার ল্যাবের উদ্বোধন হয়েছে। এটি শিক্ষার্থীদের জন্য একটি গুরুত্বপূর্ণ সুবিধা।',
                'link': 'https://example.com/computer-lab',
                'order': 2
            },
            {
                'title': 'শিক্ষক প্রশিক্ষণ কর্মশালা',
                'description': 'আগামী সপ্তাহে শিক্ষকদের জন্য একটি বিশেষ প্রশিক্ষণ কর্মশালা অনুষ্ঠিত হবে।',
                'link': 'https://example.com/teacher-training',
                'order': 3
            },
            {
                'title': 'ছাত্র-ছাত্রীদের সাফল্য',
                'description': 'আমাদের বিদ্যালয়ের ছাত্র-ছাত্রীরা জাতীয় পর্যায়ে অসাধারণ সাফল্য অর্জন করেছে।',
                'link': 'https://example.com/student-success',
                'order': 4
            },
            {
                'title': 'পাঠ্যক্রম আপডেট',
                'description': 'নতুন শিক্ষাবর্ষের জন্য পাঠ্যক্রম আপডেট করা হয়েছে। সকল শিক্ষার্থী ও অভিভাবকদের অবগত করা যাচ্ছে।',
                'link': 'https://example.com/curriculum-update',
                'order': 5
            }
        ]
        
        for news_item_data in news_data:
            news_item, created = News.objects.get_or_create(
                title=news_item_data['title'],
                defaults={
                    'description': news_item_data['description'],
                    'link': news_item_data['link'],
                    'order': news_item_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created news item: {news_item.title}')
            else:
                self.stdout.write(f'News item already exists: {news_item.title}')
        
        self.stdout.write(self.style.SUCCESS('Demo news data created successfully!')) 