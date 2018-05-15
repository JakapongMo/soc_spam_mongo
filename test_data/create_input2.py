import csv

list_set_b = []
with open('D:\spamer_detector\graph\mongoDB\\set_b_input_0_3.json', 'w', newline = '') as fp:
    writer = csv.writer(fp, delimiter=':')
    writer.writerow('{')
    with open('D:\spamer_detector\graph\mongoDB\set_b_0_3.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['spam_10_percent_0_3'])
            list_set_b.append(row['set_b_0_3_input'])
        writer.writerow(["set_b_0_3_input", str(list_set_b)])

    writer.writerow('}')
