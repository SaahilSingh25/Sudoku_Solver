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

def goal_test(board):
    fin = True
    for x in board:
        if len(x) != 1:
            fin = False
            break
    return fin
def get_most_const(board):
    smallest = N
    most_const = None
    ind = 0
    for x in board:
        if len(x) > 1:
            if len(x) < smallest:
                smallest = len(x)
                most_const = ind
        ind+=1
    return most_const

def find_solved_and_mod(board, solved):
    solved.clear()
    for x in range(N**2):
        if board[x] != "." and len(board[x]) == 1 and x not in solved:
            solved.append(x)
        else:
            board[x] = "".join(symbol_set)
    return (solved,board)
    
def forward_look(board, solved):
    for x in solved:
         for ind in neighbors[x]:
            # temp = len(board[ind])
            if board[x] in board[ind]:
                board[ind] = board[ind].replace(board[x], "")
                if len(board[ind]) == 1 and ind not in solved:
                    solved.append(ind)
                elif len(board[ind]) < 1:
                    return None
    return board

def conprop(board, solved):
    for row in range(N):
        visited = []
        count = []
        for col in range(N):
            cur_val = board[(row*N)+col]
            if len(cur_val) > 1:
                for char in cur_val:
                    visited.append(char) 
                    count.append(col)
        for char in symbol_set:
            if visited.count(char) == 1:
                temp = (row*N) + count[visited.index(char)]
                board[temp]=board[temp].replace(board[temp], char)
                solved.append(temp)
    return (board, solved)

def get_new_values(board, ind):
    return board[ind]

def backtracking_with_forward_and_conprop(state, solved):
    if goal_test(state):
        return state
    var = get_most_const(state)
    for val in get_new_values(state,var):
        new_state = state.copy()
        new_state[var] = val
        solved.clear()
        solved.append(var)
        checked = forward_look(new_state, solved)
        if checked is not None:
            while len(solved) >= 1 and checked is not None:
                solved.clear()
                temp = conprop(new_state, solved)
                new_state = temp[0]
                solved = temp[1]
                if len(solved) >= 1:
                    checked = forward_look(new_state, solved)
        if checked is not None:
            result = backtracking_with_forward_and_conprop(checked, solved)
            if result is not None:
                return result
    return None
                
with open(sys.argv[1]) as f:
    prev = 0
    for line in f:
        line=line.strip()
        board = line[0::]  
        new_board = list(board)
        solved = []
        presolved = []
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
        temp = find_solved_and_mod(new_board, presolved)
        new_board = temp[1]
        presolved = temp[0]
        temp = forward_look(new_board, presolved)
        soln = backtracking_with_forward_and_conprop(new_board, solved)
        display_board(soln)
        print("".join(soln))
