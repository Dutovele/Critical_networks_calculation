from collections import defaultdict
from copy import deepcopy

num_nodes = 0
num_edges = 0
degrees = set()
Dvalues = []

class Stack:
  def __init__(self):
    self.storage = []
  def isEmpty(self):
    return len(self.storage) == 0
  def push(self, node):
    self.storage.append(node)
  def pop(self):
    return self.storage.pop()

class Graph:

    def __init__(self):
        self.num_nodes = num_nodes
        self.graph = defaultdict(list)
        self.keys = set()

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.keys.add(u)
        self.keys.add(v)

    def DFS(self):
        counter = 0
        # Mark the current node as visited and print it
        visited = [False] * g.num_nodes
        stack = Stack()
        stack.push(list(new_g.graph.keys())[0])
        visited[list(new_g.graph.keys())[0]] = True

        while (not stack.isEmpty()):
            node = stack.pop()
            nbrs = new_g.graph[node]
            # print("CURRENT NODE")
            # print("The DFS node", node, "The neighbours", nbrs)

            for n in nbrs:
                if not visited[n]:
                    stack.push(n)
                    visited[n] = True
        for v in visited:
            if v == True:
                counter += 1

        # print("The counter", counter)
        return counter


def create_graph(dir):
    global num_nodes
    global num_edges

    line_number = 0

    file = open(dir, 'r')
    for line in file:
        if line_number == 0:
            num_nodes, num_edges = line.split(" ")
            num_nodes = int(num_nodes)
            num_edges = int(num_edges)
            # print(num_nodes, num_edges)
            g.num_nodes = num_nodes

        else:
            templine = line.strip("\n")
            v1, v2 = templine.split()
            v1 = int(v1)
            v2 = int(v2)
            # print(v1,v2)
            g.addEdge(v1, v2)
            g.addEdge(v2, v1)

        line_number += 1
    file.close()


def reduce_graph(new_g, deg):

    removed = []
    for k, v in list(new_g.graph.items()):
        # print("CURRENT NODE ", k)
        if len(v) == deg:
            removed.append(k)
            new_g.graph.pop(k)
    # print(removed)

    for x in removed:
        for k,v in new_g.graph.items():
            # print(k, v)
            for i in v:
                if i == x: # This can be improved with binary search !!!
                    # print("removing ", i)
                    v.remove(i)
    return new_g


#The function will check if k is in the servers list
def search_for_k(sorted_list,k,low=None, high=None):

    if low is None:
        low = 0
    if high is None:
        high = len(sorted_list)-1

    if high < low:
        return False

    midpoint = (low+high) // 2

    if sorted_list[midpoint] == k:
        return True
    elif k < sorted_list[midpoint]:
        return search_for_k(sorted_list,k, low, midpoint-1)
    else:
        return search_for_k(sorted_list,k, midpoint+1, high)


def mergeSort(arr):
    if len(arr) > 1:
        left_arr = arr[:len(arr)//2]
        right_arr = arr[len(arr)//2:]

        #recurtion
        mergeSort(left_arr)
        mergeSort(right_arr)

        #merge step
        i = 0 # left array index
        j = 0 # right array index
        k = 0 # merged array idx
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i +=1
            k +=1
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j +=1
            k +=1
    return arr


# Iterate over the graph, sort the neibours in ascending order using MergeSort, and get min degree and max degree values
# Then for i in range(min_degree, max_degree+1): create a deep copy of the graph, delete all nodes with value i
# then call DFS on the new version of the graph and see if it is connected, if no, add the i value to a container of Dvalues

def modify_graph():
    global max_degree
    global min_degree
    # Iterate over the graph, sort the neibours in ascending order using MergeSort, and get min degree and max degree values
    for k,v in g.graph.items():
        degrees.add(len(v))
        v = mergeSort(v)

    # print("Initial graph degrees ", degrees)

def get_Dvalues():
    global degrees
    global Dvalues

    new_g = deepcopy(g)
    # print("The new g", new_g.graph)
    for d in degrees:
        reduce_graph(new_g,d)
    # print("new_g.graph", new_g.graph)
    # print("------------")
        # nodes = len(list(new_g.graph.keys()))
        # new_g.DFS()
    # for i in degrees:
    #     reduce_graph(new_g,i)



g = Graph()
create_graph('./pubdata_critical_networks/pub01.in')
# print(g.graph)
modify_graph()

for d in degrees:
    # print("----------")
    # print("NOW d is ", d)
    new_g = deepcopy(g)
    new_g = reduce_graph(new_g,d)
    nodes = len(list(new_g.graph.keys()))
    # print("Nodes", nodes)
    # print(new_g.graph)
    counter = new_g.DFS()
    if nodes != counter:
        Dvalues.append(d)

print(" +++++++++++++++++++++++++++ ")
print("Dvalues", Dvalues)
