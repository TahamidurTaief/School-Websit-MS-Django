import os
from django.core.management.base import BaseCommand
from web.models import SchoolHistory


class Command(BaseCommand):
    help = 'Adds sample school history data to the SchoolHistory model.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample school history...")

        # Sample history data
        sample_history = {
            'title': 'আমাদের প্রতিষ্ঠানের গৌরবময় ইতিহাস',
            'content': '''আমাদের শিক্ষা প্রতিষ্ঠানের ইতিহাস অত্যন্ত গৌরবময় এবং সমৃদ্ধ। ১৯৭৫ সালে প্রতিষ্ঠিত এই বিদ্যালয়টি গত কয়েক দশক ধরে শিক্ষার আলো ছড়িয়ে দিয়ে আসছে। শুরুর দিকে মাত্র ৫০ জন শিক্ষার্থী নিয়ে যাত্রা শুরু করা এই প্রতিষ্ঠানটি আজ হাজারেরও বেশি শিক্ষার্থীর স্বপ্নের ঠিকানা।

প্রতিষ্ঠানের প্রতিষ্ঠাতা মরহুম আব্দুল করিম সাহেবের স্বপ্ন ছিল এমন একটি শিক্ষা প্রতিষ্ঠান গড়ে তোলা যা শুধু পাঠ্যবই পড়ানো নয়, বরং নৈতিক শিক্ষা, চরিত্র গঠন এবং মানবিক মূল্যবোধ বিকাশেও ভূমিকা রাখবে। তাঁর এই স্বপ্নকে বাস্তবায়ন করতে প্রাথমিক পর্যায়ে যুক্ত হয়েছিলেন স্থানীয় শিক্ষানুরাগী ব্যক্তিত্বরা।

১৯৮০ সালে প্রথমবারের মতো এসএসসি পরীক্ষায় শতভাগ পাস করে প্রতিষ্ঠানটি এলাকায় সুনাম অর্জন করে। ১৯৯০ সাল থেকে উচ্চ মাধ্যমিক শাখা চালু হওয়ার পর প্রতিষ্ঠানটির জনপ্রিয়তা আরও বৃদ্ধি পায়। ২০০০ সালে ডিজিটাল শিক্ষা ব্যবস্থা চালু করে প্রতিষ্ঠানটি আধুনিকতার সাথে তাল মিলিয়ে চলার প্রমাণ দেয়।

বর্তমানে প্রতিষ্ঠানটিতে রয়েছে আধুনিক শ্রেণিকক্ষ, সমৃদ্ধ গ্রন্থাগার, বিজ্ঞানাগার, কম্পিউটার ল্যাব, এবং খেলাধুলার জন্য পর্যাপ্ত সুবিধা। গত পাঁচ দশকে এই প্রতিষ্ঠান থেকে পাস করা হাজার হাজার শিক্ষার্থী দেশ ও বিদেশে নিজেদের প্রতিভার স্বাক্ষর রেখেছেন।''',
            'is_active': True,
            'order': 1,
        }

        # Check if history with this title already exists
        if SchoolHistory.objects.filter(title=sample_history['title']).exists():
            self.stdout.write(
                self.style.WARNING(f"School history '{sample_history['title']}' already exists. Skipping...")
            )
            return

        # Create the school history
        history = SchoolHistory.objects.create(**sample_history)
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created school history: {history.title}")
        )
        
        self.stdout.write(
            self.style.SUCCESS("Sample school history data has been added! You can now edit it in the Django admin.")
        )
