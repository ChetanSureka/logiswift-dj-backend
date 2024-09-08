from django.db.models import Q, Value, Case, When, IntegerField
from crm.models import ConsigneeConsigner
from serializers.distributors import DistributorSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view

@api_view(["GET"])
def getDistributor(request, id):
    try:
        distributor = ConsigneeConsigner.objects.get(id=id, deleted=False)
        serailizer = DistributorSerializer(distributor)
        return HttpResponse.Ok(data=serailizer.data, message="Distributor fetched successfully")
    
    except ConsigneeConsigner.DoesNotExist:
        return HttpResponse.BadRequest(message="Distributor not found")
    
    except Exception as e:
        print("[ERROR] Exception occured while fetching distributor: ", e)
        return HttpResponse.Failed(message="Exception occured while fetching distributor")


@api_view(["GET"])
def getDistributors(request):
    search = request.query_params.get("search")
    limit = request.query_params.get("limit")
    offset = request.query_params.get("offset")
    
    
    try:
        queryset = ConsigneeConsigner.objects.filter(deleted=False)
        
        if search:
            queryset = queryset.filter(
                Q(name__iexact=search) | Q(name__istartswith=search) | Q(name__icontains=search)
            )
        
        total_results = queryset.count()
        if limit or offset:
            limit = int(limit)
            offset = int(offset)
            queryset = queryset[offset:offset+limit]
        
        serializer = DistributorSerializer(queryset, many=True)
        data = serializer.data
        response_data = {
            "limit": limit,
            "offset": offset,
            "results_count": len(data),
            "total_results": total_results,
            "results": data,
        }
        return HttpResponse.Ok(data=response_data, message="Distributors fetched successfully")
    
    except Exception as e:
        print("[ERROR] Error fetching distributors: ", e)
        return HttpResponse.Failed(message="Error fetching distributors")
    
    # try:
    #     distributors = ConsigneeConsigner.objects.all()
    #     serializer = DistributorSerializer(distributors, many=True)
    #     data = serializer.data
    #     return HttpResponse.Ok(data=data, message="Distributors fetched successfully")
    # except Exception as e:
    #     print("[ERROR] Error fetching distributors: ", e)
    #     return HttpResponse.Failed()

@api_view(["POST"])
def createDistributors(request):

    try:
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Distributor created successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] Error creating distributor: ", e)
        return HttpResponse.Failed()


@api_view(["PATCH", "PUT"])
def updateDistributors(request, id):
    
    try:
        distributor = ConsigneeConsigner.objects.get(id=id, deleted=False)
    except ConsigneeConsigner.DoesNotExist:
        return HttpResponse.BadRequest(message="Distributor does not exist")

    try:
        serializer = DistributorSerializer(instance=distributor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Distributor updated successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] Error updating distributor: ", e)
        return HttpResponse.Failed(error=e)


@api_view(["DELETE"])
def deleteDistributor(request, id):
    try:
        distributor = ConsigneeConsigner.objects.get(id=id, deleted=False)
    except ConsigneeConsigner.DoesNotExist:
        return HttpResponse.BadRequest(message="Distributor does not exist")
    
    try:
        distributor.soft_delete()
        return HttpResponse.Ok(message="Distributor deleted successfully")
    except Exception as e:
        print("[ERROR] deleting distributor: ", e)
        return HttpResponse.Failed(message="An error occurred while deleting the distributor")


