if __name__ == '__main__':
    N = int(input())
    vet = []
    for i in range(N):
        vet.append(int(input()))
    sol = None
    if 1 not in vet:
        sol = 1
    else:
        for i in range(0, N):
            if vet[i] + 1 not in vet and (sol is None or sol > vet[i] + 1):
                sol = vet[i] + 1
    print(sol)

if __name__ == '__main__':
    str1 = list(input())
    str2 = list(input())
    str1.sort()
    str2.sort()
    if str1 == str2:
        print("true")
    else:
        print("false")

if __name__ == '__main__':
    N = int(input())
    vet = []
    for i in range(N):
        vet.append(int(input()))
    summin = None
    for i in range(N):
        for j in range(1,N-i+1):
            print("[{},{}]".format(i,i+j))
            subvet = vet[i:i+j]
            submin = subvet if summin is None or sum(subvet) < summin else submin
            summin = sum(subvet) if summin is None or sum(subvet) < summin else summin
            print(subvet)
            print(submin)
    if summin > 0:
        print(0)
    else:
        for i in range(len(submin)):
            print(submin[i])

ways = []

class Treenode:
    def __init__(self, seq, val, coins):
        self.val = val
        self.seq = seq
        self.coins = coins

    def DFS(self):
        global ways
        for coin in self.coins:
            if sum(self.seq)+coin == val:
                nseq = self.seq.copy()
                nseq.append(coin)
                nseq.sort()
                if nseq not in ways:
                    ways.append(nseq)
            elif sum(self.seq)+coin < val:
                nseq = self.seq.copy()
                nseq.append(coin)
                son = Treenode(nseq, val, coins)
                son.DFS()

if __name__ == '__main__':
    val = int(input())
    N = int(input())
    coins = []
    for i in range(N):
        coins.append(int(input()))
    root = Treenode([],val,coins)
    root.DFS()
    print(len(ways))
