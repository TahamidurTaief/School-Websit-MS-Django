import os
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from web.models import Gallery
import random

class Command(BaseCommand):
    help = 'Generates fake gallery images for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('--num_images', type=int, default=10, help='The number of fake images to create.')

    def handle(self, *args, **kwargs):
        fake = Faker('en_US')
        num_images = kwargs['num_images']

        self.stdout.write(f"Generating {num_images} fake gallery images...")
        for i in range(num_images):
            title = fake.sentence(nb_words=4)
            description = fake.paragraph(nb_sentences=1)
            category = random.choice([choice[0] for choice in Gallery.CATEGORIES])

            # Create a dummy image file (e.g., a small black PNG)
            dummy_image_path = os.path.join(os.path.dirname(__file__), 'dummy_image.png')
            from PIL import Image
            img = Image.new('RGB', (600, 400), color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            img.save(dummy_image_path)

            with open(dummy_image_path, 'rb') as f:
                gallery_obj = Gallery.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    image=File(f, name=f'gallery_image_{i}.png')
                )
            os.remove(dummy_image_path) # Clean up dummy file

            self.stdout.write(f"Created gallery image: {gallery_obj.title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_images} fake gallery images."))
