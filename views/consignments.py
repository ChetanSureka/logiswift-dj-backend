from django.db.models import Q, F
from django.utils import timezone
from crm.models import Consignment
from serializers.consignments import ConsignmentSerializer, getConsignmentSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view

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
        return HttpResponse.Failed()


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
        return HttpResponse.Failed()


@api_view(["GET"])
def getFilteredConsignments(request):
    status = request.query_params.get('status')
    mode = request.query_params.get('mode')
    from_date = request.query_params.get('fromDate')
    to_date = request.query_params.get('toDate')
    distributor = request.query_params.get('distributor')
    channel_partner = request.query_params.get('channelPartner')
    limit = request.query_params.get('limit')
    offset = request.query_params.get('offset')
    
    
    try:
        queryset = Consignment.objects.select_related("consignee_id", "consigner_id", "vendor_id").annotate(
            consigneeName=F('consignee_id__name'),
            consignerName=F('consigner_id__name'),
            vendorName=F('vendor_id__name')
        ).order_by('-lrDate')
        
        total_count = Consignment.objects.count()
        
        
        if status:
            queryset = queryset.filter(status=status)
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
        
        if limit or offset:
            limit = int(limit)
            offset = int(offset)
            queryset = queryset[offset: offset+limit]
        
        print("Consignments filtered: ", queryset)
        serilaizer = getConsignmentSerializer(queryset, many=True)
        data = serilaizer.data
        response_data = {
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "results_count": len(data),
            "results": data
        }
        return HttpResponse.Ok(data=response_data, message="Filtered consignments fetched successfully")
    
    except Exception as e:
        print("[ERROR] Failed to filter consignments: ", e)
        return HttpResponse.Failed()


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
        return HttpResponse.Failed()


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
        serializer = ConsignmentSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Consignment created successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] failed to create consignment: ", e)
        return HttpResponse.Failed(message="Failed to create consignment")



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
        serializer = ConsignmentSerializer(consignment, data=req_data, partial=True)
        if serializer.is_valid():
            status = serializer.validated_data.get("status", None)
            deliveryDate = serializer.validated_data.get("deliveryDate", None)
            if status == "delivered" and deliveryDate is None:
                serializer.validated_data["deliveryDate"] = timezone.now().date()
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Consignment updated successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] failed to create consignment: ", e)
        return HttpResponse.Failed(message="Failed to create consignment")


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
        return HttpResponse.Failed({"error": "Failed to get status count"})

    