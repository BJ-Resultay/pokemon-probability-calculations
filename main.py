# This program is designed to create a matchup matrix based on obtained data from the 81 fully-
# evolved Generation 1 Pokemon.

# Last edited Sep 2021

import numpy as np
import sys
import classes as c
import re
import time
import math
from math import comb
from statistics import mean
import csv
np.set_printoptions(threshold=sys.maxsize)

#FILE_PATH = "./"   # main branch
FILE_PATH = "./dummy-data/blizzard/"
NUM_POKEMON = sum((0 if line[0] == "\n" or line[0] == "#" else 1)
                  for line in open(FILE_PATH + "alphabetical-pokemon.txt", "r").readlines())
MAX_MOVES = 40
MOVES_LIST = []
POKEMON_LIST = []
MATCHUP_LIST = [[None for x in range(NUM_POKEMON)] for y in range(NUM_POKEMON)]

def printMatrix():
   for x in range(len(MATCHUP_LIST)):
      print("\n")
      for y in range(len(MATCHUP_LIST)):
         if MATCHUP_LIST[x][y] != None:
            print('1', end='')
         else: print('0', end='')
   return

#Returns the indeces of two pokemon in alphabetical order. Used for creating matchups.
def indexPokemon(p1, p2, pokeList):
   if p1 < p2:
      return pokeList.index(p1), pokeList.index(p2)
   else:
      return pokeList.index(p2), pokeList.index(p1)

#Reads the input text (i.e. "guaranteed 3HKO") and turns that into a useful integer.
def determineBestCase(text):
   if text[0].isnumeric(): ans = int(text[0])
   elif text == "OHKO": ans = 1
   else: ans = MAX_MOVES
   return ans

def parseDamageAmounts(line):
   damages = []
   for x in range(3, len(line)):
      num = re.sub("[^0-9]", "", line[x])
      if(not num.isnumeric()):
         return "Error"
      damages.append(int(num))
   return damages

# Takes one pair of lines from botData and inserts it into the matchup list.
def placeIntoMatchup(textline1, textline2, pokeList):
   p1 = textline1[0] #p1 is the attacking pokemon, p2 is defending.
   p2 = textline1[3]
   p2 = re.sub(r'[^\w\s]', '', p2) # A regex to remove the colon from p2's name
   # Regardless of who is attacking, we want the first alphabetical Pokemon to be first in our
   # index. For instance, Aerodactyl vs Alakazam and Alakazam vs Aerodactyl are both matchup [0][1].
   # Matchup [1][0] doesn't exist.
   firstP, secondP = indexPokemon(p1, p2, pokeList)
   # Create the matchup if it doesn't exist.
   if(MATCHUP_LIST[firstP][secondP] == None):
      m = c.Matchup(firstP, secondP)
      MATCHUP_LIST[firstP][secondP] = m

   bc = determineBestCase(textline1[len(textline1)-1])
   moveName = textline1[1]
   # This loop creates a Move object and, based on the data, decides which move it is and where to
   # put it.
   for x in MOVES_LIST:
      if x.name == moveName:
         move = c.Move(x.name, x.accuracy, x.isDamagingMove, bc)
         move.drawbacks = x.drawbacks
         move.statusAffliction = x.statusAffliction
         move.trapping = x.trapping
         if pokeList.index(p1) == firstP:
            MATCHUP_LIST[firstP][secondP].pokemon1moves[move] = textline2
         else:
            MATCHUP_LIST[firstP][secondP].pokemon2moves[move] = textline2
   return

