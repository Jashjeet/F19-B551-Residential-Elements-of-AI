# a0

Report. For each assignment, we’ll require a written report that summarizes your programming solutions
and that answers specific questions that we pose. Please put the report in the Readme.md file in your Github
repository. For each programming problem, your report should include 
	a brief overview of how your solution works, 
	including any problems you faced, 
	any assumptions, 
	simplifications, 
	or design decisions you made, 
	any parts of your solution that you feel are particualrly innovative, etc. 
These comments are your opportunity for us to better understand your code and the amount of work that you did in writing it; 
they are especially important if your code does not work as well as you would like, since it is a chance to document how much
energy and thought you put into your solution. 
For example, if you tried several different approaches before
finding one that worked, feel free to describe this process so that we can appreciate the work that you did
that might not otherwise be reflected in your final solution.

In other words, what is the set of valid states, the successor function, the cost function,
the goal state definition, and the initial state?
Why does the program often fail to find a solution? Implement a fix to make the code work better,
and explain what you did in the report.
The existing code is missing a number of the specifications given above. (For example, it doesn’t
display the path as a string of compass directions.) Complete the implementation, and explain what
you did in your report.

Find Luddy.py

The solution works using the Breadth First Search, which uses queue data structure. Initially, in the program it was using Depth First Search which made use of a stack. The problem with this implementaion is that it manages to get into a loop after inserting new nodes. Hence, it will take infinite time, since it will keep looping by popping the last element and then inserting new element which referenced the previously popped element. BFS always finds a solution, if there is one. Among many paths, it returns the shortest one, because it keeps finding the solution starting from the shortest.

Since it was the first assignment, and being new to python, it took a couple of days to understand the code itself. The searching techniques taught in the class, seemed easy in theory, but its implementation took some brainstorming.

The code has been simplified by introducing a new data structure, which stores the previously traversed points. This helped in removing the duplicacy of traversing the same point over and over again. In this way, one point was explored only once by checking if the point was already present in the traversed list, and subsequently not adding in the fringe.

Set of valid states: The coordinates in the map which have characters . or @

The successor function: It is the condition which is used to determine the next set of points which are retured when we pass the points of our points. These are basically the points on all the four directions of the point i.e. in the East, West, North, and South. If the point is on the edge or in the corner, there might not be all the four values returned. The following is its code.

def moves(map, row, col):
    moves=((row+1,col,'S'), (row-1,col,'N'), (row,col-1,'W'), (row,col+1,'E'))

    # Return only moves that are within the board and legal (i.e. on the sidewalk ".")
    return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]



The cost function: It is the maximum length to which our function can travel. If the solution does not exist for the particular problem, then the cost function is breadth times depth, which is rows times columns without any conditions.

The goal state definition: Luddy Hall, which is denoted by @

The initial state: Our position, which is represented by #


Hide.py
In this problem, the solution required implementation of Depth First Search. It could have been done through Breadth First Search also, but DFS gives result faster. Here, we need to find the maximum number of friends, which is denoted by F, that can be placed. It is more practical to traverse length wise to see the maximum that can be achieved. If our solution is found before that, it returns the solution and breaks.

This problem required handling and storing of multidimentional arrays or lists in the fringe and then expanding the state space. The state space here is the subsequent placement of friends(F) on the board.

Here also, I have added a datastructure which stores already created versions of the map. Hence, if a returned configuration of the map is already formed before, it is not pushed into the fringe.