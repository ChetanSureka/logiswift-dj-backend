from django.db.models import Sum, F

def get_bill_stats(queryset):
    """
    Calculate billing stats for the given queryset.
    Returns a dictionary with total weight, total quantity, additional charge, etc.
    """
    stats = queryset.aggregate(
        total_weight=Sum('chargeableWeight'),
        total_qty=Sum('quantity'),
        total_additional_charge=Sum('additionalCharge'),
        total_amount_excluding_oda=Sum(F('totalAmount') - F('odaCharge')),
        grand_total_amount=Sum('totalAmount'),
        total_oda_charge=Sum('odaCharge')
    )

    # Set default values to 0 if any of the stats are None
    return {
        "total_weight": stats.get('total_weight') or 0,
        "total_qty": stats.get('total_qty') or 0,
        "total_additional_charge": stats.get('total_additional_charge') or 0,
        "total_amount_excluding_oda": stats.get('total_amount_excluding_oda') or 0,
        "grand_total_amount": stats.get('grand_total_amount') or 0,
        "total_oda_charge": stats.get('total_oda_charge') or 0,
    }
