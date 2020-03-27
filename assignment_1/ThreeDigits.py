import sys
import edgenode
import queue

limit = 1000

fringe = queue.Queue()
priority_fringe = []
root_int = None
goal = None
# priority_fringe = 
forbidden = None
expanded = []
expanded_ids = []
solution = queue.LifoQueue()
opr = "sub"

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

        if len(expanded) == limit or len(current_node.get_current_node_content()) != 3 or len(goal) !=3:
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


def dfs(cur_node, depth_limit= None):
    global expanded
    cur_opr = "sub"
    if cycle(cur_node):
        # print("elephant")
        return "found_cycle"
        # return None

    if len(expanded) == limit or len(cur_node.get_current_node_content()) != 3 or len(goal) !=3:
        fail_output()
    if len(expanded_ids) > limit:
        print("No solution found.")
        expanded = expanded_ids[:1000]
        show_expanded()
        sys.exit(0)

    if cur_node.get_current_node_content() == goal:
        solution.put(cur_node)
        expanded.append(cur_node)
        traverse_back(cur_node)
        # print("Solution FOUND!!! ")
        return True

    expanded.append(cur_node)

    if depth_limit == 0:
        return None

    if cur_opr == "sub" and cur_node.get_digit_space() != 0:
        child = produce_child(cur_node, cur_opr,0, False)
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)

        cur_opr = "add"

    if solution.qsize() > 0:
        return True

    if cur_opr == "add" and cur_node.get_digit_space() != 0:
        child = produce_child(cur_node, cur_opr,0, False)
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)
        cur_opr = "sub"

    if solution.qsize() > 0:
        return True

    if cur_opr == "sub" and cur_node.get_digit_space() != 1:
        child = produce_child(cur_node, cur_opr,1, False)
        # print("1")
        # print(child)
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)
        cur_opr = "add"

    if solution.qsize() > 0:
        return True

    if cur_opr == "add" and cur_node.get_digit_space() != 1:
        child = produce_child(cur_node, cur_opr,1, False)
        # print(child.get_current_node_content())
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)
        cur_opr = "sub"

    if solution.qsize() > 0:
        return True

    if cur_opr == "sub" and cur_node.get_digit_space() != 2:
        child = produce_child(cur_node, cur_opr,2, False)
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)
        cur_opr = "add"

    if solution.qsize() > 0:
        return True

    if cur_opr == "add" and cur_node.get_digit_space() != 2:
        child = produce_child(cur_node, cur_opr,2, False)
        if child and depth_limit is None :
            dfs(child)
        if child and depth_limit is not None:
            dfs(child, depth_limit-1)

    if solution.qsize() > 0:
        return True

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

def greedy(heuristic_node=None, is_a_star = False):
    opr = "sub"

    if cycle(heuristic_node[1]):
        return "found_cycle"

    if len(expanded) == limit or len(heuristic_node[1].get_current_node_content()) != 3 or len(goal) !=3:
        fail_output()

    if heuristic_node[1].get_current_node_content() == goal:
        solution.put(heuristic_node[1])
        expanded.append(heuristic_node[1])
        traverse_back(heuristic_node[1])
        return True

    if opr == "sub" and heuristic_node[1].get_digit_space() != 0:
        local_child = produce_child(heuristic_node[1],opr,0,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])
        opr = "add"

    if opr == "add" and heuristic_node[1].get_digit_space() != 0:
        local_child = produce_child(heuristic_node[1],opr,0,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])
            
        opr = "sub"

    if opr == "sub" and heuristic_node[1].get_digit_space() != 1:
        local_child = produce_child(heuristic_node[1],opr,1,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])
            
        opr = "add"

    if opr == "add" and heuristic_node[1].get_digit_space() != 1:
        local_child = produce_child(heuristic_node[1],opr,1,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])
            
        opr = "sub"

    if opr == "sub" and heuristic_node[1].get_digit_space() != 2:
        local_child = produce_child(heuristic_node[1],opr,2,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])
        opr = "add"

    if opr == "add" and heuristic_node[1].get_digit_space() != 2:
        local_child = produce_child(heuristic_node[1],opr,2,False)
        if local_child:
            local_heuristic_value = manhatten_heuristic(local_child)
            num_edges = 0
            if is_a_star:
                num_edges = path_cost(local_child)
            insert_priority_fringe([ num_edges + local_heuristic_value,local_child])

    expanded.append(heuristic_node[1])
    if len(priority_fringe) != 0:
        if is_a_star:
            greedy(priority_fringe.pop(0), True)
        else:
            greedy(priority_fringe.pop(0))


def hill_climbing():
    print("Hill climbing works")

def insert_priority_fringe(list_object):
    if len(priority_fringe) == 0:
        priority_fringe.append(list_object)
    else:
        for i in range(len(priority_fringe)):
            if priority_fringe[i][0] == list_object[0] or list_object[0] < priority_fringe[i][0]:
                priority_fringe.insert(i,list_object)
                return True
        priority_fringe.append(list_object)
        #Find the place to insert into priority fringe so we get an ordered fringed

def cycle(node):
    # print(node.get_current_node_content)
    for item in expanded:
        if item.get_current_node_content() == node.get_current_node_content() and item.get_digit_space() == node.get_digit_space() :
            return True
    return False

def manhatten_heuristic(cur_node):
    cur_node = cur_node.get_current_node_content()
    return abs(int(cur_node[0]) - int(goal[0])  ) + abs(int(cur_node[1]) -int(goal[1])) + abs(int(cur_node[2]) -int(goal[2]))

def produce_child(current_node, current_opr,current_flag, update_fringe):
    if current_node.generate_next_node(current_opr,current_flag):
        current_node.generate_next_node(current_opr,current_flag) 
        current_node.set_parent_of_child(current_node)
        child = current_node.get_next_node()
        if check_forbidden(child):
            # print("Forbidden "+ child.get_current_node_content())
            return None

        if update_fringe:
            fringe.put(child)
        else:
            return child

def path_cost(cur_node):
    count = 0
    while cur_node.get_parent():
        count += 1
        cur_node = cur_node.get_parent()
    return count

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
    dfs(fringe.get())
elif sys.argv[1] == 'I':
    ids(fringe.get())
elif sys.argv[1] == 'G' or sys.argv[1] == 'A' :
    g_node = fringe.get()
    root_int = int(g_node.get_current_node_content())
    temp_list = [None, g_node]
    if sys.argv[1] == 'G':
        greedy(temp_list)
    elif sys.argv[1] == 'A':
        greedy(temp_list, True)

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