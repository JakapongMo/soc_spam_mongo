import csv
sim_csv = open('D:\\spamer_detector\\graph\\40_non-spam\\filter_sim_0.4_more_than_0.9_table.csv', 'r')
cnt =0
user_key = 1
list_user = []
list_sim = []

with open('D:\spamer_detector\graph\mongoDB\\test_data\server\mongo_sim_user_dict.csv', 'w', newline = '') as fp:
    writer = csv.writer(fp, delimiter=':' , quoting=csv.QUOTE_NONE  ,escapechar=' ')
    writer.writerow('[')

    while True :
        line = sim_csv.readline().replace('\n','').split(',')
        if line == ['{']:
            continue
        if line == ['}']:
            string_line = "{'from':"+str(user_key)+ ",'list':"+str(list_sim)+"}"
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
            list_sim.append(sim)
        elif user_key != user_1 :
            string_line = "{'from':"+str(user_key)+ ",'list':"+str(list_sim)+"},"
            writer.writerow([string_line])
            user_key = user_1
            list_user = []
            list_sim = []
            list_sim.append(sim)
            list_user.append(user_2)
