# Generated by Django 4.0.5 on 2022-06-23 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_guest_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest_user',
            old_name='contact',
            new_name='contact_number',
        ),
    ]
