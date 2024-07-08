from django.urls import path
from views.distributors import *

urlpatterns = [
    path("distributor/create/", createDistributors),
    
    path("distributors/", getDistributors),
    path("distributor/<int:id>/", getDistributor),
    
    path("distributor/<int:id>/update/", updateDistributors),
    
    path("distributor/<int:id>/delete/", deleteDistributor),
    
]
