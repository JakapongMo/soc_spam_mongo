import csv
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/socspam')
db = client.socspam
collection = db.edge_0_3
a = open("D:\spamer_detector\graph\mongoDB\edge_test.csv","r")

#with open('D:\spamer_detector\graph\mongoDB\edge_mongoDB_test.csv', 'w', newline='') as fp:
    #writer = csv.writer(fp , quoting=csv.QUOTE_NONE  ,escapechar=' ')
    #writer.writerow(['['])
while True:
    line = a.readline().strip()
    if (line == '{' or line == '}') :
        continue
    if not line:
        break
    #print (line)
    key_1 = int(line.split(',')[0].strip('\''))
    temp = line.split(',')[1]
    key_2 = int(temp.split(':')[0].strip('\''))
    value = float(temp.split(':')[1])

    #print (key_1)
    #print (key_2)
    #print (value)
    #string_line = "{'from':"+ str(key_1) + "," + "'"+"to':" + str(key_2) + ",'edge':"+str(value)+"},"
    pcollection = {'from': key_1, 'to': key_2, 'edge': value}
    collection.insert_one(pcollection)
    #writer.writerow([string_line])
    #print (string_line)
    #writer.writerow([']'])


'''
cursor = collection.aggregate([{'$match':{'from':key_1,'to':key_2}}])
edge = 0
for i in cursor :
    edge = i['edge']
    break
'''
