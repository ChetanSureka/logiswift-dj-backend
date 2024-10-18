from django.utils import timezone
from rest_framework.decorators import api_view
from helpers.response import HttpResponse
from crm.models import Consignment


@api_view(["GET"])
def tatUpdate(request):
    current_date = timezone.now().date()
    ctu = Consignment.objects.filter(expectedDeliveryDate__lt=current_date)
    if ctu.count() > 0:    
        count = ctu.update(tatstatus="failed")
        return HttpResponse.Ok(message=f"updated {count} consignments with failed status")
    return HttpResponse.Ok(message="no consignments with edd > today found")