import os

try:
    from bin_search import bin_search
    from db_proccessing_address import proccessing_fulladdress
except ModuleNotFoundError:
    from . import bin_search
    from . import proccessing_fulladdress

from bin_search import bin_search
from db_proccessing_address import proccessing_fulladdress
        
def get_addresses_from_file():
    file = os.path.join(os.path.dirname(__file__), "Moscow_Map_addresses_processed.tsv") 
    with open(file, "r") as f_r:
        moscow_map_data = []
        line = f_r.readline()
        line = f_r.readline()
        while line:
            line = line.strip('\n').split('\t')
            moscow_map_data.append(line)
            line = f_r.readline()
        moscow_map_data.sort()
    return moscow_map_data

def processing_line(moscow_map_data, line, words):
    line_save = line
    line = proccessing_fulladdress(line, words)
    if line == -1: return "Incorrect line%s" % line_save
    else:
        line_array = line.strip("\n").split("\t")
        id_ = line_array[0]
        address = line_array[1:5]
        year = line_array[5]
        type_ = line_array[6]
        floors = line_array[7]
        find_pos = bin_search(moscow_map_data, address)
        if find_pos != -1:
            if moscow_map_data[find_pos][4] != "None": year = moscow_map_data[find_pos][4]
            if moscow_map_data[find_pos][5] != "None": type_ = moscow_map_data[find_pos][5]
            if moscow_map_data[find_pos][6] != "None": floors = moscow_map_data[find_pos][6]
        return [id_, year, type_, floors]

# формат строки: "id\tfulladdress\tbuildyear\tisbuildingliving\tfloorscount\n"
lines = []
with open("13.csv", "r") as f_r:
    for line in f_r:
        lines.append(line)
words = ["улица", "бульвар", "переулок", "проспект", "проезд", "шоссе", "площадь", "набережная", "аллея", "тупик"]
moscow_map_data = get_addresses_from_file()
for line in lines:
    print (processing_line(moscow_map_data, line, words))