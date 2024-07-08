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
from crm.models import Billings

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

def calculate_bill(consignment):
    weight = consignment.weight
    additionalCharges = 0 if consignment.additionalCharges is None else consignment.additionalCharges

    consigner = consignment.consigner_id
    consignee = consignment.consignee_id

    rate = 0 if consigner.rate is None else consigner.rate
    odaCharge = 0 if consigner.odaCharge is None else consigner.odaCharge

    chargable_weight = custom_round(weight)
    amount = (chargable_weight * rate) + odaCharge
    if additionalCharges is None:
        additionalCharges = 0
    total_amount = amount + additionalCharges
    
    
    
    bill_obj, created = Billings.objects.update_or_create(
        lr=consignment,
        tatstatus=consignment.tatstatus,
        variance=consignment.variance,
        
        consigneeId=consignee.id,
        consigneeName=consignee.name,
        
        consignerId=consigner.id,
        consignerName=consigner.name,
        
        chargeableWeight=chargable_weight,
        amount=amount,
        rate=rate,
        odaCharge=odaCharge,
        additionalCharge=additionalCharges,
        totalAmount=total_amount,
        
        quantity=consignment.quantity,
        
        cp_chargeableWeight=chargable_weight,
        cp_amount=amount,
        cp_rate=rate,
        cp_odaCharge=odaCharge,
        cp_additionalCharge=additionalCharges,
        cp_totalAmount=total_amount,
        
        created_by='system',
        updated_by='system'
    )
    
    return bill_obj