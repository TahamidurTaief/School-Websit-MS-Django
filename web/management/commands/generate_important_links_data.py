from django.core.management.base import BaseCommand
from web.models import ImportantLink

class Command(BaseCommand):
    help = 'Generate demo ImportantLink data for the important links section.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating demo important links data...')

        # Demo important links
        links_data = [
            {
                'title': 'শিক্ষা বোর্ড',
                'url': 'https://www.educationboard.gov.bd/',
                'icon': 'fas fa-graduation-cap',
                'is_active': True
            },
            {
                'title': 'জাতীয় বিশ্ববিদ্যালয়',
                'url': 'https://www.nu.ac.bd/',
                'icon': 'fas fa-university',
                'is_active': True
            },
            {
                'title': 'ঢাকা বিশ্ববিদ্যালয়',
                'url': 'https://www.du.ac.bd/',
                'icon': 'fas fa-university',
                'is_active': True
            },
            {
                'title': 'শিক্ষা মন্ত্রণালয়',
                'url': 'https://www.moedu.gov.bd/',
                'icon': 'fas fa-landmark',
                'is_active': True
            },
            {
                'title': 'বাংলাদেশ সরকার',
                'url': 'https://www.bangladesh.gov.bd/',
                'icon': 'fas fa-flag',
                'is_active': True
            },
            {
                'title': 'শিক্ষা অধিদপ্তর',
                'url': 'https://www.dshe.gov.bd/',
                'icon': 'fas fa-building',
                'is_active': True
            }
        ]

        for link_data in links_data:
            link, created = ImportantLink.objects.get_or_create(
                title=link_data['title'],
                defaults={
                    'url': link_data['url'],
                    'icon': link_data['icon'],
                    'is_active': link_data['is_active']
                }
            )
            if created:
                self.stdout.write(f'Created important link: {link.title}')
            else:
                self.stdout.write(f'Important link already exists: {link.title}')

        self.stdout.write(self.style.SUCCESS('Demo important links data created successfully!')) 