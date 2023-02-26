# Generated by Django 4.1.7 on 2023-02-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiBasic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('country', models.EmailField(max_length=100)),
                ('birth_date', models.DateField()),
            ],
        ),
    ]