# Generated by Django 4.2 on 2023-05-04 09:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sdcc_compiler', '0010_alter_directory_access_change_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='access_change',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='file',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='file',
            name='last_modification',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]