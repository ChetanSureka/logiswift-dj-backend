from crm.models import VendorDetails
from rest_framework import serializers


class ChannelPartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorDetails
        fields = [
            "id",
            "name",

            "address",
            "email",
            "phone",

            "pincode",
            "pin",
            
            "odaCharge",
            "rate",
            "additionalCharges",
        ]