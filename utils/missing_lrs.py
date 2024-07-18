def find_missing_numbers(consignments):
    arr = [int(consignment.lr) for consignment in consignments]
    
    if not arr:
        return []

    min_val = min(arr)
    max_val = max(arr)
    
    full_set = set(range(min_val, max_val + 1))
    arr_set = set(arr)
    
    missing_numbers = sorted(list(full_set - arr_set))

    return missing_numbers