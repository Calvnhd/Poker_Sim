# Readme.md
## About
* A poker simulator by Calvin Davidson (work in progress)
## Progress Notes
### Branches
* new -- most up to date, new features and work in progress
* master -- latest milestone
### In Progress
* Extend make_hands() to include playing the board
* Make rounds loopable
    * Extend Player class with all changing info, and store players in a list to iterate through and update each round
    * Create Game class with all info, including player list etc
* Add betting
    * Basic
    * Extend Player class with archetypes and rulesets for betting actions
* Add statistic tracking
    * bake into Game class (tbc)
### Complete
* Deck builder and dealing hands
* Analysing a 5 card hand
* Find the best hand out of 5 to 7 cards
* Comparing two hands, comparing multiple hands
* Single game (not looped), no betting
### Ideas to extend
* Visualise sorting algorithms
* Game based on influencing player emotions
* Machine Learning model for best decisions to refine player archetypes
