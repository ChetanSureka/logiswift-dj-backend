from django.urls import path
from views.billings import *

urlpatterns = [
    path("billings/update/bulk/", bulk_create_bills),
    
    path("billings/", get_filtered_bills),
    path("billings/stats/", getBillStats),
    path("billings/<int:id>/", get_bill_by_id),
    path("billings/<int:id>/delete/", delete_bills),
    path("billings/<int:id>/update/", update_bill),
]
