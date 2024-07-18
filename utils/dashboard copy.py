from crm.models import Consignment, ConsignemntStatusChoices
from django.db.models import Sum
from django.utils import timezone
from datetime import date



def total_intransit_lrs():
    consignment_count = Consignment.objects.filter(status="in-transit").count()
    print("Total intransit: ", consignment_count)
    return consignment_count


# def pending_lrs():
#     pending_count = Consignment.objects.exclude(status__in=["delivered", "in-transit"]).count()
#     pending_count -= pending_count
#     print("Pending Lrs: ", pending_count)
#     return pending_count


def current_month_delivered_lrs():
    '''
    Filter consignments by current month, delivered return count
    '''
    current_date = timezone.now()
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
    current_date = timezone.now()
    current_month_start = current_date.replace(day=1)
    total_weight = Consignment.objects.filter(
        lrDate__gte=current_month_start,
        lrDate__lt=current_date.replace(month=current_date.month + 1, day=1)
    ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    print("Current month total weight: ", total_weight)
    return total_weight


def lr_ofd():
    '''
    Filter consignments for lrs ofd status and return count
    '''
    consignment_count = Consignment.objects.filter(status="out-for-delivery").count()
    print("OFD Count: ", consignment_count)
    return consignment_count


# def tat_status():
#     '''
#     Filter consignments for tat status and return count
#     '''
#     passed_count = Consignment.objects.filter(tatstatus="passed").count()
#     failed_count = Consignment.objects.filter(tatstatus="failed").count()
#     current_month_passed_count = Consignment.objects.filter(tatstatus="passed", lrDate=
    
#     print("passed:", passed_count, "failed:", failed_count)
#     return [passed_count, current_month_passed_count, failed_count]


from django.utils import timezone
from django.db.models import Q
from datetime import date

class ConsignmentFilter:
    def __init__(self):
        self.current_month, self.current_year = self.get_current_month_year()
        self.current_date = date.today()

    def get_current_month_year(self):
        now = timezone.now()
        return now.month, now.year

    def get_count(self, filter_kwargs):
        return Consignment.objects.filter(**filter_kwargs).count()

    def tat_status_all_time(self, status):
        return self.get_count({'tatstatus': status})

    def tat_status_current_month(self, status):
        return self.get_count({'tatstatus': status, 'lrDate__year': self.current_year, 'lrDate__month': self.current_month})

    def tat_going_to_fail_all_time(self):
        return self.get_count({'expectedDeliveryDate': self.current_date})

    def tat_going_to_fail_current_month(self):
        return self.get_count({'expectedDeliveryDate': self.current_date, 'lrDate__year': self.current_year, 'lrDate__month': self.current_month})

    def lr_status_all_time(self, delayed):
        return self.get_count({'delayed': delayed})

    def lr_status_current_month(self, delayed):
        return self.get_count({'delayed': delayed, 'lrDate__year': self.current_year, 'lrDate__month': self.current_month})

class ConsignmentStats:
    def __init__(self):
        self.filter = ConsignmentFilter()

    def get_stats(self):
        stats = {
            "tat_passed_i_all_time": self.filter.tat_status_all_time("passed"),
            # "tat_passed_i_current_month": self.filter.tat_status_current_month("passed"),
            
            "tat_failed_i_all_time": self.filter.tat_status_all_time("failed"),
            # "tat_failed_i_current_month": self.filter.tat_status_current_month("failed"),
            
            "tat_going_to_fail": self.filter.tat_going_to_fail_all_time(),
            
            "lr_delayed_i_all_time": self.filter.lr_status_all_time(True),
            # "lr_delayed_i_current_month": self.filter.lr_status_current_month(True),
        }
        
        return stats


def generate_dashboard():
    
    stats = ConsignmentStats()
    tat = stats.get_stats()
    
    dashboard_data = {
        "in_transit_i_all_time": total_intransit_lrs(),
        # "pending_i_all_time": pending_lrs(),
        "delivered_i_current_month": current_month_delivered_lrs(),
        "out_for Delivery_i_all_time": lr_ofd(),
        "total_weight_i_current_month": current_month_total_weight(),
    }
    
    dashboard_data.update(tat)
    
    return dashboard_data