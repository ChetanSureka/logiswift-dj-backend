from django.db.models import Q
from crm.models import Consignment
import pandas as pd
import os, zipfile
from datetime import datetime, timedelta

def get_details(consignment: Consignment) -> dict:
    '''
        Sl no
        lr date
        distributor name
        address
        sub - location
        location
        weight
        qty
        status
        delivery date (empty)
        vaiance + tat (tat taken)
        tat status (pass / failed) => (hit/miss)
        location type (ODA / Normal)
        remarks
    '''
    
    if (consignment.mode).lower() == "forward":
        distributor = consignment.consigner_id
        tat = distributor.tat
    elif (consignment.mode).lower() == "reverse":
        distributor = consignment.consignee_id
        tat = distributor.tat + 1
    
    tat_taken = consignment.variance + tat if consignment.variance else None
    
    
    details = {
        "sl_no": 0,
        "lrDate": consignment.lrDate,
        "distributor": distributor.name,
        "address": distributor.address,
        # "sub_location": distributor.locationMappingId.sublocation,
        # "location": distributor.locationMappingId.location,
        "weight": consignment.weight,
        "quantity": consignment.quantity,
        "status": consignment.status,
        "deliveryDate": consignment.deliveryDate,
        "tat_taken": tat_taken,
        "tat_status": consignment.tatstatus,
        "remarks": consignment.remarks,
        # "location_type": distributor.location_type,
    }
    
    return details

def get_previous_month(date):
    previous_month = date.month - 1
    previous_year = date.year
    if previous_month == 0:
        previous_month = 12
        previous_year -= 1
    return datetime(previous_year, previous_month, 1)



def generate_mis_report(fromDate, toDate):
    '''
    Filter consignments for the given date ranges.
    and pass the filtered results to the above function.
    get the list of details and add them to the pandas data frame to create an excel report.
    
    conditions to filter consignments:
    - get all consignments
    - if there are consignments from the previous month create a seperate excel file don't include them in the current month mis
    - in seperate excel make sure that all the consignments from the previous month are included.
    - forward_consignments = Consignment.objects.filter(
            Q(lrDate__gte=fromDate, lrDate__lte=toDate),
            mode='forward'
        ).order_by('lrDate')

    - reverse_consignments = Consignment.objects.filter(
            Q(deliveryDate__gte=fromDate, deliveryDate__lte=toDate) |
            Q(deliveryDate__isnull=True, lrDate__lte=toDate),
            mode='reverse'
        ).order_by('lrDate')
        
    - consignments = forward_consignments | reverse_consignments
    '''
    # Filter forward consignments
    forward_consignments = Consignment.objects.filter(
        Q(lrDate__gte=fromDate, lrDate__lte=toDate),
        mode='forward'
    ).order_by('lrDate')

    # Filter reverse consignments
    reverse_consignments = Consignment.objects.filter(
        Q(deliveryDate__gte=fromDate, deliveryDate__lte=toDate) |
        Q(deliveryDate__isnull=True, lrDate__lte=toDate),
        mode='reverse'
    ).order_by('lrDate')

    # Combine consignments
    consignments = forward_consignments | reverse_consignments

    # Initialize data lists
    current_month_forward = []
    current_month_reverse = []
    previous_month_forward = []
    previous_month_reverse = []

    # Process each consignment
    for consignment in consignments:
        details = get_details(consignment)
        if consignment.lrDate.month == fromDate.strptime().month:
            if consignment.mode.lower() == "forward":
                current_month_forward.append(details)
            else:
                current_month_reverse.append(details)
        else:
            if consignment.mode.lower() == "forward":
                previous_month_forward.append(details)
            else:
                previous_month_reverse.append(details)
    
    # Create DataFrames
    current_month_forward_df = pd.DataFrame(current_month_forward)
    current_month_reverse_df = pd.DataFrame(current_month_reverse)
    previous_month_forward_df = pd.DataFrame(previous_month_forward)
    previous_month_reverse_df = pd.DataFrame(previous_month_reverse)
    
    # Create file names
    current_month_name = fromDate.strftime("%b_%Y")
    previous_month_date = get_previous_month(fromDate)
    previous_month_name = previous_month_date.strftime("%b_%Y")
    
    current_file = f'MIS_{current_month_name}.xlsx'
    previous_file = f'MIS_{previous_month_name}.xlsx'


    with pd.ExcelWriter(current_file) as writer:
        current_month_forward_df.to_excel(writer, sheet_name='Forward', index=False)
        current_month_reverse_df.to_excel(writer, sheet_name='Reverse', index=False)

    if not previous_month_forward_df.empty or not previous_month_reverse_df.empty:
        with pd.ExcelWriter(previous_file) as writer:
            previous_month_forward_df.to_excel(writer, sheet_name='Forward', index=False)
            previous_month_reverse_df.to_excel(writer, sheet_name='Reverse', index=False)
        
        # Create a zip file
        with zipfile.ZipFile('MIS_Report.zip', 'w') as zipf:
            zipf.write(current_file)
            zipf.write(previous_file)
        
        # Remove the individual files after zipping
        os.remove(current_file)
        os.remove(previous_file)
        return 'MIS_Report.zip'
      
    os.remove(current_file)
    return current_file
