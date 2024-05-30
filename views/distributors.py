from crm.models import ConsigneeConsigner
from serializers.distributors import DistributorSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def getDistributors(request):
    try:
        distributors = ConsigneeConsigner.objects.all()
        serializer = DistributorSerializer(distributors, many=True)
        data = serializer.data
        return HttpResponse.Ok(data=data, message="Distributors fetched successfully")
    except Exception as e:
        print("[ERROR] Error fetching distributors: ", e)
        return HttpResponse.Failed()

