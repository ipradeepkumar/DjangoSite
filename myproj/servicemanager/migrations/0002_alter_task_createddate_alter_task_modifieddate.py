# Generated by Django 4.0.6 on 2022-08-30 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicemanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='CreatedDate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='ModifiedDate',
            field=models.DateTimeField(null=True),
        ),
    ]