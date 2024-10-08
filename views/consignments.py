import os
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Q, F, Case, When, Value, IntegerField
from django.utils import timezone
from crm.models import Consignment, ConsigneeConsigner
from serializers.consignments import ConsignmentSerializer, getConsignmentSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view
from utils.edd import calculate_expected_delivery
from utils.bill_calculator import calculate_bill
from utils.mis_report import generate_mis_report
from utils.bulk_consignment import process_bulk_consignment_creation
from django.http.response import FileResponse

@api_view(["GET"])
def getConsignments(request):
    '''
    [deprecated]
    '''
    try:
        # adding pagination limit offset
        limit = int(request.GET.get('limit', 90))
        offset = int(request.GET.get('offset', 0))
        
        total_count = Consignment.objects.count()
        
        # consignments = Consignment.objects.all().order_by('-lrDate')
        consignments = Consignment.objects.select_related("consignee_id", "consigner_id", "vendor_id").annotate(
            consigneeName=F('consignee_id__name'),
            consignerName=F('consigner_id__name'),
            vendorName=F('vendor_id__name')
        ).order_by('-lrDate')[offset: offset+limit]
        
        print("Consignments: %s" % len(consignments))
        
        serializer = getConsignmentSerializer(consignments, many=True)
        data = serializer.data
        response_data = {
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "results": data
        }
        return HttpResponse.Ok(data=response_data, message="Consignments fetched successfully")
    except Exception as e:
        print("Failed to fetch Consignments [ERROR]: ", e)
        return HttpResponse.Failed(error=e)


@api_view(["GET"])
def getConsignmentByLr(request, lr):
    try:
        consignment = Consignment.objects.get(lr=lr)
        if consignment:
            serializer = ConsignmentSerializer(consignment)
            data = [serializer.data]
            return HttpResponse.Ok(data=data, message="Consignment fetched successfully")
    except Consignment.DoesNotExist:
        print("[ERROR] Consignment not found.")
        return HttpResponse.BadRequest(message="Consignment not found")
    except Exception as e:
        print("Failed to get Consignment [ERROR]: ", e)
        return HttpResponse.Failed(error=e)


