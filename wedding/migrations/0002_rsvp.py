# Generated by Django 5.1.3 on 2024-12-22 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('presence', models.CharField(max_length=10)),
                ('food', models.CharField(max_length=100)),
            ],
        ),
    ]
