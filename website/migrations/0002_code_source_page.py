# Generated by Django 5.1.3 on 2024-11-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='source_page',
            field=models.CharField(default='suggest', max_length=10),
        ),
    ]
