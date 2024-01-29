import random

def room_gen(min, max):
    room = []
    for i in range(1, max):
        room.append(random.randint(min, i+min-1))
    room = sorted(room)
    return room

def lvl_gen(x, y):
    lvl = []
    for i in range(1, y):
        list = []
        lvl.append(list)
        for j in range(1, x+i-1):
            ranlen = random.randint(0, j-1)
            list.append(room_gen(1+ranlen, j+2-ranlen))
    return lvl