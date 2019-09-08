import math
import time
global debug, infinite

class QueueingFn:
    def __init__(self):
        self.lista = []

    def insertRec(self, node, ini, end, astar = False):
        if ini >= end:
            self.lista.insert(ini, node)
        else:
            med = int((ini+end)/2)
            if astar:
                if node.projection() > self.lista[med].projection():
                    self.insertRec(node, med+1, end, astar)
                else:
                    self.insertRec(node, ini, med, astar)
            else:
                if node.node.heuristic > self.lista[med].node.heuristic:
                    self.insertRec(node, med+1, end, astar)
                else:
                    self.insertRec(node, ini, med, astar)

    def insert(self, node, astar = False):
        self.insertRec(node, 0, len(self.lista)-1, astar)

    def remove(self, node):
        self.lista.remove(node)

class Node:
    def __init__(self, item):
        self.id = item[0] - 1
        self.name = item[1]
        self.x = item[2]
        self.y = item[3]
        self.initialNode = False
        self.finalNode = False
        self.children = [(-1,-1),(-1,-1),(-1,-1)]
        self.heuristic = -1

    def distance(self, n):
        dx = self.x - n.x
        dy = self.y - n.y
        return math.sqrt(dx*dx + dy*dy)


class Graph:
    def __init__(self, items, ini, end):
        self.items = items
        self.initialNode = ini
        self.endNode = end
        def getid(val):
            return val[0]

        self.items.sort(key = getid)
        self.adj = [[(-1,-1), (-1,-1), (-1,-1)] for j in range(len(items))]
        self.adj = []
        for i in range(len(self.items)):
            node = Node(self.items[i])
            if i == self.initialNode:
                node.initialNode = True
            if i == self.endNode:
                node.finalNode = True
            self.adj.append(node)

        for i in range(0, len(self.items)):
            node = self.adj[i]
            node.heuristic = node.distance(self.adj[self.endNode])
            if i % 2 == 1:
                if i > 0:
                    j = i - 1
                    d = node.distance(self.adj[j])
                    self.adj[i].children[0] = (j, d*1.1)
                    self.adj[j].children[2] = (i, d*1.1)
                    print(str(i) + ", " + str(j) + ": " + str(d*1.1))
                if i < len(self.items) - 2:
                    j = i + 2
                    d = node.distance(self.adj[j])
                    self.adj[i].children[2] = (j, d*1.1)
                    self.adj[j].children[1] = (i, d*1.1)
                    print(str(i) + ", " + str(j) + ": " + str(d*1.1))
            elif i % 2 == 0:
                if 1 < i:
                    j = i - 2
                    d = node.distance(self.adj[j])
                    self.adj[i].children[0] = (j, d*1.1)
                    self.adj[j].children[1] = (i, d*1.1)
                    print(str(i) + ", " + str(j) + ": " + str(d*1.1))
                if i < len(self.items) - 1:
                    j = i + 1
                    d = node.distance(self.adj[j])
                    self.adj[i].children[2] = (j, d*1.1)
                    self.adj[j].children[0] = (i, d*1.1)
                    print(str(i) + ", " + str(j) + ": " + str(d*1.1))

        self.printMatrix(debug)

    def printMatrix(self, f):
        for i in range(len(self.adj[0].children) + 1):
            f.write("|%13d" % (i))
        f.write("| h(n) |\n")
        for i in range(len(self.adj)):
            if i == self.initialNode:
                f.write("|*%12d" % i)
            elif i == self.endNode:
                f.write("|**%11d" % i)
            else:
                f.write("|%13d" % i)
            for j in range(len(self.adj[0].children)):
                f.write("|(%3d, %06.03f)" % (self.adj[i].children[j][0],self.adj[i].children[j][1]))
            f.write("|%06.03f|\n" % self.adj[i].heuristic)
        f.write("\n")


class TreeNode:
    def __init__(self, node, father, height):
        self.node = node
        self.father = father
        self.cost = 0
        self.height = height
        self.expanded = False

    def projection(self):
        return self.cost + self.node.heuristic


