from io import BytesIO
from django.db.models import Q, F, Case, When, Value, IntegerField
from crm.models import Consignment, Billings
from helpers.response import HttpResponse
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from utils.bill_calculator import calculate_bill
from utils.edd import calculate_expected_delivery
from utils.bill_stats import get_bill_stats
from serializers.consignments import ConsignmentSerializer
from serializers.billings import GetBillingsSerializer
import pandas as pd
from django.http.response import FileResponse

def update_consignment(consignment: Consignment):
    # fetch consignee tat
    try:
        if consignment.mode == "reverse":
            tat = consignment.consignee_id.tat+1
        else:
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



@api_view(["POST", "GET"])
def bulk_create_bills(request):
    try:
        fromDate = request.GET.get('fromDate', None)
        toDate = request.GET.get('toDate', None)
        
        if fromDate is None or toDate is None:
            today = datetime.today()
            fromDate = today.replace(day=1).strftime("%Y-%m-%d")
            toDate = ((today.replace(day=1) + timedelta(days=32)).replace(day=1) + timedelta(days=-1)).strftime("%Y-%m-%d")
        
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
        toDate = datetime.strptime(toDate, "%Y-%m-%d")
        print("request dates: ", toDate, ", fromDate: ", fromDate)
    except Exception as e:
        print("[ERROR] Invalid dates for bulk create request")
        return HttpResponse.BadRequest(message="Invalid date format. use yyyy-mm-dd")
    
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
        
        # write the bill data to excel file
        if bills:
            df = pd.DataFrame(bills)
        else:
            return HttpResponse.Ok(message="No consignments are delivered for the current month.")
        
        # Convert the DataFrame to an Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_forward = df[df["mode"].str.lower() == 'forward']
            df_reverse = df[df["mode"].str.lower() == 'reverse']
            
            df_forward.to_excel(writer, index=False, sheet_name='Forward')
            df_reverse.to_excel(writer, index=False, sheet_name='Reverse')
            
        # Seek to the beginning of the stream
        output.seek(0)

        # Create a FileResponse
        response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, filename=f"bill_{fromDate.date()}-{toDate.date()}.xlsx")
        response['Content-Disposition'] = f'attachment; filename=bill_{fromDate.date()}-{toDate.date()}.xlsx'

        return response
    
    
        # data = {
        #     "total_bills": len(bills),
        #     "total_delivered": consignments.count(),
        #     "fromDate": fromDate,
        #     "toDate": toDate,
        #     "excel_file": filepath,
        #     "bills": bills
        # }
        
        # return HttpResponse.Ok(data, message="Bills created successfully")
    
    except Exception as e:
        print("Error creating bulk bills: ", e)
        return HttpResponse.BadRequest(message="Error creating bills")


