# Generated by Django 4.0.6 on 2022-07-19 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('papers_app', '0006_alter_profile_profile_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers_app.question', unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]