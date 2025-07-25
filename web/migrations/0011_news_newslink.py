# Generated by Django 5.2.4 on 2025-07-26 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_alter_principalmessage_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='শিরোনাম')),
                ('description', models.TextField(blank=True, verbose_name='বিবরণ')),
                ('link', models.URLField(verbose_name='লিঙ্ক')),
                ('is_active', models.BooleanField(default=True, verbose_name='সক্রিয়')),
                ('order', models.IntegerField(default=0, verbose_name='ক্রম')),
            ],
            options={
                'verbose_name': 'সংবাদ',
                'verbose_name_plural': 'সংবাদসমূহ',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NewsLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='সংবাদ/প্রয়োজনীয় লিংক', max_length=200, verbose_name='শিরোনাম')),
                ('is_active', models.BooleanField(default=True, verbose_name='সক্রিয়')),
            ],
            options={
                'verbose_name': 'সংবাদ ও লিঙ্ক বিভাগ',
                'verbose_name_plural': 'সংবাদ ও লিঙ্ক বিভাগসমূহ',
            },
        ),
    ]
