# Readme.md
## About
* A poker simulator by Calvin Davidson (work in progress)
## Progress Notes
### Branches
* new -- most up to date, new features and work in progress
* master -- latest milestone
### In Progress
* Betting fundamental mechanics Pre Flop to River
* Thresholds on chips and removing players
* Side pots
* More complex decision making
* Add betting
    * Basic
        * only bet / call same amount all players for now.  Extend this later
        * folded player  = inactivity
        * figure out how to deal with players being knocked out.  Kill the game and make a new one might be easiest??
        * Side pots!  Keep this in mind as you're writing betting rules.  Need to deal with hard limits
    * Extend Player class with archetypes and rulesets for betting actions
    * Decisions.  Need to build functions to determine the following
        * Pre-Flop -- rate starting hand
        * Flop -- hand made? Number of outs?
        * Turn -- improvement? best hand? Number of outs?
        * River -- hand ranking
* Add statistic tracking
    * A class above Game() ?

### Complete
* Deck() class, build deck and dealing hands
* Analysing a 5 card hand
* Find the best hand out of 5 to 7 cards
* Comparing two hands, comparing multiple hands
* Game() class with loopable steps, storing all game info including instances of Player and Deck objects
* Rating for starting hands, outs on flop and turn, to predict

### Ideas to extend
* Visualise sorting algorithms
* Game based on influencing player emotions
* Machine Learning model for best decisions to refine player archetypes
