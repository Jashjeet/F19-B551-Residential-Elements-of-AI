#!/usr/local/bin/python3

# put your routing program here!

import sys
import math
from math import radians
import heapq

cities_gps = [ ]
road_segments = [ ]

with open( "city-gps.txt" , "r" ) as file :
    for line in file :
        l = line.split( )
        cities_gps.append( [ l[ 0 ] , float( l[ 1 ] ) , float( l[ 2 ] ) ] )

with open( "road-segments.txt" , "r" ) as file :
    for line in file :
        l = line.split( )
        road_segments.append( [ l[ 0 ] , l[ 1 ] , int( l[ 2 ] ) , float( l[ 3 ] ) , l[ 4 ] ] )
        road_segments.append( [ l[ 1 ] , l[ 0 ] , int( l[ 2 ] ) , float( l[ 3 ] ) , l[ 4 ] ] )
        
     
        
def dist_bw_cities( start_city , end_city ) :

    start_city_gps = [ city for city in cities_gps if city[ 0 ] == start_city ]
    end_city_gps = [ city for city in cities_gps if city[ 0 ] == end_city ]

#    print( "GPS" , start_city_gps )

    start_lat = float( start_city_gps[ 0 ][ 1 ] )
    end_lat = float( end_city_gps[ 0 ][ 1 ] )

    start_long = float( start_city_gps[ 0 ][ 2 ] )
    end_long = float( end_city_gps[ 0 ][ 2 ] )
#    
#    print(start_lat, start_long)
#    print(end_lat, end_long)

    distance = get_distance( radians(start_lat) ,radians(start_long) , radians(end_lat) , radians(end_long) )
    
    return (distance)


def get_distance( start_lat , start_long , end_lat , end_long ) :

    d_lat = end_lat - start_lat
    d_lng = end_long - start_long

    distance = (
         math.sin(d_lat / 2) ** 2
       + math.cos(start_lat)
       * math.cos(end_lat)
       * math.sin(d_lng / 2) ** 2
    )

    return( 3958.134 * ( 2 * math.atan2( math.sqrt( distance ) , math.sqrt( 1 - distance ) ) ) )    
        

def is_goal( succ , end_city ) :
    if ( succ == end_city ):
        return True
    
    
def successors( state , visited_cities ) :
    return  [ next_city[1:] for next_city in road_segments if ( next_city[0] == state ) and ( next_city[ 1 ] not in visited_cities ) ]

def cost_function( constraint, start_city, end_city ) :
    if( constraint == 'distance' ) :
        optimum_distance( start_city , end_city)
    elif( constraint == 'segments' ) :
        optimum_segments( start_city , end_city)
    elif( constraint == 'time' ) :
        optimum_time( start_city , end_city)
    elif( constraint == 'mpg' ) :
        optimum_mpg( start_city , end_city)        
        
        
def optimum_distance( start_city , end_city) :
   
    your_loc=start_city
    distance=0    
    segments=0
    time=0
    visited_cities= [ ]
    mpg=0
    fringe=[(distance, your_loc, your_loc, segments, time, mpg)]
    
    heapq.heapify(fringe)
    

    while len( fringe ) > 0 :
        (curr_dist, curr_move, route, segments, time, mpg)=heapq.heappop(fringe)
        for next_cities in successors(curr_move , visited_cities) :    
            visited_cities.append( next_cities[ 0 ] )    
            if (next_cities[0])==end_city:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))        
                mpg= (8/3)*velocity*((1-(velocity/150))**4)        
                gallons=(curr_dist+next_cities[1])/mpg
                print(segments+1 , curr_dist+next_cities[1], time+(next_cities[1]/next_cities[2]), gallons, route+ " " +next_cities[0]  )        
                return (curr_dist+next_cities[1], route+ " " +next_cities[0], segments+1, time+(next_cities[1]/next_cities[2]), mpg)    
            else:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))         
                mpg= ((8/3)*velocity*((1-(velocity/150))**4))         
                heapq.heappush( fringe, [curr_dist + next_cities[1], next_cities[0], route+ " " +next_cities[0] , segments+1 , time+(next_cities[1]/next_cities[2]), mpg])                

    return False

