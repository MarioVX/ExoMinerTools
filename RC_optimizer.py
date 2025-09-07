# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:04:31 2023

Refinery vs Constructor Optimizer and Planetary Scheduler
for the game Exominer by Exocorp

@author: Mario Kantz
"""
import numpy as np
from scipy.optimize import linprog

item_names = []
rb = np.array(())

def rec(product, time, ingredients:dict[str,int]):
    global rb
    global item_names
    assert product not in item_names
    j = len(item_names)
    item_names.append(product)
    assert item_names.index(product) == j
    if j==0:
        rb = np.array([[1.1/time,],], dtype='double')
    else:
        rb = np.pad(rb, ((0,1),(0,1)))
        rb[j,j] = 1.1/time
    for ing in ingredients:
        assert ing in item_names
        rb[item_names.index(ing),j] = -ingredients[ing]/time
    return None

# ===== Settings, Recipes, Ranks =====
slots_complete = True

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
rec("Etherium Alloy", 960, {"Kriptonite Alloy":1})
rec("Cosmium Alloy", 1080, {"Coreium Alloy":1})
rec("Galaxium Alloy", 1200, {"Cerythium Alloy":1})
rec("Mythril Alloy", 1440, {"Etherium Alloy":1})
rec("Xenon Alloy", 1680, {"Cosmium Alloy":1})

rec("Cables", 60, {"Refined Carbon":4,})
rec("Fuse", 120, {"Refined Tin":4,})
rec("Heat Sensor", 240, {"Cables":1, "Refined Carbon":8})
rec("Ball Bearing", 480, {"Fuse":1, "Refined Cobalt":4})
rec("Glass", 720, {"Refined Bismuth":8,})
rec("Circuit", 1200, {"Refined Cerussite":4, "Refined Bismuth":4, "Cables":8})
rec("Lense", 2400, {"Glass":1, "Refined Manganese":4})
rec("Laser Optic", 3600, {"Refined Einherjer":4, "Refined Tin":8, "Lense":1})
rec("Mini Rover", 4800, {"Refined Manganese":4, "Circuit":4, "Ball Bearing":3})
rec("Solar Panel", 6000, {"Circuit":4, "Glass":8})
rec("Laser Blaster", 7200, {"Manganese Alloy":4, "Laser Optic":1, "Lense":4})
rec("Advanced Sensors", 9000, {"Cobalt Alloy":16, "Heat Sensor":24})
rec("Surface Scanner", 10800, {"Kriptonite Alloy":4, "Laser Optic":1, "Glass":4})
rec("Planet Explorer", 12600, {"Coreium Alloy":4, "Mini Rover":4})
rec("Planet Dust Collector", 13500, {"Laser Blaster":1, "Surface Scanner":1, "Manganese Alloy":8})
rec("Plasma Cannon", 15000, {"Cerythium Alloy":12, "Laser Blaster":4})
rec("Ion Rocket Engine", 15600, {"Kriptonite Alloy":48, "Refined Cerussite":120, "Coreium Alloy":32})
rec("Mobile Telescope", 16800, {"Lense":16, "Planet Explorer":1})
rec("Advanced Antenna", 18000, {"Cobalt Alloy":120, "Etherium Alloy":16})
rec("Xenon Engine", 19800, {"Manganese Alloy":320, "Ball Bearing":160})
rec("Planet Radar", 21000, {"Etherium Alloy":16, "Advanced Sensors":1})
rec("Infrared Homing Turret", 21600, {"Galaxium Alloy":4, "Plasma Cannon":1})
rec("Gravity Reactor", 24000, {"Refined Cerussite":120, "Xenon Engine":1})
rec("Exospace Probe", 25200, {"Advanced Antenna":1, "Mobile Telescope":1, "Solar Panel":20})
rec("Space Protector X1000", 27600, {"Cerythium Alloy":240, "Infrared Homing Turret":1})
rec("Supercombustion Fuel", 29700, {"Mythril Alloy":400, "Xenon Alloy":80})
rec("Space Fleet Station", 31500, {"Planet Explorer":48, "Exospace Probe":1})

ranks = {0:{1:{"Make":{"Refined Carbon":50},},
            3:{"Make":{"Refined Tin":100},},
            4:{"Make":{"Fuse":10, "Cables":20},},
            5:{"Make":{"Refined Cobalt":200, "Ball Bearing":10},},
            6:{"Make":{"Glass":50},},
            7:{"Make":{"Heat Sensor":50},},
            9:{"Make":{"Refined Manganese":100, "Lense":20},},
           10:{"Make":{"Refined Cerussite":500},},
           11:{"Make":{"Refined Bismuth":500, "Circuit":50},},
           12:{"Make":{"Refined Einherjer":100},},
           13:{"Make":{"Kriptonite Alloy":1, "Mini Rover":1},},
           15:{"Make":{"Laser Blaster":10},},
           16:{"Make":{"Cobalt Alloy":200, "Advanced Sensors":10},},
           17:{"Make":{"Surface Scanner":1, "Cables":5000},},
           18:{"Make":{"Cerythium Alloy":50, "Planet Explorer":1},}},
         1:{1:{"Make":{"Refined Tin":50,},},
            2:{"Make":{"Heat Sensor":15,},},
            3:{"Make":{"Refined Cobalt":50, "Ball Bearing":15},},
            4:{"Make":{"Refined Bismuth":750, "Glass":50},},
            6:{"Make":{"Refined Cerussite":150,},},
            7:{"Make":{"Cables":500,},"Have":{"Circuit":25}},
            8:{"Make":{"Refined Manganese":150, "Lense":20},},
            9:{"Make":{"Refined Einherjer":75, "Laser Optic":10},},
            10:{"Make":{"Circuit":40,},"Have":{"Solar Panel":8,}},
            11:{"Make":{"Cobalt Alloy":100, "Manganese Alloy":25, "Advanced Sensors":5},},
            12:{"Make":{"Kriptonite Alloy":20,},},
            13:{"Have":{"Surface Scanner":1,},},
            14:{"Make":{"Planet Dust Collector":1,},"Have":{"Laser Blaster":8,}},
            15:{"Make":{"Coreium Alloy":50, "Cerythium Alloy":15, "Plasma Cannon":1},},
            16:{"Make":{"Ion Rocket Engine":2,},"Have":{"Etherium Alloy":10,}},
            17:{"Make":{"Mini Rover":5, "Planet Explorer":1, "Mobile Telescope":1},},
            18:{"Have":{"Etherium Alloy":100, "Manganese Alloy":800, "Cobalt Alloy":800},},
            19:{"Make":{"Advanced Antenna":3, "Xenon Engine":2, "Planet Radar":1},}},
         2:{1:{"Make":{"Refined Carbon":100, "Refined Tin":50, "Cables":4}},
            2:{"Make":{"Fuse":20, "Heat Sensor":15}},
            3:{"Make":{"Refined Bismuth":1000}},
            4:{"Make":{"Refined Cerussite":20, "Glass":100}},
            5:{"Make":{"Refined Manganese":50, "Lense":30, "Circuit":30}},
            6:{"Make":{"Refined Einherjer":20, "Mini Rover":4}},
            7:{"Make":{"Solar Panel":6, "Manganese Alloy":30, "Laser Blaster":6}},
            8:{"Make":{"Refined Cerussite":450, "Surface Scanner":3, "Kriptonite Alloy":120}},
            9:{"Make":{"Etherium Alloy":40, "Planet Dust Collector":3, "Ion Rocket Engine":2}},
            10:{"Make":{"Cobalt Alloy":540}},
            11:{"Make":{"Advanced Antenna":2, "Cerythium Alloy":30, "Cosmium Alloy":10}},
            12:{"Make":{"Plasma Cannon":1, "Xenon Engine":1, "Galaxium Alloy":5}},
            13:{"Make":{"Infrared Homing Turret":1, "Refined Cerussite":150, "Mobile Telescope":5}},
            14:{"Make":{"Cobalt Alloy":600, "Kriptonite Alloy":2500}},
            15:{"Make":{"Gravity Reactor":1, "Coreium Alloy":500}},
            16:{"Make":{"Exospace Probe":1, "Cerythium Alloy":300, "Etherium Alloy":1200}},
            17:{"Make":{"Cosmium Alloy":250, "Space Protector X1000":1}},
            18:{"Make":{"Mythril Alloy":600, "Xenon Alloy":120, "Supercombustion Fuel":1}},
            19:{"Make":{"Planet Explorer":60, "Mini Rover":300, "Space Fleet Station":1}}}}
# ==========

item_names = tuple(item_names)
max_name_length = max(len(x) for x in item_names)
n_itm = len(item_names)
n_ref = item_names.index("Cables")

for x in ranks:
    for y in ranks[x]:
        if "Make" in ranks[x][y]:
            for z in ranks[x][y]["Make"]:
                assert z in item_names
        if "Have" in ranks[x][y]:
            for z in ranks[x][y]["Have"]:
                assert z in item_names
del x, y, z

def rates(R,C):
    res = np.copy(rb)
    res[:,:n_ref] *= R
    res[:,n_ref:] *= C
    return res

def vari_names(pmod):
    res = []
    for r in ranks[pmod]:
        split = False
        if "Make" in ranks[pmod][r] and "Have" in ranks[pmod][r]:
            for x in ranks[pmod][r]["Have"]:
                for y in ranks[pmod][r]["Make"]:
                    if rb[item_names.index(x), item_names.index(y)] < 0.0:
                        split = True
        if split:
            for i in item_names:
                res.append(("x",i,str(r)+"_H"))
            for i in item_names:
                res.append(("s",i,str(r)+"_H"))
            res.append(("t",str(r)+"_H"))
            for i in item_names:
                res.append(("x",i,str(r)+"_C"))
            for i in item_names:
                res.append(("s",i,str(r)+"_C"))
            res.append(("t",str(r)+"_C"))
        else:
            for i in item_names:
                res.append(("x",i,r))
            for i in item_names:
                res.append(("s",i,r))
            res.append(("t",r))
    assert len(res) % (2 * n_itm + 1) == 0
    return res

def solve(R,C,pmod):
    rt = rates(R,C)
    var_names = vari_names(pmod)
    n_rnk = len(var_names) // (2 * n_itm + 1)
    # build A_eq
    # item count consistency
    Ae = np.hstack((np.copy(rt), -np.eye(n_itm), np.zeros((n_itm,1))))
    for r in range(1,n_rnk):
        Ae = np.pad(Ae, ((0,n_itm),(0,2*n_itm+1)))
        Ae[-n_itm:,-(3*n_itm+2):-1] = np.hstack((np.eye(n_itm),np.zeros((n_itm,1)),np.copy(rt),-np.eye(n_itm)))
    be = np.zeros(n_rnk*n_itm)
    # build A_ub and b_ub
    # time consistency
    bu = np.zeros(2*n_rnk)
    for r in range(n_rnk):
        row1 = np.array([0,]*((2*n_itm+1)*r) + [1,]*n_ref + [0,]*(n_itm-n_ref+n_itm) + [-1,] + [0,]*((2*n_itm+1)*(n_rnk-r-1)))
        row2 = np.array([0,]*((2*n_itm+1)*r+n_ref) + [1,]*(n_itm-n_ref) + [0,]*n_itm + [-1,] + [0,]*((2*n_itm+1)*(n_rnk-r-1)))
        assert row1.shape[0] == len(var_names)
        assert row2.shape[0] == len(var_names)
        if r == 0:
            Au = np.vstack((row1,row2))
        else:
            Au = np.vstack((Au,row1,row2))
    # rank quest satisfaction
    for r in range(n_rnk):
        rank = var_names[(2*n_itm+1)*r][2]
        if type(rank) == str:
            # split case. can reach the "have" goal in _H and then consume the item to meet "make" goal in _C.
            if rank[-1] == "C":
                continue
            assert rank[-1] == "H"
            intrank = int(rank[:-2])
            for item in ranks[pmod][intrank]["Have"]:
                row = np.zeros((2*n_itm+1)*n_rnk)
                row[var_names.index(("s",item,rank))] = -1
                Au = np.vstack((Au,row))
                bu = np.append(bu, -ranks[pmod][intrank]["Have"][item])
            for item in ranks[pmod][intrank]["Make"]:
                row = np.zeros((2*n_itm+1)*n_rnk)
                i = item_names.index(item)
                row[var_names.index(("x",item,rank))] = -rt[i,i]
                row[var_names.index(("x",item,rank[:-1]+"C"))] = -rt[i,i]
                Au = np.vstack((Au,row))
                bu = np.append(bu, -ranks[pmod][intrank]["Make"][item])
        else:
            # normal case
            if "Have" in ranks[pmod][rank]:
                for item in ranks[pmod][rank]["Have"]:
                    row = np.zeros((2*n_itm+1)*n_rnk)
                    row[var_names.index(("s",item,rank))] = -1
                    Au = np.vstack((Au,row))
                    bu = np.append(bu, -ranks[pmod][rank]["Have"][item])
            if "Make" in ranks[pmod][rank]:
                for item in ranks[pmod][rank]["Make"]:
                    row = np.zeros((2*n_itm+1)*n_rnk)
                    i = item_names.index(item)
                    row[var_names.index(("x",item,rank))] = -rt[i,i]
                    Au = np.vstack((Au,row))
                    bu = np.append(bu, -ranks[pmod][rank]["Make"][item])
    # objective function
    c = np.array(([0,]*(2*n_itm)+[1,])*n_rnk)
    result = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be)
    obval = result.fun
    # of all the optimal production chains, we want one that maximizes idle time
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
    # of all those, try to complete earlier ranks earlier
    Ae = np.vstack((Ae,c))
    be = np.append(be, result.fun)
    c = []
    for x in var_names:
        if x[0] == "t":
            c.append(10/var_names.index(x))
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
    p = 1 + rank//20
    pmod = (p-1)%len(ranks)
    res_now = solve(Rs*speed(Rl)*1.25**2,Cs*speed(Cl)*1.25**2, pmod)
    if not slots_complete:
        res_rs = solve((Rs+1)*speed(Rl)*1.25**2,Cs*speed(Cl)*1.25**2,pmod).fun
        res_cs = solve(Rs*speed(Rl)*1.25**2,(Cs+1)*speed(Cl)*1.25**2,pmod).fun
    res_rl = sum(solve(Rs*speed(Rl+1)*1.25**2,Cs*speed(Cl)*1.25**2,m).fun for m in range(len(ranks)))
    res_cl = sum(solve(Rs*speed(Rl)*1.25**2,Cs*speed(Cl+1)*1.25**2,m).fun for m in range(len(ranks)))
    total_time = res_now.fun
    print("Plan for Planetary",p,"from rank",(p-1)*20+(p==1),"to",p*20)
    print("at\n",Rs,"Refinery slots, Refinery level",Rl,",\n",Cs,"Constructor slots, Constructor level",Cl)
    print()
    print("Total time required:",timestring(total_time*p))
    print()
    if not slots_complete:
        print("Improvement options information:")
        print("Time saved with next Refinery slot:",timestring((res_now.fun-res_rs)*p))
        print("Time saved with next Constructor slot:",timestring((res_now.fun-res_cs)*p))
    if res_rl <= res_cl:
        nextup = "Refinery"
    else:
        nextup = "Constructor"
    print("Recommended next speed level upgrade:", nextup)
    print()
    var_names = vari_names(pmod)
    def k(rank):
        if type(rank) == int:
            return rank
        else:
            a = int(rank[:-2])
            if rank[-1] == "C":
                a += 0.5
            return a
    rd = dict((x,[]) for x in sorted(list(set(y[-1] for y in var_names)), key=lambda x:k(x)))
    for i in range(len(var_names)):
        if res_now.x[i] > 10**(-8) or var_names[i][0] == "t":
            rd[var_names[i][-1]].append(var_names[i][:-1]+(res_now.x[i],))
    for rank in rd.keys():
        if type(rank) == int:
            print("="*8,"Rank",(p-1)*20+rank,"="*16)
        else:
            print("="*8,"Rank",(p-1)*20+int(rank[:-2]), rank[-2:], "="*14)
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
        res_r = sum(solve(Rslots*speed(rl+1)*1.25**2, Cslots*speed(cl)*1.25**2, m).fun for m in range(len(ranks)))
        res_c = sum(solve(Rslots*speed(rl)*1.25**2, Cslots*speed(cl+1)*1.25**2, m).fun for m in range(len(ranks)))
        if res_c < res_r:
            cl += 1
        else:
            rl += 1
        n -= 1
        print(rl,cl,speed(rl)*Rslots/(speed(cl)*Cslots), speed(rl)/speed(cl))

if __name__ == "__main__":
    if slots_complete:
        Rs = 10
        Cs = 9
    else:
        Rs = int(input("How many Refinery slots can be considered available? "))
    Rl = int(input("What's the current Speed Level of your Refinery? "))
    if not slots_complete:
        Cs = int(input("How many Constructor slots can be considered available? "))
    Cl = int(input("What's the current Speed Level of your Constructor? "))
    rank = int(input("What's your current Rank? "))
    print()
    main(Rs, Rl, Cs, Cl, rank)
    input()
