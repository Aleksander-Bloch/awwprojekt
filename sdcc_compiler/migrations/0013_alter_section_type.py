# Generated by Django 4.2 on 2023-05-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdcc_compiler', '0012_statusdata_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(choices=[('PROC', 'Procedure'), ('COM', 'Comment'), ('DIR', 'Compiler directive'), ('VAR', 'Variable declaration'), ('ASM', 'Inline assembly')], max_length=4),
        ),
    ]
