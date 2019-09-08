houses = [1, 2, 3, 4, 5]
people = ["norwegian", "english", "spanish", "ukrainian", "japanese"]
colors = ["red", "yellow", "white", "blue", "green"]
animals = ["fox", "dog", "snail", "horse", "zebra"]
drinks = ["juice", "tea", "coffee", "milk", "water"]
cigarettes = ["kool", "chesterfield", "winston", "lucky strike", "parliament"]


class PSRState:
    def __init__(self, vars):
        self.unassigned = {}
        self.assigned = {}
        for var in vars:
            if var.value is None:
                self.unassigned[var.name] = var
            else:
                self.assigned[var.name] = var


class PSRVariable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.value = None


class PSR:
    def __init__(self, state):
        self.state = state

    def ruleCheck(self, state):
        vars = state.assigned

        # O inglês mora na casa vermelha
        #   Inglês = people[1], Vermelho = colors[0]
        if "people" in vars.keys() and \
                "colors" in vars.keys() and \
                vars["people"].value[1] != vars["colors"].value[0]:
            return False
        # O espanhol é dono do cachorro
        #   Espanhol = people[2], Cachorro = animals[1]
        if "people" in vars.keys() and \
                "animals" in vars.keys() and \
                vars["people"].value[2] != vars["animals"].value[1]:
            return False

        # O norueguês mora na primeira casa à esquerda
        #   Norueguês = people[0]
        if "people" in vars.keys() and\
                vars["people"].value[0] != 1:
            return False

        # Fumam-se cigarros Kool na casa amarela
        #   Amarelo = colors[1], Kool = cigarettes[0]
        if "cigarettes" in vars.keys() and \
                "colors" in vars.keys() and \
                vars["cigarettes"].value[0] != vars["colors"].value[1]:
            return False


        # O homem que fuma cigarros Chesterfield mora na casa ao lado do homem que mora com a raposa
        #   Raposa = animals[0], Chesterfield = cigarettes[1]
        if "cigarettes" in vars.keys() and \
                "animals" in vars.keys() and \
                abs(vars["cigarettes"].value[1] - vars["animals"].value[0]) != 1:
            return False
        # O norueguês mora ao lado da casa azul
        #   Norueguês = people[0], Azul = colors[3]
        if "people" in vars.keys() and \
                "colors" in vars.keys() and \
                abs(vars["people"].value[0] - vars["colors"].value[3]) != 1:
            return False
        # O fumante de cigarros Winston cria caramujos.
        if "cigarettes" in vars.keys() and \
                "animals" in vars.keys() and \
                vars["cigarettes"].value[2] != vars["animals"].value[2]:
            return False
        # O fumante de cigarros Lucky Strike bebe suco de laranja
        if "cigarettes" in vars.keys() and \
                "drinks" in vars.keys() and \
                vars["cigarettes"].value[3] != vars["drinks"].value[0]:
            return False
        # O ucraniano bebe chá
        if "people" in vars.keys() and \
                "drinks" in vars.keys() and \
                vars["people"].value[3] != vars["drinks"].value[1]:
            return False
        # O japonês fuma cigarros Parliament
        if "cigarettes" in vars.keys() and \
                "people" in vars.keys() and \
                vars["cigarettes"].value[4] != vars["people"].value[4]:
            return False
        # Fumam-se cigarros Kool em uma casa ao lado da casa em que fica o cavalo
        if "cigarettes" in vars.keys() and \
                "animals" in vars.keys() and \
                abs(vars["cigarettes"].value[0] - vars["animals"].value[3]) != 1:
            return False
        # Bebe-se café na casa verde
        if "drinks" in vars.keys() and \
                "colors" in vars.keys() and \
                vars["drinks"].value[2] == vars["colors"].value[4]:
            return False
        # A casa verde está imediatamente à direita (à sua direita) da casa marfim
        if "colors" in vars.keys() and \
                vars["colors"].value[4] - vars["colors"].value[2] != 1:
            return False
        # Bebe-se leite na casa do meio
        if "drinks" in vars.keys() and \
                vars["drinks"].value[3] != 3:
            return False
        return True


def backtrackingRec(state, problem):
    if len(state.unassigned) == 0:
        return state
    vars = [*state.unassigned.values()]
    vars.extend([*state.assigned.values()])
    var = [*state.unassigned.values()][0]
    print("Trying to assign {}".format(var.name))
    for value in var.domain:
        print("\tTrying value {}".format(value))
        st = []
        for v in vars:
            if v != var:
                newv = PSRVariable(v.name, v.domain)
                newv.value = v.value
                st.append(newv)
            else:
                newv = PSRVariable(v.name, v.domain)
                newv.value = value
                st.append(newv)
        newstate = PSRState(st)
        if problem.ruleCheck(newstate):
            print("\tAssignment checks out!")
            result = backtrackingRec(newstate, problem)
            if result is not None:
                return result
        else:
            print("\tAssignment does not check out.")
    return None


def backtracking(problem):
    return backtrackingRec(problem.state, problem)

def genDomain():
    domain = []
    for i1 in range(len(houses)):
        for i2 in range(len(houses)):
            if i2 not in [i1]:
                for i3 in range(len(houses)):
                    if i3 not in [i1, i2]:
                        for i4 in range(len(houses)):
                            if i4 not in [i1, i2, i3]:
                                for i5 in range(len(houses)):
                                    if i5 not in [i1, i2, i3, i4]:
                                        domain.append([i1+1, i2+1, i3+1, i4+1, i5+1])
    return domain

if __name__ == '__main__':
    permut = genDomain()
    problem = PSR(
        PSRState({
            PSRVariable("people", permut),
            PSRVariable("colors", permut),
            PSRVariable("animals", permut),
            PSRVariable("drinks", permut),
            PSRVariable("cigarettes", permut)
        })
    )
    ansState = backtracking(problem)

    print("ANSWER:")
    print("People:")
    for i in range(len(people)):
        print("\t{}: Casa {}".format(people[i], ansState.assigned["people"].value[i]))
    print("Colors:")
    for i in range(len(colors)):
        print("\t{}: Casa {}".format(colors[i], ansState.assigned["colors"].value[i]))
    print("Animals:")
    for i in range(len(animals)):
        print("\t{}: Casa {}".format(animals[i], ansState.assigned["animals"].value[i]))
    print("Drinks:")
    for i in range(len(drinks)):
        print("\t{}: Casa {}".format(drinks[i], ansState.assigned["drinks"].value[i]))
    print("Cigarettes:")
    for i in range(len(cigarettes)):
        print("\t{}: Casa {}".format(cigarettes[i], ansState.assigned["cigarettes"].value[i]))
