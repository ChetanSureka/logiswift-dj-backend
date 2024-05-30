# Generated by Django 4.1.5 on 2023-05-01 22:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConsigneeConsigner",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("address", models.CharField(max_length=200, verbose_name="Address")),
                (
                    "destination",
                    models.CharField(max_length=100, verbose_name="Destination"),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="State"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "pincode",
                    models.CharField(
                        blank=True, max_length=7, null=True, verbose_name="Pincode"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        default=0,
                        max_length=10,
                        null=True,
                        verbose_name="Phone",
                    ),
                ),
                (
                    "location_type",
                    models.CharField(
                        choices=[("ODA", "ODA"), ("Normal", "Normal")],
                        default="Normal",
                        max_length=100,
                        verbose_name="Location Type",
                    ),
                ),
                (
                    "createdDate",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date"
                    ),
                ),
                (
                    "createdBy",
                    models.CharField(
                        default=0, max_length=100, verbose_name="Created By"
                    ),
                ),
                (
                    "modifiedDate",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Modified Date"
                    ),
                ),
                (
                    "modifiedBy",
                    models.CharField(
                        default=0, max_length=100, verbose_name="Modified By"
                    ),
                ),
                (
                    "deletedOn",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Deleted On"
                    ),
                ),
            ],
            options={
                "verbose_name": "Distributor",
                "verbose_name_plural": "Distributors",
            },
        ),
        migrations.CreateModel(
            name="Consignment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "lr",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="LR No.",
                    ),
                ),
                ("quantity", models.IntegerField(default=0, verbose_name="Quantity")),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=7,
                        verbose_name="Weight in kgs",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ["Created", "Created"],
                            ["In-transit", "In-transit"],
                            ["Reached", "Reached"],
                            ["Out For Delivery", "Out For Delivery"],
                            ["Delivered", "Delivered"],
                            ["Attempted", "Attempted"],
                            ["Returned", "Returned"],
                            ["undelivered", "undelivered"],
                        ],
                        default="Shipped",
                        max_length=100,
                        verbose_name="Consignment Status",
                    ),
                ),
                (
                    "pod",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="pod/",
                        verbose_name="Proof of Delivery",
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[["Forward", "Forward"], ["Reverse", "Reverse"]],
                        default="Forward",
                        max_length=100,
                        verbose_name="Consignment Mode",
                    ),
                ),
                (
                    "reverseDocketNo",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Reverse Docket Number",
                    ),
                ),
                (
                    "remarks",
                    models.CharField(
                        blank=True, max_length=500, null=True, verbose_name="Remarks"
                    ),
                ),
                ("createdDate", models.DateField(verbose_name="LR Date")),
                (
                    "createdBy",
                    models.CharField(max_length=100, verbose_name="Created By"),
                ),
                (
                    "deliveryDate",
                    models.DateField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Delivery Date",
                    ),
                ),
                (
                    "modifiedDate",
                    models.DateTimeField(auto_now=True, verbose_name="Modified Date"),
                ),
                (
                    "modifiedBy",
                    models.CharField(max_length=100, verbose_name="Modified By"),
                ),
                (
                    "deletedOn",
                    models.DateTimeField(auto_now=True, verbose_name="Deleted On"),
                ),
            ],
            options={
                "verbose_name": "Consignment",
                "verbose_name_plural": "Consignments",
            },
        ),
        migrations.CreateModel(
            name="ConsignmentAudit",
            fields=[
                ("audit_id", models.AutoField(primary_key=True, serialize=False)),
                ("quantity", models.IntegerField(default=0, verbose_name="Quantity")),
                (
                    "weight",
                    models.IntegerField(default=0, verbose_name="Weight in gms"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ["Created", "Created"],
                            ["In-transit", "In-transit"],
                            ["Reached", "Reached"],
                            ["Out For Delivery", "Out For Delivery"],
                            ["Delivered", "Delivered"],
                            ["Attempted", "Attempted"],
                            ["Returned", "Returned"],
                            ["undelivered", "undelivered"],
                        ],
                        default="Shipped",
                        max_length=100,
                        verbose_name="Consignment Status",
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[["Forward", "Forward"], ["Reverse", "Reverse"]],
                        default="Forward",
                        max_length=100,
                        verbose_name="Consignment Mode",
                    ),
                ),
                (
                    "reverseDocketNo",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Reverse Docket Number",
                    ),
                ),
                (
                    "createdDate",
                    models.DateTimeField(auto_now_add=True, verbose_name="LR Date"),
                ),
                (
                    "createdBy",
                    models.CharField(max_length=100, verbose_name="Created By"),
                ),
                (
                    "deliveryDate",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Delivery Date",
                    ),
                ),
                (
                    "modifiedDate",
                    models.DateTimeField(auto_now=True, verbose_name="Modified Date"),
                ),
                (
                    "modifiedBy",
                    models.CharField(max_length=100, verbose_name="Modified By"),
                ),
                (
                    "deletedOn",
                    models.DateTimeField(auto_now=True, verbose_name="Deleted On"),
                ),
            ],
            options={
                "verbose_name": "Consignment Audit",
                "verbose_name_plural": "Consignment Audits",
            },
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.CharField(blank=True, max_length=100, null=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(blank=True, max_length=100, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                ("amount", models.IntegerField(default=0, verbose_name="Amount")),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("Cash", "Cash"),
                            ("UPI", "UPI"),
                            ("NEFT", "NEFT"),
                            ("Others", "Others"),
                        ],
                        default="Cash",
                        max_length=100,
                        verbose_name="Mode",
                    ),
                ),
                ("transaction_date", models.DateField(verbose_name="Transaction Date")),
                (
                    "transaction_number",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Transaction Number",
                    ),
                ),
                (
                    "expense_type",
                    models.CharField(
                        choices=[("Credit", "Credit"), ("Debit", "Debit")],
                        default="Debit",
                        max_length=100,
                        verbose_name="Expense Type",
                    ),
                ),
                ("is_loan", models.BooleanField(default=False, verbose_name="Is Loan")),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Completed", "Completed")],
                        default="Pending",
                        max_length=100,
                        verbose_name="Status",
                    ),
                ),
            ],
            options={
                "verbose_name": "Expense",
                "verbose_name_plural": "Expenses",
            },
        ),
        migrations.CreateModel(
            name="ExpenseCategory",
            fields=[
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.CharField(blank=True, max_length=100, null=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(blank=True, max_length=100, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("category", models.CharField(max_length=100, verbose_name="Category")),
                (
                    "sub_category",
                    models.CharField(max_length=100, verbose_name="Sub Category"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Inactive", "Inactive")],
                        default="Active",
                        max_length=100,
                        verbose_name="Status",
                    ),
                ),
            ],
            options={
                "verbose_name": "Expense Category",
                "verbose_name_plural": "Expense Categories",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("location", models.CharField(max_length=100)),
                (
                    "sublocation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("createdDate", models.DateTimeField(auto_now_add=True)),
                ("createdBy", models.CharField(blank=True, max_length=100, null=True)),
                ("modifiedDate", models.DateTimeField(auto_now=True, null=True)),
                ("modifiedBy", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.CharField(blank=True, max_length=100, null=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(blank=True, max_length=100, null=True)),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "mobile",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="Mobile"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=100, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Address"
                    ),
                ),
            ],
            options={
                "verbose_name": "Staff",
                "verbose_name_plural": "Staffs",
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(default=0, max_length=10)),
                ("pincode", models.CharField(max_length=7)),
                ("pin", models.IntegerField(default=0)),
                ("createdDate", models.DateTimeField(auto_now_add=True)),
                ("createdBy", models.CharField(max_length=100)),
                ("modifiedDate", models.DateTimeField(auto_now=True)),
                ("modifiedBy", models.CharField(max_length=100)),
                ("deletedOn", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(default=0, max_length=10)),
                ("pin", models.IntegerField(default=0)),
                ("createdDate", models.DateTimeField(auto_now_add=True)),
                ("createdBy", models.IntegerField()),
                ("modifiedDate", models.DateTimeField(auto_now=True)),
                ("modifiededBy", models.IntegerField()),
                ("deletedOn", models.DateTimeField(auto_now=True)),
                ("last_login", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Vendor",
                "verbose_name_plural": "Vendors",
            },
        ),
        migrations.CreateModel(
            name="VendorDetails",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Vendor Name")),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "vendorType",
                    models.CharField(
                        choices=[
                            ["CoLoader", "CoLoader"],
                            ["ChannelPartner", "ChannelPartner"],
                        ],
                        max_length=100,
                        verbose_name="Vendor Type",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "phone",
                    models.CharField(default=0, max_length=10, verbose_name="Phone"),
                ),
                (
                    "pincode",
                    models.CharField(
                        blank=True, max_length=7, null=True, verbose_name="Pincode"
                    ),
                ),
                (
                    "pin",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="pin"
                    ),
                ),
                (
                    "createdDate",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date"
                    ),
                ),
                (
                    "createdBy",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Created By"
                    ),
                ),
                (
                    "modifiedDate",
                    models.DateTimeField(auto_now=True, verbose_name="Modified Date"),
                ),
                (
                    "modifiedBy",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Modified By",
                    ),
                ),
                (
                    "deletedOn",
                    models.DateTimeField(auto_now=True, verbose_name="Deleted On"),
                ),
            ],
            options={
                "verbose_name": "Partner",
                "verbose_name_plural": "Partner",
            },
        ),
        migrations.CreateModel(
            name="VendorLocation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "createdDate",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2023, 5, 1, 22, 15, 24, 600142, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "createdBy",
                    models.CharField(
                        blank=True, default="System", max_length=100, null=True
                    ),
                ),
                ("modifiedDate", models.DateTimeField(auto_now=True)),
                (
                    "modifiedBy",
                    models.CharField(
                        blank=True, default="System", max_length=100, null=True
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.location"
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crm.vendordetails",
                    ),
                ),
            ],
            options={
                "verbose_name": "Location Mapping",
                "verbose_name_plural": "Location Mapping",
            },
        ),
        migrations.CreateModel(
            name="Manifest",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "manifest_id",
                    models.CharField(max_length=100, verbose_name="Manifest ID"),
                ),
                (
                    "coloader_amount",
                    models.IntegerField(default=0, verbose_name="Coloader Amount"),
                ),
                (
                    "vehicle_number",
                    models.CharField(
                        default="NA", max_length=100, verbose_name="Vehicle Number"
                    ),
                ),
                (
                    "vehicle_amount",
                    models.IntegerField(default=0, verbose_name="Vehicle Amount"),
                ),
                ("bag_count", models.IntegerField(default=0, verbose_name="Bag Count")),
                (
                    "status",
                    models.CharField(
                        choices=[["Created", "Created"], ["Drafted", "Drafted"]],
                        default="Created",
                        max_length=100,
                        verbose_name="Manifest Status",
                    ),
                ),
                (
                    "createdDate",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date"
                    ),
                ),
                (
                    "createdBy",
                    models.CharField(
                        default="Admin", max_length=100, verbose_name="Created By"
                    ),
                ),
                (
                    "modifiedDate",
                    models.DateTimeField(auto_now=True, verbose_name="Modified Date"),
                ),
                (
                    "modifiedBy",
                    models.CharField(
                        default="Admin", max_length=100, verbose_name="Modified By"
                    ),
                ),
                (
                    "deletedDate",
                    models.DateTimeField(auto_now=True, verbose_name="Deleted Date"),
                ),
                (
                    "coloader_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coloader_id",
                        to="crm.vendordetails",
                        verbose_name="Coloader",
                    ),
                ),
            ],
            options={
                "verbose_name": "Manifest",
                "verbose_name_plural": "Manifests",
            },
        ),
        migrations.AddIndex(
            model_name="expensecategory",
            index=models.Index(
                fields=["category", "sub_category"],
                name="crm_expense_categor_a38cd8_idx",
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expense_category",
                to="crm.expensecategory",
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="loan_linked",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="loan_linked_expense",
                to="crm.expense",
                verbose_name="Loan Linked",
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expense_staff",
                to="crm.staff",
                verbose_name="Staff",
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="vendor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expense_vendor",
                to="crm.vendordetails",
                verbose_name="Partner",
            ),
        ),
        migrations.AddField(
            model_name="consignmentaudit",
            name="consignee_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audit_consignee_id",
                to="crm.consigneeconsigner",
                verbose_name="Sender",
            ),
        ),
        migrations.AddField(
            model_name="consignmentaudit",
            name="consigner_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audit_consigner_id",
                to="crm.consigneeconsigner",
                verbose_name="Reciever",
            ),
        ),
        migrations.AddField(
            model_name="consignmentaudit",
            name="consignment_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audit_consignment_id",
                to="crm.consignment",
                verbose_name="Consignment",
            ),
        ),
        migrations.AddField(
            model_name="consignmentaudit",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audit_consignment_user_id",
                to="crm.users",
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="consignmentaudit",
            name="vendor_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audit_vendor_id",
                to="crm.vendordetails",
                verbose_name="Channel Partner",
            ),
        ),
        migrations.AddField(
            model_name="consignment",
            name="consignee_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="consignee_id",
                to="crm.consigneeconsigner",
                verbose_name="Sender",
            ),
        ),
        migrations.AddField(
            model_name="consignment",
            name="consigner_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="consigner_id",
                to="crm.consigneeconsigner",
                verbose_name="Reciever",
            ),
        ),
        migrations.AddField(
            model_name="consignment",
            name="manifestId",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="consignment_manifest_id",
                to="crm.manifest",
                verbose_name="Manifest",
            ),
        ),
        migrations.AddField(
            model_name="consignment",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="consignment_user_id",
                to="crm.users",
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="consignment",
            name="vendor_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vendor_id",
                to="crm.vendordetails",
                verbose_name="Channel Partner",
            ),
        ),
        migrations.AddField(
            model_name="consigneeconsigner",
            name="locationMappingId",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="locationMappingId",
                to="crm.location",
                verbose_name="Location",
            ),
        ),
        migrations.AddField(
            model_name="consigneeconsigner",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_id",
                to="crm.users",
                verbose_name="Users",
            ),
        ),
    ]