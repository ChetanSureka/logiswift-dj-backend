from crm.models import ConsigneeConsigner
from rest_framework import serializers


class DistributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsigneeConsigner
        fields = [
            "id",
            "name",
            "address",
            "destination",

            "state",
            "email",
            "phone",

            "vendor_id",

            "tat",
            "rate",
            "odaCharge",
        ]
