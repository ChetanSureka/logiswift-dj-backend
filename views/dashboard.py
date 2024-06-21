from helpers.response import HttpResponse
from rest_framework.decorators import api_view
from utils.dashboard import *


@api_view(["GET"])
def getDashboard(request):
    try:
        data = generate_dashboard()
        return HttpResponse.Ok(data=data, message="Dashboard fetched successfully")
    except Exception as e:
        print("[ERROR] Error fetching Dashboard: ", e)
        return HttpResponse.Failed()

