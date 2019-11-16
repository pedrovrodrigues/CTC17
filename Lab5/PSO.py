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


class Particle:
    def __init__(self, fname):
        self.x = [rand() for i in range(dim)]
        self.val = function(fname, self.x)
        self.v = [rand()/abs(lims[0]) for i in range(dim)]
        self.p = self.x
        self.pval = function(fname, self.p)
        self.g = self.x
        self.gval = function(fname, self.g)

class Swarm:
    def __init__(self, w, selfc, swarmc, npart, fname):
        self.w = w
        self.selfc = selfc
        self.swarmc = swarmc
        phi = selfc + swarmc
        self.constrict = 2/abs(4-phi-math.sqrt(phi*phi-4*phi))
        self.parts = [Particle(fname) for i in range(npart)]
        self.fname = fname

    def update(self):
        print("\tUpdating p and g")
        for p in self.parts:
            if p.val < p.pval:
                p.p = p.x.copy()
                p.pval = p.val
                print("\t\tNew p for particle {}".format(self.parts.index(p)))
                print("\t\tposition: {}, value {}".format(p.p, p.pval))
            if p.val < p.gval:
                print("\t\tNew g! Particle {}".format(self.parts.index(p)))
                print("\t\tposition: {}, value {}".format(p.x, p.val))
                for pp in self.parts:
                    pp.g = p.x.copy()
                    pp.gval = p.val

        phi1 = random.random()
        phi2 = random.random()
        print("\tUpdating velocity and position, phi1 = {}, phi2 = {}".format(phi1,phi2))
        for p in self.parts:
            for d in range(dim):
                newVid = self.w * p.v[d]
                newVid += self.selfc * phi1 * (p.p[d] - p.x[d])
                newVid += self.swarmc * phi2 * (p.g[d] - p.x[d])
                newVid = self.constrict*newVid
                p.v[d] = newVid
                p.x[d] += newVid
                if p.x[d] > lims[1]:
                    p.x[d] = lims[1]
                if p.x[d] < lims[0]:
                    p.x[d] = lims[0]
            p.val = function(self.fname, p.x)
            print("\t\tParticle {}: x {}, value {}".format(self.parts.index(p), p.x, p.val))

    def checkConv(self):
        centroid = [0 for i in range(dim)]
        for p in self.parts:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.parts)
        allIn = True
        print("\tCentroid: {}".format(centroid))
        for p in self.parts:
            distance = 0
            for d in range(dim):
                distance += (p.x[d]-centroid[d])*(p.x[d]-centroid[d])
            distance = math.sqrt(distance)
            if distance > convRad:
                allIn = False
        return allIn

    def estimate(self):
        centroid = [0 for i in range(dim)]
        for p in self.parts:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.parts)
        return centroid, function(self.fname, centroid)

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

if __name__ == '__main__':
    dim = 2
    lims = [-10,10]
    convRad = 0.01
    PSOSwarm = Swarm(w=0.1,selfc=2.5,swarmc=2.5,npart=60,fname="Sphere")
    PSOSwarm.optimization()
