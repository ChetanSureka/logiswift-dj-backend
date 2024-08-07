from io import BytesIO
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import FileResponse
from rest_framework.decorators import api_view
from crm.models import Consignment
from utils.bill_calculator import calculate_bill
from utils.edd import calculate_expected_delivery
from serializers.consignments import ConsignmentSerializer
import pandas as pd
from helpers.response import HttpResponse

def update_consignment(consignment: Consignment):
    try:
        if consignment.mode == "reverse":
            tat = consignment.consignee_id.tat + 1
        else:
            tat = consignment.consigner_id.tat
        if tat is None:
            tat = 0
    except Exception as e:
        print("Error fetching consignee tat: \n", e)
    
    req_data = {
        "expectedDeliveryDate": calculate_expected_delivery(str(consignment.lrDate), tat),
        "deliveryDate": consignment.deliveryDate
    }
    
    serializer = ConsignmentSerializer(consignment, data=req_data, partial=True)
    if serializer.is_valid():
        deliveryDate = serializer.validated_data.get("deliveryDate", None)
        expectedDeliveryDate = serializer.validated_data.get("expectedDeliveryDate", None)
        
        if deliveryDate and expectedDeliveryDate:
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

@api_view(["POST", "GET"])
def bulk_create_bills(request):
    try:
        fromDate = request.GET.get('fromDate', None)
        toDate = request.GET.get('toDate', None)
        
        if fromDate is None or toDate is None:
            today = datetime.today()
            fromDate = today.replace(day=1).strftime("%d-%m-%Y")
            toDate = ((today.replace(day=1) + timedelta(days=32)).replace(day=1) + timedelta(days=-1)).strftime("%d-%m-%Y")
        
        fromDate = datetime.strptime(fromDate, "%d-%m-%Y")
        toDate = datetime.strptime(toDate, "%d-%m-%Y")
        print("request dates: ", toDate, ", fromDate: ", fromDate)
    except Exception as e:
        print("[ERROR] Invalid dates for bulk create request")
        return HttpResponse.BadRequest(message="Invalid date format. use dd-mm-yyyy")
    
    try:
        forward_consignments = Consignment.objects.filter(
            Q(lrDate__gte=fromDate, lrDate__lte=toDate),
            mode='forward'
        ).order_by('lrDate')

        reverse_consignments = Consignment.objects.filter(
            Q(deliveryDate__gte=fromDate, deliveryDate__lte=toDate) |
            Q(deliveryDate__isnull=True, lrDate__lte=toDate),
            mode='reverse'
        ).order_by('lrDate')
        
        consignments = forward_consignments | reverse_consignments

        bills = []
        if consignments:
            for consignment in consignments:
                bill = update_consignment(consignment)
                if bill:
                    bills.append({
                        "lr": int(consignment.lr),
                        "lrDate": consignment.lrDate.strftime("%d-%b-%y"),
                        "sender": bill.consigneeName,
                        "reciever": bill.consignerName,
                        "actual_weight": float(consignment.weight),
                        "quantity": int(bill.quantity),
                        "chargable_weight": int(bill.chargeableWeight),
                        "rate": int(bill.rate),
                        "amount": int(bill.amount),
                        "odaCharge": int(bill.odaCharge),
                        "additionalCharge": float(bill.additionalCharge),
                        "totalAmount": float(bill.totalAmount),
                        "mode": consignment.mode,
                        "location": consignment.consigner_id.destination if consignment.mode == 'forward' else consignment.consignee_id.destination
                    })
        
        if not bills:
            return HttpResponse.Ok(message="No consignments are delivered for the current month.")
        
        df = pd.DataFrame(bills)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_forward = df[df["mode"].str.lower() == 'forward']
            df_reverse = df[df["mode"].str.lower() == 'reverse']
            
            df_forward.to_excel(writer, index=False, sheet_name='Forward')
            df_reverse.to_excel(writer, index=False, sheet_name='Reverse')
            
        output.seek(0)

        response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, filename=f"bill_{fromDate.date()}-{toDate.date()}.xlsx")
        response['Content-Disposition'] = f'attachment; filename=bill_{fromDate.date()}-{toDate.date()}.xlsx'

        return response
    
    except Exception as e:
        print("Error creating bulk bills: ", e)
        return HttpResponse.BadRequest(message="Error creating bills")
