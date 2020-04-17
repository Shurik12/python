import os

# input data
def input_data():
    head_array = ['id', 'price', 'fulladdress', 'buildingclass', 'buildyear', 'floorscount']
    head_line = ''
    for word in head_array:
        head_line += word + '\t'
    head_line = head_line.strip() + '\n'
    return head_array, head_line

# proccessing field fulladdress
def proccessing_fulladdress(line, words):
    line = line.replace("наб.", "набережная ")
    line = line.replace("ул.", "улица ")
    line = line.replace("бул.", "бульвар ")
    line = line.replace("б-р", "бульвар ")
    line = line.replace("пер.", "переулок ")
    line = line.replace("пр.", "проезд ")
    line = line.replace("просп.", "проезд ")
    
    
    line = line.strip("\n").split('\t')
    if len(line) != 6: return -1
    for i in range(len(line)):
        if line[i] == "": line[i] = "None"
    fulladdress = line[2].split(', ')
    new_line = []
    new_line.append(line[0]) 
    new_line.append(line[1])
    count_words = 0
    for word in words:
        count_words += 1
        if word in line[2]:
            for k in range (len(fulladdress)):
                if word in fulladdress[k]:
                    street = fulladdress[k]
                    break
            if k < len(fulladdress)-1:
                new_line.append(word + ' ' + street.replace(word, "").strip()) 
                # обработка дома
                house = fulladdress[k+1].lower().strip()
                k = house.find("к")
                c = house.find("с")
                if k < 0 and c < 0:
                    new_line.append(house)
                    new_line.append('')
                    new_line.append('') 
                elif k < 0 and c > 0:
                    new_line.append(house[:c])
                    new_line.append('')
                    new_line.append(house[c+1:])
                elif k > 0 and c < 0:
                    new_line.append(house[:k])
                    new_line.append('')
                    new_line.append(house[k+1:])
                else:
                    if k < c:
                        new_line.append(house[:k])
                        new_line.append(house[k+1:c])
                        new_line.append(house[c+1:])
                    else: 
                        new_line.append(house[:k])
                        new_line.append(house[c+1:k])
                        new_line.append(house[k+1:])
                # конец обработки дома 
            else:
                new_line.append(word + ' ' + street.replace(word, "").strip())
                new_line.append('')
                new_line.append('')
                new_line.append('')
            break 
        else:
            if count_words == len(words):
                return -1
    for i in range(3, 6):
        new_line.append(line[i])
    return new_line

# в файле 'dictionary of addresses.tsv' хранятся обработанные адреса
# считываем их из него
def get_processed_addresses():
    file = os.path.join(os.path.dirname(__file__), 'dictionary of addresses.tsv')
    array_addresses = []
    with open(file, 'r') as f_r:
        for line in f_r:
            line = line.strip('\n').split('\t')
            array_addresses.append(line[0:5])
    array_addresses.sort()
    return array_addresses

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