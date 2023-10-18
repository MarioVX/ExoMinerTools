# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:04:31 2023

Refinery vs Constructor Optimizer and Planetary Scheduler
for the game Exominer by Exocorp

@author: Mario Kantz
"""
import numpy as np
from scipy.optimize import linprog

n_itm = 25
item_names = ("Refined Carbon", "Refined Tin", "Refined Cobalt", "Refined Bismuth", "Refined Cerussite",
              "Refined Manganese", "Refined Einherjer", "Manganese Alloy", "Cobalt Alloy", "Kriptonite Alloy",
              "Coreium Alloy", "Cerythium Alloy", "Cables", "Fuse", "Heat Sensor",
              "Ball Bearing", "Glass", "Circuit", "Lense", "Laser Optic",
              "Mini Rover", "Laser Blaster", "Advanced Sensors", "Surface Scanner", "Planet Explorer")
max_name_length = max(len(x) for x in item_names)
n_rnk = 15
ranks = {1:{"Refined Carbon":50},
         3:{"Refined Tin":100},
         4:{"Fuse":10, "Cables":20},
         5:{"Refined Cobalt":200, "Ball Bearing":10},
         6:{"Glass":50},
         7:{"Heat Sensor":50},
         9:{"Refined Manganese":100, "Lense":20},
         10:{"Refined Cerussite":500},
         11:{"Refined Bismuth":500, "Circuit":50},
         12:{"Refined Einherjer":100},
         13:{"Kriptonite Alloy":1, "Mini Rover":1},
         15:{"Laser Blaster":10},
         16:{"Cobalt Alloy":200, "Advanced Sensors":10},
         17:{"Surface Scanner":1, "Cables":5000},
         18:{"Cerythium Alloy":50, "Planet Explorer":1}}

rb = np.zeros((25,25))

def rec(product, time, ingredients:dict[str,int]):
    global rb
    j = item_names.index(product)
    rb[j,j] = 1.1/time
    for ing in ingredients:
        rb[item_names.index(ing),j] = -ingredients[ing]/time
    return None

rec("Refined Carbon", 20, dict())
rec("Refined Tin", 30, dict())
rec("Refined Cobalt", 40, dict())
rec("Refined Bismuth", 60, dict())
rec("Refined Cerussite", 80, dict())
rec("Refined Manganese", 120, dict())
rec("Refined Einherjer", 180, dict())
rec("Manganese Alloy", 240, {"Refined Manganese":1, "Refined Carbon":8})
rec("Cobalt Alloy", 480, {"Refined Cobalt":12, "Refined Tin":24})
rec("Kriptonite Alloy", 600, {"Refined Einherjer":1,})
rec("Coreium Alloy", 720, {"Manganese Alloy":1,})
rec("Cerythium Alloy", 840, {"Cobalt Alloy":1,})
rec("Cables", 60, {"Refined Carbon":4,})
rec("Fuse", 120, {"Refined Tin":4,})
rec("Heat Sensor", 240, {"Cables":1, "Refined Carbon":8})
rec("Ball Bearing", 480, {"Fuse":1, "Refined Cobalt":4})
rec("Glass", 720, {"Refined Bismuth":8,})
rec("Circuit", 1200, {"Refined Cerussite":4, "Refined Bismuth":4, "Cables":8})
rec("Lense", 2400, {"Glass":1, "Refined Manganese":4})
rec("Laser Optic", 3600, {"Refined Einherjer":4, "Refined Tin":8, "Lense":1})
rec("Mini Rover", 4800, {"Refined Manganese":4, "Circuit":4, "Ball Bearing":3})
rec("Laser Blaster", 7200, {"Manganese Alloy":4, "Laser Optic":1, "Lense":4})
rec("Advanced Sensors", 9000, {"Cobalt Alloy":16, "Heat Sensor":24})
rec("Surface Scanner", 10800, {"Kriptonite Alloy":4, "Laser Optic":1, "Glass":4})
rec("Planet Explorer", 12600, {"Coreium Alloy":4, "Mini Rover":4})

n_ref = 12

def rates(R,C):
    res = np.copy(rb)
    res[:,:n_ref] *= R
    res[:,n_ref:] *= C
    return res

var_names = []
for r in ranks:
    for i in item_names:
        var_names.append(("x",i,r))
    for i in item_names:
        var_names.append(("s",i,r))
for r in ranks:
    var_names.append(("t",r))
del i, r

def solve(R,C):
    rt = rates(R,C)
    # build A_eq
    for r in range(n_rnk):
        for bc in range(n_rnk):
            if bc==0:
                if r==0:
                    blockrow = np.hstack((np.copy(rt),-np.eye(n_itm)))
                elif r==1:
                    blockrow = np.hstack((np.zeros((n_itm,n_itm)),np.eye(n_itm)))
                else:
                    blockrow = np.zeros((n_itm,2*n_itm))
            else:
                if r-bc == 1:
                    blockrow = np.hstack((blockrow, np.zeros((n_itm,n_itm)), np.eye(n_itm)))
                elif r == bc:
                    blockrow = np.hstack((blockrow, np.copy(rt), -np.eye(n_itm)))
                else:
                    blockrow = np.hstack((blockrow, np.zeros((n_itm,2*n_itm))))
        blockrow = np.hstack((blockrow, np.zeros((n_itm, n_rnk))))
        if r==0:
            Ae = blockrow
        else:
            Ae = np.vstack((Ae, blockrow))
    be = np.zeros(n_rnk*n_itm)
    # build A_ub and b_ub
    bu = np.zeros(2*n_rnk)
    for r in range(n_rnk):
        row1 = np.array([0,]*(2*n_itm*r) + [1,]*n_ref + [0,]*(n_itm-n_ref+n_itm+2*n_itm*(n_rnk-r-1)+r) + [-1,] + [0,]*(n_rnk-1-r))
        row2 = np.array([0,]*(2*n_itm*r+n_ref) + [1,]*(n_itm-n_ref) + [0,]*(n_itm+2*n_itm*(n_rnk-1-r)+r) + [-1,] + [0,]*(n_rnk-1-r))
        if r == 0:
            Au = np.vstack((row1,row2))
        else:
            Au = np.vstack((Au,row1,row2))
    for rank in ranks:
        for item in ranks[rank]:
            row = np.zeros((2*n_itm+1)*n_rnk)
            i = item_names.index(item)
            row[var_names.index(("x",item,rank))] = -rt[i,i]
            Au = np.vstack((Au,row))
            bu = np.append(bu, -ranks[rank][item])
    c = np.array([0,]*(2*n_rnk*n_itm)+[1,]*n_rnk)
    result = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be)
    obval = result.fun
    Ae = np.vstack((Ae,c))
    be = np.append(be, obval)
    c = []
    for x in var_names:
        if x[0] == "x":
            c.append(1)
        else:
            c.append(0)
    c = np.array(c)
    result = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be)
    result.fun = obval
    assert result.success
    return result

def speed(lvl):
    if type(lvl) != int or lvl<1:
        raise ValueError()
    if lvl == 1:
        return 1
    if lvl == 2:
        return 1.25
    if lvl == 3:
        return 1.75
    if lvl == 4:
        return 2.5
    else:
        return 1.25 * lvl - 2.75

def timestring(num_time:float) -> str:
    t = num_time
    s = ""
    if t>=3600:
        s += str(int(t/3600)) + " h "
        t -= 3600*int(t/3600)
    if t>=60:
        s += str(int(t/60)) + " min "
        t -= 60 * int(t/60)
    s += str(int(t)) + " sec"
    return s

def main(Rs, Rl, Cs, Cl, rank) -> None:
    res_now = solve(Rs*speed(Rl)*1.25**2,Cs*speed(Cl)*1.25**2)
    res_rs = solve((Rs+1)*speed(Rl)*1.25**2,Cs*speed(Cl)*1.25**2).fun
    res_cs = solve(Rs*speed(Rl)*1.25**2,(Cs+1)*speed(Cl)*1.25**2).fun
    res_rl = solve(Rs*speed(Rl+1)*1.25**2,Cs*speed(Cl)*1.25**2).fun
    res_cl = solve(Rs*speed(Rl)*1.25**2,Cs*speed(Cl+1)*1.25**2).fun
    p = 1 + rank//20
    total_time = res_now.fun
    print("Plan for Planetary",p,"from rank",(p-1)*20+(p==1),"to",p*20)
    print("at",Rs,"Refinery slots, Refinery level",Rl,",",Cs,"Constructor slots, Constructor level",Cl)
    print()
    print("Total time required:",timestring(total_time*p))
    print()
    print("Improvement options information:")
    print("Time saved with next Refinery slot:",timestring((res_now.fun-res_rs)*p))
    print("Time saved with next Constructor slot:",timestring((res_now.fun-res_cs)*p))
    if res_rl <= res_cl:
        nextup = "Refinery"
    else:
        nextup = "Constructor"
    print("Recommended next speed level upgrade:", nextup)
    print()
    rd = dict((x,[]) for x in ranks)
    for i in range(len(var_names)):
        if res_now.x[i] > 10**(-8):
            rd[var_names[i][-1]].append(var_names[i][:-1]+(res_now.x[i],))
    for rank in ranks:
        print("="*8,"Rank",(p-1)*20+rank,"="*16)
        assert rd[rank][-1][0] == "t"
        tr = rd[rank][-1][1]
        print("Duration:",timestring(p*tr))
        rs = dict((x,0.0) for x in item_names)
        for x in rd[rank]:
            if x[0] == "s":
                rs[x[1]] = x[2] * p
        ref = list()
        con = list()
        i = 0
        while rd[rank][i][0] == "x":
            if item_names.index(rd[rank][i][1]) < n_ref:
                ref.append((rd[rank][i][1],rd[rank][i][2]/tr,rs[rd[rank][i][1]]))
            else:
                con.append((rd[rank][i][1],rd[rank][i][2]/tr,rs[rd[rank][i][1]]))
            i += 1
        del i
        print("-"*8,"Refinery","-"*16)
        for x in ref:
            namestring = x[0] + " "*(max_name_length+1-len(x[0]))
            percentstring = str(float(round(x[1]*100,ndigits=4)))
            percentstring = ' '*(3-percentstring.index(".")) + percentstring
            if len(percentstring) < 8:
                percentstring += ' '*(8-len(percentstring))
            percentstring += '% to '
            stockstring = str(int(-(-(x[2])//1)))
            print(namestring+percentstring+stockstring)
        actsum = sum(x[1] for x in ref)
        if actsum < 1 - 10**(-8):
            namestring = "idle" + " "*(max_name_length+1-len("idle"))
            percentstring = str(float(round((1-actsum)*100,ndigits=4)))
            percentstring = ' '*(3-percentstring.index(".")) + percentstring
            if len(percentstring) < 8:
                percentstring += " "*(8-len(percentstring))
            percentstring += "%"
            print(namestring+percentstring)
        print("-"*8,"Constructor","-"*13)
        for x in con:
            namestring = x[0] + " "*(max_name_length+1-len(x[0]))
            percentstring = str(float(round(x[1]*100,ndigits=4)))
            percentstring = ' '*(3-percentstring.index(".")) + percentstring
            if len(percentstring) < 8:
                percentstring += ' '*(8-len(percentstring))
            percentstring += '% to '
            stockstring = str(int(-(-(x[2])//1)))
            print(namestring+percentstring+stockstring)
        actsum = sum(x[1] for x in con)
        if actsum < 1 - 10**(-8):
            namestring = "idle" + " "*(max_name_length+1-len("idle"))
            percentstring = str(float(round((1-actsum)*100,ndigits=4)))
            percentstring = ' '*(3-percentstring.index(".")) + percentstring
            if len(percentstring) < 8:
                percentstring += " "*(8-len(percentstring))
            percentstring += "%"
            print(namestring+percentstring)
        print()
    return None

def speedratio(Rslots, Cslots, Rlevel=1, Clevel=1, n_iterations=1000):
    rl = Rlevel
    cl = Clevel
    n = n_iterations
    while n>0:
        res_r = solve(Rslots*1.25**2 * speed(rl+1), Cslots*1.25**2 * speed(cl)).fun
        res_c = solve(Rslots*1.25**2 * speed(rl), Cslots*1.25**2 * speed(cl+1)).fun
        if res_c < res_r:
            cl += 1
        else:
            rl += 1
        n -= 1
    return (rl,cl,speed(rl)*Rslots/(speed(cl)*Cslots))

if __name__ == "__main__":
    Rs = int(input("How many Refinery slots can be considered available? "))
    Rl = int(input("What's the current Speed Level of your Refinery? "))
    Cs = int(input("How many Constructor slots can be considered available? "))
    Cl = int(input("What's the current Speed Level of your Constructor? "))
    rank = int(input("What's your current Rank? "))
    print()
    main(Rs, Rl, Cs, Cl, rank)
    input()