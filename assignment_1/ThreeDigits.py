import sys
import Edgenode
import queue

limit = 1000

fringe = queue.Queue()
goal = None
# priority_fringe = 
forbidden = None
expanded = []
solution = queue.LifoQueue()

def bfs():
    cur = fringe.get()
    if cur 


def dfs():
    print("dfs working")

def ids():
    print("ids working")

def greedy():
    print("greedy work")

def a_star():
    print("a_star work")

def hill_climbing():
    print("Hill climbing works")




file = open("sample.txt",'r')
Lines = file.readlines()
clean = []

for line in Lines:
    line = line.rstrip("\n")
    clean.append(line)

if len(clean) == 2:
    fringe.put(clean[0])
    goal = clean[1]
elif len(clean) == 3:
    fringe.put(clean[0])
    goal = clean[1]
    forbidden = clean[2].split(",")

print(fringe.queue)
print(goal)
print(forbidden)

if sys.argv[1] == 'B':
    bfs()
elif sys.argv[1] == 'D':
    dfs()
elif sys.argv[1] == 'I':
    ids() 
elif sys.argv[1] == 'G':
    greedy() 
elif sys.argv[1] == 'A':
    a_star()
elif sys.argv[1] == 'H':
    hill_climbing() 