@api_view(["GET"])
def getFilteredConsignments(request):
    status = request.query_params.get('status')
    tatStatus = request.query_params.get('tatStatus')
    lrDelayed = request.query_params.get('delayed')
    notified = request.query_params.get('notified')
    mode = request.query_params.get('mode')
    from_date = request.query_params.get('fromDate')
    to_date = request.query_params.get('toDate')
    distributor = request.query_params.get('distributor')
    channel_partner = request.query_params.get('channelPartner')
    limit = request.query_params.get('limit')
    offset = request.query_params.get('offset')
    search = request.query_params.get('search')
    sort_by = request.query_params.get('sort_by', 'lrDate')
    sort_order = request.query_params.get('sort_order', '-1')
    
    
    try:
        queryset = Consignment.objects.select_related("consignee_id", "consigner_id", "vendor_id").annotate(
            consigneeName=F('consignee_id__name'),
            consignerName=F('consigner_id__name'),
            vendorName=F('vendor_id__name')
        )
        
        total_count = Consignment.objects.count()
        
        if search:
            queryset = queryset.filter(
                Q(lr=search) | Q(lr__startswith=search) | Q(lr__contains=search)
            ).annotate(
                search_order=Case(
                    When(lr=search, then=Value(0)),
                    When(lr__startswith=search, then=Value(1)),
                    When(lr__contains=search, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            ).order_by('search_order', 'lr')


        if status:
            queryset = queryset.filter(status=status)
        if tatStatus:
            queryset = queryset.filter(tatstatus=tatStatus)
        if lrDelayed:
            if lrDelayed == 'true':
                queryset = queryset.filter(delayed=True)
            else:
                queryset = queryset.filter(delayed=False)
        
        if notified == "true":
            if lrDelayed == 'true':
                queryset = queryset.filter(delayed=True)
            else:
                queryset = queryset.filter(delayed=False)
        
        if mode:
            queryset = queryset.filter(mode=mode)
        if from_date:
            queryset = queryset.filter(lrDate__gte=from_date)
        if to_date:
            queryset = queryset.filter(lrDate__lte=to_date)

        if distributor:
            try:
                distributor = int(distributor)
                queryset = queryset.filter(Q(consignee_id=distributor) | Q(consigner_id=distributor))
            except ValueError:
                pass

        if channel_partner:
            try:
                channel_partner = channel_partner
                queryset = queryset.filter(vendor_id=channel_partner)
            except ValueError:
                pass
        
        # Sorting
        sort_order_prefix = '-' if sort_order == '-1' else ''

        # If sorting by 'lr' numerically
        if sort_by == 'lr':
            queryset = sorted(queryset, key=lambda x: int(x.lr))
        
            # If sorting direction needs to be reversed
            if sort_order_prefix == '-':
                queryset = reversed(queryset)
        
            # Convert queryset to a list to get its length
            queryset = list(queryset)
        
        else:
            queryset = queryset.order_by(f"{sort_order_prefix}{sort_by}")
            # queryset = queryset.order_by("-lrDate")

        
        total_results = len(queryset)
        
        if limit or offset:
            limit = int(limit)
            offset = int(offset)
            queryset = queryset[offset: offset+limit]
        
        print("Consignments filtered: ", queryset)
        serilaizer = getConsignmentSerializer(queryset, many=True)
        data = serilaizer.data
        response_data = {
            # "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "results_count": len(data),
            "total_results": total_results,
            "results": data,
        }
        return HttpResponse.Ok(data=response_data, message="Filtered consignments fetched successfully")
    
    except Exception as e:
        print("[ERROR] Failed to filter consignments: ", e)
        return HttpResponse.Failed(error=e)


@api_view(["DELETE"])
def deleteConsignment(request, lr):
    try:
        consignment = Consignment.objects.get(lr=lr)
    
        if consignment:
            consignment.delete()
            pass
        else:
            return HttpResponse.BadRequest(message="Consignment with the given lr doesn't exist")
    
        return HttpResponse.Ok(data=None, message="Consignment deleted successfully")
    
    except Exception as e:
        print("[ERROR] Failed to delete consignment: ", e)
        return HttpResponse.Failed(error=e)


@api_view(["POST"])
def createConsignment(request):
    '''
    request body:
    {
        "lr": 123,
        "lrDate": "2023-05-02",
        "quantity": 1,
        "weight": 12.09,
        "status": 1,
        "mode": 1,
        "remarks": "This is a remark",
        "deliveryDate": "2023-05-02",
        "consigneeId": 1,
        "consignerId": 2,
        "coloaderId": 1
    }
    '''

    req_data = request.data
    if not req_data:
        return HttpResponse.BadRequest(message="Invalid request")
    
    try:
        
        # fetch consignee tat
        try:
            tat = ConsigneeConsigner.objects.get(id=req_data['consigner_id']).tat
            if tat is None:
                tat = 0
        except Exception as e:
            print("Error fetching consignee tat: \n", e)
        
        req_data["expectedDeliveryDate"] = calculate_expected_delivery(req_data['lrDate'], tat)
        
        # Ensure weight and additionalCharges are in decimal format
        try:
            req_data['weight'] = Decimal(req_data.get('weight', 0))
            req_data['additionalCharges'] = Decimal(req_data.get('additionalCharges', 0))
        except (TypeError, ValueError) as e:
            print("[ERROR] Invalid decimal values: ", e)
            return HttpResponse.BadRequest(message="Invalid decimal values.")
        
        
        serializer = ConsignmentSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Consignment created successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] failed to create consignment: ", e)
        return HttpResponse.Failed(message="Failed to create consignment", error=e)



@api_view(["POST"])
def createBulkConsignment(request):
    req_data = request.data

    if not req_data or not isinstance(req_data, list):
        return HttpResponse.BadRequest(
            message="Invalid request. Expected a list of consignments"
        )

    # Process the consignment list
    response_data = process_bulk_consignment_creation(req_data)
    total_count = len(response_data)
    success_count = 0
    failure_count = 0

    # Single pass over response data
    for item in response_data:
        if item["status_code"] == 201:
            success_count += 1
        elif item["status_code"] in (400, 500):
            failure_count += 1

    # Check the results
    if success_count == total_count:
        # All consignments were successfully created
        return HttpResponse.Ok(
            data=response_data,
            message="All consignments were successfully created.",
            statusCode=200
        )
    elif failure_count == total_count:
        # All consignments failed
        return HttpResponse.Ok(
            data=response_data,
            message="Failed to create all consignments.",
            statusCode=400
        )
    else:
        # Partial success
        return HttpResponse.Ok(
            data=response_data,
            message="Bulk consignment creation partially complete with some errors.",
            statusCode=207,
            status="multi-status"
        )




@api_view(["PATCH", "PUT", "POST"])
def updateConsignment(request, lr):
    '''
    request body:
    {
        "lr": 123,
        "lrDate": "2023-05-02",
        "quantity": 1,
        "weight": 12.09,
        "status": 1,
        "mode": 1,
        "remarks": "This is a remark",
        "deliveryDate": "2023-05-02",
        "consigneeId": 1,
        "consignerId": 2,
        "coloaderId": 1
    }
    '''

    # Check if the consignment alredy exists
    consignment = Consignment.objects.get(lr=lr)
    if not consignment:
        return HttpResponse.BadRequest(message="Consignment not found")
    
    # check if there's any request body
    req_data = request.data
    if not req_data:
        return HttpResponse.BadRequest(message="Invalid request")
    
    
    try:
        
        # fetch consignee tat
        try:
            if consignment.mode == "reverse":
                tat = ConsigneeConsigner.objects.get(id=req_data['consignee_id']).tat
            else:
                tat = ConsigneeConsigner.objects.get(id=req_data['consigner_id']).tat
            if tat is None:
                tat = 0
        except Exception as e:
            print("Error fetching consignee tat: \n", e)
        
        req_data["expectedDeliveryDate"] = calculate_expected_delivery(req_data['lrDate'], tat)
        
        serializer = ConsignmentSerializer(consignment, data=req_data, partial=True)
        if serializer.is_valid():
            status = serializer.validated_data.get("status", None)
            deliveryDate = serializer.validated_data.get("deliveryDate", None)
            expectedDeliveryDate = serializer.validated_data.get("expectedDeliveryDate", None)
            
            if status == "delivered":
            
                if deliveryDate is None:
                    deliveryDate = timezone.now().date()
                    serializer.validated_data["deliveryDate"] = deliveryDate
            
                if deliveryDate and expectedDeliveryDate:
                    deliveryDate = datetime.strptime(str(deliveryDate), '%Y-%m-%d').date()
                    expectedDeliveryDate = datetime.strptime(str(expectedDeliveryDate), '%Y-%m-%d').date()
                    
                    variance = (deliveryDate - expectedDeliveryDate).days
                    tatStatus = "passed" if deliveryDate <= expectedDeliveryDate else "failed"
                    
                    serializer.validated_data["variance"] = variance
                    serializer.validated_data["tatstatus"] = tatStatus
                
                saved_consignment = serializer.save()
                bill = calculate_bill(saved_consignment)
                serializer.data["bill"] = bill.id
            else:
                serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Consignment updated successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] failed to update consignment: ", e)
        return HttpResponse.Failed(message="Failed to update consignment")


