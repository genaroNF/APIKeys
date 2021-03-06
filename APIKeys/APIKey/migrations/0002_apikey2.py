# Generated by Django 3.0 on 2019-12-08 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIKey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('prefix', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
