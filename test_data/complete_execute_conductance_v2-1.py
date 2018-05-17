import csv
import pymongo
from pymongo import MongoClient
import datetime
import sys

client = pymongo.MongoClient()
db_name = 'socspam'
col_edge = 'mongo_edge_test'
col_user = 'mongo_user_dict_test'
client = MongoClient()
db = client[db_name]

dict_spam = eval(open("D:\spamer_detector\graph\mongoDB\\test_data\input_set_a.json").read())
dict_set_b = eval(open("D:\spamer_detector\graph\mongoDB\\test_data\input_set_b.json").read())
number_node = 6 + 1

def mongo_find_edge(from_1, to_2):
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

def cal_conductance(e_ab, e_aa, e_bb) :
    #print ("e_ab :", e_ab)
    #print ("e_aa :", e_aa)
    #print ("e_bb :", e_bb)
    res = e_ab/(e_ab+(2*min(e_aa,e_bb)))
    return res

def find_cross(element) :
    sim_cross_a = 0
    sim_cross_b = 0
    list_user = mongo_find_list_user(element)
    for user in list_user :
        c,d = swap(element, user)
        if type_list[user] == 0 :
            text = f'{element} cross A : {c}, {d}'
            time_stamp(text)
            sim_cross_a += mongo_find_edge(c, d)
        elif type_list[user] == 1 :
            text = f'{element} cross B : {c}, {d}'
            time_stamp(text)
            sim_cross_b += mongo_find_edge(c,d)

    return sim_cross_a, sim_cross_b

def finde_conductance_min(element, conductance, e_aa, e_ab, e_bb, element2, conductance2, new_e_aa, new_e_ab, new_e_bb) :
    if conductance <= conductance2:
        return element, conductance, e_aa, e_ab, e_bb
    return element2, conductance2, new_e_aa, new_e_ab, new_e_bb


def time_stamp(text) :
    now = datetime.datetime.now()
    print (f'{text} :: {now}', file=sys.stderr, flush = True)
    #print(f'test', file=sys.stderr)
    #sys.stderr.flush()

def cal_edge_first(set_A, set_B) :
    count_cal_edge = 0
    sim_e_aa = 0
    sim_e_ab = 0
    sim_e_bb = 0
    set_Sum = set_A + set_B
    for element in set_Sum :
        count_cal_edge += 1
        text = f'Node {count_cal_edge} List user(mongo_find) of {element}'
        time_stamp(text)
        list_user = mongo_find_list_user(element)
        if type_list[element] == 0 :
            for user in list_user :
                if type_list[user] == 0 and element < user:
                    text = f' Edge E_AA(mongo find) between {element} {user}'
                    time_stamp(text)
                    sim_e_aa += mongo_find_edge(element,user)
                elif type_list[user] == 1 :
                    c, d = swap(element,user)
                    #time_stamp('mogodb_find_edge')
                    text = f' Edge E_AB(mongo find) between {element} {user}'
                    time_stamp(text)
                    sim_e_ab += mongo_find_edge(c,d)

        elif type_list[element] == 1 :
            for user in list_user :
                if type_list[user] == 1 and element < user:
                    text = f' Edge E_BB(mongo find between {element} {user}'
                    time_stamp(text)
                    sim_e_bb += mongo_find_edge(element,user)
    return sim_e_aa, sim_e_ab, sim_e_bb

print ('user,conductance', flush = True)
set_A = dict_spam['set_A']
set_B = dict_set_b['set_B']
type_list = [-1] * number_node

for x in set_A :
    type_list[x] = 0
for x in set_B :
    type_list[x] = 1


conductance_old = 2
element_old = -1
dict_conductance = {}
time_stamp('!!!Cal_edge_first : start!!!')
e_aa , e_ab, e_bb = cal_edge_first(set_A, set_B)
time_stamp('!!!Cal_edge_first : finish!!!')
e_aa =round(e_aa, 15)
e_ab =round(e_ab, 15)
e_bb =round(e_bb, 15)
e_aa_chosen = e_aa
e_ab_chosen = e_ab
e_bb_chosen = e_bb

while len(set_B) != 0 :
    if len(set_B) == 1 :
        set_A.append(set_B[0])
        print (f'{set_B[0]},{1.0}')
        set_B.remove(set_B[0])
        break
    conductance_old = 2
    element_old = -1
    e_aa = e_aa_chosen
    e_ab = e_ab_chosen
    e_bb = e_bb_chosen
    e_aa =round(e_aa, 15)
    e_ab =round(e_ab, 15)
    e_bb =round(e_bb, 15)
    new_e_aa = round(e_aa, 15)
    new_e_ab = round(e_ab, 15)
    new_e_bb = round(e_bb, 15)
    text = (f'e_aa = {e_aa}, e_bb = {e_bb}, e_ab = {e_ab}')
    time_stamp(text)
	#print ('fighting Mo')
    dict_conductance = {}
    new_set_B = []
    for e in set_B :
        new_set_B.append(e)
    for element in set_B :
        time_stamp('!!!start_find_cross!!!')
        e_cross_set_A, e_cross_set_B = find_cross(element)
        e_cross_set_A = round(e_cross_set_A, 15)
        e_cross_set_B = round(e_cross_set_B, 15)
        new_set_B.remove(element)
        set_A.append(element)
        new_e_aa = e_aa + e_cross_set_A
        new_e_ab = e_ab - e_cross_set_A + e_cross_set_B
        #text =  (f'e_bb= {e_bb} - e_cross_set_B= {e_cross_set_B}')
        #time_stamp(text)
        new_e_bb = e_bb - e_cross_set_B
        conductance = cal_conductance(new_e_ab, new_e_aa, new_e_bb)
        #text =  (f'element = {element} conductance = {conductance}')
        #time_stamp(text)
        element_old, conductance_old, e_aa_chosen, e_ab_chosen, e_bb_chosen = finde_conductance_min(element_old, conductance_old, e_aa_chosen, e_ab_chosen, e_bb_chosen, element, conductance, new_e_aa, new_e_ab, new_e_bb)
        new_e_aa = new_e_aa - e_cross_set_A
        new_e_ab = new_e_ab + e_cross_set_A - e_cross_set_B
        new_e_bb = new_e_bb + e_cross_set_B
        #print (f'set A = {set_A} , new_set B = {new_set_B}')
        set_A.remove(element)
        new_set_B.append(element)
    user_min = element_old
    min_conductance = conductance_old
    print (str(user_min) + ',' + str(min_conductance), flush=True)
    set_A.append(user_min)
    set_B.remove(user_min)
    type_list[user_min] = 0