def filter_bills(queryset, filters: dict):
    tatstatus = filters.get('tatstatus')
    search = filters.get('search')
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    mode = filters.get('mode')
    
    if tatstatus:
        queryset = queryset.filter(tatstatus=tatstatus)
    
    if search:
        queryset = queryset.filter(
            Q(consignment__lr__iexact=search) | 
            Q(consignment__lr__startswith=search) | 
            Q(consignment__lr__icontains=search)
        ).annotate(
            search_order=Case(
                When(consignment__lr__iexact=search, then=Value(0)),
                When(consignment__lr__startswith=search, then=Value(1)),
                When(consignment__lr__icontains=search, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('search_order', 'consignment__lr')
    
    if from_date:
        queryset = queryset.filter(consignment__lrDate__gte=from_date)
    
    if to_date:
        queryset = queryset.filter(consignment__lrDate__lte=to_date)
    
    if mode:
        queryset = queryset.filter(consignment__mode=mode)
    
    queryset = queryset.order_by('-consignment__lrDate')
    
    return queryset

@api_view(["GET"])
def get_filtered_bills(request):
    '''
    filter by date
    filter by tatStatus
    
    search by lr
    '''
    limit = request.query_params.get('limit')
    offset = request.query_params.get('offset')
    
    queryset = Billings.objects.all()
    filters = {
        'tatstatus': request.query_params.get('tatstatus'),
        'search': request.query_params.get('search'),
        'from_date': request.query_params.get('fromDate'),
        'to_date': request.query_params.get('toDate'),
        'mode': request.query_params.get('mode'),
    }
    
    try:
        queryset = filter_bills(queryset, filters)
        
        total_results = len(queryset)
        
        if limit or offset:
            limit = int(limit)
            offset = int(offset)
            queryset = queryset[offset: offset+limit]
        
        serializer = GetBillingsSerializer(queryset, many=True)
        data = serializer.data
        response_data = {
            "limit": limit,
            "offset": offset,
            "results_count": len(data),
            "total_results": total_results,
            "results": data,
        }
        
        return HttpResponse.Ok(data=response_data, message="Filtered bills fetched successfully")
    
    except Exception as e:
        print("[ERROR] Failed to filter bills: ", e)
        return HttpResponse.Failed()


@api_view(["DELETE"])
def delete_bills(request, id):
    '''
    delete bills by lr
    '''
    try:
        billings = Billings.objects.filter(id=id)
        
        if not billings.exists():
            return HttpResponse.NotFound(message="No billings found for the provided id")

        count, _ = billings.delete()

        return HttpResponse.Ok(data={"deleted_count": count}, message=f"Successfully deleted {count} billing(s) with id {id}")
    
    except Exception as e:
        print("[ERROR] Failed to delete bills by id:", e)
        return HttpResponse.Failed(message="Failed to delete bills by id")


@api_view(["PUT", "PATCH"])
def update_bill(request, id):
    try:
        bill = Billings.objects.get(id=id)
        serializer = GetBillingsSerializer(bill, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # save the changes to qty and additionalcharge to the consignment table
            quantity = serializer.validated_data.get('quantity', bill.quantity)
            additionalCharge = serializer.validated_data.get('additionalCharge', bill.additionalCharge)
            
            consignment = bill.consignment
            consignment.quantity = quantity
            consignment.additionalCharges = additionalCharge
            consignment.save()
            
            # recalculate the bill based on updated values
            updated_bill = calculate_bill(consignment)
            updated_serializer = GetBillingsSerializer(updated_bill)
            res_data = updated_serializer.data
            
            return HttpResponse.Ok(data=res_data, message="Bill updated successfully")
        else:
            return HttpResponse.BadRequest(data=serializer.errors, message="Invalid data")
    
    except Billings.DoesNotExist:
        return HttpResponse.BadRequest(message="Bill not found")

    except Exception as e:
        print("[ERROR] Failed to update bill: ", e)
        return HttpResponse.Failed(message="Failed to update bill")


@api_view(["GET"])
def get_bill_by_id(request, id):
    try:
        bill = Billings.objects.get(id=id)
        serializer = GetBillingsSerializer(bill)
        return HttpResponse.Ok(data=serializer.data, message="Bill retrieved successfully")
    except Billings.DoesNotExist:
        return HttpResponse.BadRequest(message="Bill not found")
    except Exception as e:
        print("[ERROR] Failed to retrieve Bill: ", e)
        return HttpResponse.Failed(message="Failed to retrieve Bill")
    


@api_view(["GET"])
def getBillStats(request):
    queryset = Billings.objects.all()
    filters = {
        'tatstatus': request.query_params.get('tatstatus'),
        'search': request.query_params.get('search'),
        'from_date': request.query_params.get('fromDate'),
        'to_date': request.query_params.get('toDate'),
        'mode': request.query_params.get('mode'),
    }
    
    try:
        queryset = filter_bills(queryset, filters)
        stats = get_bill_stats(queryset)
        
        return HttpResponse.Ok(data=stats, message="Successfully fetched bill stats")
        
    except Exception as e:
        print("[ERROR] Failed to get bill stats")
        return HttpResponse.Failed(message="Failed to get bill stats")