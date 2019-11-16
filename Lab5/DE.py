import math, random
implementedFunctions = ["Sphere","Rosenbrock","Rastrigin","Griewank","Ackley","Queens"]

def function(name, input):
    output = 0
    if name ==  "Sphere":
        for x in input:
            output += x*x
        return output
    if name == "Rosenbrock":
        for i in range(len(input)-1):
            output += 100*(input[i+1] - input[i]*input[i])
            output += (input[i] - 1)*(input[i] - 1)
        return output
    if name == "Rastrigin":
        for x in input:
            output += x*x + 10
            output -= 10*math.cos(2*math.pi*x)
        return output
    if name == "Griewank":
        grie1 = 0
        grie2 = 1
        for i in range(len(input)):
            x = input[i]
            grie1 += x*x
            grie2 *= math.cos(x/math.sqrt(i))
        output = grie1/4000 - grie2 + 1
        return output
    if name == "Ackley":
        ack1 = 0
        ack2 = 0
        for x in input:
            ack1 += x*x/len(input)
            ack2 += math.cos(2*math.pi*x)/len(input)
        output = -20*math.exp(-0.2*math.sqrt(ack1))-math.exp(ack2)+20+math.e
        return output
    if name == "Queens":
        for i in range(len(input)):
            for j in range(len(input)):
                if i != j:
                    if input[i] == input[j]:
                        output += 1
                    elif abs(input[i] - input[j]) == abs(i - j):
                        output += 1
        return output/2
    return 0

def rand():
    return lims[0] + (lims[1] - lims[0])*random.random()

class Genome:
    def __init__(self, fname):
        self.x = [rand() for i in range(dim)]
        self.v = [0 for i in range(dim)]
        self.u = [0 for i in range(dim)]
        self.val = function(fname, self.x)
        self.fname = fname


class DifferentialEvolution:
    def __init__(self, ngens, F, CR, fname):
        self.gens = [Genome(fname) for i in range(ngens)]
        self.F = F
        self.CR = CR

    def update(self):
        for g in self.gens:
            r1 = random.randint(0,len(self.gens)-1)
            xr1 = self.gens[r1].x
            r2 = r1
            while r2 == r1:
                r2 = random.randint(0,len(self.gens)-1)
            xr2 = self.gens[r2].x
            r3 = r1
            while r3 == r1 or r3 == r2:
                r3 = random.randint(0,len(self.gens)-1)
            xr3 = self.gens[r3].x
            for d in range(dim):
                g.v[d] = xr1[d] + self.F*(xr2[d] - xr3[d])
                if g.v[d] > lims[1]:
                    g.v[d] = lims[1]
                if g.v[d] < lims[0]:
                    g.v[d] = lims[0]
                dice = random.random()
                if dice < self.CR:
                    g.u[d] = g.v[d]
                else:
                    g.u[d] = g.x[d]
            print("\tParticle {}: x = {} u = {}".format(self.gens.index(g),g.x, g.u))
            uval = function(g.fname, g.u)
            print("\t             f(x) = {} f(u) = {}".format(g.val, uval))
            if g.val > uval:
                print("\t\tU was chosen!")
                g.x = g.u.copy()
                g.val = uval

    def optimization(self):
        tries = 1
        while not self.checkConv():
            print("Iteration {}:".format(tries))
            self.update()
            tries += 1
        print("End of otimization!")
        est = self.estimate()
        print("Found minimum: {}, value = {}".format(est[0], est[1]))
        return est

    def checkConv(self):
        centroid = [0 for i in range(dim)]
        for p in self.gens:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.gens)
        allIn = True
        print("\tCentroid: {}".format(centroid))
        for p in self.gens:
            distance = 0
            for d in range(dim):
                distance += (p.x[d]-centroid[d])*(p.x[d]-centroid[d])
            distance = math.sqrt(distance)
            if distance > convRad:
                allIn = False
        return allIn

    def estimate(self):
        centroid = [0 for i in range(dim)]
        for p in self.gens:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.gens)
        return centroid, function(self.gens[0].fname, centroid)


if __name__ == '__main__':
    dim = 2
    lims = [-10,10]
    convRad = 0.01
    DE = DifferentialEvolution(15, 0.7, 0.75, "Sphere")
    DE.optimization()
