import os
import tempfile
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from datetime import datetime, timedelta
from notice.models import Notice, NoticeType
from web.models import Class, Department


class Command(BaseCommand):
    help = 'Adds 5 sample notices to the Notice model with different titles and dates.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample notices...")

        # Create or get notice types
        notice_types = [
            NoticeType.objects.get_or_create(name='প্রশাসনিক নোটিশ', slug='administration-notice')[0],
            NoticeType.objects.get_or_create(name='স্কুল/কলেজ নোটিশ', slug='school-college-notice')[0],
            NoticeType.objects.get_or_create(name='শিক্ষার্থী নোটিশ', slug='student-notice')[0],
            NoticeType.objects.get_or_create(name='শিক্ষক নোটিশ', slug='teacher-notice')[0],
            NoticeType.objects.get_or_create(name='পরীক্ষা নোটিশ', slug='exam-notice')[0],
        ]

        # Get classes and departments if they exist
        classes = list(Class.objects.all())
        departments = list(Department.objects.all())

        # Sample notices data
        sample_notices = [
            {
                'title': 'শীতকালীন ছুটির নোটিশ ২০২৫',
                'short_description': 'আগামী ১৫ জানুয়ারি থেকে ৩১ জানুয়ারি পর্যন্ত শীতকালীন ছুটি থাকবে। সকল শিক্ষার্থী ও শিক্ষকবৃন্দ এ বিষয়ে অবগত থাকুন।',
                'notice_type': notice_types[1],  # স্কুল/কলেজ নোটিশ
                'created_at': timezone.now() - timedelta(days=1),
            },
            {
                'title': 'বার্ষিক পরীক্ষার সময়সূচি প্রকাশ',
                'short_description': 'আগামী ফেব্রুয়ারি মাসে অনুষ্ঠিতব্য বার্ষিক পরীক্ষার সময়সূচি প্রকাশিত হয়েছে। সকল শিক্ষার্থী নিজ নিজ শ্রেণির সময়সূচি দেখে নিন।',
                'notice_type': notice_types[4],  # পরীক্ষা নোটিশ
                'created_at': timezone.now() - timedelta(days=3),
            },
            {
                'title': 'নতুন ভর্তির আবেদন শুরু',
                'short_description': 'আগামী শিক্ষাবর্ষের জন্য নতুন ভর্তির আবেদন শুরু হয়েছে। আগ্রহী শিক্ষার্থীরা নির্ধারিত ফরমে আবেদন করুন।',
                'notice_type': notice_types[2],  # শিক্ষার্থী নোটিশ
                'created_at': timezone.now() - timedelta(days=5),
            },
            {
                'title': 'শিক্ষক-অভিভাবক সভার আয়োজন',
                'short_description': 'আগামী শুক্রবার সকাল ১০টায় শিক্ষক-অভিভাবক সভা অনুষ্ঠিত হবে। সকল অভিভাবকদের উপস্থিত থাকার জন্য অনুরোধ করা হচ্ছে।',
                'notice_type': notice_types[0],  # প্রশাসনিক নোটিশ
                'created_at': timezone.now() - timedelta(days=7),
            },
            {
                'title': 'বিজ্ঞান মেলা ২০২৫ আয়োজনের ঘোষণা',
                'short_description': 'আগামী মার্চ মাসে বার্ষিক বিজ্ঞান মেলা অনুষ্ঠিত হবে। আগ্রহী শিক্ষার্থীরা প্রজেক্ট জমা দেওয়ার জন্য প্রস্তুতি নিন।',
                'notice_type': notice_types[2],  # শিক্ষার্থী নোটিশ
                'created_at': timezone.now() - timedelta(days=10),
            },
        ]

        created_count = 0
        for notice_data in sample_notices:
            # Check if notice with this title already exists
            if Notice.objects.filter(title=notice_data['title']).exists():
                self.stdout.write(
                    self.style.WARNING(f"Notice '{notice_data['title']}' already exists. Skipping...")
                )
                continue

            # Create a temporary PDF file for the notice
            temp_file = self.create_temp_pdf_file(notice_data['title'])
            
            # Create the notice
            notice = Notice.objects.create(
                title=notice_data['title'],
                short_description=notice_data['short_description'],
                notice_type=notice_data['notice_type'],
                class_name=classes[0] if classes else None,
                department=departments[0] if departments else None,
                is_active=True,
            )
            
            # Set the created_at field manually
            notice.created_at = notice_data['created_at']
            
            # Attach the file
            with open(temp_file, 'rb') as f:
                notice.file.save(
                    f"notice_{notice.id}.pdf",
                    File(f),
                    save=True
                )
            
            # Save with the updated created_at
            notice.save()
            
            # Clean up temp file
            os.unlink(temp_file)
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"Created notice: {notice_data['title']}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} sample notices!")
        )

    def create_temp_pdf_file(self, title):
        """Create a temporary PDF file for the notice."""
        # Create a simple text file (you could use reportlab for actual PDF)
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        content = f"""Sample Notice Document
        
Title: {title}
Date: {timezone.now().strftime('%Y-%m-%d')}

This is a sample notice document created by the management command.
""".encode('utf-8')
        
        temp_file.write(content)
        temp_file.close()
        return temp_file.name
