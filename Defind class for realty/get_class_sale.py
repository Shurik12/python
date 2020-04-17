# функция get_class получает на вход строку вида "id\tprice\taddress\tclass\tyear\tfloors\n"
# с табами в роле разделителей и \n как символ конца строки
# и возвращает id и класс объекта в случае корректного адреса и -1 иначе

def get_class(line):
    
    try:
        import determinating_class as d_c_s
        import proccessing_string as p_s
    except ModuleNotFoundError:
        from . import determinating_class_sale as d_c_s
        from . import proccessing_string as p_s
    
    # объявляем переменные
    words = ["улица", "проспект", "бульвар", "переулок", 
             "проезд", "шоссе", "набережная",  "площадь", "тупик"]
    
    addresses = p_s.get_processed_addresses()
    line = p_s.proccessing_fulladdress(line, words)
    if line == -1: return -1
    else:
        try:
            find_pos = p_s.bin_search(addresses, line)
            id_ = line[0]
            if find_pos == -1: class_ = d_c_s.get_class(line)
            else: classes = addresses[find_pos][4]
            return id_, class_ 
        except:
            return -1

def main():
    line = "1469734\t30000.0\tМосква, ЮАО, район Даниловский, Кожевническая улица, 14\tb\t1986\t9\n"
    result = get_class(line)
    if result == -1:
        print ("Incorrect address")
    else:
        print (result)
        
if __name__ == "__main__":
    main()