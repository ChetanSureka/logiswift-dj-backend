# Generated by Django 4.1 on 2024-09-14 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_rename_lr_billings_consignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendordetails',
            old_name='miscCharge',
            new_name='additionalCharges',
        ),
        migrations.RenameField(
            model_name='vendordetails',
            old_name='fixedCharge',
            new_name='rate',
        ),
    ]
