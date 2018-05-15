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

def cal_conductance(e_ab, e_aa, e_bb) :
    print ("e_ab :", e_ab)
    print ("e_aa :", e_aa)
    print ("e_bb :", e_bb)
    res = e_ab/(e_ab+(2*min(e_aa,e_bb)))
    return res

def find_cross(element , set_x, type) :
    sim = 0
    list_user = mongo_find_list_user(element)
    for b in list_user :
        c,d = swap(element,b)
        if type_list[b] == type:
            print (c, d)
            print (mongo_find_edge(c,d))
            sim += mongo_find_edge(c, d)

    return sim

def finde_conductance_min(element, conductance, e_aa, e_ab, e_bb, element2, conductance2, new_e_aa, new_e_ab, new_e_bb) :
    if conductance <= conductance2:
        return element, conductance, e_aa, e_ab, e_bb
    return element2, conductance2, new_e_aa, new_e_ab, new_e_bb

def cal_e_aa(set_a, type) :
    sim = 0
    for a in set_a :
        list_user = mongo_find_list_user(a)
        for b in list_user :
            if type_list[b] == type and a < b:
                #print (a, b)
                #print (mongo_find_edge(a, b))
                sim += mongo_find_edge(a, b)
    return sim

def cal_e_ab(set_a, set_b) :
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


print ('user,conductance')
#set_A = [1,2,3]
set_A = dict_spam['set_A']
set_B = dict_set_b['set_B']
con_list = [0,0,0]
type_list = [-1] * 7

for x in set_A :
    type_list[x] = 0
for x in set_B :
    type_list[x] = 1


conductance_old = 2
element_old = -1
dict_conductance = {}
e_aa = cal_e_aa(set_A, 0)
e_ab = cal_e_ab(set_A, set_B)
e_bb = cal_e_aa(set_B, 1)
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
        con_list.append(0)
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
    print(f'e_aa = {e_aa}, e_bb = {e_bb}, e_ab = {e_ab}')
    #print ('fighting Mo')
    dict_conductance = {}
    new_set_B = []
    for e in set_B :
        new_set_B.append(e)
    for element in set_B :
        #print (f'element = {element}')
        print (f'{element} cross set_A')
        e_cross_set_A = find_cross(element, set_A, 0)
        e_cross_set_A = round(e_cross_set_A, 15)
        print (f'{element} cross set_B')
        e_cross_set_B = find_cross(element, set_B, 1)
        e_cross_set_B = round(e_cross_set_B, 15)
        new_set_B.remove(element)
        set_A.append(element)
        #print (f'set A = {set_A} , new_set B = {new_set_B}')
        new_e_aa = e_aa + e_cross_set_A
        new_e_ab = e_ab - e_cross_set_A + e_cross_set_B
        print (f'e_bb= {e_bb} - e_cross_set_B= {e_cross_set_B}')
        new_e_bb = e_bb - e_cross_set_B
        conductance = cal_conductance(new_e_ab, new_e_aa, new_e_bb)
        #dict_conductance[element] = conductance
        print (f'element = {element} conductance = {conductance}')
        element_old, conductance_old, e_aa_chosen, e_ab_chosen, e_bb_chosen = finde_conductance_min(element_old, conductance_old, e_aa_chosen, e_ab_chosen, e_bb_chosen, element, conductance, new_e_aa, new_e_ab, new_e_bb)
        new_e_aa = new_e_aa - e_cross_set_A
        new_e_ab = new_e_ab + e_cross_set_A - e_cross_set_B
        new_e_bb = new_e_bb + e_cross_set_B
        print (f'set A = {set_A} , new_set B = {new_set_B}')
        set_A.remove(element)
        new_set_B.append(element)
    #user_min = min(dict_conductance.items(), key=lambda x: x[1])[0]
    user_min = element_old
    #con_list.append(min(dict_conductance.items(), key=lambda x: x[1])[1])
    con_list.append(conductance_old)
    #print ('user_min : ',user_min, 'conductance',min(dict_conductance.items(), key=lambda x: x[1])[1])
    #min_conductance = min(dict_conductance.items(), key=lambda x: x[1])[1]
    min_conductance = conductance_old
    print (str(user_min) + ',' + str(min_conductance))
    set_A.append(user_min)
    set_B.remove(user_min)
    type_list[user_min] = 0
    print (f'set_A = {set_A}, set_B = {set_B}')
    print (f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1 round')


#print (f'set A = {set_A} , Set B = {set_B}')
'''
for key, list_user in dict_user.items() :
    print (key, list_user)
'''
