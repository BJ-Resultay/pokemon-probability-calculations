The basis of this program is the matchup() class. A matchup consists of the following:
    - pokemon1 and pokemon2: These are the indices for the first and second Pokemon involved in the
    matchup in the global list POKEMON_LIST. pokemon1 comes before pokemon2 alphabetically. This is
    mostly for looking up attributes specific to a Pokemon, like its stats.
    - pokemon1moves and pokemon2moves: These are dictionaries for the pokemon's movesets. The key is
     a Move object; the value is the move's damage vector.
    - winProbability: This should store the probability for pokemon1 to defeat pokemon2.

 1. dataInitialization()- Data is read in initially. We parse through the text files
(alphabeticalPokemon.txt, bot-data.txt, and moves.txt) and get the data we need; information on the
Pokemon and their stats, information on their matchups, moves, and damage values, and information on
 the moves themselves, including their hit rate. We store these lists in global variables
 MATCHUP_LIST, MOVE_LIST, and POKEMON_LIST.

 2. successVectorDriver()- We then call this function for every matchup. This function sorts a
 Pokemon's moves according to their best cases and creates a success vector one by one. It either
 calls SuccessDistribution or IrwinHall, depending on the best case. It then checks a list of
 conditions to determine whether or not it is worth looking for a better move within the moveset.

 3. successDistribution() and recursiveProb() are as you described them. They return the
 successVector of a given move; for example, a move with 40% 2HKO and 60% 3HKO is represented as
 [0, 0, 0.4, 0.6, 0, 0...]
 (The indexing begins at 0, but obviously, no battle can be won in 0 moves.)

 4. criticalRecalculation() uses a lookup table (in classes.py) to create a criticalVector based on
 the successVector and the Pokemon's individual critical hit rate (barring moves like Slash which
 already have that taken into account).

 5. moveSelector() simply chooses a move based on expected value, for now. I added in an "options"
 parameter, in case this function needs to be modified for the future (such as choosing different
 strategies, or avoiding using certain moves.)

 6. probabilityGivenTwoMoves() drives probFormula(), the calculation itself. probFormula() takes the
  faster and slower pokemon and applies Dr. Goldsmith's formula to yield a result between 0 and 1.

