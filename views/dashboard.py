from helpers.response import HttpResponse
from rest_framework.decorators import api_view
from utils.dashboard import *


@api_view(["GET"])
def getDashboard(request):
    try:
        # Extract request parameters with default values
        from_date = request.GET.get('fromDate', None)
        to_date = request.GET.get('toDate', None)
        
        # Generate the dashboard data based on the parameters
        data = generate_dashboard(from_date=from_date, to_date=to_date)
        return HttpResponse.Ok(data=data, message="Dashboard fetched successfully")
    except Exception as e:
        print("[ERROR] Error fetching Dashboard: ", e)
        return HttpResponse.Failed(error=e)

