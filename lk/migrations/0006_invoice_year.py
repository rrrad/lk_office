# Generated by Django 4.0.3 on 2022-04-05 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0005_invoice_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='year',
            field=models.CharField(default=2022, max_length=4),
        ),
    ]
