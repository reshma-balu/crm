# Generated by Django 4.2.4 on 2023-11-09 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_employees_image_alter_employees_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employees',
            old_name='image',
            new_name='profile_pic',
        ),
    ]
