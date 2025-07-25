# Generated by Django 5.2.4 on 2025-07-25 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('youtube_id', models.CharField(help_text='The YouTube video ID (e.g., dQw4w9WgXcQ)', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Videos',
                'ordering': ['-created_at'],
            },
        ),
    ]
