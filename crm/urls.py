from django.urls import path
from views.consignments import *
from views.coloaders import *
from views.distributors import *



urlpatterns = [
    path("consignments/", getConsignments),
    path("consignments/filter/", getFilteredConsignments),
    path("consignment/create/", createConsignment),
    path("consignment/<str:lr>/update/", updateConsignment),
    path("consignment/<str:lr>/", getConsignmentByLr),
    path("consignment/<str:lr>/delete/", deleteConsignment),


    path("coloaders/", getColoaders),
    path("consigners/", getDistributors),
]
