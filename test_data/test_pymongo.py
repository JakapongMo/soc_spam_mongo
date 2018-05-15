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


edge = mongo_find_edge(1, 2)
print (edge)
list_user = mongo_find_list_user(1)
print (list_user)
