from datetime import datetime, timedelta
from crm.models import PublicHolidays

class DeliveryDateCalculator:
    def __init__(self, lr_date, tat):
        self.lr_date = datetime.strptime(lr_date, "%Y-%m-%d").date()
        self.tat = tat
        self.temp_edd = self.lr_date + timedelta(days=tat+1) # add 1 to not include the lrDate
        self.public_holidays = set(PublicHolidays.objects.values_list('date', flat=True))
    
    def adjust_for_sunday(self, date):
        if date.weekday() == 6:  # 6 = Sunday
            date += timedelta(days=1)
        return date
    
    def adjust_for_holidays(self, start_date, end_date):
        while any(holiday in self.public_holidays for holiday in self.date_range(start_date, end_date)):
            end_date += timedelta(days=1)
            end_date = self.adjust_for_sunday(end_date)
        return end_date

    def date_range(self, start, end):
        delta = end - start
        return [start + timedelta(days=i) for i in range(delta.days + 1)]

    def calculate_expected_delivery(self):
        # Initial adjustment for Sundays and public holidays
        self.temp_edd = self.adjust_for_sunday(self.temp_edd)
        self.temp_edd = self.adjust_for_holidays(self.lr_date, self.temp_edd)
        
        # Final check if the adjusted temp_edd is a Sunday or a holiday
        while self.temp_edd in self.public_holidays or self.temp_edd.weekday() == 6:
            self.temp_edd += timedelta(days=1)
            self.temp_edd = self.adjust_for_sunday(self.temp_edd)

        return self.temp_edd.strftime("%Y-%m-%d")

def calculate_expected_delivery(lrDate, tat):
    calculator = DeliveryDateCalculator(lrDate, tat)
    return calculator.calculate_expected_delivery()