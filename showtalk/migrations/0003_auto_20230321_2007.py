# Generated by Django 2.2.27 on 2023-03-21 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtalk', '0002_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=20, verbose_name='邮箱'),
        ),
    ]
