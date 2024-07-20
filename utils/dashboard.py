from django.db.models import Sum, Q
from datetime import date, timedelta
from crm.models import Consignment

def get_count(filter_kwargs):
    return Consignment.objects.filter(**filter_kwargs).count()

def get_total_weight():
    return Consignment.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0

def get_current_month_total_weight(start_date, end_date):
    return Consignment.objects.filter(
        Q(lrDate__gte=start_date, lrDate__lte=end_date) |
        Q(deliveryDate__gte=start_date, deliveryDate__lte=end_date)
    ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0

def get_current_month_total_consignments(start_date, end_date):
    return Consignment.objects.filter(
        Q(lrDate__gte=start_date, lrDate__lte=end_date) |
        Q(deliveryDate__gte=start_date, deliveryDate__lte=end_date)
    ).count()
    

def get_current_month_counts(status, start_date, end_date):
    return get_count({
        'status': status,
        'lrDate__gte': start_date,
        'lrDate__lte': end_date
    })

def generate_dashboard():
    current_date = date.today()
    start_date = current_date.replace(day=1)
    next_month = start_date + timedelta(days=32)
    end_date = next_month.replace(day=1)

    stats = {
        "overall_stats": [
            {
                "title": "Total Weight",
                "value": get_total_weight(),
                "time": "all time",
                "isclickable": False,
                "url": None
            },
            {
                "title": "Total Consignments",
                "value": get_count({}),
                "time": "all time",
                "isclickable": False,
                "url": None
            },
            {
                "title": "In Transit",
                "value": get_count({'status': 'in-transit'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=in-transit",
                "query_param": "status=in-transit"
            },
            {
                "title": "Delivered",
                "value": get_count({'status': 'delivered'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=delivered",
                "query_param": "status=delivered"
            },
            {
                "title": "Out for Delivery",
                "value": get_count({'status': 'out-for-delivery'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=out-for-delivery",
                "query_param": "status=out-for-delivery"
            },
            {
                "title": "TAT Passed",
                "value": get_count({'tatstatus': 'passed'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&tatStatus=passed",
                "query_param": "tatStatus=passed"
            },
            {
                "title": "TAT Failed",
                "value": get_count({'tatstatus': 'failed'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&tatStatus=failed",
                "query_param": "tatStatus=failed"
            },
            {
                "title": "LR Delayed",
                "value": get_count({'delayed': True}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&delayed=true",
                "query_param": "delayed=true"
            }
        ],
        
        "current_month": [
            {
                "title": "Total Weight",
                "value": get_current_month_total_weight(start_date, end_date),
                "time": "current month",
                "isclickable": False,
                "url": None
            },
            {
                "title": "Total Consignments",
                "value": get_current_month_total_consignments(start_date, end_date),
                "time": "current month",
                "isclickable": False,
                "url": None                
            },
            {
                "title": "In Transit",
                "value": get_current_month_counts('in-transit', start_date, end_date),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=in-transit&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"status=in-transit&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            },
            {
                "title": "Delivered",
                "value": get_current_month_counts('delivered', start_date, end_date),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=delivered&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"status=delivered&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            },
            {
                "title": "Out for Delivery",
                "value": get_current_month_counts('out-for-delivery', start_date, end_date),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=out-for-delivery&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"status=out-for-delivery&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            },
            {
                "title": "TAT Passed",
                "value": get_count({'tatstatus': 'passed', 'lrDate__gte': start_date, 'lrDate__lte': end_date}),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&tatStatus=passed&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"tatStatus=passed&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            },
            {
                "title": "TAT Failed",
                "value": get_count({'tatstatus': 'failed', 'lrDate__gte': start_date, 'lrDate__lte': end_date}),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&tatStatus=failed&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"tatStatus=failed&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            },
            # {
            #     "title": "TAT Going to Fail",
            #     "value": get_count({'expectedDeliveryDate': current_date, 'lrDate__gte': start_date, 'lrDate__lt': end_date}),
            #     "time": "current month",
            #     "isclickable": False,
            #     "url": None
            # },
            {
                "title": "LR Delayed",
                "value": get_count({'delayed': True, 'lrDate__gte': start_date, 'lrDate__lt': end_date}),
                "time": "current month",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&delayed=true&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}",
                "query_param": f"delayed=true&fromDate={start_date.strftime('%Y-%m-%d')}&toDate={end_date.strftime('%Y-%m-%d')}"
            }
        ]
    }
    
    return stats
