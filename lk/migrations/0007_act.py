# Generated by Django 4.0.3 on 2022-04-05 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lk', '0006_invoice_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_document', models.DateTimeField(blank=True, default=None, null=True)),
                ('number_invoice', models.CharField(max_length=10)),
                ('number_document', models.CharField(max_length=10)),
                ('client', models.CharField(max_length=100)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('inn', models.CharField(max_length=12)),
                ('kpp', models.CharField(blank=True, max_length=12, null=True)),
                ('adres', models.CharField(max_length=100)),
                ('telephon', models.CharField(blank=True, max_length=12, null=True)),
                ('service', models.CharField(max_length=150)),
                ('cost', models.CharField(max_length=11)),
                ('month', models.CharField(choices=[('январь', 'январь'), ('февраль', 'февраль'), ('март', 'март'), ('апрель', 'апрель'), ('май', 'май'), ('июнь', 'июнь'), ('июль', 'июль'), ('август', 'август'), ('сентябрь', 'сентябрь'), ('октябрь', 'октябрь'), ('ноябрь', 'ноябрь'), ('декабрь', 'декабрь')], default='январь', max_length=9)),
                ('year', models.CharField(default=2022, max_length=4)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