def optimum_segments( start_city , end_city) :
   
    your_loc=start_city
    distance=0    
    segments=0
    time=0
    visited_cities= [ ]
    mpg=0
    fringe=[(segments, your_loc, your_loc, distance, time, mpg)]
    
    heapq.heapify(fringe)
    

    while len( fringe ) > 0 :
        (segments, curr_move, route, curr_dist, time, mpg)=heapq.heappop(fringe)
        for next_cities in successors(curr_move , visited_cities) :    
            visited_cities.append( next_cities[ 0 ] )    
            if (next_cities[0])==end_city:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))        
                mpg= (8/3)*velocity*((1-(velocity/150))**4)   
                gallons=(curr_dist+next_cities[1])/mpg
                print(segments+1 , curr_dist+next_cities[1], time+(next_cities[1]/next_cities[2]), gallons, route+ " " +next_cities[0]  )        
                return (segments+1, route+ " " +next_cities[0], curr_dist+next_cities[1] , time+(next_cities[1]/next_cities[2]), mpg)    
            else:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))         
                mpg= ((8/3)*velocity*((1-(velocity/150))**4))         
                heapq.heappush( fringe, [segments+1 , next_cities[0], route+ " " +next_cities[0] , curr_dist + next_cities[1], time+(next_cities[1]/next_cities[2]), mpg])                

    return False

def optimum_time( start_city , end_city) :
   
    your_loc=start_city
    distance=0    
    segments=0
    time=0
    visited_cities= [ ]
    mpg=0
    fringe=[(time, your_loc, your_loc, distance, segments, mpg)]
    
    heapq.heapify(fringe)
    

    while len( fringe ) > 0 :
        (time, curr_move, route, curr_dist, segments, mpg)=heapq.heappop(fringe)
        for next_cities in successors(curr_move , visited_cities) :    
            visited_cities.append( next_cities[ 0 ] )    
            if (next_cities[0])==end_city:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))        
                mpg= (8/3)*velocity*((1-(velocity/150))**4)    
                gallons=(curr_dist+next_cities[1])/mpg
                print(segments+1 , curr_dist+next_cities[1], time+(next_cities[1]/next_cities[2]), gallons, route+ " " +next_cities[0]  )        
                return (time+(next_cities[1]/next_cities[2]), route+ " " +next_cities[0], curr_dist+next_cities[1] , segments+1, mpg)    
            else:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))         
                mpg= ((8/3)*velocity*((1-(velocity/150))**4))         
                heapq.heappush( fringe, [time+(next_cities[1]/next_cities[2]), next_cities[0], route+ " " +next_cities[0] , curr_dist + next_cities[1], segments+1 , mpg])                

    return False


def optimum_mpg( start_city , end_city) :
   
    your_loc=start_city
    distance=0    
    segments=0
    time=0
    visited_cities= [ ]
    mpg=0
    fringe=[(mpg, your_loc, your_loc, segments, time, distance)]
    
    heapq._heapify_max(fringe)
    

    while len( fringe ) > 0 :
        (mpg, curr_move, route, segments, time, curr_dist)=heapq._heappop_max(fringe)
        for next_cities in successors(curr_move , visited_cities) :    
            visited_cities.append( next_cities[ 0 ] )    
            if (next_cities[0])==end_city:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))        
                mpg= (8/3)*velocity*((1-(velocity/150))**4)   
                gallons=(curr_dist+next_cities[1])/mpg
                print(segments+1 , curr_dist+next_cities[1], time+(next_cities[1]/next_cities[2]), gallons, route+ " " +next_cities[0]  )        
                return (mpg, route+ " " +next_cities[0], segments+1, time+(next_cities[1]/next_cities[2]), curr_dist+next_cities[1])    
            else:        
                velocity= (curr_dist+next_cities[1])/(time+(next_cities[1]/next_cities[2]))         
                mpg= ((8/3)*velocity*((1-(velocity/150))**4))         
                heapq.heappush( fringe, [mpg, next_cities[0], route+ " " +next_cities[0] , segments+1 , time+(next_cities[1]/next_cities[2]), curr_dist + next_cities[1]])                

    return False


if __name__ =="__main__":

    if( len( sys.argv ) != 4 ) :
        raise Exception( 'Error: expected 3 command line arguments' )

    start_city = str( sys.argv[1])
    end_city = str( sys.argv[2]) 
    constraint = str( sys.argv[3])
    
    dist_bw_cities(start_city, end_city)
    
    if (start_city ==city_set[0] for city_set in road_segments):
        cost_function(  constraint.lower( ) , start_city , end_city)
    else:
        print("Inf")
