# Generated by Django 4.0.3 on 2022-04-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0007_act'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='cost_str',
            field=models.CharField(default=' ', max_length=150),
        ),
        migrations.AddField(
            model_name='invoice',
            name='cost_str',
            field=models.CharField(default=' ', max_length=150),
        ),
    ]