#Reading in the data from the text files.
def dataInitialization():
   pokeTextPath = FILE_PATH + "alphabetical-pokemon.txt"
   moveTextPath = "moves.txt"
   botDataPath = FILE_PATH + "bot-data.txt"
   f = open(pokeTextPath)
   g = open(botDataPath)
   h = open(moveTextPath)
   pokeList = []
   speedList = []
   HPList = []
   critRateList = []

   #Create the array of Pokemon, including name, HP, speed, and crit chance.
   statsList = f.readlines()
   for p in range(0, len(statsList)):
      if statsList[p][0] == "\n" or statsList[p][0] == "#": continue
      statsList[p] = statsList[p].split()
      name = statsList[p][0]
      hp = int(statsList[p][1])
      spd = int(statsList[p][2])
      crit = float(statsList[p][3])
      pokemonToAppend = c.Pokemon(name, hp, spd, crit)

      POKEMON_LIST.append(pokemonToAppend)
      pokeList.append(statsList[p][0])
      HPList.append(int(statsList[p][1]))
      speedList.append(int(statsList[p][2]))
      critRateList.append(float(statsList[p][3]))

   # Creates the array of Moves, including name, accuracy, whether it's a damaging move, and other
   # things.
   # This is mostly just a template for when we create individual Moves for matchups later.
   moveData = h.readlines()
   for m in range(0, len(moveData)):
      moveData[m] = moveData[m].split()
      name = moveData[m][0]
      acc = int(moveData[m][1])
      isDamagingMove = moveData[m][2]
      moveToAdd = c.Move(name, acc, isDamagingMove, 0)
      # Here we're adding some flags to the moves, so we can easily look at their properties later.
      if name == "HyperBeam": moveToAdd.drawbacks.append("hyperbeam")
      elif name == "Explosion": moveToAdd.drawbacks.append("explosion")
      elif name == "Submission" or name == "DoubleEdge": moveToAdd.drawbacks.append("recoil")
      elif name == "Wrap" or name == "Bind" or name == "Clamp" or name == "FireSpin":
         moveToAdd.trapping = 1
      elif name == "ThunderWave" or name == "StunSpore" or name == "Glare":
         moveToAdd.statusAffliction["Paralysis"]=100
      elif name == "BodySlam": moveToAdd.statusAffliction["Paralysis"] = 30
      elif name == "Thunder" or name == "Thunderbolt": moveToAdd.statusAffliction["Paralysis"] = 10
      elif name == "SleepPowder" or name == "Spore" or name == "LovelyKiss" or name == "Hypnosis"\
              or name == "Sing":
         moveToAdd.statusAffliction["Sleep"] = 100
      elif name == "Sludge": moveToAdd.statusAffliction["Poison"] = 30
      elif name == "Toxic": moveToAdd.statusAffliction["Toxic"] = 100
      elif name == "Blizzard" or name == "IceBeam": moveToAdd.statusAffliction["Freeze"] = 10
      elif name == "Flamethrower": moveToAdd.statusAffliction["Burn"] = 10
      elif name == "FireBlast": moveToAdd.statusAffliction["Burn"] = 30
      elif name == "RazorLeaf" or name == "Crabhammer" or name=="Slash": moveToAdd.alwaysCritical=1
      #if acc < 100: moveToAdd.drawbacks.append("inaccurate")
      MOVES_LIST.append(moveToAdd)

   # Read in the matchup data.
   # We skip blank lines and lines dedicated to damage output, because when we read in the
   # initial line with the Pokemon and moves, we take the next line as well.
   botData = g.readlines()
   counter = 0
   print("Forming matchups...")
   for b in range(0, len(botData)):
      if botData[b] == "\n" or botData[b][0] == "Possible" or botData[b][0] == "#": continue
      botData[b] = botData[b].split()
      if(botData[b][0] in pokeList):
         counter += 1
         botData[b+1] = botData[b+1].split()
         damages = parseDamageAmounts(botData[b + 1])
         placeIntoMatchup(botData[b], damages, pokeList)

   # Closing our data files
   f.close()
   g.close()
   h.close()
   return


