# Generated by Django 2.2.27 on 2023-03-21 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showtalk', '0004_auto_20230321_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tv',
            name='img',
        ),
    ]
