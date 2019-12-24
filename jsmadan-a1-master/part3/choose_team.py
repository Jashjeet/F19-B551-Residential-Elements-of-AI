#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: Devansh Jain devajain- Sanyam Rajpal srajpal- Jashjeet Madan jsmadan
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
import random
def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ]
    return people

def approx_solve( people , budget ) :
    people_list= [[v[0],v[1],k, v] for k, v in people.items()]
    temp=[]
    solution=[]
    for i in people_list:
        if i[3][1]<=budget:
            temp.append(i[0:3])
            for j in solution:
                if i[3][1]+j[1]<=budget:
                    new_cost=i[3][1]+j[1]
                    new_skills=i[3][0]+j[0]
                    temp.append([new_skills,new_cost,i[2]+ " "+j[2]])
        for k in temp:
            solution.append(k)
        temp.clear()
    max_skills=0
    for l in range(len(solution)):
        if solution[l][0]>max_skills:
            max_skills=solution[l][0]
            sol=solution[l]
    return sol

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')
    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution = approx_solve(people, budget)
    skill=solution[0]
    people=solution[2].split()
    if solution is not None:
        print (f"Found a group with {len(people)} people costing {solution[1]} with total skill {skill} ")
        for s in people:
            print(s, "1.0000")
    else:
        print("Inf")

