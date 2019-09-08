import time
import random
global debug, infinite, dim, goal, directions, fat, timeChecking, timeExpanding, timeInserting, nodesExp

class QueueingFn:
    def __init__(self):
        self.lista = []

    def insertRec(self, node, ini, end, astar = False):
        if ini >= end:
            self.lista.insert(ini, node)
        else:
            med = int((ini+end)/2)
            if astar:
                if node.projection > self.lista[med].projection:
                    self.insertRec(node, med+1, end, astar)
                else:
                    self.insertRec(node, ini, med, astar)
            else:
                if node.heuristic > self.lista[med].heuristic:
                    self.insertRec(node, med+1, end, astar)
                else:
                    self.insertRec(node, ini, med, astar)

    def insert(self, node, astar = False):
        self.insertRec(node, 0, len(self.lista)-1, astar)

    def remove(self, node):
        self.lista.remove(node)


def printMatrix(m):
    for i in range(len(m)):
        # f.write("|%3d" % i)
        for j in range(len(m[i])):
            print("|%3d" % m[i][j], end="")
        print("|")
    print("")


def printNode(n, f):
    #for i in range(len(n.state[0]) + 1):
        #f.write("|%3d" % (i))
    for i in range(len(n.state)):
        #f.write("|%3d" % i)
        for j in range(len(n.state[i])):
            f.write("|%3d" % n.state[i][j])
        f.write("|\n")
    f.write("heuristic = %d\n" % n.heuristic)
    f.write("projection = %d\n" % n.projection)
    f.write("\n")