#Finds the success distribution of a single move
#Input: enemy HP, damage value vector, and best-case (given from file)
#Output: A vector of the success distribution for each move.
def successDistribution(HP, d, i):
   #print(HP, d, i)
   lookups = {}
   total = 0
   output = [0 for x in range(MAX_MOVES+1)]
   if(d[0] == 0) or (i > MAX_MOVES): return output
   while total < 1:
      if((HP, i) not in lookups):
         startTime = time.perf_counter()
         r = recursiveProb(HP, d, i, startTime)
         lookups[(HP, i)] = r
      else: r = lookups[(HP, i)]
      output[i] = r - total #We start with the lowest turn count.
      total = r
      i += 1
   del lookups

   return output

def recursiveProb(HP, d, i, startTime):
   currTime = time.perf_counter()
   t = currTime - startTime
   if(t > 10):
       return 0
   frac = HP/i
   if frac > max(d):
      return 0
   elif frac < min(d):
      return 1
   elif i == 1:
      s = 0
      for n in d:
         if n > HP: s += 1
      return s/39
   else:
      sum = 0
      for j in d:
         sum += recursiveProb(HP-j, d, i-1, startTime)/39
      return sum

#PDF Irwin Hall distribution
def IHPDF(n, x):
   result = 0
   for k in range(0, math.floor(x)):
      summand = pow(-1, k) * comb(n, k) * pow((x-k), (n-1))
      result += summand
   result = result * 1/(math.factorial(n-1))
   return result

#CDF Irwin Hall distribution
def IHCDF(n, x):
   result = 0
   for k in range(0, math.floor(x)):
      summand = pow(-1, k) * comb(n, k) * pow((x-k), n)
      result += summand
   result = result * 1/(math.factorial(n))
   return result

def irwinHall(HP, d, i):
   #print(HP, d, i)
   output = [0 for x in range(MAX_MOVES+1)]
   if (d[0] == 0) or (i > MAX_MOVES): return output
   sum = 0
   while sum < 1 and i <= MAX_MOVES:
      if min(d) * i > HP: p = 1
      else:
         m = mean(d)*i
         v = i*((max(d)-min(d))^2)/12
         if(v == 0):
            return output
         sd = (HP - m)/v
         xHP = i/2 + sd*i/12
         #this either needs to be the pdf or 1-cdf
         #p = IHPDF(i, xHP)
         p = 1 - IHCDF(i, xHP)
      output[i] = p - sum
      i += 1
      sum = p
   return output

def criticalRecalculation(move, pokemon):
   if(move.alwaysCritical) or move.bestCase > 9 or move.bestCase == 1:
      move.criticalVector = move.successVector
      return move.successVector
   move.criticalVector = [0 for x in range(MAX_MOVES)]
   cv = [0 for x in range(MAX_MOVES)]
   critChance = pokemon.critRate/100
   for x in range(len(move.successVector)):
      if(move.successVector[x] > 0):
         cv = [0 for x in range(MAX_MOVES)]
         critDict = c.getCritDictionary(x)
         cv = c.getCriticalVector(critDict, critChance, move, cv)
         for y in range(len(cv)):
            cv[y] = cv[y] * move.successVector[x]
         for y in range(len(move.criticalVector)):
            move.criticalVector[y] += cv[y]
   return move.criticalVector

def moveSelector(matchup, pokemon, option):
   # I guess this is where we can put changes regarding the 21 nonstandard move cases.
   # For now, it's just returning the highest expected value move.
   if option == "default":
      if(matchup.pokemon1 == pokemon):
         set = matchup.pokemon1moves
         sortedMoves = sorted(set, key=lambda Move: Move.bestCase)
         bestMove = sortedMoves[0]
      else:
         set = matchup.pokemon2moves
         sortedMoves = sorted(set, key=lambda Move: Move.bestCase)
         bestMove = sortedMoves[0]
      max = 0
      for m in set:
         sum = 0
         for x in range(1, len(m.successVector)):
            sum += m.successVector[x]/x
         sum = sum * m.accuracy/100
         if sum > max:
            bestMove = m
   return bestMove