@api_view(["GET"])
def getStatusCount(request):
    '''
    Returns counts of consignments for various statuses:
    - all
    - in-transit
    - reached
    - out-for-delivery
    - delivered
    '''
    try:
        consignment_obj = Consignment.objects
        all_count = consignment_obj.all().count()
        in_transit_count = consignment_obj.filter(status="in-transit").count()
        reached_count = consignment_obj.filter(status="reached").count()
        out_for_delivery_count = consignment_obj.filter(status="out-for-delivery").count()
        delivered_count = consignment_obj.filter(status="delivered").count()
        
        
        status_counts = {
            "all": all_count,
            "in-transit": in_transit_count,
            "reached": reached_count,
            "out-for-delivery": out_for_delivery_count,
            "delivered": delivered_count,
        }
        
        return HttpResponse.Ok(data=status_counts, message="Status count fetched successfully")
    
    except Exception as e:
        print("[ERROR] failed to get status count: ", e)
        return HttpResponse.Failed("Failed to get status count", error=e)


@api_view(["GET"])
def getMis(request):
    """
    Generates an Excel MIS report for a given date range or for the current month by default.
    """
    today = datetime.now().date()
    
    # Get fromDate and toDate from the request, default to current month's date range if not provided
    fromDate = request.GET.get('fromDate', None)
    toDate = request.GET.get('toDate', None)
    
    if fromDate is None and toDate is None:
        # Default to the current month's date range
        fromDate = today.replace(day=1).strftime('%Y-%m-%d')
        toDate = today.strftime('%Y-%m-%d')
    
    # Convert fromDate and toDate to datetime objects
    try:
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
        toDate = datetime.strptime(toDate, "%Y-%m-%d")
    except ValueError:
        return HttpResponse.BadRequest(message="Invalid date format. Please use YYYY-MM-DD.")
    
    # Ensure toDate is not earlier than fromDate
    if toDate < fromDate:
        return HttpResponse.BadRequest(message="End date must be on or after the start date.")
    
    try:
        # Generate the MIS report for the specified date range
        report_file = generate_mis_report(fromDate, toDate)
        response = FileResponse(open(report_file, 'rb'), as_attachment=True, filename=report_file)
        # os.remove(report_file)
        return response
    except Exception as e:
        print("Error generating MIS report: ", e)
        return HttpResponse.Failed(message="Error generating MIS report")