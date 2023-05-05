# Generated by Django 4.2 on 2023-05-05 18:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sdcc_compiler', '0011_alter_file_access_change_alter_file_creation_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compilation_log', models.TextField()),
                ('target_line', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_line', models.IntegerField()),
                ('end_line', models.IntegerField()),
                ('content', models.TextField()),
                ('type', models.CharField(choices=[('P', 'Procedure'), ('C', 'Comment'), ('D', 'Compiler directive'), ('V', 'Variable declaration'), ('I', 'Inline assembly')], max_length=1)),
                ('status', models.CharField(choices=[('OK', 'Compiles without warnings'), ('ERR', 'Does not compile'), ('WARN', 'Compiles with warnings')], default='OK', max_length=4)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='sdcc_compiler.file')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='sdcc_compiler.section')),
                ('status_data', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sdcc_compiler.statusdata')),
            ],
        ),
    ]
