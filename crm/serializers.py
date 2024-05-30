from .models import Consignment, ConsigneeConsigner, VendorDetails
from rest_framework import serializers


class ConsignmentSerializer(serializers.ModelSerializer):
    consigneeName = serializers.SerializerMethodField()
    consignerName = serializers.SerializerMethodField()
    vendorName = serializers.SerializerMethodField()

    class Meta:
        model = Consignment
        fields = [
            "id",
            "lr",
            "lrDate",
            "quantity",
            "weight",
            "status",
            "mode",
            "remarks",
            "deliveryDate",
            "consignee_id",
            "consigneeName",
            "consigner_id",
            "consignerName",
            "vendor_id",
            "vendorName",
        ]

    def get_consigneeName(self, obj):
        consignee = obj.consignee_id
        return consignee.name if consignee else None

    def get_consignerName(self, obj):
        consigner = obj.consigner_id
        return consigner.name if consigner else None

    def get_vendorName(self, obj):
        vendor = obj.vendor_id
        return vendor.name if vendor else None
