import os
from django.core.management.base import BaseCommand
from faker import Faker
from web.models import Video
import random

class Command(BaseCommand):
    help = 'Generates fake videos for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('--num_videos', type=int, default=10, help='The number of fake videos to create.')

    def handle(self, *args, **kwargs):
        fake = Faker('en_US') # Using English locale for YouTube IDs
        num_videos = kwargs['num_videos']

        self.stdout.write(f"Generating {num_videos} fake videos...")
        for i in range(num_videos):
            title = fake.sentence(nb_words=5)
            # Generate a plausible YouTube-like ID (11 alphanumeric characters)
            youtube_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ ', k=11))
            description = fake.paragraph(nb_sentences=2)

            video_obj = Video.objects.create(
                title=title,
                youtube_id=youtube_id,
                description=description,
                is_active=True
            )
            self.stdout.write(f"Created video: {video_obj.title} (YouTube ID: {video_obj.youtube_id})")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_videos} fake videos."))
