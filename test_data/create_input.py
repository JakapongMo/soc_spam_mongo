import csv

list_spam = []
with open('D:\spamer_detector\graph\mongoDB\\spam_input_0_3.json', 'w', newline = '') as fp:
    writer = csv.writer(fp, delimiter=':')
    writer.writerow('{')
    with open('D:\spamer_detector\graph\mongoDB\\spam_10_percent_0_3.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['spam_10_percent_0_3'])
            list_spam.append(row['spam_10_percent_0_3'])
        writer.writerow([str('\"spam_input_0_3\"'), str(list_spam)])

    writer.writerow('}')
