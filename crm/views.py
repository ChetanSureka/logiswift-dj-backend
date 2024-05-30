from .models import Consignment, ConsigneeConsigner, VendorDetails, Location
from .serializers import ConsignmentSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view

@api_view(["GET"])
def getConsignments(request):
    try:
        consignments = Consignment.objects.all().order_by('-lrDate')
        print("Consignments: %s" % len(consignments))
        serializer = ConsignmentSerializer(consignments, many=True)
        data = serializer.data
        return HttpResponse.Ok(data=data, message="Consignments fetched successfully")
    except Exception as e:
        print("Failed to fetch Consignments [ERROR]: ", e)
        return HttpResponse.Failed()


@api_view(["GET"])
def getConsignmentByLr(request, lr):
    try:
        consignment = Consignment.objects.get(lr=lr)
        if consignment:
            serializer = ConsignmentSerializer(consignment)
            data = serializer.data
            return HttpResponse.Ok(data=data, message="Consignment fetched successfully")
    except Exception as e:
        print("Failed to get Consignment [ERROR]: ", e)
        return HttpResponse.Failed()