from django.db.models import Q
from crm.models import ConsigneeConsigner, VendorDetails
from serializers.channel_partners import ChannelPartnerSerializer
from helpers.response import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def getChannelPartners(request):
    limit = request.query_params.get("limit")
    offset = request.query_params.get("offset")
    search = request.query_params.get("search")
    distributor = request.query_params.get('distributor')

    try:
        queryset = VendorDetails.objects.filter(
            deleted=False)

        if search:
            queryset = queryset.filter(
                Q(name__iexact=search) | Q(
                    name__istartswith=search) | Q(name__icontains=search)
            )

        if distributor:
            try:
                distributor = int(distributor)
                queryset = queryset.filter(distributors=distributor)
            except ValueError:
                pass

        total_results = queryset.count()

        if offset:
            offset = int(offset)
            queryset = queryset[offset:]
        else:
            offset = 0

        if limit:
            limit = int(limit)
            queryset = queryset[:limit]

        serializer = ChannelPartnerSerializer(queryset, many=True)
        data = serializer.data
        response_data = {
            "limit": limit,
            "offset": offset,
            "results_count": len(data),
            "total_results": total_results,
            "results": data,
        }
        return HttpResponse.Ok(data=response_data, message="Channel Partners fetched successfully")

    except Exception as e:
        print("[ERROR] Error fetching channel partners: ", e)
        return HttpResponse.Failed(message="Error fetching channel partners")


@api_view(["GET"])
def getChannelPartnerById(request, id):
    try:
        channel_partner = VendorDetails.objects.get(id=id, deleted=False)
        serailizer = ChannelPartnerSerializer(channel_partner)
        return HttpResponse.Ok(data=serailizer.data, message="Channel Partner fetched successfully")

    except VendorDetails.DoesNotExist:
        return HttpResponse.BadRequest(message="Channel Partner not found")

    except Exception as e:
        print("[ERROR] Exception occured while fetching channel partner: ", e)
        return HttpResponse.Failed(message="Exception occured while fetching channel partner")


@api_view(["POST"])
def createChannelPartner(request):
    try:
        serializer = ChannelPartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Channel Partner created successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] Error creating channel partner: ", e)
        return HttpResponse.Failed()


@api_view(["PATCH", "PUT"])
def updateChannelPartner(request, id):

    try:
        cp = VendorDetails.objects.get(id=id, deleted=False)
    except VendorDetails.DoesNotExist:
        return HttpResponse.BadRequest(message="Channel Partner does not exist")

    try:
        serializer = ChannelPartnerSerializer(
            instance=cp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse.Ok(data=serializer.data, message="Channel Partner updated successfully")
        return HttpResponse.BadRequest(message=serializer.errors)
    except Exception as e:
        print("[ERROR] Error updating channel partner: ", e)
        return HttpResponse.Failed()


@api_view(["DELETE"])
def deleteChannelPartner(request, id):
    try:
        cp = VendorDetails.objects.get(id=id, deleted=False)
    except VendorDetails.DoesNotExist:
        return HttpResponse.BadRequest(message="Channel Partner does not exist")

    try:
        cp.soft_delete()
        return HttpResponse.Ok(message="Channel Partner deleted successfully")
    except Exception as e:
        print("[ERROR] deleting channel partner: ", e)
        return HttpResponse.Failed(message="An error occurred while deleting the channel partner")
