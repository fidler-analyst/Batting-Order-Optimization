import pandas as pd

#df1 is composed of all the game id's, batters, and play types
df1 = pd.read_csv(r'C:\Users\maxfi\Desktop\Python\baseball\2021-mlb-season-pbp-feed.csv', usecols \
    = ['GAME ID', 'BATTER', 'PLAYTYPE'])
df1 = df1.dropna(axis = 0)


#df2 replaces the play type with the number of bases earned by that playtype
df2 = df1.replace({'PLAYTYPE': {'SINGLE':1,'DOUBLE':2,'TRIPLE':3, 'HOME RUN':4, \
'STRIKEOUT':0, 'FLYOUT':0, 'LINEOUT':0, 'POP OUT':0, 'GROUNDOUT':0, 'GROUNDED INTO DP':0, \
'FORCEOUT':0, 'FIELD ERROR':1, 'FIELDERS CHOICE':0, 'DOUBLE PLAY':0, \
'WALK':1, 'SAC BUNT':0, 'SAC FLY':0, 'HIT BY PITCH':1, 'CATCHER INTERFERENCE':1, 'INTENT WALK':1}})


#rockies lineup
rockies = ['Raimel Tapia', 'Brendan Rodgers', 'Charlie Blackmon', 'Trevor Story', 'C.J. Cron', \
           'Elias Diaz', 'Sam Hilliard', 'Joshua Fuentes']
#rockies player data frame  
rockies_df = pd.DataFrame(index = rockies, columns = ['1st', '2nd', '3rd', '4th'])


for rocky in rockies:
    #set counter of appearance number
    #Fst, Scd, Thd, Fth = 0, 0, 0, 0
    
    #creates a dataframe of the players appearances
    player_df = df2.loc[df2['BATTER'] == rocky]
    #creates a list of the game id's
    player_games = pd.Series(player_df['GAME ID']).drop_duplicates().to_list()
    player_games_df = pd.DataFrame()
    for game in player_games:
        #creates a dataframe of the appearances for the individual game
        player_game_df = player_df.loc[player_df['GAME ID'] == game]
        player_game_df.reset_index(inplace = True)
        player_game_df.drop(columns = ['index', 'GAME ID', 'BATTER'], inplace = True)
        player_games_df = pd.concat([player_games_df, player_game_df], axis = 1, ignore_index = True)
        
        #store the mean number of bases by appearance number in rockies_df
    rockies_df.loc[rocky, '1st'] = player_games_df.iloc[0].mean()
    rockies_df.loc[rocky, '2nd'] = player_games_df.iloc[1].mean()
    rockies_df.loc[rocky, '3rd'] = player_games_df.iloc[2].mean()
    rockies_df.loc[rocky, '4th'] = player_games_df.iloc[3].mean()
        
        
        
