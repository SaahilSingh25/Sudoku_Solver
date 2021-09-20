#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:27:29 2020

@author: Saahil
"""
import sys

N = 0
subblock_height = 0
subblock_width = 0
symbol_set = []
symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dictionary = {"row": [], "col": [] , "block": []}
neighbors = []

def display_board(line):
    s = ""
    count_w = 0
    count_h = 0
    for x in range(len(line)):
        if x != 0:
            if x % N == 0:
                s = s+"\n"
        s = s+str(line[x])+" "
        count_w += 1
        count_h += 1
        if count_w == subblock_width:
            s = s + " | "
            count_w = 0
        if count_h == subblock_height*N:
            s = s + "\n"
            for x in range(N):
                s = s + "---"
            count_h = 0
    print(s)

def makeDict(line):
    dictionary["row"].clear()
    dictionary["col"].clear()
    dictionary["block"].clear()
    neighbors.clear()
    for x in range(N):              
            symbol_set.append(symbols[x])
            dictionary["col"].append([])
            dictionary["block"].append([])
            dictionary["row"].append([])
    count_col = 0
    count_row = 0
    for x in range(len(line)):
        neighbors.append([])
        dictionary["row"][count_row].append(x)
        dictionary["col"][count_col].append(x)
        count_col+=1
        if count_col % N == 0:
            count_col = 0
            count_row +=1
    for row in range(subblock_width):
        for col in range(subblock_height):
            for block_row in range(subblock_height):
                for block_col in range(subblock_width):
                    val = block_col+(block_row*N)+(col*subblock_width)+(row*N*subblock_height)
                    dictionary["block"][col+(row*subblock_height)].append(val)
    # if N != 9:
    #     print(N)  
    for y in range(len(line)):
        for x in (dictionary["row"], dictionary["col"], dictionary["block"]):
            for z in range(N):
                if(y in x[z]):
                    for a in x[z]:
                        if a != y and a not in neighbors[y]:
                            neighbors[y].append(a)

def check_symbols(state):
    sym_tally = {}
    for x in symbol_set:
        sym_tally[x] = 0
    sym_tally["."] = 0
    for x in state:
        sym_tally[x] += 1
    for key, value in sym_tally.items(): 
        print(key + ": % d"%(value)) 
        
def backtracking(state):
    if state.find(".") == -1:
        return state
    var = get_next_var(state)
    for val in get_sorted_values(state,var):
        new_state = state
        new_state = new_state.replace(new_state[var],val,1)
        result = backtracking(new_state)
        if result is not None:
            return result
    return None
    
def get_next_var(state):
    return state.index(".")

def get_sorted_values(state,var):
    unav = []
    aval = []
    temp = neighbors[var]
    for x in temp:
        if state[x] not in unav:
            unav.append(state[x])
    for x in symbol_set:
        if x not in unav and x not in aval:
            aval.append(x)
    return aval
count = 0
with open(sys.argv[1]) as f:
    prev = 0
    for line in f:
        line=line.strip()
        board = line[0::]  
        total = len(line)
        N = int(total**(1/2))
        if int((N**(1/2))**2) == N:
            subblock_height = int(N**(1/2))
            subblock_width = int(N**(1/2))
        else:
            count = int(N**(1/2))
            while count < N:
                if count > N**(1/2) and N % count == 0:
                    subblock_width = count
                    count = 1
                    break
                count+=1
            greatest = 0
            count = 1
            while count < N**(1/2):
                if N % count == 0:
                    if count > greatest:
                        greatest = count
                        count+=1
                    else:
                        count+=1
            subblock_height=greatest
        if N != prev:
            symbol_set.clear()
            makeDict(line)
            prev = N
            for x in range(N):              
                symbol_set.append(symbols[x])
        soln = backtracking(line)
        print(soln)
        display_board(soln)
        print()