class SearchTree:
    def __init__(self, graph):
        self.tree = []
        self.graph = graph
        self.tree.append([TreeNode(self.graph.adj[self.graph.initialNode], None, 1)])
        self.height = 1

    def PrintTree(self, f, astar = False):
        for i in range(len(self.tree)):
            f.write("|%3d" % i)
            for j in range(len(self.tree[i])):
                if astar:
                    if self.tree[i][j].expanded:
                        if self.tree[i][j].father is None:
                            f.write("|(*%3d, %06.03f,  -1)" % (self.tree[i][j].node.id, self.tree[i][j].projection()))
                        else:
                            f.write("|(*%3d, %06.03f, %3d)" % (
                                self.tree[i][j].node.id, self.tree[i][j].projection(), self.tree[i][j].father.node.id))
                    else:
                        if self.tree[i][j].father is None:
                            f.write("|(%4d, %06.03f,  -1)" % (self.tree[i][j].node.id, self.tree[i][j].projection()))
                        else:
                            f.write("|(%4d, %06.03f, %3d)" % (
                                self.tree[i][j].node.id, self.tree[i][j].projection(), self.tree[i][j].father.node.id))
                else:
                    if self.tree[i][j].expanded:
                        if self.tree[i][j].father is None:
                            f.write("|(*%3d, %06.03f,  -1)" % (self.tree[i][j].node.id, self.tree[i][j].node.heuristic))
                        else:
                            f.write("|(*%3d, %06.03f, %3d)" % (
                                self.tree[i][j].node.id, self.tree[i][j].node.heuristic, self.tree[i][j].father.node.id))
                    else:
                        if self.tree[i][j].father is None:
                            f.write("|(%4d, %06.03f,  -1)" % (self.tree[i][j].node.id, self.tree[i][j].node.heuristic))
                        else:
                            f.write("|(%4d, %06.03f, %3d)" % (
                                self.tree[i][j].node.id, self.tree[i][j].node.heuristic, self.tree[i][j].father.node.id))
            f.write("|\n")
        f.write("\n")


def GreedySearch(graph):
    #initialize the search tree
    tree = SearchTree(graph)
    tree.PrintTree(debug)
    path = []
    tries = 0
    # add the root in the candidate list
    candidates = QueueingFn()
    candidates.insert(tree.tree[0][0])
    expanded = []
    while tries < 10000:
        tries += 1
        # if no candidates to expand return failure
        if len(candidates.lista) == 0:
            return -1

        # choose the best leaf node for expansion
        cmin = candidates.lista[0]
        candidates.remove(cmin)
        if len(path) == 0:
            d = 0
        else:
            for ci in cmin.father.node.children:
                if ci[0] == cmin.node.id:
                    d = ci[1]
        path.append((cmin.father, d, cmin))
        cmin.expanded = True
        expanded.append(cmin.node.id)
        # check the node for the goal state
        # if its the goal, return the solution
        if cmin.node.finalNode:
            tree.PrintTree(debug)
            return path
        # else expand leaf and append to the tree
        for child in cmin.node.children:
            if child[0] != -1 and (cmin.father is None or child[0] != cmin.father.node.id) and child[0] not in expanded:
                if len(tree.tree) <= cmin.height:
                    tree.tree.append([])
                childnode = TreeNode(graph.adj[child[0]], cmin, cmin.height+1)
                tree.tree[cmin.height].append(childnode)
                candidates.insert(node = childnode)
        tree.PrintTree(debug)
    return path


