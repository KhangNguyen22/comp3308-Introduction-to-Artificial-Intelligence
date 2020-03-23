import sys
import edgenode
import queue

limit = 1000

fringe = queue.Queue()
goal = None
# priority_fringe = 
forbidden = None
expanded = []
expanded_ids = []
solution = queue.LifoQueue()
opr = "sub"
# flag = 0

def show_expanded():
    expanded_string = ""
    if len(expanded) == 1:
        print(expanded[0].get_current_node_content())
    else:
        count = 0
        for item in expanded:
            if count == 0:
                expanded_string += item.get_current_node_content()
                count += 1
            else:
                expanded_string += "," + item.get_current_node_content()
        print(expanded_string)

def fail_output():
    print("No solution found.")
    show_expanded()
    sys.exit(0)

def bfs():
    global opr
    # global flag
    while not fringe.empty():
        current_node = fringe.get()
        if cycle(current_node):
            continue
        # print("expanded size: " + str(expanded.qsize()))

        if len(expanded) == limit:
            fail_output()
        # current_node.print_current_node()
        # Check if goal node
        if current_node.get_current_node_content() == goal:
            solution.put(current_node)
            expanded.append(current_node)
            traverse_back(current_node)
            # print("Solution FOUND!!! ")
            return
        
        if opr == "sub" and current_node.get_digit_space() != 0:
            produce_child(current_node,opr,0,True)
            opr = "add"
        
        if opr == "add" and current_node.get_digit_space() != 0:
            produce_child(current_node,opr,0,True)
            opr = "sub"

        if opr == "sub" and current_node.get_digit_space() != 1:
            produce_child(current_node,opr,1,True)
            opr = "add"

        if opr == "add" and current_node.get_digit_space() != 1:
            produce_child(current_node,opr,1,True)
            opr = "sub"
    
        if opr == "sub" and current_node.get_digit_space() != 2:
            produce_child(current_node,opr,2,True)
            opr = "add"

        if opr == "add" and current_node.get_digit_space() != 2:
            produce_child(current_node,opr,2,True)
            opr = "sub"
        expanded.append(current_node)


def dfs(cur_node, depth_limit):
    cur_opr = "sub"
    if cycle(cur_node):
        # print("elephant")
        return "elephant"
        # return None
    
    if len(expanded) == limit:
        fail_output()
    
    if cur_node.get_current_node_content() == goal:
        solution.put(cur_node)
        expanded.append(cur_node)
        traverse_back(cur_node)
        # print("Solution FOUND!!! ")
        return True
    
    expanded.append(cur_node)

    if cur_opr == "sub" and cur_node.get_digit_space() != 0:
        child = produce_child(cur_node, cur_opr,0, False)
        if child and depth_limit != 0 :
            answer = dfs(child, depth_limit -1)
            if answer:
                return True

        cur_opr = "add"
            
    if solution.qsize() > 0:
        return
    
    if cur_opr == "add" and cur_node.get_digit_space() != 0:
        child = produce_child(cur_node, cur_opr,0, False)
        if child and depth_limit != 0:
            answer = dfs(child, depth_limit - 1)
            if answer:
                return True
        cur_opr = "sub"

    if solution.qsize() > 0:
        return

    if cur_opr == "sub" and cur_node.get_digit_space() != 1:
        child = produce_child(cur_node, cur_opr,1, False)
        # print("1")
        # print(child)
        if child and depth_limit != 0:
            answer = dfs(child, depth_limit - 1)
            if answer:
                return True
        cur_opr = "add"
    
    if solution.qsize() > 0:
        return
    
    if cur_opr == "add" and cur_node.get_digit_space() != 1:
        child = produce_child(cur_node, cur_opr,1, False)
        # print(child.get_current_node_content())
        if child and depth_limit != 0:
            answer = dfs(child, depth_limit -1)
            if answer:
                return True
        cur_opr = "sub"

    if solution.qsize() > 0:
        return 

    if cur_opr == "sub" and cur_node.get_digit_space() != 2:
        child = produce_child(cur_node, cur_opr,2, False)
        if child and depth_limit != 0 :
            answer = dfs(child, depth_limit - 1)
            if answer:
                return True
        cur_opr = "add"
    
    if solution.qsize() > 0:
        return
    
    if cur_opr == "add" and cur_node.get_digit_space() != 2:
        child = produce_child(cur_node, cur_opr,2, False)
        if child and depth_limit != 0:
            answer = dfs(child, depth_limit - 1)
            if answer:
                return True

    if solution.qsize() > 0:
        return

def ids(cur_node):
    global expanded
    depth_limit = 0
    while True:
        result = dfs(cur_node, depth_limit)
        # print(result)
        if result:
            add_to_expanded_ids()
            break
        add_to_expanded_ids()
        expanded = []
        depth_limit += 1
    
    expanded = expanded_ids

def add_to_expanded_ids():
    for item in expanded:
        expanded_ids.append(item)

def greedy():
    print("greedy work")

def a_star():
    print("a_star work")

def hill_climbing():
    print("Hill climbing works")

def cycle(node):
    # print(node.get_current_node_content)
    for item in expanded:
        if item.get_current_node_content() == node.get_current_node_content() and item.get_digit_space() == node.get_digit_space() :
            return True
    return False

def produce_child(current_node, current_opr,current_flag, update_fringe):
    if current_node.generate_next_node(current_opr,current_flag):
        current_node.generate_next_node(current_opr,current_flag) 
        current_node.set_parent_of_child(current_node)
        # current_node.print_next_node()
        child = current_node.get_next_node()
        if check_forbidden(child):
            # print("Forbidden "+ child.get_current_node_content())
            return None
        
        if update_fringe:
            fringe.put(child)
        else:
            return child

def traverse_back(cur_node):
    while cur_node.get_parent():
        solution.put(cur_node.get_parent())
        cur_node = cur_node.get_parent()

def check_forbidden(node):
    if forbidden == None:
        return False
    else:
        for forbidden_node in forbidden:
            if node.get_current_node_content() == forbidden_node:
                return True
    return False

file = open(sys.argv[2],'r')
Lines = file.readlines()
clean = []

for line in Lines:
    line = line.rstrip("\n")
    clean.append(line)

if len(clean) == 2:
    fringe.put(edgenode.Edgenode(clean[0]))
    goal = clean[1]
elif len(clean) == 3:
    fringe.put(edgenode.Edgenode(clean[0]))
    goal = clean[1]
    forbidden = clean[2].split(",")

# print(fringe.queue)
# print(goal)
# print(forbidden)

if sys.argv[1] == 'B':
    bfs()
elif sys.argv[1] == 'D':
    dfs(fringe.get(), -1)
elif sys.argv[1] == 'I':
    ids(fringe.get()) 
elif sys.argv[1] == 'G':
    greedy() 
elif sys.argv[1] == 'A':
    a_star()
elif sys.argv[1] == 'H':
    hill_climbing() 

# print("Printing out your solution: ")
def print_out(type_queue):
    printable_solution = ""
    count = 0
    while not type_queue.empty():
        if count == 0:
            printable_solution += type_queue.get().get_current_node_content()
            count += 1
        else:
            printable_solution += ","+ type_queue.get().get_current_node_content()
    print(printable_solution)
print_out(solution)

# print(len(expanded))



show_expanded()