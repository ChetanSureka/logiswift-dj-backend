from crm.models import VendorDetails
from rest_framework import serializers


class ColoaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorDetails
        fields = [
            "id",
            "name",
        ]