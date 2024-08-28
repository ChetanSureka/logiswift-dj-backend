from django.db.models import Q
from crm.models import Consignment
import pandas as pd
import os, zipfile
from datetime import datetime, timedelta


def get_details(consignment: Consignment, sl: int) -> dict:
    """
    Returns a dictionary with consignment details for the MIS report.
    """
    if consignment.mode.lower() == "forward":
        distributor = consignment.consigner_id
        tat = distributor.tat
    else:  # mode == "reverse"
        distributor = consignment.consignee_id
        tat = distributor.tat + 1

    # Ensure tat and variance are not None before calculating tat_taken
    tat_taken = None
    if tat is not None and consignment.variance is not None:
        tat_taken = tat - consignment.variance

    return {
        "sl_no": sl,
        "lrDate": consignment.lrDate,
        "distributor": distributor.name,
        "address": distributor.address,
        "weight": consignment.weight,
        "quantity": consignment.quantity,
        "status": consignment.status,
        "deliveryDate": consignment.deliveryDate,
        "tat_taken": tat_taken,
        "tat_status": consignment.tatstatus,
        "remarks": consignment.remarks,
    }


def get_previous_month_date(current_date: datetime) -> datetime:
    """
    Returns the first date of the previous month given a current date.
    """
    previous_month = current_date.month - 1
    previous_year = current_date.year
    if previous_month == 0:
        previous_month = 12
        previous_year -= 1
    return datetime(previous_year, previous_month, 1)


def filter_consignments(date_from: datetime, date_to: datetime, mode: str) -> list:
    """
    Filters consignments based on date range and mode.
    """
    return Consignment.objects.filter(
        Q(lrDate__gte=date_from, lrDate__lte=date_to),
        mode=mode
    ).order_by('lrDate')


def filter_undelivered_consignments(consignments):
    """
    Filters out consignments with a status other than 'delivered'.
    """
    return consignments.exclude(status='delivered')


def generate_excel(dataframes: dict, filename: str):
    """
    Generates an Excel file from given dataframes and saves it with the provided filename.
    """
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for sheet_name, df in dataframes.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get the xlsxwriter worksheet object
                worksheet = writer.sheets[sheet_name]
                
                # Auto-fit column widths
                for i, col in enumerate(df.columns):
                    column_len = df[col].astype(str).str.len().max()
                    # Considering the column header length as well
                    header_len = len(col)
                    # Set the column width
                    worksheet.set_column(i, i, max(column_len, header_len) + 2)


def generate_mis_report(current_date: datetime):
    """
    Generates MIS report based on the current and previous month consignments.
    """
    # Define date ranges
    first_day_current_month = current_date.replace(day=1)
    first_day_previous_month = get_previous_month_date(current_date)
    last_day_previous_month = first_day_current_month - timedelta(days=1)

    # Filter current month's consignments
    current_forward = filter_consignments(first_day_current_month, current_date, 'forward')
    current_reverse = filter_consignments(first_day_current_month, current_date, 'reverse')

    # Prepare data for current month
    current_month_forward_data = [get_details(consignment, sl) for sl, consignment in enumerate(current_forward, start=1)]
    current_month_reverse_data = [get_details(consignment, sl) for sl, consignment in enumerate(current_reverse, start=1)]

    current_month_dfs = {
        'Forward': pd.DataFrame(current_month_forward_data),
        'Reverse': pd.DataFrame(current_month_reverse_data),
    }

    # Generate current month's Excel report
    current_month_filename = f'MIS_{current_date.strftime("%b_%Y")}.xlsx'
    generate_excel(current_month_dfs, current_month_filename)

    # Check for undelivered consignments in the previous month
    previous_forward = filter_consignments(first_day_previous_month, last_day_previous_month, 'forward')
    previous_reverse = filter_consignments(first_day_previous_month, last_day_previous_month, 'reverse')

    undelivered_previous_forward = filter_undelivered_consignments(previous_forward)
    undelivered_previous_reverse = filter_undelivered_consignments(previous_reverse)

    if undelivered_previous_forward.exists() or undelivered_previous_reverse.exists():
        previous_month_forward_data = [get_details(consignment) for consignment in previous_forward]
        previous_month_reverse_data = [get_details(consignment) for consignment in previous_reverse]

        previous_month_dfs = {
            'Forward': pd.DataFrame(previous_month_forward_data),
            'Reverse': pd.DataFrame(previous_month_reverse_data),
        }

        previous_month_filename = f'MIS_{first_day_previous_month.strftime("%b_%Y")}.xlsx'
        generate_excel(previous_month_dfs, previous_month_filename)

        # Zip files together
        zip_filename = 'MIS_Report.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(current_month_filename)
            zipf.write(previous_month_filename)

        # Clean up individual files
        os.remove(current_month_filename)
        os.remove(previous_month_filename)

        return zip_filename

    return current_month_filename
