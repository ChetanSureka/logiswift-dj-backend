from crm.models import ConsigneeConsigner
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from utils.edd import calculate_expected_delivery
from serializers.consignments import ConsignmentSerializer

def process_bulk_consignment_creation(consignment_list):
    """
    Processes a list of consignments for bulk creation.
    Returns a list of consignments with status and errors (if any).
    """
    result = []

    for consignment_data in consignment_list:
        lr_number = consignment_data.get('lr', 'N/A')
        client_id = consignment_data.get('client_id', 'N/A')
        consignment_result = {
            "client_id": client_id,
            "lr": lr_number,
            "status": None,
            "status_code": None,
            "errors": None
        }

        try:
            # Fetch consignee TAT
            try:
                tat = ConsigneeConsigner.objects.get(id=consignment_data['consigner_id']).tat
                if tat is None:
                    tat = 0
            except ObjectDoesNotExist:
                tat = 0
                consignment_result["errors"] = "Consigner ID not found. Defaulting TAT to 0."

            # Calculate expected delivery date
            consignment_data["expectedDeliveryDate"] = calculate_expected_delivery(
                consignment_data['lrDate'], tat
            )

            # # Ensure weight and additionalCharges are in decimal format
            # try:
            #     consignment_data['weight'] = Decimal(consignment_data.get('weight', 0))
            #     consignment_data['additionalCharges'] = Decimal(consignment_data.get('additionalCharges', 0))
            # except (TypeError, ValueError) as e:
            #     raise ValueError("Invalid decimal values: " + str(e))

            # Serialize and save the consignment
            serializer = ConsignmentSerializer(data=consignment_data)
            if serializer.is_valid():
                serializer.save()
                consignment_result["status"] = "success"
                consignment_result["status_code"] = 201
            else:
                consignment_result["status"] = "failed"
                consignment_result["status_code"] = 400
                consignment_result["errors"] = serializer.errors

        except (ValueError, IntegrityError) as e:
            consignment_result["status"] = "failed"
            consignment_result["status_code"] = 400
            consignment_result["errors"] = str(e)
        except Exception as e:
            consignment_result["status"] = "failed"
            consignment_result["status_code"] = 500
            consignment_result["errors"] = "Failed to create consignment: " + str(e)

        result.append(consignment_result)

    return result
