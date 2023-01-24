### Hyper Beam
If Hyper Beam connects, the user must spend the next turn doing nothing.
There is no penalty for using Hyper Beam if it knocks out the opponent,
so reducing the damage by half is not an accurate measurement.
If a move has more than half the expected utility of Hyper Beam,
that move should be used until Hyper Beam has at least a 55% chance to KO the opponent.
Otherwise, a staggered distribution for Hyper Beam must be calculated.

### Explosion
Explosion instantly knocks out the user.
Explosion should only be used if the user has a less than 50% chance to win without using it,
on the turn that maximizes utility (utility is equal to
.5\*(remaining available utility)\*(probability of knocking out opponent)).

### Wrap, Bind, Fire Spin, and Clamp
These moves trap the opponent.
If the user moves before the opponent, and the attack connects,
the opponent will be unable to attack for several iterations of this move.
However, moving second will allow the opponent a chance to strike.
This makes calculating the distributions for these moves quite complicated.
What’s more, this distribution should be compared against the alternative if the user knows another attack.

### Agility
If the user knows Agility, AND the user knows Wrap or Bind or Fire Spin or Clamp, AND the opponent has a higher speed than the user,
the user should use Agility (doubling its current speed) until it outspeeds the opponent.
This will need to be part of the trapping move routine and, again,
will need to be compared against the result of any appealing alternative.

### Blizzard
If Blizzard hits, it has a 10% chance to render the opponent frozen, operatively knocking them out instantly.
The success distribution can be calculated similarly to how critical hits are calculated.

### Thunder Wave, Glare, and Stun Spore
Renders the opponent paralyzed.
This reduces the current speed of the opponent to 75% and similarly multiplies all accuracy values by 75% for opponent’s subsequent turns.
These moves also have to pass an accuracy check.
There are three possible strategies: do not use, use once, and use until successful.
Because the opponent’s speed is affected, these moves interact with the trapping move strategy.

### Sleep Powder, Sing, Hypnosis, Lovely Kiss, and Spore
Renders the opponent asleep.
A sleeping pokemon cannot be paralyzed, and vice versa.
A sleeping pokemon cannot move until it is no longer asleep, which happens after 1 to 7 turns, determined randomly.
A slower pokemon than the user may be inert indefinitely, similarly to the trapping moves.
There are three strategies as with paralysis-causing moves, but unlike paralysis-causing moves,
the strategy must be reselected when the opponent wakes up.

### Substitute
The user sacrifices 25% of its own HP.
Until the opponent deals a cumulative total of at least that much damage, the user takes no additional damage.

### Recover and Soft-boiled
The user restores 50% of its own HP.
An opponent that has no trapping move and is unable to deal more than 25% damage automatically loses against the user.
Otherwise, attack-recover-attack-recover...

### Rest
The user fully restores its own HP, then does nothing for the next two turns.
An opponent that has no trapping move and is unable to deal more than 25% damage automatically loses.
Otherwise, attack-rest-nothing-nothing-attack-rest-nothing- nothing...

### Double-Edge and Submission
These attacks damage the user proportionally to the damage dealt to the opponent.

### Amnesia
Any ”special” attacks used by the user AND the opponent will need to have their distributions recalculated.
Amnesia can be used up to three times, leading to four possible strategies, each with a distinct set of outcomes.
Note that the critical mechanic prevents simply halving the number of successes needed.

### Swords Dance
Any ”physical” attacks used by the user will need to have distribution recalculated.
Swords Dance can be used up to three times, leading to four possible strategies, each with a distinct set of outcomes.
Note that the critical mechanic prevents simply halving the number of successes needed.

### Fire Blast and Flamethrower
If the opponent is neither paralyzed nor asleep when these attacks connect, there is a chance the opponent will be burned.
This reduces damage for the opponent’s ”physical” moves and steadily deals additional damage.

### Body Slam, Thunderbolt, and Thunder
If the opponent is not asleep, it can be paralyzed by these attacks.

### Mega Drain
The user restores an amount of HP proportional to the damage dealt.

### Toxic
The opponent will be badly poisoned, steadily taking increasing damage.

### Confuse Ray
The opponent will be confused.

### Counter
If the opponent uses a Normal-type attack or Fighting-type attack, the user takes the hit and deals double damage.

### Super Fang
Super Fang deals half of the opponent’s current HP.
It should be used until another move’s expected value exceeds half the opponent’s current HP.

### Psychic
Chance of lowering the opponent’s Special stat.
If this happens, damage distribution of Psychic and of opponent’s Special moves will be altered.
