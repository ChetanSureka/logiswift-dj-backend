# logiswift-dj-backend
Django backend 


#### helpers/dashboard.py

```python
from django.db.models import Sum, Q
from datetime import date, timedelta
from crm.models import Consignment
from .fr_consignments import fr_consginment

class FilterConsignmets():
    def __init__(self):
        self.consignmets = Consignment.objects.all()
        self.current_date = date.today()
        self.from_date = date(2000, 1, 1)
        self.total_weight = self.consignmets.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
    
    def rangeFilter(self, query, fromDate=None, toDate=None):
        '''
        filters consignments based on the date range and a query dictionary
        return filtered results list
        '''
        
        if fromDate is None or toDate is None:
            fromDate = self.from_date
            toDate = self.current_date
            
        fc = self.consignmets.filter({
            "lrDate__gte": fromDate,
            "lrDate__lte": toDate,
            **query
        })
        return fc
    
    def format_url(self, model="consignments", limit=15, offset=0, **query_params):
        """
        Constructs the URL for API requests with filters and pagination.
        """
        base_url = f"{model}?limit={limit}&offset={offset}"
        query_str = "&".join([f"{key}={value}" for key, value in query_params.items()])
        return f"{base_url}&{query_str}"

    
    def setStatsDict(self, title, query: dict, fromDate=None, toDate=None, isClickable=False, url=None, query_param=None):
        # returns a dictionary of stats

        result = self.rangeFilter(fromDate=fromDate, toDate=toDate, query=query)
        
        self.stat = {
            "title": title,
            "value": result.count(),
            "time": f"{fromDate.strftime('%b %Y')} - {toDate.strftime('%b %Y')}",
            "isclickable": isClickable,
            "url": self.format_url(query_param=query_param),
            "query_param": query_param
        }
        
        if fromDate or toDate is None:
            self.stat["time"] = "all time"
        
        return self.stat
    
    def month_total_weight(self, start_date, end_date):
        fc, rc = fr_consginment(start_date, end_date)
    
        fw = fc.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        rw = rc.aggregate(total_weight=Sum('weight'))['total_weight'] or 0

        return fw + rw
```