# This drives the calls to SuccessDistribution. I
# It looks a little disgusting, but all it's really doing is gathering the necessary data to send
# to successDistribution and deciding whether to continue or not.
def successVectorDriver(matchup):
   #We sort the moves dictionary by best case to calculate the strongest moves first.
   p1MovesSorted = sorted(matchup.pokemon1moves, key=lambda Move: Move.bestCase)
   bestMove = p1MovesSorted[0]
   counter = 0
   for m in (p1MovesSorted):
      if(m.bestCase > (2.22 * bestMove.bestCase)):
         m.successVector = [0 for x in range(0, 39)]
         break
      enemyHP = POKEMON_LIST[matchup.pokemon2].HP
      moveDamage = matchup.pokemon1moves[m]
      bestCase = m.bestCase
      if bestCase <= 5:
         v = successDistribution(enemyHP, moveDamage, bestCase)
      else:
         v = irwinHall(enemyHP, moveDamage, bestCase)
      m.successVector = v
      criticalRecalculation(m, POKEMON_LIST[matchup.pokemon1])
      #print("Success vector", m.successVector)

      # Here we write the conditions for continuation. If one of these conditions are met,
      # we have a possible better move to examine. If not, we break and move on.
      if(counter < 3):
         condition1 = bool(len(m.drawbacks) > 0)
         if(counter < len(p1MovesSorted)):
            condition2 = bool(counter < len(p1MovesSorted) and p1MovesSorted[counter + 1].bestCase <=
                           m.bestCase)
         else: condition2 = False
         if(p1MovesSorted[counter + 1].accuracy > m.accuracy):
            if (p1MovesSorted[counter + 1].accuracy - m.accuracy) <= 10:
                  condition3 = bool(abs(p1MovesSorted[counter + 1].bestCase - m.bestCase) <= 1)
            else:
                  condition3 = bool(abs(p1MovesSorted[counter + 1].bestCase - m.bestCase) <= 2)
         else: condition3 = False
         condition4 = bool(p1MovesSorted[counter + 1].trapping == 1)
      else: condition1, condition2, condition3, condition4 = False, False, False, False
      if not (condition1 or condition2 or condition3 or condition4):
         break
      counter += 1

   # This is a repeat of the past 2 blocks, but for the defending Pokemon.
   counter = 0
   p2MovesSorted = sorted(matchup.pokemon2moves, key=lambda Move: Move.bestCase)
   bestMove = p2MovesSorted[0]
   for m in p2MovesSorted:
      #print(counter, p2MovesSorted[counter].name)
      if (m.bestCase > (2.22 * bestMove.bestCase)):
         m.successVector = [0 for x in range(0, 39)]
         break
      enemyHP = POKEMON_LIST[matchup.pokemon1].HP
      moveDamage = matchup.pokemon2moves[m]
      bestCase = m.bestCase
      if bestCase <= 5:
         v = successDistribution(enemyHP, moveDamage, bestCase)
      else:
         v = irwinHall(enemyHP, moveDamage, bestCase)
      m.successVector = v
      criticalRecalculation(m, POKEMON_LIST[matchup.pokemon1])
      #print("Success vector", m.successVector)

      # Here we're writing the conditions for continuation. If one of these conditions are met,
      # we have a possible better move to examine. If not, we break and move on.
      if (counter < 3):
         condition1 = bool(len(m.drawbacks) > 0)
         if(counter < len(p2MovesSorted)):
            condition2 = bool(counter < len(p2MovesSorted) and p2MovesSorted[counter + 1].bestCase <=
                           m.bestCase)
         else: condition2 = False
         if (p2MovesSorted[counter + 1].accuracy > m.accuracy):
            if (p2MovesSorted[counter + 1].accuracy - m.accuracy) <= 10:
                  condition3 = bool(abs(p2MovesSorted[counter + 1].bestCase - m.bestCase) <= 1)
            else:
                  condition3 = bool(abs(p2MovesSorted[counter + 1].bestCase - m.bestCase) <= 2)
         else: condition3 = False
         condition4 = bool(p2MovesSorted[counter + 1].trapping == 1)
      else: condition1, condition2, condition3, condition4 = False, False, False, False

      if not (condition1 or condition2 or condition3 or condition4):
         break
      counter += 1
   return

