from django.utils import timezone
from django.db.models import Sum
from datetime import date
from crm.models import Consignment

class ConsignmentDashboard:
    def __init__(self):
        self.current_month, self.current_year = self.get_current_month_year()
        self.current_date = date.today()

    def get_current_month_year(self):
        now = timezone.now()
        return now.month, now.year

    def get_count(self, filter_kwargs):
        return Consignment.objects.filter(**filter_kwargs).count()

    def total_intransit_lrs(self):
        return self.get_count({'status': 'in-transit'})

    def current_month_delivered_lrs(self):
        current_date = timezone.now()
        current_month_start = current_date.replace(day=1)
        return self.get_count({
            'status': 'delivered',
            'deliveryDate__gte': current_month_start,
            'deliveryDate__lt': current_date.replace(month=current_date.month + 1, day=1)
        })

    def current_month_total_weight(self):
        current_date = timezone.now()
        current_month_start = current_date.replace(day=1)
        return Consignment.objects.filter(
            lrDate__gte=current_month_start,
            lrDate__lt=current_date.replace(month=current_date.month + 1, day=1)
        ).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    
    def total_weight(self):
        return Consignment.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0

    def lr_ofd(self):
        return self.get_count({'status': 'out-for-delivery'})

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

    def generate_dashboard(self):
        stats = {
            "overall_stats": {
                "total_weight_i_all_time": self.total_weight(),
                "tat_passed_i_all_time": self.tat_status_all_time("passed"),
                "tat_failed_i_all_time": self.tat_status_all_time("failed"),
                # "tat_going_to_fail_i_all_time": self.tat_going_to_fail_all_time(),
                "lr_delayed_i_all_time": self.lr_status_all_time(True),
                "in_transit_i_all_time": self.total_intransit_lrs(),
                "delivered_i_all_time": self.get_count({'status': 'delivered'}),
                "out_for_delivery_i_all_time": self.lr_ofd(),
            },
            
            "current_month": {
                "tat_passed_i_current_month": self.tat_status_current_month("passed"),
                "tat_failed_i_current_month": self.tat_status_current_month("failed"),
                "tat_going_to_fail": self.tat_going_to_fail_current_month(),
                "total_weight_i_current_month": self.current_month_total_weight(),
                "lr_delayed_i_current_month": self.lr_status_current_month(True),
                "in_transit_i_current_month": self.get_count({'status': 'in-transit', 'lrDate__year': self.current_year, 'lrDate__month': self.current_month}),
                "delivered_i_current_month": self.current_month_delivered_lrs(),
                "out_for_delivery_i_current_month": self.get_count({'status': 'out-for-delivery', 'lrDate__year': self.current_year, 'lrDate__month': self.current_month}),
            },
        }
        return stats

def generate_dashboard():
    dashboard = ConsignmentDashboard()
    result = dashboard.generate_dashboard()
    return result
