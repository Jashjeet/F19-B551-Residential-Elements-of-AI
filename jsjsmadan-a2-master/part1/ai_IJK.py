#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: PLEASE ENTER YOUR NAMES AND USER ID'S HERE

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import random
import copy
import numpy as np

#def build_tree( board , empty_tiles , score , sum_average_diff , player  ) :

#def game_tree(  ):
    # called recursively
    

def heuristic_move( board , player ) :
    # heuristic_0 - minimize the number of filled tiles
    empty_tiles = 0
    max_tile = 'A'
    sum_average_diff = 0.0
    max_tile_upper = 'A'
    max_tile_lower = 'a'
    for i in range( len( board ) ) :
        for j in range( len( board[ 0 ] ) ) :
            if( board[ i ][ j ] == ' ' ):
                empty_tiles += 1
                continue
            sum_average_diff += ( abs(ord(board[ i ][ j ]) - ord(board[ max( i - 1 , 0 ) ][ j ] )) + abs(ord(board[ i ][ j ]) - ord(board[ min( i + 1 , len( board ) - 1 ) ][ j ] )) \
                                        + abs(ord(board[ i ][ j ]) - ord(board[ i ][ max( j - 1 , 0 ) ] )) \
                                        + abs(ord(board[ i ][ j ]) - ord(board[ i ][ min( j + 1 , len( board[ 0 ] ) - 1 ) ] ) )) / 4
            if( player == '+' ):
                if (board[i][j]).isupper() and (board[i][j]) > max_tile_upper :
                    max_tile_upper = board[i][j]
                    
            else:
                if (board[i][j]).islower() and (board[i][j]) > max_tile_lower :
                    max_tile_lower = board[i][j]

    if( player == '+' ):
        score = pow( 2 , ord(max_tile_upper) - ord('A') )
    else:
        score = pow( 2 , ord(max_tile_lower) - ord('a') )
    #game_tree( board , empty_tiles , score , sum_average_diff , player )
    return ( empty_tiles + ( score / 2 ) - sum_average_diff )
    # take score of opponent and square of it and subtract it.

def moves_run( board , game , player ) :
    
    tempU = copy.deepcopy(game)
    tempL = copy.deepcopy(game)
    tempD = copy.deepcopy(game)
    tempR = copy.deepcopy(game)
    
    #player_temp = game.getCurrentPlayer( )
    #deterministic = game.getDeterministic( )
    
    gameU = tempU.makeMove('U')    
    #print( gameU )     
    up_move = heuristic_move(gameU.getGame( ), player )
    
    gameL = tempL.makeMove('L')         
    left_move = heuristic_move(gameL.getGame( ), player )
    
    gameD = tempD.makeMove('D')         
    down_move = heuristic_move(gameD.getGame( ), player )
    
    gameR = tempR.makeMove('R')         
    right_move = heuristic_move(gameR.getGame( ), player )
    
    #min_max_U = copy.deepcopy(tempU)
    directions = [ 'U' , 'D' , 'L' , 'R' ]
    move = [ ]
    k = 0
    for i in directions :
        min_max = copy.deepcopy( tempU )
        min_max.makeMove( i )
        move.append( heuristic_move( min_max.getGame( ) , player ) )
        if( move[ k ] <= up_move ) :
            break
        k +=1
    move = np.array( move )
    up_move = max( move.min( ) , up_move )
    
    move = [ ]
    k = 0
    for i in directions :
        min_max = copy.deepcopy( tempR )
        min_max.makeMove( i )
        move.append( heuristic_move( min_max.getGame( ) , player ) )
        if( move[ k ] <= right_move ) :
            break
        k +=1
    move = np.array( move )
    right_move = max( move.min( ) , right_move )
    
    move = [ ]
    k = 0
    for i in directions :
        min_max = copy.deepcopy( tempD )
        min_max.makeMove( i )
        move.append( heuristic_move( min_max.getGame( ) , player ) )
        if( move[ k ] <= down_move ) :
            break
        k +=1
    move = np.array( move )
    down_move = max( move.min( ) , down_move )
    
    move = [ ]
    k = 0
    for i in directions :
        min_max = copy.deepcopy( tempL )
        min_max.makeMove( i )
        move.append( heuristic_move( min_max.getGame( ) , player ) )
        if( move[ k ] <= left_move ) :
            break
        k +=1
    move = np.array( move )
    left_move = max( move.min( ) , left_move )

    max_move = max( up_move , left_move , down_move , right_move )
    
    if max_move == up_move :
        return 'U'
    if max_move == down_move :
        return 'D'
    if max_move == left_move :
        return 'L'
    if max_move == right_move :
        return 'R'


def next_move(game: Game_IJK)-> None:

    
    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()
    print( "Player" , player )
    yield moves_run( board , game , player )
    
    #yield random.choice(['U', 'D', 'L', 'R'])
