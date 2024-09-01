from crm.models import ConsigneeConsigner
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from utils.edd import calculate_expected_delivery
from serializers.consignments import ConsignmentSerializer


def process_bulk_consignment_creation(consignment_list):
    successful_creations = []
    failed_creations = []

    for consignment_data in consignment_list:
        try:
            # Fetch consignee TAT
            try:
                tat = ConsigneeConsigner.objects.get(id=consignment_data['consigner_id']).tat
                if tat is None:
                    tat = 0
            except ObjectDoesNotExist:
                tat = 0
                print("Consigner ID not found. Defaulting TAT to 0.")

            # Calculate expected delivery date
            consignment_data["expectedDeliveryDate"] = calculate_expected_delivery(consignment_data['lrDate'], tat)

            # Ensure weight and additionalCharges are in decimal format
            try:
                consignment_data['weight'] = Decimal(consignment_data.get('weight', 0))
                consignment_data['additionalCharges'] = Decimal(consignment_data.get('additionalCharges', 0))
            except (TypeError, ValueError) as e:
                raise ValueError("Invalid decimal values: " + str(e))

            # Serialize and save the consignment
            serializer = ConsignmentSerializer(data=consignment_data)
            if serializer.is_valid():
                serializer.save()
                successful_creations.append(serializer.data)
            else:
                failed_creations.append({"data": consignment_data, "errors": serializer.errors})
        except (ValueError, IntegrityError) as e:
            # Handle specific errors and log them
            failed_creations.append({"data": consignment_data, "errors": str(e)})
        except Exception as e:
            # Handle any other unexpected errors
            failed_creations.append({"data": consignment_data, "errors": "Failed to create consignment: " + str(e)})

    return {"successful": successful_creations, "failed": failed_creations}

