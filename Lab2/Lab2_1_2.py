# Busca de melhoria iterativa - N Rainhas
import time, math, random, sys
dims = [10, 15, 20, 25]
#dims = [4, 5, 6]
global dim, debug, tries, randrange


def calcFunc(x,y):
    ret = 4*math.exp(-1*(x*x + y*y))
    ret += math.exp(-1*((x-5)*(x-5) + (y-5)*(y-5)))
    ret += math.exp(-1*((x+5)*(x+5) + (y-5)*(y-5)))
    ret += math.exp(-1*((x-5)*(x-5) + (y+5)*(y+5)))
    ret += math.exp(-1*((x+5)*(x+5) + (y+5)*(y+5)))
    return ret

def calcGrad(x,y):
    gradx = -4*2*x*math.exp(-1*(x*x + y*y))
    gradx += -2*(x-5)*math.exp(-1*((x-5)*(x-5) + (y-5)*(y-5)))
    gradx += -2*(x+5)*math.exp(-1*((x+5)*(x+5) + (y-5)*(y-5)))
    gradx += -2*(x-5)*math.exp(-1*((x-5)*(x-5) + (y+5)*(y+5)))
    gradx += -2*(x+5)*math.exp(-1*((x+5)*(x+5) + (y+5)*(y+5)))
    grady = -4*2*y*math.exp(-1*(x*x + y*y))
    grady += -2*(y-5)*math.exp(-1*((x-5)*(x-5) + (y-5)*(y-5)))
    grady += -2*(y-5)*math.exp(-1*((x+5)*(x+5) + (y-5)*(y-5)))
    grady += -2*(y+5)*math.exp(-1*((x-5)*(x-5) + (y+5)*(y+5)))
    grady += -2*(y+5)*math.exp(-1*((x+5)*(x+5) + (y+5)*(y+5)))
    len = math.sqrt(gradx*gradx + grady*grady)
    if len > 0:
        gradx, grady = gradx/len, grady/len
    gradx = float("%.3f" % gradx)
    grady = float("%.3f" % grady)
    return (gradx, grady)


def nextRandom(x,y):
    global randrange
    dx = (random.random()-0.5)*2*randrange
    dy = (random.random()-0.5)*2*randrange
    x = x+dx
    y = y+dy
    x = float("%.3f" % x)
    y = float("%.3f" % y)
    return (x, y)


def nextGrad(x,y):
    global randrange
    dl = random.random()*randrange
    grad = calcGrad(x,y)
    x, y = (x+dl*grad[0], y+dl*grad[1])
    x = float("%.3f" % x)
    y = float("%.3f" % y)
    return (x, y)


def hillClimbing(initial, tries):
    next = initial
    maxval = 0
    curmax = initial
    while tries > 0:
        next = initial
        current = None
        while current is None or calcFunc(next[0],next[1]) > calcFunc(current[0],current[1]):
            current = next
            debug.write("X = {}, Y = {}\n".format(current[0], current[1]))
            next = nextGrad(current[0], current[1])
        curmax = current if calcFunc(next[0], next[1]) > maxval else curmax
        maxval = calcFunc(next[0], next[1]) if calcFunc(next[0], next[1]) > maxval else maxval
        initial = generateStart()
        tries -= 1
    return next


def simulatedAnnealling(initial, schedule):
    current = initial
    t = 0
    T = schedule[t]
    while T > 0:
        debug.write("X = {}, Y = {}\n".format(current[0], current[1]))
        next = nextRandom(current[0], current[1])
        delE = calcFunc(next[0],next[1]) - calcFunc(current[0],current[1])
        if delE > 0:
            current = next
            t += 1
        else:
            prob = random.random()
            if prob < math.exp(delE/T):
                current = next
                t += 1
        T = schedule[t]
    return current


def generateStart():
    x, y = 20*(random.random() - 0.5), 20*(random.random() - 0.5)
    x = float("%.3f" % x)
    y = float("%.3f" % y)
    return x,y


if __name__ == '__main__':
    randrange = 1
    fans = open("answer.txt", "w")
    debug = open("debug_HC.txt", "w")
    config = generateStart()
    print("X = {}, Y = {}, F(X,Y) = {}".format(config[0], config[1], calcFunc(config[0], config[1])))
    #printMatrix(config, sys.stdout)
    # Hill Climbing
    ini = time.time()
    answer = hillClimbing(config,100)
    delay = time.time() - ini
    print("Hill Climbing")
    fans.write("Hill Climbing\n")
    print("X = {}, Y = {}, F(X,Y) = {}".format(answer[0], answer[1], calcFunc(answer[0], answer[1])))
    fans.write("X = {}, Y = {}, F(X,Y) = {}\n".format(answer[0], answer[1], calcFunc(answer[0], answer[1])))
    print("Delayed time: %.3f s" % (delay))
    fans.write("Delayed time: %.3f s\n" % (delay))
    debug.close()

    # Simulated Annealling
    schedule = []
    debug = open("debug_SA.txt", "w")
    for i in range(100+1):
        schedule.append(1-i/100)
    ini = time.time()
    answer = simulatedAnnealling(config, schedule)
    delay = time.time() - ini
    print("Simulated Annealling")
    fans.write("Simulated Annealling\n")
    print("X = {}, Y = {}, F(X,Y) = {}".format(answer[0], answer[1], calcFunc(answer[0], answer[1])))
    fans.write("X = {}, Y = {}, F(X,Y) = {}\n".format(answer[0], answer[1], calcFunc(answer[0], answer[1])))
    print("Delayed time: %.3f s" % (delay))
    fans.write("Delayed time: %.3f s\n" % (delay))

        # # Hybrid
        # schedule = []
        # debug = open("debug_H_" + str(dim) + ".txt", "w")
        # for i in range(dim*1000+1):
        #     schedule.append(dim*1000-i)
        # ini = time.time()
        # answer = hybrid(config, schedule)
        # delay = time.time() - ini
        # print("Hybrid")
        # fans.write("Hybrid\n")
        # fans.write("dim = {}\n".format(dim))
        # printMatrix(answer.config, fans)
        # print("Number of attacks remaining for dimension %d: %d" % (dim
        # , checkConfig(answer.config)))
        # print("Number tries for dimension %d: %d" % (dim, tries))
        # print("Delayed time for dimension %d: %.3f s" % (dim, delay))
        # fans.write("Number of attacks remaining for dimension %d: %d\n" % (dim, checkConfig(answer.config)))
        # fans.write("Number tries for dimension %d: %d\n" % (dim, tries))
        # fans.write("Delayed time for dimension %d: %.3f s\n" % (dim, delay))

