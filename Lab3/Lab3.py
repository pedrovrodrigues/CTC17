import time, os
occupations = {
    0:  "other",
    1:  "academic/educator",
    2:  "artist",
    3:  "clerical/admin",
    4:  "college/grad student",
    5:  "customer service",
    6:  "doctor/health care",
    7:  "executive/managerial",
    8:  "farmer",
    9:  "homemaker",
    10:  "K-12 student",
    11:  "lawyer",
    12:  "programmer",
    13:  "retired",
    14:  "sales/marketing",
    15:  "scientist",
    16:  "self-employed",
    17:  "technician/engineer",
    18:  "tradesman/craftsman",
    19:  "unemployed",
    20:  "writer"
}

class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

class Movie:
    def __init__(self, id, name, year, genres):
        self.id = id
        self.name = name
        self.year = year
        self.genres = genres

class Person:
    def __init__(self, id, gender, age, profession):
        self.id = id
        self.gender = gender
        self.age = age
        self.profession = profession

class Rating:
    def __init__(self, userid, movieid, rating, user=None, movie=None):
        self.userid = userid
        self.user = user
        self.movieid = movieid
        self.movie = movie
        self.score = rating
    
    def getValue(self, var):
        if var.name == "name":
            if self.movie is None:
                for movie in movies:
                    if movie.id == self.movieid:
                        self.movie = movie
                        break
            return self.movie.name
        if var.name == "genre":
            if self.movie is None:
                for movie in movies:
                    if movie.id == self.movieid:
                        self.movie = movie
                        break
            return self.movie.genres
        if var.name == "age":
            if self.user is None:
                for user in people:
                    if user.id == self.userid:
                        self.user = user
                        break
            return self.user.age
        if var.name == "occupation":
            if self.user is None:
                for user in people:
                    if user.id == self.userid:
                        self.user = user
                        break
            return self.user.profession
        if var.name == "gender":
            if self.user is None:
                for user in people:
                    if user.id == self.userid:
                        self.user = user
                        break
            return self.user.gender


def majorityRating(ratings):
    counters = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    for r in ratings:
        counters[r.score] += 1
    cmax = 0
    rmax = 0
    for c, v in counters.items():
        rmax = c if v > cmax else rmax
        cmax = v if v > cmax else cmax
    return rmax, cmax/len(ratings)


def chooseBest(vars, ratings):
    return vars[0]


class TreeNode:
    def __init__(self, vars, ratings, default, father, height):
        # Test: is ratings empty?
        self.father = father
        self.height = height
        self.children = []

        if len(ratings) == 0:
            print("No examples left, using default: {}".format(default))
            self.leaf = True
            self.value = default
            self.prob = 1
            return

        # Test: are all ratings the same?
        val = None
        equal = True
        for r in ratings:
            if val is None:
                val = r.score
            elif r.score != val:
                equal = False
                break
        if equal:
            print("All examples equal, using value: {}".format(val))
            self.leaf = True
            self.value = val
            self.prob = 1
            return

        # Test: is there no more variables?
        if len(vars) == 0:
            self.leaf = True
            self.value, self.prob = majorityRating(ratings)
            print("No variables left, using majority: {}".format(self.value))
            return

        # Algorithm
        self.var = chooseBest(vars, ratings)
        print("Choosing to fan out variable {}".format(self.var.name))
        self.leaf = False
        self.value, self.prob = majorityRating(ratings)
        print("Current prediction: {} with probability {}".format(self.value, self.prob))
        for val in self.var.domain:
            examplesi = []
            for ex in ratings:
                if (type(ex.getValue(self.var)) is not list and val == ex.getValue(self.var)) or\
                        (type(ex.getValue(self.var)) is list and val in ex.getValue(self.var)):
                    examplesi.append(ex)
            varsi = vars.copy()
            varsi.remove(self.var)
            print("Creating child with {} = {}".format(self.var.name, val))
            self.children.append(TreeNode(varsi, examplesi, self.value, self, self.height + 1))


