# Generated by Django 4.1 on 2024-07-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_consignment_tatstatus_consignment_variance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consignment',
            name='variance',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]