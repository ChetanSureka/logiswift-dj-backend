from django.utils import timezone
from crm.models import Consignment
from helpers.response import HttpResponse

def updateTatStatus(request):
    current_date = timezone.now().date()
    ctu = Consignment.objects.filter(expectedDeliveryDate__lt=current_date)
    count = ctu.update(tatstatus="failed")
    
    return HttpResponse.Ok(message=f"updated {count} consignments with failed status")
    
