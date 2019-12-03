import time, math, random, sys

def printMatrix(config, f):
    # Função para imprimir a matriz config no arquivo f
    for i in range(dim + 1):
        f.write("|%3d" % i)
    f.write("|\n")
    for i in range(dim):
        f.write("|%3d" % i)
        for j in range(dim):
            if i == round(config[j]):
                f.write("| * ")
            else:
                f.write("|   ")
        f.write("|\n")
    f.write("\n")


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
                    if round(input[i]) == round(input[j]):
                        output += 1
                    elif abs(round(input[i]) - round(input[j])) == abs(i - j):
                        output += 1
        return output/2
    return 0


def generateStart():
    config = []
    for i in range(dim):
        pos = random.randint(0, dim - 1)
        while pos in config:
            pos = random.randint(0, dim - 1)
        config.append(pos)
    return config


class Particle:
    def __init__(self, fname):
        self.x = generateStart()
        self.val = function(fname, self.x)
        self.v = [0 for i in range(dim)]
        self.p = self.x
        self.pval = function(fname, self.p)
        self.g = self.x
        self.gval = function(fname, self.g)


class Swarm:
    def __init__(self, w=0.1,selfc=2.5,swarmc=2.5,npart=60, fname="Queens"):
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
                newVid = p.v[d]
                newVid += self.selfc * phi1 * (p.p[d] - p.x[d])
                newVid += self.swarmc * phi2 * (p.g[d] - p.x[d])
                newVid = self.constrict*newVid
                p.v[d] = newVid
                p.x[d] = int(p.x[d]+newVid)
                if p.x[d] > lims[1]:
                    p.x[d] = lims[1]
                if p.x[d] < lims[0]:
                    p.x[d] = lims[0]
            p.val = function(self.fname, p.x)
            print("\t\tParticle {}: x {}, value {}".format(self.parts.index(p), p.x, p.val))

    def checkConv(self, majority=1.0):
        centroid = [0 for i in range(dim)]
        for p in self.parts:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.parts)
        inParts = 0
        print("\tCentroid: {}".format(centroid))
        for p in self.parts:
            distance = 0
            for d in range(dim):
                distance += (p.x[d]-centroid[d])*(p.x[d]-centroid[d])
            distance = math.sqrt(distance)
            if distance < convRad:
                inParts += 1
        allIn = (inParts >= majority*len(self.parts))
        return allIn

    def estimate(self):
        centroid = [0 for i in range(dim)]
        for p in self.parts:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.parts)
        return centroid, function(self.fname, centroid)

    def optimization(self):
        tries = 1
        ini = time.time()
        while not self.checkConv(majority=majority):
            print("Iteration {}:".format(tries))
            self.update()
            tries += 1
        print("End of otimization!")
        est = self.estimate()
        print("Found minimum: {}, value = {} after {} tries".format(est[0], est[1], tries))
        delTime = time.time() - ini
        return (est[0], est[1], tries, delTime)


class Genome:
    def __init__(self, fname):
        self.x = generateStart()
        self.v = [0 for i in range(dim)]
        self.u = [0 for i in range(dim)]
        self.val = function(fname, self.x)
        self.fname = fname


