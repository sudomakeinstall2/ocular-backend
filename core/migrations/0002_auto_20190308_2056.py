# Generated by Django 2.1.7 on 2019-03-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cost',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='cost',
            field=models.PositiveIntegerField(),
        ),
    ]
