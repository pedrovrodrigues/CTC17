# Busca de melhoria iterativa - N Rainhas
import time, math, random, sys
dims = [10, 15, 20, 25]
#dims = [4, 5, 6]
global dim, debug


def printMatrix(config, f):
    # Função para imprimir a matriz config no arquivo f
    for i in range(dim + 1):
        f.write("|%3d" % i)
    f.write("|\n")
    for i in range(dim):
        f.write("|%3d" % i)
        for j in range(dim):
            if i == config[j]:
                f.write("| * ")
            else:
                f.write("|   ")
        f.write("|\n")
    f.write("\n")


def checkConfig(config):
    # Função que checa quantas rainhas se atacam numa dada configuração
    attacks = 0
    for i in range(dim):
        for j in range(dim):
            if i != j:
                if config[i] == config[j]:
                    attacks += 1
                elif abs(config[i] - config[j]) == abs(i - j):
                    attacks += 1
    return attacks/2


class Node:
    def __init__(self, config):
        self.config = config
        self.attacks = checkConfig(self.config)

    def next(self):
        nextconf = None
        minattacks = dim*dim
        for i in range(dim):
            for j in range(dim):
                if i != j:
                    newconf = self.config.copy()
                    aux = newconf[i]
                    newconf[i] = newconf[j]
                    newconf[j] = aux
                    newattacks = checkConfig(newconf)
                    nextconf = newconf if newattacks < minattacks else nextconf
                    minattacks = newattacks if newattacks < minattacks else minattacks
        return Node(nextconf)

    def randomNext(self):
        i = random.randint(0, dim-1)
        j = i
        while j == i:
            j = random.randint(0,dim-1)
        newconf = self.config.copy()
        aux = newconf[i]
        newconf[i] = newconf[j]
        newconf[j] = aux
        return Node(newconf)


def hillClimbing(initial):
    next = Node(initial)
    current = None
    while current is None or next.attacks < current.attacks:
        current = next
        printMatrix(current.config, debug)
        next = current.next()
    return next


def simulatedAnnealling(initial, schedule):
    current = Node(initial)
    t = 0
    T = schedule[t]
    while T > 0:
        printMatrix(current.config, debug)
        next = current.randomNext()
        delE = current.attacks - next.attacks
        if delE < 0:
            current = next
            t += 1
        else:
            prob = random.random()
            if prob < math.exp(-delE/T):
                current = next
                t += 1
        T = schedule[t]
    return current


def hybrid(initial, schedule):
    current = Node(initial)
    t = 0
    T = schedule[t]
    while T > 0:
        printMatrix(current.config, debug)
        if T%2==0:
            next = current.randomNext()
            delE = current.attacks - next.attacks
            if delE < 0:
                current = next
                t += 1
            else:
                prob = random.random()
                if prob < math.exp(-delE/T):
                    current = next
                    t += 1
        else:
            next = current.next()
            if next.attacks >= current.attacks:
                break
            current = next
            t+=1
        T = schedule[t]

    return current


if __name__ == '__main__':
    fans = open("answer.txt", "w")
    for dim in dims:
        debug = open("debug_HC_" + str(dim) + ".txt", "w")
        config = []
        for i in range(dim):
            pos = random.randint(0,dim-1)
            while pos in config:
                pos = random.randint(0,dim-1)
            config.append(pos)
        #printMatrix(config, sys.stdout)
        # Hill Climbing
        ini = time.time()
        answer = hillClimbing(config)
        delay = time.time() - ini
        print("Hill Climbing")
        fans.write("Hill Climbing\n")
        fans.write("dim = {}\n".format(dim))
        printMatrix(answer.config, fans)
        print("Number of attacks remaining for dimension %d: %d" % (dim, checkConfig(answer.config)))
        print("Delayed time for dimension %d: %.3f s" % (dim, delay))
        fans.write("Number of attacks remaining for dimension %d: %d\n" % (dim, checkConfig(answer.config)))
        fans.write("Delayed time for dimension %d: %.3f s\n" % (dim, delay))

        # Simulated Annealling
        schedule = []
        debug = open("debug_SA_" + str(dim) + ".txt", "w")
        for i in range(dim*1000+1):
            schedule.append(dim*1000-i)
        ini = time.time()
        answer = simulatedAnnealling(config, schedule)
        delay = time.time() - ini
        print("Simulated Annealling")
        fans.write("Simulated Annealling\n")
        fans.write("dim = {}\n".format(dim))
        printMatrix(answer.config, fans)
        print("Number of attacks remaining for dimension %d: %d" % (dim, checkConfig(answer.config)))
        print("Delayed time for dimension %d: %.3f s" % (dim, delay))
        fans.write("Number of attacks remaining for dimension %d: %d\n" % (dim, checkConfig(answer.config)))
        fans.write("Delayed time for dimension %d: %.3f s\n" % (dim, delay))

        # Hybrid
        schedule = []
        debug = open("debug_H_" + str(dim) + ".txt", "w")
        for i in range(dim*1000+1):
            schedule.append(dim*1000-i)
        ini = time.time()
        answer = hybrid(config, schedule)
        delay = time.time() - ini
        print("Hybrid")
        fans.write("Hybrid\n")
        fans.write("dim = {}\n".format(dim))
        printMatrix(answer.config, fans)
        print("Number of attacks remaining for dimension %d: %d" % (dim, checkConfig(answer.config)))
        print("Delayed time for dimension %d: %.3f s" % (dim, delay))
        fans.write("Number of attacks remaining for dimension %d: %d\n" % (dim, checkConfig(answer.config)))
        fans.write("Delayed time for dimension %d: %.3f s\n" % (dim, delay))

