import csv
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient()
db_name = 'socspam'
col_edge = 'mongo_edge_test'
col_user = 'mongo_user_dict_test'
client = MongoClient()
db = client[db_name]

dict_spam = eval(open("D:\spamer_detector\graph\mongoDB\\test_data\input_set_a.json").read())
dict_set_b = eval(open("D:\spamer_detector\graph\mongoDB\\test_data\input_set_b.json").read())
type_list = [-1]*7
set_A = [1,2,3]
set_B = [4,5,6]
for x in set_A :
    type_list[x] = 0
for x in set_B :
    type_list[x] = 1
print (type_list)
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

def swap(a,b) :
	sw = a
	if a < b :
		return a ,b
	return b, a

def cal_e_ab(set_a, set_b) :
    list_user = []
    sim = 0
    for a in set_a :
        list_user = mongo_find_list_user(a)
        for b in set_b :
            print(a,b)
            if (b in list_user) :
                print (f'chosse = {a}, {b}')
                c,d = swap(a,b)
                print (f'find = {mongo_find_edge(c, d)}')
                sim += mongo_find_edge(c, d)
    return sim
def cal_e_ab_new(set_a, set_b) :
    sim = 0
    for a in set_a :
        list_user = mongo_find_list_user(a)
        for b in list_user :
            if type_list[b] == 1 :
                c,d = swap(a,b)
                #print (c, d)
                #print (f'find = {mongo_find_edge(c, d)}')
                sim += mongo_find_edge(c,d)
    return sim

def cal_e_aa(set_a, set_b) :
    sim = 0
    for a in set_a :
        for b in set_b :
            if a < b :
                print (a, b)
                if (b in mongo_find_list_user(a)) :
                    sim += mongo_find_edge(a, b)
    return sim

def cal_e_aa_new(set_a, type) :
    sim = 0
    for a in set_a :
        list_user = mongo_find_list_user(a)
        for b in list_user :
            if type_list[b] == type and a < b:
                #print (a, b)
                #print (mongo_find_edge(a, b))
                sim += mongo_find_edge(a, b)
    return sim

def find_cross(element , set_x) :
    sim = 0
    for x in set_x :
        #print (x)
        if element in mongo_find_list_user(x) :
            max_edge = max(element, x)
            min_edge = min(element, x)
            print (min_edge, max_edge)
            #print (mongo_find_edge(min_edge, max_edge))
            sim += mongo_find_edge(min_edge, max_edge)
    return sim

def find_cross_new(element , set_x, type) :
    sim = 0
    list_user = mongo_find_list_user(element)
    for b in list_user :
        c,d = swap(element,b)
        if type_list[b] == type:
            print (c, d)
            sim += mongo_find_edge(c, d)

    return sim
'''
#sim1 = cal_e_ab(set_A, set_B)
#print (sim1)
#sim3 = cal_e_aa(set_B, set_B)
#print (sim3)
sim5 = find_cross(2, set_B)
print (sim5)
sim7 = find_cross(2, set_A)
print (sim7)
print ('============================')
#sim2 = cal_e_ab_new(set_A,set_B)
#print (sim2)
#sim4 = cal_e_aa_new(set_B, 1)
#print (sim4)
sim6 =find_cross_new(2, set_B, 1)
print (sim6)
sim8 =find_cross_new(2, set_A, 0)
print (sim8)
'''
b = 0.19999999999999999
a =round(b,16)
print (a)
print (b)