def printTree(root, f):
    root = TreeNode()
    queue = [root]
    curheight = root.height
    val = None
    count = 1
    while len(queue) > 0:
        node = queue[0]
        queue.pop(0)
        if curheight != node.height:
            count = 1
            f.write("\n")
            curheight = node.height
        if node.father is None:
            if node.leaf:
                f.write("(leaf: rat:{}, p:{}".format(node.value, node.prob))
            else:
                f.write("({}?)".format(node.var.name))
                queue.extend(node.children)
        else:
            branch = node.father.var.domain[node.father.children.index(node)]
            if node.leaf:
                f.write("(leaf: {} = {}, rat:{} p:{})".format(node.father.var.name, branch, node.value, node.prob))
            else:
                f.write("({} = {}, {}?)".format(node.father.var.name, branch, node.var.name))
                queue.extend(node.children)





if __name__ == '__main__':
    ##################################
    # 3.1 DATA ANALYSIS              #
    ##################################
    vars = []

    varage = Variable("age", [1, 18, 25, 35, 45, 50, 56])
    vars.append(varage)

    vargender = Variable("gender", ["M", "F"])
    vars.append(vargender)
    vargenre = Variable("genre", ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary",
                                   "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
                                   "Thriller", "War", "Western"])
    vars.append(vargenre)
    varoccup = Variable("occupation", [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    vars.append(varoccup)

    files = os.listdir("ml-1m")
    if "full.txt" not in files:
        people = []
        peoplefile = open("ml-1m\\users.dat",  "r")
        movies = []
        moviesfile = open("ml-1m\\movies.dat", "r")
        ratings = []
        ratingfile = open("ml-1m\\ratings.dat","r")

        for line in peoplefile.readlines():
            user = int(line.split("::")[0])
            gender = line.split("::")[1]
            age = int(line.split("::")[0])
            occupation = int(line.split("::")[0])
            people.append(Person(user, gender, age, occupation))
        print("Read people!")
        for line in moviesfile.readlines():
            id = int(line.split("::")[0])
            name = line.split("::")[1]
            year = int(name.split("(")[-1][0:-1])
            name = name.split("(")[0][0:-1]
            genres = line.replace("\n", "").split("::")[2].split("|")
            movies.append(Movie(id, name, year, genres))
        print("Read movies!")
        for line in ratingfile.readlines():
            user = int(line.split("::")[0])
            movie = int(line.split("::")[1])
            score = int(line.split("::")[2])
            ratings.append(Rating(user, movie, score))
        print("Read ratings!")

        print("Creating single file...")
        fullfile = open("ml-1m\\full.txt", "w")
        for r in ratings:
            # userId :: gender :: age :: occupation :: movieId :: movieName :: movieYear :: movieGenres :: rating
            if r.movie is None:
                for movie in movies:
                    if movie.id == r.movieid:
                        r.movie = movie
                        break
            if r.user is None:
                for user in people:
                    if user.id == r.userid:
                        r.user = user
                        break

            fullfile.write("{}::{}::{}::{}::".format(r.userid, r.user.gender, r.user.age, r.user.profession))
            fullfile.write("{}::{}::{}::".format(r.movieid, r.movie.name, r.movie.year))
            for genre in r.movie.genres:
                if genre != r.movie.genres[0]:
                    fullfile.write("|")
                fullfile.write("{}".format(genre))
            fullfile.write("::{}\n".format(r.score))
    else:
        ratings = []
        fullfile = open("ml-1m\\full.txt", "r")
        # userId :: gender :: age :: occupation :: movieId :: movieName :: movieYear :: movieGenres :: rating
        for line in fullfile.readlines():
            uid = line.split("::")[0]
            gender = line.split("::")[1]
            age = line.split("::")[2]
            occup = line.split("::")[3]
            mid = line.split("::")[4]
            mname = line.split("::")[5]
            myear = line.split("::")[6]
            genres = line.split("::")[7].split("|")
            score = line.split("::")[8]
            ratings.append(
                Rating(uid, mid, score,
                       Person(uid, genres, age, occup),
                       Movie(mid, mname, myear, genres)
                       ))

    ##################################
    # 3.2 DECISION TREE CLASSIFIER   #
    ##################################
    majority, prob = majorityRating(ratings)
    print("A priori: rating {} with probability {}".format(majority, prob))
    decisionTree = TreeNode(vars, ratings, majority, None, 0)
    debug = open("debug.txt", "w")
    printTree(decisionTree, debug)

    ##################################
    # 3.3 RANDOM CLASSIFIER          #
    ##################################

    ##################################
    # 3.4 CLASSIFIER COMPARISON      #
    ##################################


