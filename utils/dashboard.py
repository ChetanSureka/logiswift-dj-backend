from crm.models import Consignment, ConsignemntStatusChoices
from django.utils.timezone import now
from django.db.models import Sum


def total_intransit_lrs():
    consignment_count = Consignment.objects.filter(status="in-transit").count()
    print("Total intransit: ", consignment_count)
    return consignment_count


def pending_lrs():
    # [TODO]
    # need pending lrs only
    # pending lrs are not delivered
    pending_count = Consignment.objects.filter(status="delivered").count()
    pending_count -= pending_count
    print("Pending Lrs: ", pending_count)
    return pending_count


def current_month_delivered_lrs():
    '''
    Filter consignments by current month, delivered return count
    '''
    current_date = now()
    current_month_start = current_date.replace(day=1)
    delivered_count = Consignment.objects.filter(
        status="delivered",
        deliveryDate__gte=current_month_start,
        deliveryDate__lt=current_date.replace(month=current_date.month + 1, day=1)
    ).count()
    print("Current month delivered LRs: ", delivered_count)
    return delivered_count
    
    
    
def current_month_total_weight():
    '''
    Filter consignments by current month, sum weights and return total weight
    '''
    current_date = now()
    current_month_start = current_date.replace(day=1)
    total_weight = Consignment.objects.filter(
        lrDate__gte=current_month_start,
        lrDate__lt=current_date.replace(month=current_date.month + 1, day=1)
    ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    print("Current month total weight: ", total_weight)
    return total_weight


def generate_dashboard():
    dashboard_data = {
        "in_transit_i_total": total_intransit_lrs(),
        "pending": pending_lrs(),
        "delivered_i_current_month": current_month_delivered_lrs(),
        "total_weight_i_current_month": current_month_total_weight(),
    }
    
    return dashboard_data