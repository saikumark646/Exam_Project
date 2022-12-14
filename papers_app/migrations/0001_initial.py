# Generated by Django 4.0.5 on 2022-06-13 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('question_marks', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TestPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_questions', models.IntegerField()),
                ('total_marks', models.IntegerField()),
                ('checker_review', models.TextField()),
                ('examiner_review', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('checker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='checked_papers', to=settings.AUTH_USER_MODEL)),
                ('examiner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='examined_papers', to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(to='papers_app.question')),
                ('setter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_papers', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers_app.subject')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers_app.subject'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers_app.question')),
            ],
        ),
    ]
