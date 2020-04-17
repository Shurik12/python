# бинарный поиск
def bin_search(addresses, value):
    lenght = len(addresses)
    mid = lenght // 2
    low = 0
    high = lenght - 1

    while addresses[mid][:4] != value and low <= high:
        if value > addresses[mid][:4]:
            low = mid + 1
        else:
            high = mid - 1
        mid = (low + high) // 2
    if low > high:
        return -1
    else:
        return mid