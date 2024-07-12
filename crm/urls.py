from django.urls import path
from views.consignments import *
from views.coloaders import *
from views.dashboard import getDashboard
from urls.distributors import urlpatterns as distributor_urlpatterns

urlpatterns = [
    # path("consignments/", getConsignments),
    # path("consignments/filter/", getFilteredConsignments),
    path("consignments/statuscount/", getStatusCount),
    path("consignments/", getFilteredConsignments),
    path("consignment/create/", createConsignment),
    path("consignment/<str:lr>/update/", updateConsignment),
    path("consignment/<str:lr>/", getConsignmentByLr),
    path("consignment/<str:lr>/delete/", deleteConsignment),


    path("vendors/", getColoaders),
    
    path("dashboard/", getDashboard),
]

urlpatterns += distributor_urlpatterns