# This is the function that calls Dr. Goldsmith's formula.
# As of right now I haven't tested it fully...
def probabilityGivenTwoMoves(matchup, p1move, p2move):
   p1speed = POKEMON_LIST[matchup.pokemon1].speed
   p2speed = POKEMON_LIST[matchup.pokemon2].speed
   if(p1speed >= p2speed):
      result = probFormula(p1move, p2move)
   elif(p2speed > p1speed):
      result = 1 - probFormula(p2move, p1move)
   matchup.winProbability = result
   return result

# The formula itself. Given a faster move and a slower move, with their success vectors and best
# cases, it decides the probability that the faster one wins.
# Or at least it should.
def probFormula(fasterMove, slowerMove):
   #a = fasterMove.accuracy/100
   successVector1 = fasterMove.criticalVector
   #b = slowerMove.accuracy/100
   successVector2 = slowerMove.criticalVector
   result = 0
   counter = 0
   n = MAX_MOVES
   for x in range(len(successVector1)):
      if (successVector1[x] > 0 and x < MAX_MOVES):
         #print("x=", x)
         for y in range(len(successVector2)):
            if (successVector2[y] > 0 and y < MAX_MOVES):
               counter += 1
               #print("y=", y)
               a = fasterMove.accuracy / 100 * successVector1[x]
               b = slowerMove.accuracy / 100 * successVector2[y]
               # Here is the implementation of Dr. Goldsmith's formula.
               outerSum = 0
               for t in range(x, n):
                  factor1 = (a * comb(t - 1, x - 1) * math.pow(a, x - 1) * math.pow(1 - a, t - 1 - (
                             x - 1)))
                  innerSum = 0
                  for i in range(0, y - 1):
                     innerSum += (comb(t, i) * math.pow(b, i) * math.pow(1 - b, t - i))
                  outerSum += factor1 * innerSum
               result += outerSum
   if(counter > 0):
      result = result/counter
   else:
      result = 0.0
   return result


if __name__ == '__main__':
   print("Hello!")
   start = time.perf_counter()
   print("Reading data from files...")
   dataInitialization()

   resultsMatrix = [[0 for x in range(NUM_POKEMON)] for y in range(NUM_POKEMON)]

   print("Calculating success vectors...")
   counter = 0
   for x in range(0, len(MATCHUP_LIST)):
      for y in range(x+1, len(MATCHUP_LIST)):
         counter += 1
         print("Matchup", counter, "...")
         print(POKEMON_LIST[x].name, POKEMON_LIST[y].name)
         
         if MATCHUP_LIST[x][y] is None:
            continue
         successVectorDriver(MATCHUP_LIST[x][y])

         m = moveSelector(MATCHUP_LIST[x][y], MATCHUP_LIST[x][y].pokemon1, "default")
         n = moveSelector(MATCHUP_LIST[x][y], MATCHUP_LIST[x][y].pokemon2, "default")

         r = probabilityGivenTwoMoves(MATCHUP_LIST[x][y], m, n)
         print("Result of this matchup:", r, "\n")
         resultsMatrix[x][y] = r
         
   filename = FILE_PATH + "results.csv"
   header = ([vars(pokemon)["name"] for pokemon in POKEMON_LIST])
   with open(filename, 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(header)
      csvwriter.writerows(resultsMatrix)

   print("Done!")
   stop = time.perf_counter()
   print("Elapsed time:", stop-start, "seconds")
