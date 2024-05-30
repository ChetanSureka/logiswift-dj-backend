import pandas as pd
from .models import *
import datetime, pytz, os, json
import qrcode
from django.conf import settings
from PIL import Image
from django.db.models import Q
from fpdf import FPDF

path_to_excel = settings.BASE_DIR

def getDataFrame(consignments):
    '''
        Create a dataframe from the consignments
    '''
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    df = pd.DataFrame(
        columns=[
            'SL No.',
            'LR No.',
            'LR Date',
            'Party Name',
            'Address',
            'Sub-location',
            'Location',
            'QTY',
            'Weight',
            'Status',
            'Delivery Date',
            'Remarks'
        ]
    )
    count = 0
    consignments = consignments.order_by('lr')
    for consignment in consignments:
        '''
        Get consignments from this month only and carry forward the consignments from last month which are not delivered
        '''
        # condition = consignment.createdDate.month != current_time.month or consignment.status == 'Delivered'
        # if not condition:
        #     continue
        count += 1
        try:
            sublocation = consignment.consigner_id.locationMappingId.sublocation
            # delivery_date = consignment.deliveryDate.strftime("%d-%b-%Y")
        except:
            sublocation = ''
            # delivery_date = ''
        location = consignment.consigner_id.locationMappingId.location if consignment.consigner_id.locationMappingId else ''
        df = df.append({
            'SL No.': count,
            'LR No.': consignment.lr,
            'LR Date': consignment.createdDate.strftime("%d-%b-%Y"),
            'Party Name': consignment.consigner_id.name,
            'Address': consignment.consigner_id.address,
            'Sub-location': sublocation,
            'Location': location,
            'QTY': consignment.quantity,
            'Weight': consignment.weight,
            'Status': consignment.status,
            'Delivery Date': consignment.deliveryDate.strftime("%d-%b-%Y") if consignment.deliveryDate else '',
            'Remarks': ""
            # 'Remarks': consignment.status
        }, ignore_index=True)
    return df


def GenerateMISReport():
    '''
    Generate MIS Report
    '''
    current_month = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).month
    previous_month = current_month - 1 if current_month != 1 else 12

    current_consignments = Consignment.objects.filter(
    
        # previous month consignments which are not delivered
        (Q(createdDate__month=previous_month) & ~Q(status="Delivered")) |
    
        # current month consignments
        (Q(createdDate__month=current_month))
    ).order_by('id')
    print(current_consignments)
    forward_consignments = current_consignments.filter(mode="Forward")
    reverse_consignments = current_consignments.filter(mode="Reverse")
    # forward_consignments = Consignment.objects.filter(mode="Forward")
    # reverse_consignments = Consignment.objects.filter(mode="Reverse")
    forward_df = getDataFrame(forward_consignments)
    reverse_df = getDataFrame(reverse_consignments)
    date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%b-%Y")
    # with pd.ExcelWriter(path_to_excel + f'MIS_{date}.xlsx') as writer:
    #     forward_df.to_excel(writer, sheet_name="Forward", index=False)
    #     reverse_df.to_excel(writer, sheet_name="Reverse", index=False)
    file_path = os.path.join(path_to_excel, f'MIS_{date}.csv')
    forward_df.to_csv(file_path, index=False)
    return f'MIS_{date}.csv'


def GenerateBills(consignments):
    '''
    Generate Bills
    Consignments are passed as a list of objects, bills are generated for each consignment
    '''
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    for consignment in consignments:
        bill_obj = Billing.objects.create(
            lr_no=consignment,
            bill_date=current_time,
            bill_no = consignment.lr,
        )
        bill_obj.save()

        consignment.billGenerated = True
        consignment.save()
    

def generateBillingdf(bills):
    billing_df = pd.DataFrame(
        columns=[
            'Chargable Weight',
            'Rate',
            'Amount',
            'ODA Charge',
            'Miscellaneous Charge',
            'Total',
        ]
    )

    # get related Consignment transactions from the bills
    cts = ConsignmentTransaction.objects.filter(bill_id__in=bills)

    for ct in cts:
        billing_df = billing_df.append({
            'Chargable Weight': ct.cp_chargable_weight,
            'Rate': ct.cp_rate,
            'ODA Charge': ct.cp_oda_charge,
            'Amount': ct.cp_amount,
            'Miscellaneous Charge': ct.cp_miscellaneous,
            'Total': ct.cp_total,
        }, ignore_index=True)
    
    print("\n\n\nBilling DF inside function: \n", billing_df)
    billing_df = billing_df.append({
        'Chargable Weight': sum(billing_df['Chargable Weight']),
        'Total': sum(billing_df['Total']),
    }, ignore_index=True)
    return billing_df



def GenerateBillingReport():
    # Filter by month
    current_month = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).month
    previous_month = current_month - 1 if current_month != 1 else 12
    
    # consignments = Consignment.objects.all()
    consignments = Consignment.objects.filter(createdDate__month=previous_month).order_by('id')
    # GenerateBills(consignments)
    billing_obj = Billing.objects.all()
    consignment_df = getDataFrame(consignments)
    billing_df = generateBillingdf(billing_obj)
    report_df = pd.concat([consignment_df, billing_df], axis=1).drop(['Remarks', 'Address'], axis=1)
    grouped_df = report_df.groupby(['Location'])
    new_df = pd.DataFrame()
    for i in grouped_df:
        new_df = new_df.append(i[1], ignore_index=True)
    print("\n\n\n\nreport_df: \n\n", new_df.head())

    date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%b-%Y")
    file_path = os.path.join(path_to_excel, f'Bill_{date}.csv')
    new_df.to_csv(file_path, index=False)
    return f'Bill_{date}.csv'



def GenrateQR(consignments):
    '''
    Generate QR Code
    '''
    imagelist = []
    for consignment in consignments:
        url = settings.SITE_URL + f'admin/crm/consignment/{consignment.id}/change/'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = settings.BASE_DIR / f'qrcodes/{consignment.id}.png'
        imagelist.append(img_path)
        img.save(img_path)

    pdf = FPDF()
    count = 0
    pdf.add_page()
    for image in imagelist:
        count += 1
        if count > 2:
            pdf.add_page()
            count = 0
        pdf.image(str(image), type='PNG', w=120, h=120)
    pdf_path = settings.BASE_DIR / 'qrcodes/qr_codes.pdf'
    pdf.output(pdf_path, "F")
    for image in imagelist:
        image.unlink()
    return pdf_path
