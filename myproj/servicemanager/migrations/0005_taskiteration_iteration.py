# Generated by Django 4.0.6 on 2022-09-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicemanager', '0004_taskiteration_task_currentiteration_task_taskid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskiteration',
            name='Iteration',
            field=models.IntegerField(null=True),
        ),
    ]