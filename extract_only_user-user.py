import csv
sim_csv = open('D:\\spamer_detector\\graph\\40_non-spam\\sim_test_user_1.txt', 'r')
cnt =0
user_key = 1
list_user = []

with open('D:\\spamer_detector\\graph\\40_non-spam\\user_dict_raw2.csv', 'w', newline = '') as fp:
    writer = csv.writer(fp, delimiter=':' , quoting=csv.QUOTE_NONE  ,escapechar=' ')
    writer.writerow('[')

    while True :
        line = sim_csv.readline().replace('\n','').split(',')
        if line == ['{']:
            continue
        if line == ['}']:
            string_line = "{'from':"+str(user_key)+ ",'list':"+str(list_user)+"}"
            writer.writerow([string_line])
            writer.writerow(']')
            break

        user_1 = line[0].replace('\'','')
        user_1 = int(user_1)
        second_sec = line[1].replace('\'','').split(':')
        user_2 = int(second_sec[0])
        sim = float(second_sec[1])
        #print (user_1, user_2, sim)
        if user_key == user_1 :
            list_user.append(user_2)
        elif user_key != user_1 :
            string_line = "{'from':"+str(user_key)+ ",'list':"+str(list_user)+"},"
            writer.writerow([string_line])
            user_key = user_1
            list_user = []
            list_user.append(user_2)
