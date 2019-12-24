#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: devajain-srajpal-jsmadan
#
# Based on skeleton code by D. Crandall, September 2019
#

from queue import PriorityQueue
import sys


Goal=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

def parity(initial_board):
    zero_position=initial_board.index(0)
    row_of_zero=zero_position//4
    parity_count=0
    for i in initial_board:
        for j in initial_board[initial_board.index(i):]:
            if j<i and j!=0:
                parity_count+=1
    parity_even_odd=parity_count%2            
    if ((row_of_zero in (1,3) and parity_even_odd==0) or (row_of_zero in (0,2) and parity_even_odd==1)):
        return True
    else:
        return False

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors_original(state, MOVES):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]

def successors_circular(state, MOVES):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, (empty_row+i)%4, (empty_col+j)%4), c) \
             for (c, (i, j)) in MOVES.items() if valid_index((empty_row+i)%4, (empty_col+j)%4) ]
    
def successors_luddy(state, MOVES):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]
    
    
# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
# The solver! - using BFS right now
def solve_original(initial_board, MOVES):
    fringe=PriorityQueue()
    fringe.put( (0,initial_board, "",0) )
    temp=[initial_board]
    while not fringe.empty():
        (total_cost, state, route_so_far,moves_cost) = fringe.get()
        for (succ, move) in successors_original( state, MOVES ):
            if is_goal(succ):
                return( route_so_far + move )
            if succ not in temp:
                fringe.put((len(route_so_far)+1+sum(a != b for a,b in zip(Goal, succ)),succ, route_so_far + move , len(route_so_far)+1))
                temp.append(succ)
    return False



def solve_circular(initial_board, MOVES):
    fringe=PriorityQueue()
    fringe.put( (0,initial_board, "",0) )
    temp=[initial_board]
    while not fringe.empty():
        (total_cost, state, route_so_far,moves_cost) = fringe.get()
        for (succ, move) in successors_circular( state , MOVES):
            if is_goal(succ):
                return( route_so_far + move )
            if succ not in temp:
                fringe.put((len(route_so_far)+1+sum(a != b for a,b in zip(Goal, succ)),succ, route_so_far + move , len(route_so_far)+1)) 
                temp.append(succ)
    return False


def solve_luddy(initial_board, MOVES):
    fringe=PriorityQueue()
    fringe.put( (0,initial_board, "",0) )
    temp=[initial_board]
    while not fringe.empty():
        (total_cost, state, route_so_far,moves_cost) = fringe.get()
        for (succ, move) in successors_luddy( state, MOVES ):
            if is_goal(succ):
                return( route_so_far + move )
            if succ not in temp:
                fringe.put((sum(a != b for a,b in zip(Goal, succ)),succ, route_so_far + move , len(route_so_far)+1)) 
                temp.append(succ)
    return False

# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    check=parity(start_state)
    
    if check is True:

        print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

        if len(start_state) != 16:
            raise(Exception("Error: couldn't parse start state file"))

        if(sys.argv[2] == "original"):
            MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
            print("Solving...")
            route = solve_original(tuple(start_state), MOVES)

        elif(sys.argv[2] == "circular"):
            MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
            print("Solving...")
            route = solve_circular(tuple(start_state), MOVES)

        elif(sys.argv[2] == "luddy"):
            MOVES = { "A": (-2, -1), "B": (-2, 1), "C": (2, -1), "D": (2,1), "E": (-1,-2), "F": (-1,2), "G": (1,-2), "H": (1,2) }
            print("Solving...")
            route = solve_luddy(tuple(start_state), MOVES)
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
        
    else:
        print("Inf")