def AStarSearch(graph):
    #initialize the search tree
    tree = SearchTree(graph)
    tree.PrintTree(debug)
    path = []
    tries = 0
    candidates = QueueingFn()
    candidates.insert(tree.tree[0][0], True)
    expanded = []
    while tries < 10000:
        tries += 1
        # search for candidates to expand
        # if no candidates to expand return failure
        if len(candidates.lista) == 0:
            return -1

        # choose the best leaf node for expansion
        cmin = candidates.lista[0]
        candidates.remove(cmin)
        if len(path) == 0:
            d = 0
        else:
            for ci in cmin.father.node.children:
                if ci[0] == cmin.node.id:
                    d = ci[1]
        path.append((cmin.father, d, cmin))
        cmin.expanded = True
        expanded.append(cmin.node.id)
        # check the node for the goal state
        # if its the goal, return the solution
        if cmin.node.finalNode:
            tree.PrintTree(debug, astar=True)
            return path
        # else expand leaf and append to the tree
        for child in cmin.node.children:
            if child[0] != -1 and (cmin.father is None or child[0] != cmin.father.node.id) and child[0] not in expanded:
                if len(tree.tree) <= cmin.height:
                    tree.tree.append([])
                childnode = TreeNode(graph.adj[child[0]], cmin, cmin.height+1)
                childnode.cost = cmin.cost + child[1]
                tree.tree[cmin.height].append(childnode)
                candidates.insert(childnode, True)
        tree.PrintTree(debug, astar=True)
    return path

def TrimPath(path):
    line = path[-1]
    node = line[2]
    newpath = [line]
    while not node.node.initialNode:
        for p in range(0, path.index(line) + 1):
            if path[p][0] == node.father and path[p][2] == node:
                newline = path[p]
        if newline not in newpath:
            newpath.insert(0,newline)
        line = newline
        node = node.father
    return newpath

if __name__ == '__main__':
    infinite = 10000
    aus = open("australia.txt", "r")
    debug = open("debugG1.txt", "w")
    cts = aus.readlines()
    items = []
    ini = -1
    end = -1
    for ct in cts:
        if ct != cts[0]:
            items.append((int(ct.split(",")[0]), ct.split(",")[1], float(ct.split(",")[2]), float(ct.split(",")[3])))
            print(ct)
            if(ct.split(",")[1] == "Alice Springs"):
                ini = int(ct.split(",")[0]) - 1
                print("ini = " + str(ini))
            if(ct.split(",")[1] == "Yulara"):
                end = int(ct.split(",")[0]) -1
                print("end = " + str(end))
    graph = Graph(items, ini, end)
    print("Starting greedy search...")
    st = time.time()
    ret = GreedySearch(graph)
    delay = time.time() - st
    print("Ended greedy search!")
    if ret == -1:
        print("No path found!")
    else:
        print("Path found:")
        path = TrimPath(ret)
        pathlen = 0
        for p in path:
            pathlen += p[1]
            if p[0] is None:
                print("%s, summing to %f" % (graph.items[p[2].node.id][1], pathlen))
            else:
                print("from %s, for %f, to %s, summing to %f" % (graph.items[p[0].node.id][1], p[1], graph.items[p[2].node.id][1], pathlen))
                debug.write("%30s; %6.3f; %30s; %6.3f\n" % (graph.items[p[0].node.id][1], p[1], graph.items[p[2].node.id][1], pathlen))
    print("Delay = %.3f s" % delay)
    print("Starting A* search...")
    debug = open("debugA1.txt", "w")
    graph.printMatrix(debug)
    st = time.time()
    ret = AStarSearch(graph)
    delay = time.time() - st
    print("Ended A* search!")
    if ret == -1:
        print("No path found!")
    else:
        print("Path found:")
        path = TrimPath(ret)
        pathlen = 0
        for p in path:
            pathlen += p[1]
            if p[0] is None:
                print("%s, summing to %f" % (graph.items[p[2].node.id][1], pathlen))
            else:
                print("from %s, for %f, to %s, summing to %f" % (graph.items[p[0].node.id][1], p[1], graph.items[p[2].node.id][1], pathlen))
                debug.write("%30s; %6.3f; %30s; %6.3f\n" % (graph.items[p[0].node.id][1], p[1], graph.items[p[2].node.id][1], pathlen))
    print("Delay = %.3f s" % delay)
