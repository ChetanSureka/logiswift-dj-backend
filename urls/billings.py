from django.urls import path
from views.billings import *

urlpatterns = [
    path("billings/update/bulk/", bulk_create_bills),
]
