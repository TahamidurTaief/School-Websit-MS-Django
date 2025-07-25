# Generated by Django 5.2.4 on 2025-07-26 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20250726_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='শিরোনাম')),
                ('url', models.URLField(verbose_name='লিঙ্ক')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='আইকন (FontAwesome)')),
                ('is_active', models.BooleanField(default=True, verbose_name='সক্রিয়')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'গুরুত্বপূর্ণ লিঙ্ক',
                'verbose_name_plural': 'গুরুত্বপূর্ণ লিঙ্কসমূহ',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PrincipalRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='পদবি (Role)')),
                ('is_active', models.BooleanField(default=True, verbose_name='সক্রিয়')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'অধ্যক্ষ/প্রধান শিক্ষকের পদবি',
                'verbose_name_plural': 'অধ্যক্ষ/প্রধান শিক্ষকের পদবিসমূহ',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='principalmessage',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'অধ্যক্ষ/প্রধান শিক্ষকের বাণী', 'verbose_name_plural': 'অধ্যক্ষ/প্রধান শিক্ষকের বাণীসমূহ'},
        ),
        migrations.AddField(
            model_name='principalmessage',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='principalmessage',
            name='photo',
            field=models.ImageField(blank=True, upload_to='principal/'),
        ),
        migrations.AddField(
            model_name='principalmessage',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.principalrole', verbose_name='পদবি'),
        ),
    ]
