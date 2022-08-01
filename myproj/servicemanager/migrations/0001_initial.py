# Generated by Django 4.0.6 on 2022-07-30 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmonCounter',
            fields=[
                ('EmonCounterID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='EmonEvent',
            fields=[
                ('EmonEventID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('IdeaID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('PlatformID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('StationID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=250)),
                ('Desc', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('TaskStatusID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('ToolID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ToolEvent',
            fields=[
                ('ToolEventID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
                ('Tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.tool')),
            ],
        ),
        migrations.CreateModel(
            name='ToolCounter',
            fields=[
                ('ToolCounterID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
                ('Tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.tool')),
                ('ToolEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.toolevent')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsDebugMode', models.BooleanField(default=b'I00\n')),
                ('RegressionName', models.CharField(max_length=250)),
                ('IsEmon', models.BooleanField(default=False)),
                ('IsUploadResults', models.BooleanField(default=False)),
                ('TotalIterations', models.IntegerField()),
                ('Splitter', models.CharField(max_length=50)),
                ('MinImpurityDecrease', models.CharField(max_length=50)),
                ('MaxFeatures', models.CharField(max_length=50)),
                ('CreatedBy', models.CharField(max_length=50)),
                ('CreatedDate', models.DateField()),
                ('ModifiedBy', models.CharField(max_length=50)),
                ('ModifiedDate', models.DateField()),
                ('ErrorCode', models.CharField(max_length=10)),
                ('ErrorMessage', models.CharField(max_length=500)),
                ('Idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.idea')),
                ('Platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.platform')),
                ('PlatformCounter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.emoncounter')),
                ('PlatformEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.emonevent')),
                ('Station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.station')),
                ('Status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.taskstatus')),
                ('Tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.tool')),
                ('ToolCounter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.toolcounter')),
                ('ToolEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.toolevent')),
            ],
        ),
        migrations.AddField(
            model_name='emonevent',
            name='Platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.platform'),
        ),
        migrations.AddField(
            model_name='emoncounter',
            name='EmonEvent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.emonevent'),
        ),
        migrations.AddField(
            model_name='emoncounter',
            name='Platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicemanager.platform'),
        ),
    ]
