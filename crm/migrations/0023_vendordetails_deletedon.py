# Generated by Django 4.1 on 2024-08-02 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_remove_vendordetails_deletedon'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendordetails',
            name='deletedOn',
            field=models.DateTimeField(null=True, verbose_name='Deleted On'),
        ),
    ]
