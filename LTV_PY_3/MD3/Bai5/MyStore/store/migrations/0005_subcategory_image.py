# Generated by Django 3.1.4 on 2021-02-25 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_price_origin'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(default='store/images/default.png', upload_to='store/images'),
        ),
    ]
