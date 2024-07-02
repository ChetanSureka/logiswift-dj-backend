# Calculates Expected Delivery Date for a given consignment/lr date
from datetime import datetime, timedelta
from crm.models import PublicHolidays
from django.db.models import Q

def calculate_expected_delivery(lr_date, tat):
    
    lr_date = datetime.strptime(lr_date, '%Y-%m-%d')

    delivery_date = lr_date + timedelta(days=tat)

    # public_holidays = get_public_holidays_between(lr_date.strftime("%Y-%m-%d"), delivery_date.strftime("%Y-%m-%d"))
    public_holidays = PublicHolidays.objects.filter(
        Q(date=lr_date.strftime("%Y-%m-%d")),
        Q(date=delivery_date.strftime("%Y-%m-%d"))
    )

    days_count = 0

    # Adjust delivery date for public holidays
    if public_holidays is not None:
        for holiday in public_holidays:
            # delivery_date += timedelta(days=1)
            days_count += 1

    # Adjust delivery date for Sundays
    current_date = lr_date
    if delivery_date.weekday() == 6:
        print("Delivery date is sunday")
        delivery_date += timedelta(days=1)
    
    while current_date < delivery_date:
        if current_date.weekday() == 6:
            print("Week day added", current_date)
            # delivery_date += timedelta(days=1)
            days_count += 1
            break
        # increment to exclude lr date
        current_date += timedelta(days=1)

    
    print("Days Count: ", days_count)
    delivery_date += timedelta(days=days_count)
    return delivery_date.strftime('%Y-%m-%d')