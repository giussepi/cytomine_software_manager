# Generated by Django 3.0.6 on 2020-05-23 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.CharField(help_text='Docker image name', max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cyto_id', models.IntegerField(help_text='Project ID in Cytomine', verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cyto_id', models.IntegerField(help_text='Sofware ID in Cytomine', verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cyto_image_id', models.IntegerField(help_text='Image ID in Cytomine', verbose_name='Image ID')),
                ('docker_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cytomine_softwares.Docker', verbose_name='Docker Image')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cytomine_softwares.Project')),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cytomine_softwares.Software')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]