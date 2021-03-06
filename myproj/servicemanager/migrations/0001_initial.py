# Generated by Django 4.0.6 on 2022-07-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Station', models.CharField(max_length=50)),
                ('Counter', models.CharField(max_length=25)),
                ('Events', models.CharField(max_length=25)),
                ('TotalIterations', models.IntegerField()),
                ('RegressionName', models.CharField(max_length=100)),
                ('Idea', models.CharField(max_length=150)),
                ('Splitter', models.CharField(max_length=50)),
                ('MinImpurityDecrease', models.CharField(max_length=50)),
                ('MaxFeatures', models.CharField(max_length=50)),
            ],
        ),
    ]
