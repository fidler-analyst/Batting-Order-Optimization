# This project serves to optimize the batting lineup of a team
# specifically, we are looking at how the performance of individual players
# varies in consecutive plate appearances. For example, how one does in their
# first vs their second plate appearance, etc. The idea is you would want 
# players that perform well in same number appearance to hit back to back, thus
# linking the hits to generate more runs


# All 8! lineups are evaluated, and the best one is that with the highest sum
# product within the lineup of whichever baseball statist used.

# The model works as follows, the 8 players of interest are plugged into the
# batting_order_optimizer, it will then calculate their wOBA for their consecutive plate appearances and put it into a table.
# It will then turns this table into a single array and iterate through all 8! combinations of players and output
# the best order. Best is determined by that with the highest sum product.

# This lineup is then run through batting_order_back_test. All the games where 
# those same 8 players start are used, and then the order of them is changed to 
# match the generated lineup. This is then run through the game simulator which
# by going through the PLAYTYPE events, determines how many runs would have been scored.
# This is then compared to what actually occured.
