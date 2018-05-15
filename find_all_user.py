import csv
sim_csv = open('D:/spamer_detector/graph/40_non-spam/sim_test_user_1.txt', 'r')
cnt =0
user_key = 1
list_user = []
user_before = -1
with open('D:\spamer_detector\graph\mongoDB\\all_user_0_3.csv', 'w', newline = '') as fp:
    writer = csv.writer(fp, delimiter=':' , quoting=csv.QUOTE_NONE  ,escapechar=' ')
    writer.writerow(['user'])
    while True :
        line = sim_csv.readline().replace('\n','').split(',')
        if line == ['{']:
            continue
        if line == ['}']:
            break

        user_1 = line[0].replace('\'','')
        user_1 = int(user_1)
        if user_1 == user_before :
            continue
        else :
            string_line = str(user_1) + " ,"
            writer.writerow([string_line])
        user_before = user_1
