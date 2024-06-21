from django.urls import path
from views.consignments import *
from views.coloaders import *
from views.distributors import *
from views.dashboard import getDashboard


urlpatterns = [
    # path("consignments/", getConsignments),
    path("consignments/statuscount/", getStatusCount),
    # path("consignments/filter/", getFilteredConsignments),
    path("consignments/", getFilteredConsignments),
    path("consignment/create/", createConsignment),
    path("consignment/<str:lr>/update/", updateConsignment),
    path("consignment/<str:lr>/", getConsignmentByLr),
    path("consignment/<str:lr>/delete/", deleteConsignment),


    path("vendors/", getColoaders),
    path("distributors/", getDistributors),
    
    path("dashboard/", getDashboard),
]
