from crm.models import Consignment, ConsigneeConsigner, VendorDetails
from rest_framework import serializers


class getConsignmentSerializer(serializers.ModelSerializer):
    consigneeName = serializers.CharField()
    consignerName = serializers.CharField()
    vendorName = serializers.CharField()

    class Meta:
        model = Consignment
        # fields = '__all__'
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
            "expectedDeliveryDate",
            "delayed",
            "delayedReason",
            "notified",
            "notifiedDate"
        ]


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
            
            "expectedDeliveryDate",
            "delayed",
            "delayedReason",
            "notified",
            "notifiedDate",
            "additionalCharges",
            "additionalChargesReason",
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
    
    
    # add validations
    def validate_lr(self, value):
        try:
            value = int(value)
        except Exception as e:
            return value
        
        if value <= 0:
            raise serializers.ValidationError("LR number can't be negative or zero.")
        if value > 999999:
            raise serializers.ValidationError("LR number can't be greater than 6 digits.")
        return value


    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity can't be negative or zero.")
        if value > 9999:
            raise serializers.ValidationError("Quantity can't exceed 4 digits.")
        return value


    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight can't be negative or zero.")
        if value > 99999:
            raise serializers.ValidationError("Weight can't exceed 5 digits.")
        return value
    
    
    def validate(self, data):
        lrDate = data.get('lrDate')
        deliveryDate = data.get('deliveryDate')
        delayed = data.get('delayed', False)
        delayedReason = data.get('delayedReason', None)
        notified = data.get('notified', False)
        notifiedDate = data.get('notifiedDate', None)
        errors = {}

        # lr date and delivery date validations
        if lrDate and deliveryDate and deliveryDate < lrDate:
            errors["deliveryDate"] = "Delivery date cannot be before LR date"
        
        # delayed validations
        if delayed and not delayedReason:
            errors["delayedReason"] = "Delayed reason must be provided when delayed is true."
        if not delayed and delayedReason:
            errors["delayedReason"] = "Delayed reason must be empty when delayed is false."
        
        # notified validations
        if notified and not notifiedDate:
            errors["notifiedDate"] = "Notified date must be provided when notified is true."
        if not notified and notifiedDate:
            errors["notifiedDate"] = "Notified date must be empty when notified is false."

        if errors:
            raise serializers.ValidationError(errors)
        return data
    
