from crm.models import VendorDetails
from serializers.coloaders import ColoaderSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def getColoaders(request):
    try:
        coloaders = VendorDetails.objects.all()
        serializer = ColoaderSerializer(coloaders, many=True)
        data = serializer.data
        return HttpResponse.Ok(data=data, message="Coloaders fetched successfully")
    except Exception as e:
        print("[ERROR] Error fetching coloaders: ", e)
        return HttpResponse.Failed()

