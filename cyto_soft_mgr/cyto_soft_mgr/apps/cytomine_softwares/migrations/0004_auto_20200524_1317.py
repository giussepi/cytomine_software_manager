# Generated by Django 3.0.6 on 2020-05-24 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cytomine_softwares', '0003_auto_20200523_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('return_code', models.CharField(max_length=60)),
                ('args', models.TextField(blank=True)),
                ('stderr', models.TextField(blank=True)),
                ('stdout', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('0', 'Not started'), ('1', 'Completed'), ('2', 'In progress'), ('3', 'Failed')], default='0', max_length=1),
        ),
        migrations.AddField(
            model_name='job',
            name='error',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cytomine_softwares.JobError'),
        ),
    ]
