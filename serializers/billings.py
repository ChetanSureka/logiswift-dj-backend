from crm.models import Billings
from rest_framework import serializers


class BillingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billings
        fields = "__all__"