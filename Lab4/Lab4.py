import random

directions = ["U", "R", "D", "L"]
dirPrint = {
    "U": "/\\",
    "R": "->",
    "D": "\\/",
    "L": "<-",
    "UR": "└",
    "UD": "│",
    "UL": "┘",
    "RD": "┌",
    "RL": "─",
    "DL": "┐",
    "URD": "├",
    "URL": "┴",
    "UDL": "┤",
    "RDL": "┬",
    "URDL": "┼"
}
infinity = 1000
damping = 0.9
debug = open("debug.txt", "w",encoding="utf-8")

def printMatrix(mat, f):
    for i in range(len(mat[0]) + 1):
        f.write("|%4d" % i)
    f.write("\n")
    for i in range(len(mat)):
        f.write("|%4d" % (i+1))
        for j in range(len(mat[i])):
            f.write("|%4d" % mat[i][j])
        f.write("|\n")
    f.write("\n")

def copyMatrix(mat):
    copy = []
    for i in range(len(mat)):
        copy.append(mat[i].copy())
    return copy

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Policy:
    def __init__(self, world):
        self.world = world
        self.stateCost = copyMatrix(world)
        self.actions = copyMatrix(world)
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == " ":
                    self.actions[i][j] = directions.copy()
                else:
                    self.actions[i][j] = []
                self.stateCost[i][j] = 0
        self.util = 0

    def decision(self, xy):
        return self.actions[xy.y][xy.x]

    def valueIteration(self):
        newSC = None
        while newSC is None or newSC != self.stateCost:
            if newSC is not None:
                self.stateCost = copyMatrix(newSC)
            else:
                newSC = copyMatrix(self.stateCost)

            for i in range(len(self.stateCost)):
                for j in range(len(self.stateCost[i])):
                    newSC[i][j] = self.utilTile(i,j)
                    maxV = 0
                    for a in self.actions[i][j]:
                        summing = 0
                        aL = directions[(directions.index(a) + 3) % 4]
                        aR = directions[(directions.index(a) + 1) % 4]
                        poss = [(a,0.7), (aL,0.2), (aR,0.1)]
                        for p in poss:
                            # Para a direção, bate na parede ou anda um espaço
                            if p[0] == "U":
                                if i == 0:
                                    summing -= p[1]*-1
                                    summing += p[1]*self.stateCost[i][j]
                                else:
                                    summing -= p[1]*-0.1
                                    summing += p[1]*self.stateCost[i-1][j]
                            elif p[0] == "D":
                                if i == len(self.world) - 1:
                                    summing -= p[1]*-1
                                    summing += p[1]*self.stateCost[i][j]
                                else:
                                    summing -= p[1]*-0.1
                                    summing += p[1]*self.stateCost[i+1][j]
                            elif p[0] == "L":
                                if j == 0:
                                    summing -= p[1]*-1
                                    summing += p[1]*self.stateCost[i][j]
                                else:
                                    summing -= p[1]*-0.1
                                    summing += p[1]*self.stateCost[i][j-1]
                            elif p[0] == "R":
                                if j == len(self.world[0]) - 1:
                                    summing -= p[1]*-1
                                    summing += p[1]*self.stateCost[i][j]
                                else:
                                    summing -= p[1]*-0.1
                                    summing += p[1]*self.stateCost[i][j+1]
                        print("stateCost[{}][{}] = {}".format(i,j,summing))
                        if maxV is None:
                            maxV = summing
                        else:
                            maxV = summing if summing > maxV else maxV
                    newSC[i][j] += damping*maxV
                    newSC[i][j] = round(newSC[i][j],3)
        self.defineActions()
        self.print(debug)


    def defineActions(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                if self.utilTile(i,j) != 0:
                    self.actions[i][j] = []
                    continue
                possTiles = []
                # tile up
                if i > 0:
                    possTiles.append(self.stateCost[i-1][j])
                else:
                    possTiles.append(self.stateCost[i][j])
                # tile right
                if j < len(self.world[i]) - 1:
                    possTiles.append(self.stateCost[i][j+1])
                else:
                    possTiles.append(self.stateCost[i][j])
                # tile down
                if i < len(self.world) - 1:
                    possTiles.append(self.stateCost[i+1][j])
                else:
                    possTiles.append(self.stateCost[i][j])
                # tile left
                if j > 0:
                    possTiles.append(self.stateCost[i][j-1])
                else:
                    possTiles.append(self.stateCost[i][j])
                self.actions[i][j] = []
                maxUtil = max(possTiles)
                for k in range(len(possTiles)):
                    if possTiles[k] == maxUtil:
                        self.actions[i][j].append(directions[k])


    def restartUtil(self):
        avg = 0
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                avg += self.stateCost[i][j]
        return damping*avg/(len(self.world)*len(self.world[0]))


    def utilTile(self,i,j):
        if self.world[i][j] == "G":
            return 100 + self.restartUtil()
        if self.world[i][j] == "P":
            return -50 + self.restartUtil()
        if self.world[i][j] == "W":
            return -100 + self.restartUtil()
        return 0

    def print(self, f):
        for i in range(len(self.world[0]) + 1):
            f.write("|{:^4}".format(i))
        f.write("\n")
        for i in range(len(self.world)):
            f.write("|{:^4}".format(i + 1))
            for j in range(len(self.world[i])):
                if self.world[i][j] == " ":
                    choices = ""
                    for a in self.actions[i][j]:
                        choices += a
                    print(dirPrint[choices])
                    # f.write("|")
                    # f.write(dirPrint[choices])
                    # for i in range(4-len(dirPrint[choices])):
                    #     f.write(" ")
                    f.write("|{:^4}".format(dirPrint[choices]))
                else:
                    f.write("|{:^4}".format(self.world[i][j]))
            f.write("|\n")
        f.write("\n")


class Robot:
    def __init__(self, world, xy = None):
        self.world = world
        if xy is None or world[xy.y][xy.x] != " ":
            self.xy = XY(0,0)
            self.retries = -1
            self.restart(world)
        else:
            self.xy = xy
            self.retries = 0
        self.util = 0

    def restart(self, world):
        tile = ""
        while tile != " ":
            self.xy.x = random.randint(0,len(world))
            self.xy.y = random.randint(0,len(world[0]))
            tile = self.world[self.xy.y][self.xy.x]
        self.retries += 1

    def resolveState(self):
        if self.world[self.xy.y][self.xy.x] == "W":
            self.util -= 100
            self.restart(self.world)
        elif world[self.xy.y][self.xy.x] == "P":
            self.util -= 50
            self.restart(self.world)
        elif world[self.xy.y][self.xy.x] == "G":
            self.util += 100
            self.restart(self.world)

    def move(self, pol):
        # Política retorna uma lista de direções sugeridas
        choices = pol.decision(self.xy)
        # Escolher aleatoriamente a direção
        if len(choices) == 1:
            dir = choices[0]
        else:
            dir = choices[random.randint(0,len(choices)-1)]
        # Possibilidade do robô deslizar
        error = random.random()
        if error < 0.2:
            dir = directions[(directions.index(dir) + 3) % 4]
        elif error > 0.9:
            dir = directions[(directions.index(dir) + 1) % 4]
        # Para a direção, bate na parede ou anda um espaço
        if dir == "U":
            if self.xy.y == 0:
                self.util -= 1
            else:
                self.util -= 0.1
                self.xy.y -= 1
                self.resolveState()
        elif dir == "D":
            if self.xy.y == len(self.world) - 1:
                self.util -= 1
            else:
                self.util -= 0.1
                self.xy.y += 1
                self.resolveState()
        elif dir == "L":
            if self.xy.x == 0:
                self.util -= 1
            else:
                self.util -= 0.1
                self.xy.x -= 1
                self.resolveState()
        elif dir == "R":
            if self.xy.x == len(self.world[0]) - 1:
                self.util -= 1
            else:
                self.util -= 0.1
                self.xy.x += 1
                self.resolveState()



if __name__ == '__main__':
    wumpusWorld =  [[" ","P"," "," "," "," ","P"," "],
                    ["W","G","P"," "," "," ","P"," "],
                    [" "," "," "," ","W","G"," "," "],
                    [" "," ","P"," "," "," ","P"," "]]
    pol = Policy(wumpusWorld)
    pol.valueIteration()
    printMatrix(pol.stateCost, debug)
