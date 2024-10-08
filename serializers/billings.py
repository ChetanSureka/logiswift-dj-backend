from crm.models import Billings, Consignment
from rest_framework import serializers


class ConsignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignment
        fields = ['lr']


class GetBillingsSerializer(serializers.ModelSerializer):
    
    lr = serializers.CharField(source='consignment.lr')
    lrDate = serializers.DateField(source='consignment.lrDate')
    deliveryDate = serializers.DateField(source='consignment.deliveryDate')
    mode = serializers.DateField(source='consignment.mode')

    class Meta:
        model = Billings
        fields = [
            "id",
            "consignment",
            "lr",
            "lrDate",
            "deliveryDate",
            "mode",
            "tatstatus",
            "variance",
            "consigneeId",
            "consignerId",
            "locationId",
            "locationName",
            "consigneeName",
            "consignerName",
            "chargeableWeight",
            "quantity",
            "amount",
            "rate",
            "additionalCharge",
            "odaCharge",
            "totalAmount",
            "cp_chargeableWeight",
            "cp_amount",
            "cp_rate",
            "cp_additionalCharge",
            "cp_odaCharge",
            "cp_totalAmount",
            "vehicleCharge",
            "miscCharge",
            "miscRemark",
            "labourCharge",
            "officeExpense",
        ]


class BillingSerializer(serializers.Serializer):
    class Meta:
        model = Billings
        fields = "__all__"

