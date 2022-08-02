import csv
import pickle

#iconv -f Windows-1252 -t UTF-8 stancode.csv > stancode_utf8.csv

with open('stancode_utf8.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    rows = []
    for row in csv_reader:
        if line_count == 0:
            col_names = row
            line_count += 1
        else:
            rows.append(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

id_latin_dict = {i[4]: i[2] for i in rows}

pickle.dump(id_latin_dict, open("id_latin_dict.p", "wb"))
