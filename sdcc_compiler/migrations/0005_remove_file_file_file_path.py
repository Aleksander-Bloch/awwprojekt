# Generated by Django 4.2 on 2023-05-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdcc_compiler', '0004_file_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.AddField(
            model_name='file',
            name='path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
