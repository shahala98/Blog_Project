# Generated by Django 5.0.6 on 2024-07-18 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='updated_at',
        ),
    ]