class DifferentialEvolution:
    def __init__(self, ngens=5, F=0.7, CR=0.5, fname="Sphere", mode="rand", perts=1, CRmode="bin", lamb=0.5):
        self.gens = [Genome(fname) for i in range(ngens)]
        self.F = F
        self.CR = CR
        self.mode = mode
        self.perts = perts
        self.CRmode = CRmode
        self.lamb = lamb

    def findBest(self):
        bestg = None
        bestval = None
        for g in self.gens:
            if bestval is None or bestval > g.val:
                bestg = g
                bestval = g.val
        return bestg

    def update(self):
        best = self.findBest()
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
            r4 = r1
            while r4 == r1 or r4 == r2 or r4 == r3:
                r4 = random.randint(0, len(self.gens) - 1)
            xr4 = self.gens[r4].x
            r5 = r1
            while r5 == r1 or r5 == r2 or r5 == r3 or r5 == r4:
                r5 = random.randint(0,len(self.gens)-1)
            xr5 = self.gens[r5].x

            for d in range(dim):
                if self.mode == "rand" and self.perts == 1:
                    g.v[d] = xr1[d] + self.F*(xr2[d] - xr3[d])
                elif self.mode == "rand" and self.perts == 2:
                    g.v[d] = xr1[d] + self.F*(xr2[d] - xr3[d]) + self.F*(xr4[d] - xr5[d])
                elif self.mode == "best" and self.perts == 1:
                    g.v[d] = best.x[d] + self.F*(xr2[d] - xr3[d])
                elif self.mode == "best" and self.perts == 2:
                    g.v[d] = best.x[d] + self.F*(xr2[d] - xr3[d]) + self.F*(xr4[d] - xr5[d])
                elif self.mode == "randtobest":
                    g.v[d] = g.x[d] + self.F*(xr1[d] - xr2[d]) + self.lamb*(best.x[d] - g.x[d])

                g.v[d] = round(g.v[d])

                if g.v[d] > lims[1]:
                    g.v[d] = lims[1]
                if g.v[d] < lims[0]:
                    g.v[d] = lims[0]

                if self.CRmode == "bin":
                    dice = random.random()
                    g.u[d] = g.v[d] if dice < self.CR else g.x[d]

            if self.CRmode == "exp":
                n = int(math.floor(dim*random.random()))
                L = 1
                while random.random() < self.CR and L <= dim:
                    L += 1
                g.u = g.x.copy()
                for i in range(L):
                    g.u[(n+i)%dim] = g.v[(n+i)%dim]

            print("\tParticle {}: x = {} u = {}".format(self.gens.index(g),g.x, g.u))
            uval = function(g.fname, g.u)
            print("\t             f(x) = {} f(u) = {}".format(g.val, uval))
            if g.val > uval:
                print("\t\tU was chosen!")
                g.x = g.u.copy()
                g.val = uval

    def optimization(self):
        tries = 1
        ini = time.time()
        while not self.checkConv(majority=majority):
            print("Iteration {}:".format(tries))
            self.update()
            tries += 1
            best = self.findBest()
            if best.val == 0:
                print("End of otimization!")
                print("Found minimum: {}, value = {} in {} tries".format(best.x, best.val, tries))
                delTime = time.time() - ini
                return (best.x, best.val, tries, delTime)

        print("End of otimization!")
        est = self.estimate()
        print("Found minimum: {}, value = {} in {} tries".format(est[0], est[1], tries))
        delTime = time.time() - ini
        return est[0], est[1], tries, delTime

    def checkConv(self, majority = 1.0):
        centroid = self.centroid()
        inGens = 0
        print("\tCentroid: {}".format(centroid))
        for p in self.gens:
            distance = 0
            for d in range(dim):
                distance += (p.x[d]-centroid[d])*(p.x[d]-centroid[d])
            distance = math.sqrt(distance)
            if distance < convRad:
                inGens += 1
        allIn = (inGens >= majority*len(self.gens))
        return allIn

    def estimate(self):
        centroid = self.centroid()
        return centroid, function(self.gens[0].fname, centroid)

    def centroid(self):
        centroid = [0 for i in range(dim)]
        for p in self.gens:
            for d in range(dim):
                centroid[d] += p.x[d]/len(self.gens)
        for d in range(dim):
            centroid[d] = int(centroid[d])
        return centroid


if __name__ == '__main__':
    dim = 8
    lims = [1,8]
    convRad = 0.01
    majority = 0.8
    PSOSwarm = Swarm(w=0.1,selfc=2.5,swarmc=2.5,npart=60,fname="Queens")
    PSOconfig, PSOattacks, PSOtries, PSOtime = PSOSwarm.optimization()
    DE = DifferentialEvolution(15, 0.7, 0.75, "Queens", "best", 1, "exp")
    DEconfig, DEattacks, DEtries, DEtime = DE.optimization()
    print("PSO Solution after {} tries ({:.3f} s) with {} attacks remaining:".format(PSOtries, PSOtime, PSOattacks))
    printMatrix(PSOconfig, sys.stdout)
    print("DE Solution after {} tries ({:.3f} s) with {} attacks remaining:".format(DEtries, DEtime, DEattacks))
    printMatrix(DEconfig, sys.stdout)
