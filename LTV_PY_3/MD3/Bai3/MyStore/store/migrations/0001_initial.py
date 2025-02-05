# Generated by Django 3.1.4 on 2021-02-24 01:34

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.ImageField(default='store/images/default.png', upload_to='store/images')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('public_day', models.DateTimeField(default=datetime.datetime.now)),
                ('viewed', models.IntegerField(default=0)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.subcategory')),
            ],
        ),
    ]
