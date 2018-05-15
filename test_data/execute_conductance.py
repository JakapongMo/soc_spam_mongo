import csv

dict_sim = eval(open("D:\\spamer_detector\\graph\\40_non-spam\\copy_filter_sim_0.4_more_than_0.9_table.csv").read())

dict_user = eval(open("D:\\spamer_detector\\graph\\40_non-spam\\user_dict.csv").read())

#dict_spam = eval(open("D:\\spamer_detector\\graph\\40_non-spam\\spammer_2815_spam.csv").read())


def cal_e_ab(set_a, set_b) :
    sim = 0
    for a in set_a :
        for b in set_b :
            if a < b :
                #print (a, b)
                if (b in dict_user[a]) :
                    #print (a, b)
                    key_a = str(a) + ',' +str(b)
                    #print (dict_sim[key_a])
                    sim += dict_sim[key_a]
    return sim
def cal_conductance(e_ab, e_aa, e_bb) :
    #print ("e_ab :", e_ab)
    #print ("e_aa :", e_aa)
    #print ("e_bb :", e_bb)
    res = e_ab/(e_ab+(2*min(e_aa,e_bb)))
    return res

def find_cross(element , set_x) :
    sim = 0
    for x in set_x :
        #print (x)
        if element in dict_user[x] :
            max_edge = max(element, x)
            min_edge = min(element, x)
            #print (min_edge, max_edge)
            key_a = str(min_edge) + ',' + str(max_edge)
            #print (dict_sim[key_a])
            sim += dict_sim[key_a]
    return sim

'''
for k,v in dict_sim.items() :
    print (k, v)
'''

print ('user,conductance')
set_A = [1,2,3]
#set_A = dict_spam['spam']
con_list = [0,0,0]
set_B = [x for x in range(4,7)]
#print (f'set A = {set_A} , set B = {set_B}')
e_aa = cal_e_ab(set_A, set_A)
e_ab = cal_e_ab(set_A, set_B)
e_bb = cal_e_ab(set_B, set_B)
conductance = cal_conductance(e_ab, e_aa, e_bb)
#print (f'conductance = {conductance}')
#while len(set_b) != 2:
dict_conductance = {}
#if len(set_B) == 3 :
while len(set_B) != 0 :
    if len(set_B) == 1 :
        set_A.append(set_B[0])
        set_B.remove(set_B[0])
        con_list.append(0)
        break
    e_aa = cal_e_ab(set_A, set_A)
    e_ab = cal_e_ab(set_A, set_B)
    e_bb = cal_e_ab(set_B, set_B)
    new_e_aa = e_aa
    new_e_ab = e_ab
    new_e_bb = e_bb
    #conductance = cal_conductance(e_ab, e_aa, e_bb)
    #print ('fighting Mo')
    dict_conductance = {}
    new_set_B = []
    for e in set_B :
        new_set_B.append(e)
    for element in set_B :
        #print (f'element = {element}')
        #print (f'{element} cross set_A')
        e_cross_set_A = find_cross(element, set_A)
        #print (f'{element} cross set_B')
        e_cross_set_B = find_cross(element, set_B)
        #print (e)
        new_set_B.remove(element)
        set_A.append(element)
        #print (f'set A = {set_A} , new_set B = {new_set_B}')
        new_e_aa = e_aa + e_cross_set_A
        new_e_ab = e_ab - e_cross_set_A + e_cross_set_B
        new_e_bb = e_bb - e_cross_set_B
        conductance = cal_conductance(new_e_ab, new_e_aa, new_e_bb)
        dict_conductance[element] = conductance
        new_e_aa = new_e_aa - e_cross_set_A
        new_e_ab = new_e_ab + e_cross_set_A - e_cross_set_B
        new_e_bb = new_e_bb + e_cross_set_B
        #print (f'set A = {set_A} , new_set B = {new_set_B}')
        set_A.remove(element)
        new_set_B.append(element)
    user_min = min(dict_conductance.items(), key=lambda x: x[1])[0]
    con_list.append(min(dict_conductance.items(), key=lambda x: x[1])[1])
    #print ('user_min : ',user_min, 'conductance',min(dict_conductance.items(), key=lambda x: x[1])[1])
    min_conductance = min(dict_conductance.items(), key=lambda x: x[1])[1]
    print (str(user_min) + ',' + str(min_conductance))
    set_A.append(user_min)
    set_B.remove(user_min)

#print (f'set A = {set_A} , Set B = {set_B}')
'''
for key, list_user in dict_user.items() :
    print (key, list_user)
'''
