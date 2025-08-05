from django.core.management.base import BaseCommand
from web.models import SchoolInfo

class Command(BaseCommand):
    help = 'Update social media links for the school'

    def add_arguments(self, parser):
        parser.add_argument('--facebook', type=str, help='Facebook URL')
        parser.add_argument('--instagram', type=str, help='Instagram URL')
        parser.add_argument('--youtube', type=str, help='YouTube URL')
        parser.add_argument('--linkedin', type=str, help='LinkedIn URL')

    def handle(self, *args, **options):
        school_info = SchoolInfo.objects.first()
        
        if not school_info:
            self.stdout.write(
                self.style.ERROR('No SchoolInfo object found. Please create one in the admin first.')
            )
            return

        updated_fields = []

        if options['facebook']:
            school_info.facebook_url = options['facebook']
            updated_fields.append('Facebook')

        if options['instagram']:
            school_info.instagram_url = options['instagram']
            updated_fields.append('Instagram')

        if options['youtube']:
            school_info.youtube_url = options['youtube']
            updated_fields.append('YouTube')

        if options['linkedin']:
            school_info.linkedin_url = options['linkedin']
            updated_fields.append('LinkedIn')

        if updated_fields:
            school_info.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {", ".join(updated_fields)} URLs')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No social media URLs provided. Use --help to see available options.')
            )

        # Display current social media URLs
        self.stdout.write('\nCurrent Social Media URLs:')
        self.stdout.write(f'Facebook: {school_info.facebook_url or "Not set"}')
        self.stdout.write(f'Instagram: {school_info.instagram_url or "Not set"}')
        self.stdout.write(f'YouTube: {school_info.youtube_url or "Not set"}')
        self.stdout.write(f'LinkedIn: {school_info.linkedin_url or "Not set"}')
