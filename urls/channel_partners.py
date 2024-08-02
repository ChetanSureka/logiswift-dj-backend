from django.urls import path
from views.channel_partners import getChannelPartners, getChannelPartnerById, createChannelPartner, updateChannelPartner, deleteChannelPartner

urlpatterns = [
    path("channel-partners/", getChannelPartners),
    path("channel-partner/create/", createChannelPartner),
    path("channel-partner/<str:id>/", getChannelPartnerById),
    path("channel-partner/<str:id>/update/", updateChannelPartner),
    path("channel-partner/<str:id>/delete/", deleteChannelPartner),
]