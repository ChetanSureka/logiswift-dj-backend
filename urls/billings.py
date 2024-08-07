from django.urls import path
from views.billings import bulk_create_bills

urlpatterns = [
    path("billings/update/bulk/", bulk_create_bills),
]
