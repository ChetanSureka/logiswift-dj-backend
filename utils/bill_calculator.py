'''
this calculates the bill for each consignment
and returns the billings object created in the table

custom round off
def custom_round(x):
    decimal_part = x - int(x)
    if decimal_part > 0.4:
        return math.floor(x)
    else:
        return math.ceil(x)


Calculations
------------

Chargable weight = custom_round(weight)
Amount = (chargable weight * rate) + oda charges
total amount = Amount + additional charges


Fields to get from other models
-------------------------------

weight -> Consignment
rate -> distributors (consigneeconsigner)
odaCharge -> distributors (consigneeconsigner)
additionalCharges -> Consignment

consigneeId -> distributors (consigneeconsigner)
consigneeName -> distributors (consigneeconsigner)

consignerId -> distributors (consigneeconsigner)
consignerName -> distributors (consigneeconsigner)

locationId -> distributors (consigneeconsigner)
locationName -> location


function params
---------------
lr -> ConsignmentObject

return params
-------------
bill_id -> BillingObject.id

'''


import math
from crm.models import Billings, Consignment

def custom_round(x):
    '''
    floor if decimal part < .5 else ceil
    eg:
        5.3 -> 5
        5.5 -> 6
    '''
    decimal_part = x - int(x)
    if decimal_part < 0.5:
        return math.floor(x)
    else:
        return math.ceil(x)

def calculate_bill(consignment: Consignment):
    weight = consignment.weight
    if consignment.additionalCharges == 1 or consignment.additionalCharges is None:
        additionalCharges = 0
    else:
        additionalCharges = consignment.additionalCharges

    consignee = consignment.consignee_id
    consigner = consignment.consigner_id
    cp = consignment.vendor_id
    
    if consignment.mode == 'forward':
        rate = 0 if consignment.consigner_id.rate is None else consignment.consigner_id.rate
        odaCharge = 0 if consignment.consigner_id.odaCharge is None else consignment.consigner_id.odaCharge
    else:  # reverse
        rate = 0 if consignment.consignee_id.rate is None else consignment.consignee_id.rate
        odaCharge = 0 if consignment.consignee_id.odaCharge is None else consignment.consignee_id.odaCharge

    
    rounded_weight = custom_round(weight)
    if rounded_weight <= 15:
        chargable_weight = 15
    elif rounded_weight > 15:
        chargable_weight = rounded_weight
        
    
    amount = (chargable_weight * rate)
    if additionalCharges is None:
        additionalCharges = 0
    total_amount = amount + additionalCharges + odaCharge
    
    # cp info for bill
    cp_rate = 0 if cp.rate is None else cp.rate
    cp_odaCharge = 0 if cp.odaCharge is None else cp.odaCharge
    cp_amount = (chargable_weight * cp_rate)
    cp_total_amount = cp_amount + additionalCharges + cp_odaCharge
    
    
    bill_obj, created = Billings.objects.update_or_create(
        consignment=consignment,
        defaults={
            "tatstatus": consignment.tatstatus,
            "variance": consignment.variance,
            
            "consigneeId": consignee.id,
            "consigneeName": consignee.name,
            
            "consignerId": consigner.id,
            "consignerName": consigner.name,
            
            "chargeableWeight": chargable_weight,
            "amount": amount,
            "rate": rate,
            "odaCharge": odaCharge,
            "additionalCharge": additionalCharges,
            "totalAmount": total_amount,
            
            "quantity": consignment.quantity,
            
            "cp_chargeableWeight": chargable_weight,
            "cp_amount": cp_amount,
            "cp_rate": cp_rate,
            "cp_odaCharge": cp_odaCharge,
            "cp_additionalCharge": additionalCharges,
            "cp_totalAmount": cp_total_amount,
            
            "created_by": 'system',
            "updated_by": 'system'
        }
    )
    
    return bill_obj