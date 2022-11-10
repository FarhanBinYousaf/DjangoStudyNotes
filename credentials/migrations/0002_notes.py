# Generated by Django 4.1 on 2022-08-25 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credentials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadingDate', models.CharField(max_length=30, null=True)),
                ('branch', models.CharField(max_length=30, null=True)),
                ('subject', models.CharField(max_length=30, null=True)),
                ('notesFile', models.FileField(max_length=30, null=True, upload_to='')),
                ('fileType', models.CharField(max_length=30, null=True)),
                ('description', models.CharField(max_length=30, null=True)),
                ('status', models.CharField(max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]