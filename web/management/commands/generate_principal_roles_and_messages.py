from django.core.management.base import BaseCommand
from web.models import PrincipalRole, PrincipalMessage

class Command(BaseCommand):
    help = 'Generate demo data for PrincipalRole and PrincipalMessage (Chairman, Vice Chairman, Principal)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating demo roles and messages...')
        # Create roles
        chairman = PrincipalRole.objects.create(name='Chairman', order=1)
        vice_chairman = PrincipalRole.objects.create(name='Vice Chairman', order=2)
        principal = PrincipalRole.objects.create(name='Principal', order=3)

        # Create messages
        PrincipalMessage.objects.create(
            name='জনাব মোঃ আব্দুল কাদের',
            role=chairman,
            message='প্রিয় শিক্ষার্থীরা, আমি চেয়ারম্যান হিসেবে আপনাদের জন্য গর্বিত। শিক্ষা জীবনের প্রতিটি ধাপেই সৎ ও নিষ্ঠাবান থাকো।',
            is_active=True,
            order=1
        )
        PrincipalMessage.objects.create(
            name='জনাবা শিরিন আক্তার',
            role=vice_chairman,
            message='শিক্ষা মানুষের জীবনের আলো। সহ-সভাপতি হিসেবে আমি চাই, তোমরা সবাই আলোকিত হও।',
            is_active=True,
            order=2
        )
        PrincipalMessage.objects.create(
            name='প্রফেসর মোঃ আবদুল করিম',
            role=principal,
            message='প্রিয় শিক্ষার্থীরা, অধ্যবসায় ও সততার মাধ্যমে তোমরা দেশ ও জাতির গর্ব হয়ে উঠো।',
            is_active=True,
            order=3
        )
        self.stdout.write(self.style.SUCCESS('Demo roles and messages created successfully.')) 