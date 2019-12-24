#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.
#

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().split("\n")]

# Count total # of friends on board
def count_friends(board):
    return sum([ row.count('F') for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    flag1=1
    for i in range(row-1,-1,-1):
        if(board[i][col] in 'F'):
            flag1=0
            break
        elif (board[i][col] in "&@"):
            break
        
    flag2=1
    for i in range(col-1,-1,-1):
        if(board[row][i] in 'F'):
            flag2=0
            break
        elif (board[row][i] in "&@"):
            break
        
    flag3=1
    for i in range(row,len(board)):
        if(board[i][col] in 'F'):
            flag3=0
            break
        elif (board[i][col] in "&@"):
            break
        
    flag4=1
    for i in range(col,len(board[0])):
        if(board[row][i] in 'F'):
            flag4=0
            break
        elif (board[row][i] in "&@"):
            break
        
    if (flag1==1 and flag2==1 and flag3==1 and flag4==1):
#        print('add_friend')
        return board[0:row] + [board[row][0:col] + ['F',] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
#    print('successor')
    return [ add_friend(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' ]

# check if board is a goal state
def is_goal(board):
    return count_friends(board) == K 

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    already_created=[initial_board]
#    print(already_created)
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if s is not None:
                if is_goal(s):
                    return(s)
                if s not in already_created:
                    fringe.append(s)
                    already_created.append(s)
    return False

# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1])

    # This is K, the number of friends
    K = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(IUB_map) + "\n\nLooking for solution...\n")
    solution = solve(IUB_map)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")


