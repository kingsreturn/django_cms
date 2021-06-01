# Generated by Django 3.1.7 on 2021-05-23 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datacollection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataQuelle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(default='', max_length=100)),
                ('protocol', models.CharField(default='', max_length=10)),
                ('variable_address', models.CharField(max_length=100)),
                ('variable_name', models.CharField(max_length=100)),
            ],
        ),
    ]