def GoalState():
    ret = [[-1 for j in range(dim)] for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            ret[i][j] = dim*i + j + 1
    ret[-1][-1] = 0
    return ret


def FindBlank(state):
    blank = (-1, -1)
    for i in range(dim):
        for j in range(dim):
            if state[i][j] == 0:
                blank = (i, j)
    return blank

def MoveBlank(state, movement):
    blank = FindBlank(state)
    # Blank going up
    if blank[0] > 0 and movement == "N":
        state[blank[0]][blank[1]] = state[blank[0] - 1][blank[1]]
        state[blank[0] - 1][blank[1]] = 0
    # Blank going right
    elif blank[1] < dim - 1 and movement == "E":
        state[blank[0]][blank[1]] = state[blank[0]][blank[1] + 1]
        state[blank[0]][blank[1] + 1] = 0
    # Blank going down
    elif blank[0] < dim - 1 and movement == "S":
        state[blank[0]][blank[1]] = state[blank[0] + 1][blank[1]]
        state[blank[0] + 1][blank[1]] = 0
    # Blank going left
    elif blank[1] > 0 and movement == "W":
        state[blank[0]][blank[1]] = state[blank[0]][blank[1] - 1]
        state[blank[0]][blank[1] - 1] = 0
    return state


class TreeNode:
    def __init__(self, state, father, move, height):
        self.state = state
        self.blank = FindBlank(state)
        self.father = father
        self.fatherMove = move
        self.height = height
        self.expanded = False
        self.children = []
        self.heuristic = self.calcHeuristic()
        self.projection = self.heuristic

    def expand(self):
        self.expanded = True

        for i in range(4):
            if self.fatherMove != directions[(i+2)%4]:
                newState = []
                for row in self.state:
                    newState.append(row.copy())
                newState = MoveBlank(newState, directions[i])
                if newState != self.state:
                    self.children.append(TreeNode(newState, self, directions[i], self.height + 1))

    def calcHeuristic(self):
        ret = 0
        for i in range(dim):
            for j in range(dim):
                num = self.state[i][j] - 1
                if num == -1:
                    num = dim*dim - 1
                ii = int(num/dim)
                jj = num % dim
                ret += abs(ii-i) + abs(jj-j)
        return ret


class SearchTree:
    def __init__(self, state):
        self.tree = []
        self.tree.append([TreeNode(state, None, "", 1)])
        printNode(self.tree[0][0], debug)


def GreedySearch(state):
    #initialize the search tree
    global timeChecking, timeExpanding, timeInserting, nodesExp
    tree = SearchTree(state)
    path = []
    tries = 0
    # add the root in the candidate list
    candidates = QueueingFn()
    candidates.insert(tree.tree[0][0])
    expanded = []
    #while tries < fat/100:
    while True:
        tries += 1
        # if no candidates to expand return failure
        if len(candidates.lista) == 0:
            return -1

        # choose the best leaf node for expansion
        ini = time.time()
        cmin = candidates.lista[0]
        candidates.remove(cmin)
        path.append((cmin.father, cmin.fatherMove, cmin))
        expanded.append(cmin.state)
        cmin.expand()
        nodesExp += 1
        timeExpanding += time.time() - ini
        # check the node for the goal state
        # if its the goal, return the solution
        if cmin.state == goal:
            return path
        # else expand leaf and append to the tree
        for child in cmin.children:
            ini = time.time()
            if child.state not in expanded:
                timeChecking += time.time() - ini
                if len(tree.tree) <= cmin.height:
                    tree.tree.append([])
                child.projection = cmin.projection + 1
                tree.tree[cmin.height].append(child)
                ini = time.time()
                candidates.insert(node=child)
                timeInserting += time.time() - ini
            else:
                timeChecking += time.time() - ini
    return -2


def AStarSearch(state):
    #initialize the search tree
    global timeChecking, timeExpanding, timeInserting, nodesExp
    tree = SearchTree(state)
    path = []
    tries = 0
    # add the root in the candidate list
    candidates = QueueingFn()
    candidates.insert(tree.tree[0][0], True)
    expanded = []
    #while tries < fat/100:
    while True:
        tries += 1
        # if no candidates to expand return failure
        if len(candidates.lista) == 0:
            return -1

        # choose the best leaf node for expansion
        ini = time.time()
        cmin = candidates.lista[0]
        candidates.remove(cmin)
        path.append((cmin.father, cmin.fatherMove, cmin))
        expanded.append(cmin.state)
        cmin.expand()
        nodesExp += 1
        timeExpanding += time.time() - ini
        # check the node for the goal state
        # if its the goal, return the solution
        if cmin.state == goal:
            return path
        # else expand leaf and append to the tree
        for child in cmin.children:
            if len(tree.tree) <= cmin.height:
                tree.tree.append([])
            child.projection = cmin.projection + 1
            tree.tree[cmin.height].append(child)
            ini = time.time()
            candidates.insert(child, True)
            timeInserting += time.time() - ini
    return -2


def TrimPath(initial, path):
    line = path[-1]
    node = line[2]
    newpath = [line]
    while node.state != initial:
        for p in range(0, path.index(line) + 1):
            if path[p][0] == node.father and path[p][2] == node:
                newline = path[p]
        if newline not in newpath:
            newpath.insert(0,newline)
        line = newline
        node = node.father
    return newpath


def GenerateStart(solvable = True):
    if solvable:
        state = []
        for i in range(dim):
            state.append(goal[i].copy())
        moves = random.randint(10,20)
        printMatrix(state)
        for i in range(moves):
            d = random.randint(0,3)
            newstate = MoveBlank(state, directions[d])
            if newstate == state:
                i -= 1
            else:
                state = newstate

            printMatrix(state)
        print("moves: %d" % moves)
    else:
        st = []
        state = [[-1 for i in range(dim)] for j in range(dim)]
        for i in range(dim*dim):
            st.append(random.random())
        stsort = st.copy()
        stsort.sort()
        for i in range(dim):
            for j in range(dim):
                state[i][j] = stsort.index(st[i*dim + j])
    return state


if __name__ == '__main__':
    infinite = 10000
    dim = 9
    fat = 1
    timeChecking = 0
    timeExpanding = 0
    timeInserting = 0
    nodesExp = 0
    for i in range(dim*dim, 2, -1):
        fat *= i
    directions = ["N", "E", "S", "W"]
    goal = GoalState()
    debug = open("debugG2.txt", "w")
    print("Generating start...")
    initial = GenerateStart(solvable=True)
    print("Generated start!")
    print("Starting greedy search...")
    st = time.time()
    ret = GreedySearch(initial)
    delay = time.time() - st
    print("Ended greedy search!")
    pathlen = -1
    if ret == -1:
        print("No path found!")
    elif ret == -2:
        print("Timeout!")
    else:
        print("Path found:")
        path = TrimPath(initial, ret)
        for p in path:
            pathlen += 1
            if p[0] is None:
                debug.write("%d steps:\n" % pathlen)
                printNode(p[2], debug)
            else:
                debug.write("%d steps, going %s:\n" % (pathlen, p[1]))
                printNode(p[2], debug)
    print("Delay = %.3f s, %d steps, %d nodes" % (delay, pathlen, nodesExp  ))
    print("Insert = %.3f s, Expand = %.3f s, Check = %.3f s" % (timeInserting, timeExpanding, timeChecking))
    debug.close()
    timeChecking = 0
    timeExpanding = 0
    timeInserting = 0
    nodesExp = 0
    print("Starting A* search...")
    debug = open("debugA2.txt", "w")
    st = time.time()
    ret = AStarSearch(initial)
    delay = time.time() - st
    print("Ended A* search!")
    pathlen = -1
    if ret == -1:
        print("No path found!")
    elif ret == -2:
        print("Timeout!")
    else:
        print("Path found:")
        path = TrimPath(initial, ret)
        for p in path:
            pathlen += 1
            if p[0] is None:
                debug.write("%d steps:\n" % pathlen)
                printNode(p[2], debug)
            else:
                debug.write("%d steps, going %s:\n" % (pathlen, p[1]))
                printNode(p[2], debug)
    print("Delay = %.3f s, %d steps, %d nodes" % (delay, pathlen, nodesExp))
    print("Insert = %.3f s, Expand = %.3f s, Check = %.3f s" % (timeInserting, timeExpanding, timeChecking))
    debug.close()
