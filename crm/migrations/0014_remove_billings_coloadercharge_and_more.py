# Generated by Django 4.1 on 2024-07-05 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_consignment_delayed_consignment_delayedreason_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billings',
            name='coloaderCharge',
        ),
        migrations.AlterField(
            model_name='billings',
            name='additionalCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='cp_additionalCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='cp_odaCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='created_by',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='labourCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='miscCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='miscRemark',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='odaCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='officeExpense',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='updated_by',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billings',
            name='vehicleCharge',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]
