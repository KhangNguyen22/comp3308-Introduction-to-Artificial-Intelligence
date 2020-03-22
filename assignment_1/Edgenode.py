#!/usr/bin/env python3

class Edgenode:
    def __init__(self,current_number, wg=None,mother=None):
        self.parent_node = mother
        self.content = current_number
        self.edge_weight = wg
        self.next_node = None

    def edit_number(self,num, opr, index):
        if opr == "add":
            char = self.find_next_number(num[index])
        else:
            char = self.find_prev_number(num[index])
        
        result = num[:index]+ char + num[index+1:]
        # print(result)
        return result
    
    def find_next_number(self, character):
        if character == "0":
            return "1"
        elif character == "1":
            return "2"
        elif character == "2":
            return "3"
        elif character == "4":
            return "5"
        elif character == "5":
            return "6"
        elif character == "6":
            return "7"
        elif character == "7":
            return "8"
        elif character == "8":
            return "9"
        elif character == "9":
            return "ERROR"

    def find_prev_number(self, character):
        if character == "9":
            return "8"
        elif character == "8":
            return "7"
        elif character == "7":
            return "6"
        elif character == "6":
            return "5"
        elif character == "5":
            return "4"
        elif character == "4":
            return "3"
        elif character == "3":
            return "2"
        elif character == "2":
            return "1"
        elif character == "1":
            return "0"
        elif character == "0":
            return "ERROR" 


    def generate_next_node(self,operator,digit, weight=None):
            my_string = self.edit_number(self.content, operator,digit)
            if len(my_string) != 3:
                print("error. get me out of here")
                return
            
            self.next_node = Edgenode(my_string, weight)
        # pass

    def print_current_node(self):
        print(self.content)

    def print_next_node(self):
        print(self.next_node.content)
    
    def set_parent_of_child(self, obj):
        self.next_node.parent_node = obj

    def get_next_node(self):
        return self.next_node
    def get_parent_of_child(self):
        return self.next_node.parent_node.content
    
    


# foo = Edgenode("001")
# foo.generate_next_node("sub",2)
# foo.set_parent_of_child(foo)
# foo.print_current_node()
# print(foo.get_next_node())

# After you generate next node, remember to set the parent node, then chuck child into fringe!! 