# Generated by Django 5.2 on 2025-04-15 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thread_Inn', '0010_product_added_by_product_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_images/default.png', upload_to='product_images/'),
            preserve_default=False,
        ),
    ]
