# Generated by Django 4.0.6 on 2022-07-16 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers_app', '0005_rename_cut_0ff_marks_testpaper_cut_off_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_choice',
            field=models.CharField(choices=[('Setter', 'Setter'), ('Examinar', 'Examinar'), ('Examinar', 'Examinar')], max_length=10),
        ),
    ]