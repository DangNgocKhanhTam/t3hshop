# Generated by Django 3.1.4 on 2021-03-17 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_userprofileinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='image',
            field=models.ImageField(default='store/images/people_default.png', upload_to='store/images/'),
        ),
    ]
