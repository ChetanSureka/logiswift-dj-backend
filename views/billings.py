from django.db.models import Q, Value, Case, When, IntegerField
from crm.models import Billings, Consignment
from serializers.billings import BillingsSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view
from datetime import datetime, timezone
from utils.bill_calculator import calculate_bill
from utils.missing_lrs import find_missing_numbers
from core.settings import BASE_DIR
from utils.edd import calculate_expected_delivery
from serializers.consignments import ConsignmentSerializer
import pandas as pd
import os

def update_consignment(consignment: Consignment):
    try:
        tat = consignment.consigner_id.tat
        if tat is None:
            tat = 0
    except Exception as e:
        print("Error fetching consignee tat: \n", e)
    
    req_data = {}
    req_data["expectedDeliveryDate"] = calculate_expected_delivery(str(consignment.lrDate), tat)
    req_data["deliveryDate"] = consignment.deliveryDate
    
    serializer = ConsignmentSerializer(consignment, data=req_data, partial=True)
    if serializer.is_valid():
        deliveryDate = serializer.validated_data.get("deliveryDate", None)
        expectedDeliveryDate = serializer.validated_data.get("expectedDeliveryDate", None)
        
        if deliveryDate is None:
            deliveryDate = timezone.now().date()
            serializer.validated_data["deliveryDate"] = deliveryDate
    
        if deliveryDate and expectedDeliveryDate:
            deliveryDate = deliveryDate
            expectedDeliveryDate = datetime.strptime(str(expectedDeliveryDate), '%Y-%m-%d').date()
            
            variance = (deliveryDate - expectedDeliveryDate).days
            tatStatus = "passed" if deliveryDate <= expectedDeliveryDate else "failed"
            
            serializer.validated_data["variance"] = variance
            serializer.validated_data["tatstatus"] = tatStatus
        
        saved_consignment = serializer.save()
        bill = calculate_bill(saved_consignment)
        serializer.data["bill"] = bill.id
        
        return bill
    else:
        return None



@api_view(["POST"])
def bulk_create_bills(request):
    try:
        fromDate = request.data["fromDate"]
        fromDate = datetime.strptime(fromDate, "%d-%m-%Y")
        
        toDate = request.data["toDate"]
        toDate = datetime.strptime(toDate, "%d-%m-%Y")
        
        print("request dates: ", toDate, ", fromDate: ", fromDate)
    except Exception as e:
        print("[ERROR] Invalid dates for bulk create request")
        return HttpResponse.BadRequest(message="Invalid date format. use dd-mm-yyyy")
    
    try:
        consignments = Consignment.objects.filter(
            Q(deliveryDate__gte=fromDate),
            Q(deliveryDate__lte=toDate),
            Q(status="delivered"),
        ).order_by("-lrDate")
        
        # missing_lrs = find_missing_numbers(consignments)
        # print("[INFO] Missing LRs: ", missing_lrs)
        
        bills = []
        if consignments:
            for consignment in consignments:
                # bills[consignment.lr] = calculate_bill(consignment).id
                # bills[consignment.lr] = bill_id
                bill = update_consignment(consignment)
                bills.append({
                    "lr": consignment.lr,
                    "lrDate": consignment.lrDate,
                    "sender": bill.consigneeName,
                    "reciever": bill.consignerName,
                    "actual_weight": consignment.weight,
                    "quantity": bill.quantity,
                    "chargable_weight": bill.chargeableWeight,
                    "rate": bill.rate,
                    "odaCharge": bill.odaCharge,
                    "amount": bill.amount,
                    "additionalCharge": bill.additionalCharge,
                    "totalAmount": bill.totalAmount,
                    "mode": consignment.mode,
                    "location": consignment.consigner_id.destination
                })
        
        # write the bill data to excel file
        df = pd.DataFrame(bills)
        
        # Convert the DataFrame to an Excel file
        filepath = os.path.join(BASE_DIR,  f"bills\\bill_{fromDate.date()}-{toDate.date()}.xlsx")
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Forward')
        
        data = {
            "total_bills": len(bills),
            "total_delivered": consignments.count(),
            "fromDate": fromDate,
            "toDate": toDate,
            "bills": bills
        }
        
        return HttpResponse.Ok(data, message="Bills created successfully")
    
    except Exception as e:
        print("Error creating bulk bills: ", e)
        return HttpResponse.BadRequest(message="Error creating bills")



