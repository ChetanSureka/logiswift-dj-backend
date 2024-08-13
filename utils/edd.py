from datetime import datetime, timedelta
from crm.models import PublicHolidays

class DeliveryDateCalculator:
    def __init__(self, lr_date, tat):
        self.lr_date = datetime.strptime(lr_date, "%Y-%m-%d").date()
        self.tat = tat
        self.public_holidays = set(PublicHolidays.objects.values_list('date', flat=True))
        self.temp_edd = self.lr_date + timedelta(days=tat+1)  # add 1 to not include the lr_date
    
    def adjust_for_sunday(self, date):
        if date.weekday() == 6:  # 6 = Sunday
            date += timedelta(days=1)
        return date
    
    def adjust_for_holidays(self, start_date, end_date):
        current_date = start_date
        additional_days = 0
        
        while current_date < end_date:
            if current_date in self.public_holidays or current_date.weekday() == 6:
                additional_days += 1
            current_date += timedelta(days=1)
        
        end_date += timedelta(days=additional_days)
        end_date = self.adjust_for_sunday(end_date)
        
        return end_date

    def calculate_expected_delivery(self):
        # Initial adjustment for Sundays and public holidays
        self.temp_edd = self.adjust_for_sunday(self.temp_edd)
        self.temp_edd = self.adjust_for_holidays(self.lr_date, self.temp_edd)

        return self.temp_edd.strftime("%Y-%m-%d")

def calculate_expected_delivery(lrDate, tat):
    calculator = DeliveryDateCalculator(lrDate, tat)
    return calculator.calculate_expected_delivery()
