class Matchup:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1 #index of pokemon in POKEMON_LIST
        self.pokemon2 = pokemon2
        # A dictionary: key = move name, value = its damage vector
        self.pokemon1moves = {}
        self.pokemon2moves = {}
        self.winProbability = None



class Pokemon:
    def __init__(self, name, HP, speed, critRate):
        self.moves = []
        self.name = name
        self.HP = HP
        self.speed = speed
        self.critRate = critRate


class Move:
    def __init__(self, name, accuracy, isDamagingMove, bestCase):
        self.name = name
        self.accuracy = accuracy
        self.isDamagingMove = isDamagingMove
        self.bestCase = bestCase
        self.successVector = []
        self.criticalVector = []
        self.drawbacks = []
        self.trapping = 0
        self.statusAffliction = {}
        self.alwaysCritical = 0


# This is probably the absolute worst way to implement this, but I'm tired
def getCritDictionary(movecount):
    critDict = {}
    if(movecount == 1 or movecount > 9): return {}
    if(movecount == 2):
        critDict[1] = [[1]]
        critDict[2] = [[0]]

    elif (movecount == 3):
        critDict[2] = [[1], [0, 1]]
        critDict[3] = [[0, 0]]

    elif (movecount == 4):
        critDict[2] = [[1, 1]]
        critDict[3] = [[0, 0, 1], [0, 1], [1, 0]]
        critDict[4] = [[0, 0, 0]]

    elif (movecount == 5):
        critDict[3] = [[1, 1], [1, 0, 1], [0, 1, 1]]
        critDict[4] = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0, 1]]
        critDict[5] = [[0, 0, 0, 0]]

    elif (movecount == 6):
        critDict[3] = [[1, 1, 1]]
        critDict[4] = [[1, 1, 0], [1, 0, 1], [0, 1, 1], [0, 0, 1, 1], [1, 0, 0, 1], [0, 1, 0, 1]]
        critDict[5] = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0, 1]]
        critDict[6] = [[0, 0, 0, 0, 0]]

    elif (movecount == 7):
        critDict[4] = [[1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1]]
        critDict[5] = [[1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 1], [0, 0,
            1, 1], [0, 0, 0, 1, 1], [1, 0, 0, 0, 1], [0, 1, 0, 0, 1], [0, 0, 1, 0, 1]]
        critDict[6] = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0,
            0, 1], [0, 0, 0, 0, 0, 1]]
        critDict[7] = [[0, 0, 0, 0, 0, 0]]

    elif (movecount == 8):
        critDict[4] = [[1, 1, 1, 1]]
        critDict[5] = [[1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 0, 1],
                       [1, 0, 1, 0, 1], [1, 0, 0, 1, 1], [0, 1, 1, 0, 1], [0, 1, 0, 1, 1],
                       [0, 0, 1, 1, 1]]
        critDict[6] = [[1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1],
                       [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 1, 0],
                       [0, 0, 1, 0, 1], [0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 1], [0, 1, 0, 0, 0, 1],
                       [0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1]]
        critDict[7] = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 1]]
        critDict[8] = [[0, 0, 0, 0, 0, 0, 0]]

    elif (movecount == 9):
        critDict[5] = [[1, 1, 1, 1], [0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1],
                       [1, 1, 1, 0, 1]]
        critDict[6] = [[1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [1, 0, 1, 1, 0],
                       [1, 0, 1, 0, 1], [1, 0, 0, 1, 1], [0, 1, 1, 1, 0], [0, 1, 1, 0, 1],
                       [0, 1, 0, 1, 1], [0, 0, 1, 1, 1], [1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 1],
                       [1, 0, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1], [0, 1, 1, 0, 0, 1],
                       [0, 1, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1],
                       [0, 0, 1, 0, 1, 1], [0, 0, 0, 1, 1, 1]]
        critDict[7] = [[1, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0], [1, 0, 0, 1, 0, 0],
                       [1, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1],
                       [0, 0, 1, 1, 0, 0], [0, 0, 1, 0, 1, 0], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1],
                       [1, 0, 0, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 1],
                       [0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1, 1]]
        critDict[8] = [[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1]]
        critDict[9] = [[0, 0, 0, 0, 0, 0, 0, 0]]

    return critDict

def getCriticalVector(critDict, critChance, move, critVector):
    for i in critDict.keys():
        sum = 0
        for j in range(len(critDict[i])):
            product = 1
            for k in range(len(critDict[i][j])):
                if critDict[i][j][k] == 0:
                    product = product * (1 - critChance)
                else:
                    product = product * (critChance)
            sum += product
        critVector[i] = sum
    return critVector