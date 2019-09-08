houses = [1, 2, 3, 4, 5]
people = ["norwegian", "english", "spanish", "ukrainian", "japanese"]
colors = ["red", "yellow", "white", "blue", "green"]
animals = ["fox", "dog", "snail", "horse", "zebra"]
drink = ["juice", "tea", "coffee", "milk", "water"]
cigarettes = ["kool", "chesterfield", "winston", "lucky strike", "parliament"]


class PSRState:
    def __init__(self, vars):
        self.unassigned = vars
        self.assigned = []


class PSRVariable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.assigned = False
        self.value = None


class PSRProblem:
    def __init__(self, state):
        self.state = state

    def ruleCheck(self):
        vars = self.state.assigned
