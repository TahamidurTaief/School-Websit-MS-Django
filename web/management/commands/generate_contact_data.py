from django.core.management.base import BaseCommand
from web.models import ContactInfo

class Command(BaseCommand):
    help = 'Generate sample contact data for the contact page'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating contact data...')
        
        # Create sample contact information
        contact_info = ContactInfo.objects.create(
            title='আমাদের প্রতিষ্ঠানের যোগাযোগের তথ্য',
            address='মিরপুর-১০, ঢাকা-১২১৬, বাংলাদেশ',
            phone='+৮৮০ ১২৩৪-৫৬৭৮৯০',
            email='info@schoolproject.edu.bd',
            map_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3651.902442430136!2d90.3653!3d23.8103!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjPCsDQ4JzM3LjEiTiA5MMKwMjEnNTUuMSJF!5e0!3m2!1sen!2sbd!4v1234567890" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created contact data:\n'
                f'- Contact Info: {contact_info.title}\n'
                f'- Address: {contact_info.address}\n'
                f'- Phone: {contact_info.phone}\n'
                f'- Email: {contact_info.email}'
            )
        ) 