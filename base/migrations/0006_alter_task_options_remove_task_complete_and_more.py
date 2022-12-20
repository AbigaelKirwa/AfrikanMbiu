# Generated by Django 4.1.1 on 2022-12-19 06:36

import base.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_task_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['video']},
        ),
        migrations.RemoveField(
            model_name='task',
            name='complete',
        ),
        migrations.AlterField(
            model_name='task',
            name='video',
            field=models.FileField(blank=True, upload_to='video/%y', validators=[base.validators.file_size]),
        ),
    ]