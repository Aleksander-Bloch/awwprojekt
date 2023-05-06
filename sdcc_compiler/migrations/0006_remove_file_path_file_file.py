# Generated by Django 4.2 on 2023-05-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdcc_compiler', '0005_remove_file_file_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='path',
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]