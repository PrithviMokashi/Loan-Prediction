# Generated by Django 4.1.5 on 2023-03-23 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loandata',
            name='loantoval',
            field=models.CharField(max_length=45),
        ),
    ]
