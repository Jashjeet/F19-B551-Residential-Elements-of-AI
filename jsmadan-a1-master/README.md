# a1
<b>Submitted by Devansh Jain, Sanyam Rajpal, Jashjeet Singh Madan devajain, srajpal, jsmadan .</b>

## Part - I
This part had 3 parts. Original, Circular and Luddy.

### Part - 1 Original
The code was running for the original file as it is. We applied A* to improve its
efficiency.

### Part - 1 Circular
For the circular part, the number of possible moves from each node would be independent of
the location of the file because it can move circularly and we implemented it using the
modulo operation.

### Part - 1 Luddy
This was the most struggling part of all the 3 cases. We initially tried using a dictionary
and that gave us the right output but it took longer than the standard training time. Then we
tried using a priority queue. Since the priority queue is not traversable we tried to use 
2 separate fringes for the same. But that didn't perform as fast as expected. After repeated
attempts, we managed to get the correct output but not the most optimal in terms of time.

#### Parity Implementation
We used parity of a given situation to check whether the solution is possible for the
given state or not. If not, it doesn't need to go through the procedure of checking
each of its possible moves.

### Integrating into 1
After running all the 3 codes separately, we had to integrate the 3 files into 1.

## Part - II
This part had 4 parts. It optimizes segments, distance, time, Mileage per gallon. 
One major challenge was to extract and store all the road segments and city gps to a 
python list and at the same time handling all the cases of inconsistency in data. We also had to
 list the back and forth routes, for example, if a route is given from city A to B, we had to
make sure our algorithm includes the path from B to A as well. In this process, we also avoided
the loop of going from A to B and then again B to A. 

To maximize/minimize the cost function(s), we implemented this problem using the Priority Queue.
We created four different functions for each of the cost functions and called them according to the
command line input. 

Our successor function returned the set of all possible destinations from the current city. And then,
each of these cities was added to the fringe and checked for their optimality in the corresponding 
cost function.

### Optimizing Segments
We minimize the number of segments by choosing the route segment which minimizes the total
number of segments traversed. 

### Optimizing Distance
We optimize the distance by choosing the route segment which minimizes the total
distance traversed.

### Optimizing Time
We minimize the time by choosing the route segment which minimizes the total
travel time, given the car, travels at full speed throughout the journey.

### Optimizing Mileage Per Gallon( MPG )
We maximize the MPG by choosing the route segment which maximizes the Mileage. Since,
MPG is a function of velocity and average velocity is the total distance traveled
upon total time, which is used to maximize the MPG

## Part - III
In this part, we had to get the whole number contribution of people which maximizes the sum
of the skills and consumes no more than the cost stated.
Since the code that was written was adding fractional part we had to remove that line.
Besides, taking the code in any priority order such as the one with maximum skill per unit
cost may not work. Because, it can diminish the other high skill elements provided,
and restrict some other small elements to be added. So, checking all the possible combinations
with total cost less no more than the given cost and with no scope of adding any other
element to it with cost still remaining greater than or equal to the given cost.

The first challenge that we faced was to create an exhaustive set of all the possible combinations
of the people who were under the budget, and then we tried to maximize that set. On maximizing 
we anticipated that we would get the final output, which unfortunately that was not the case because of the 
set was too large to give the solution in optimal time.

Then we went on to add more rules to the above solution by ignoring the combinations which did not tend
to maximize the skillset provided the cost was completely exhausted. 
