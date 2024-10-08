from django.db.models import Sum, Q
from datetime import date, timedelta
from crm.models import Consignment

def get_count(filter_kwargs):
    return Consignment.objects.filter(**filter_kwargs).count()

def get_total_weight():
    return Consignment.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0

def get_current_month_total_weight(start_date, end_date):
    forward_weight = Consignment.objects.filter(
        Q(lrDate__gte=start_date, lrDate__lte=end_date),
        mode='forward'
    ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    
    reverse_weight = Consignment.objects.filter(
        Q(deliveryDate__gte=start_date, deliveryDate__lte=end_date) |
        Q(deliveryDate__isnull=True, lrDate__lte=end_date),
        mode='reverse'
    ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    
    return forward_weight + reverse_weight

def get_current_month_total_consignments(start_date, end_date):
    return Consignment.objects.filter(
        Q(lrDate__gte=start_date, lrDate__lte=end_date) 
        # | Q(deliveryDate__gte=start_date, deliveryDate__lte=end_date)
    ).count()
    

def get_current_month_counts(status, start_date, end_date):
    return get_count({
        'status': status,
        'lrDate__gte': start_date,
        'lrDate__lte': end_date
    })

def get_past_six_months_weight():
    current_date = date.today()
    weights = []
    
    for i in range(6):
        month_start = (current_date.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month = month_start + timedelta(days=32)
        month_end = next_month.replace(day=1) - timedelta(days=1)
        total_weight = get_current_month_total_weight(month_start, month_end)
        weights.append({
            "month": month_start.strftime("%B")[:3],
            "weight": total_weight
        })
    
    return weights[::-1]

def generate_month_stats(fromDate=None, toDate=None, stats={}):
    if fromDate is not None and toDate is not None:
        stats["month"] = [
            {
                "title": "total-weight",
                "value": get_current_month_total_weight(fromDate, toDate),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": False,
                "url": None
            },
            {
                "title": "in-transit",
                "value": get_current_month_counts('in-transit', fromDate, toDate),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=in-transit&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"status=in-transit&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "delivered",
                "value": get_current_month_counts('delivered', fromDate, toDate),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=delivered&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"status=delivered&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "out-for-delivery",
                "value": get_current_month_counts('out-for-delivery', fromDate, toDate),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&status=out-for-delivery&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"status=out-for-delivery&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "tat-passed",
                # "value": get_current_month_counts('tatstatus', fromDate, toDate),
                "value": get_count({
                    'tatstatus': 'passed',
                    'lrDate__gte': fromDate,
                    'lrDate__lte': toDate
                }),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&tatStatus=passed&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"tatStatus=passed&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "tat-failed",
                # "value": get_current_month_counts('tatstatus', fromDate, toDate),
                "value": get_count({
                    'tatstatus': 'failed',
                    'lrDate__gte': fromDate,
                    'lrDate__lte': toDate
                }),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&tatStatus=failed&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"tatStatus=failed&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "lr-delayed",
                "value": get_current_month_counts('delayed', fromDate, toDate),
                # "value": get_count({
                #     'delayed': True,
                #     'lrDate__gte': fromDate,
                #     'lrDate__lte': toDate
                # }),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": True,
                "url": f"consignments?limit=15&offset=0&delayed=true&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}",
                "query_param": f"delayed=true&fromDate={fromDate.strftime('%Y-%m-%d')}&toDate={toDate.strftime('%Y-%m-%d')}"
            },
            {
                "title": "total-consignments",
                "value": get_current_month_total_consignments(fromDate, toDate),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": False,
                "url": None
            },
            {
                "title": "forward",
                "value": get_count({'mode': 'forward', 'lrDate__gte': fromDate, 'lrDate__lte': toDate}),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": False,
                "url": None                
            },
            {
                "title": "reverse",
                "value": get_count({'mode': 'reverse', 'lrDate__gte': fromDate, 'lrDate__lte': toDate}),
                "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
                "isclickable": False,
                "url": None                
            },
        ]
        
        return stats
    
    

def generate_dashboard(from_date=None, to_date=None):
    if from_date and to_date:
        start_date = date.fromisoformat(from_date)
        end_date = date.fromisoformat(to_date)
    else:
        current_date = date.today()
        start_date = current_date.replace(day=1)
        next_month = start_date + timedelta(days=32)
        end_date = next_month.replace(day=1)
    
    stats = {
        "overall": [
            {
                "title": "total-weight",
                "value": get_total_weight(),
                "time": "all time",
                "isclickable": False,
                "url": None
            },
            {
                "title": "in-transit",
                "value": get_count({'status': 'in-transit'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=in-transit",
                "query_param": "status=in-transit"
            },
            {
                "title": "delivered",
                "value": get_count({'status': 'delivered'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=delivered",
                "query_param": "status=delivered"
            },
            {
                "title": "out-for-delivery",
                "value": get_count({'status': 'out-for-delivery'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&status=out-for-delivery",
                "query_param": "status=out-for-delivery"
            },
            {
                "title": "tat-passed",
                "value": get_count({'tatstatus': 'passed'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&tatStatus=passed",
                "query_param": "tatStatus=passed"
            },
            {
                "title": "tat-failed",
                "value": get_count({'tatstatus': 'failed'}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&tatStatus=failed",
                "query_param": "tatStatus=failed"
            },
            {
                "title": "lr-delayed",
                "value": get_count({'delayed': True}),
                "time": "all time",
                "isclickable": True,
                "url": "consignments?limit=15&offset=0&delayed=true",
                "query_param": "delayed=true"
            },
            {
                "title": "total-consignments",
                "value": get_count({}),
                "time": "all time",
                "isclickable": False,
                "url": None
            },
            {
                "title": "forward",
                "value": get_count({'mode': 'forward'}),
                "time": "all time",
                "isclickable": False,
                "url": None                
            },
            {
                "title": "reverse",
                "value": get_count({'mode': 'reverse'}),
                "time": "all time",
                "isclickable": False,
                "url": None                
            },
        ],
        "graph": {
            "weight": get_past_six_months_weight()
        }
    }
    
    stats = generate_month_stats(start_date, end_date, stats)

    return stats
