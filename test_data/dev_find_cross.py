import csv
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient()
db_name = 'socspam'
col_edge = 'mongo_edge_test'
col_user = 'mongo_user_dict_test'
client = MongoClient()
db = client[db_name]

def mongo_find_edge(from_1, to_2):
	#client = MongoClient()
	#db = client[db_name]
	cursor = db[col_edge].find({"from": from_1,"to" : to_2})
	doc = list(cursor)
	if len(doc) > 0 :
		return doc[0]['edge']
	return -1
def mongo_find_list_user(from_1):
	cursor = db[col_user].find({"from": from_1})
	doc = list(cursor)
	if len(doc) > 0 :
		return doc[0]['list']
	return []

def find_cross(element , set_x) :
    sim = 0
    for x in set_x :
        #print (x)
        if element in mongo_find_list_user(x) :
            max_edge = max(element, x)
            min_edge = min(element, x)
            print (min_edge, max_edge)
            key_a = str(min_edge) + ',' + str(max_edge)
            #print (dict_sim[key_a])
            sim += mongo_find_edge(min_edge, max_edge)
    return sim



find_cross(4, [5,6])
find_cross(4, [1,2,3])
