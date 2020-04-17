import os

# proccessing field fulladdress
def proccessing_fulladdress(line, words, string = ""):
    line = line.replace("наб.", "набережная ")
    line = line.replace("ул.", "улица ")
    line = line.replace("бул.", "бульвар ")
    line = line.replace("б-р", "бульвар ")
    line = line.replace("пер.", "переулок ")
    line = line.replace("пр.", "проезд ")
    line = line.replace("просп.", "проезд ")
    line = line.replace("ал.", "аллея")
    line = line.replace("ш.", "шоссе")
    line = line.replace("пл.", "площадь")
    line = line.replace("туп.", "тупик")
    line = line.strip("\n").split('\t')
    fulladdress = line[1].split(', ')
    new_line = []
    new_line.append(line[0]) 
    count_words = 0
    for word in words:
        count_words += 1
        if word in line[1]:
            for k in range (len(fulladdress)):
                if word in fulladdress[k]:
                    street = fulladdress[k]
                    break
            if k < len(fulladdress)-1:
                if string:
                    new_line.append(string + word + ' ' + street.replace(word, "").strip())
                else:  new_line.append(word + ' ' + street.replace(word, "").strip())
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
                        new_line.append(house[:c])
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
    for word in line[2:]:
        new_line.append(word)
    string = '' 
    for i in new_line:
        string += str(i) + '\t'
    string = string.strip() + '\n'
    return string