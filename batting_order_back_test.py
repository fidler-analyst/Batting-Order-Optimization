#batting_order_back_test
import pandas as pd
import numpy as np

df3 = pd.read_csv(r'C:\Users\maxfi\Desktop\Python\baseball\2021-mlb-season-pbp-feed.csv', usecols \
    = ['GAME ID', 'BATTER', 'PLAYTYPE', 'ROADSCORE', 'HOMESCORE', 'INNING'])
df3 = df3.dropna(axis = 0)

HOME = np.where(df3['INNING'] == 'B', 1, 0)
HOME_TEAM = df3['GAME ID'].str[10:13]      
ROAD_TEAM = df3['GAME ID'].str[6:9]
df3.insert(2, 'HM_TEAM', HOME_TEAM)
df3.insert(3, 'RD_TEAM', ROAD_TEAM)

df3.INNING = df3['INNING'].str[-1]

#df3 = df3.replace({'PLAYTYPE': {'SINGLE':1,'DOUBLE':2,'TRIPLE':3, 'HOME RUN':4, \
#'STRIKEOUT':0, 'FLYOUT':0, 'LINEOUT':0, 'POP OUT':0, 'GROUNDOUT':0, 'GROUNDED INTO DP':0, \
#'FORCEOUT':0, 'FIELD ERROR':1, 'FIELDERS CHOICE':0, 'DOUBLE PLAY':0, \
#'WALK':1, 'SAC BUNT':0, 'SAC FLY':0, 'HIT BY PITCH':1, 'CATCHER INTERFERENCE':1, 'INTENT WALK':1}})

    
home_games = df3[df3['HM_TEAM'] == 'COL']
home_games = home_games[home_games['INNING'] == 'B']

road_games = df3[df3['RD_TEAM'] == 'COL']
road_games = road_games[road_games['INNING'] == 'T']
    
#based off of weighted obp
best_lup = ['Yonathan Daza','C.J. Cron','Ryan McMahon','Joshua Fuentes',   \
            'Raimel Tapia','Charlie Blackmon','Garrett Hampson', 'Dom Nunez']
    
    
    
    

all_rocky_games = pd.concat([home_games, road_games])  
list_of_games = pd.Series(all_rocky_games['GAME ID']).drop_duplicates().to_list()

games_with_the_boys = []

for game in list_of_games:
    single_game = all_rocky_games[all_rocky_games['GAME ID'] == game]
    players_in_game = pd.Series(single_game['BATTER']).head(n=8)
    players_in_game.to_list()
   
    players_in_game_check = sorted(players_in_game)
    best_lup_check = sorted(best_lup)

    if players_in_game_check == best_lup_check:
        games_with_the_boys.append(game)

score_comparison = pd.DataFrame(index = games_with_the_boys, columns = ['Actual Score', 'My Model'])
    
for game in games_with_the_boys:
    game_with_my_order = all_rocky_games[all_rocky_games['GAME ID']==game]
    my_order_df = pd.DataFrame(index = best_lup, columns = ['1st', '2nd', '3rd', '4th'])
    
    for player in best_lup:
        player_df = game_with_my_order[game_with_my_order['BATTER']==player]
        player_df = player_df.reset_index(drop = True)
        my_order_df.loc[player, '1st'] = player_df.PLAYTYPE[0]
        my_order_df.loc[player, '2nd'] = player_df.PLAYTYPE[1]
        my_order_df.loc[player, '3rd'] = player_df.PLAYTYPE[2]
        my_order_df.loc[player, '4th'] = player_df.PLAYTYPE[3]    

    
    my_order_df.loc[len(my_order_df)] = ['STRIKEOUT', 'STRIKEOUT', 'STRIKEOUT', 'STRIKEOUT']
    my_order_df = my_order_df.rename(index={8:'Pitcher'})


    my_event_list = pd.Series()
    my_event_list = my_order_df['1st']
    my_event_list = my_event_list.append(my_order_df['2nd'])
    my_event_list = my_event_list.append(my_order_df['3rd'])
    my_event_list = my_event_list.append(my_order_df['4th'])

    inning = 1
    runs = 0
    outs = 0
    r1, r2, r3 = 0, 0, 0; 
    total_outs = 0
    
    for play in my_event_list:       
        
        if play == 'SINGLE':
            if r1 == 0:
                if r2 == 0:
                    if r3 == 0:
                        r1 = 1
                    else:
                        r1, r3 = 1, 0
                        runs += 1
                else:
                    if r3 == 0:
                        r1, r2 = 1, 0
                        runs +=1
                    else:
                        r1, r2, r3 = 1, 0, 0
                        runs += 2                    
            else:
                if r2 == 0:
                    if r3 == 0:
                        r2 = 1
                    elif r3 == 1:
                        r2, r3 = 1, 0
                        runs+=1
                elif r2 == 1:
                    if r3 == 0:
                        runs += 1
                    elif r3 == 1:
                        r3 = 0
                        runs += 2
                    
        elif play == 'DOUBLE':
            runs += r2 + r3
            if r1 == 1:
                r1, r2, r3 = 0, 1, 1
            else:
                r1, r2, r3 = 0, 1, 0
                
        elif play == 'TRIPLE':
            runs += r1 + r2 + r3
            r1, r2, r3 = 0, 0, 1
        
        elif play == 'HOME RUN':
            runs += r1 + r2 + r3 + 1
            r1, r2, r3 = 0, 0, 0
      
        elif play == 'FLYOUT':
            outs += 1            

        elif play == 'POP OUT':
            outs += 1            

        elif play == 'LINEOUT':
            outs += 1            
       
        elif play == 'WALK':
            if r1 == 0:
                if r2 == 0:
                    if r3 == 0:
                        r1 = 1
                    else:
                        r1, r3 = 1, 1
                else:
                    if r3 == 0:
                        r1, r2 = 1, 1
                    else:
                        r1, r2, r3 = 1, 1, 1           
            else:
                if r2 == 0:
                    if r3 == 0:
                        r2 = 1
                    elif r3 == 1:
                        r2, r3 = 1, 1
                elif r2 == 1:
                    if r3 == 0:
                        r3 = 1
                    elif r3 == 1:
                        runs += 1

        elif play == "INTENT WALK":
            if r1 == 0:
                if r2 == 0:
                    if r3 == 0:
                        r1 = 1
                    else:
                        r1, r3 = 1, 1
                else:
                    if r3 == 0:
                        r1, r2 = 1, 1
                    else:
                        r1, r2, r3 = 1, 1, 1           
            else:
                if r2 == 0:
                    if r3 == 0:
                        r2 = 1
                    elif r3 == 1:
                        r2, r3 = 1, 1
                elif r2 == 1:
                    if r3 == 0:
                        r3 = 1
                    elif r3 == 1:
                        runs += 1

        elif play == 'HIT BY PITCH':
            if r1 == 0:
                if r2 == 0:
                    if r3 == 0:
                        r1 = 1
                    else:
                        r1, r3 = 1, 1
                else:
                    if r3 == 0:
                        r1, r2 = 1, 1
                    else:
                        r1, r2, r3 = 1, 1, 1           
            else:
                if r2 == 0:
                    if r3 == 0:
                        r2 = 1
                    elif r3 == 1:
                        r2, r3 = 1, 1
                elif r2 == 1:
                    if r3 == 0:
                        r3 = 1
                    elif r3 == 1:
                        runs += 1

        elif play == 'SAC BUNT':
            #runs += 1
            outs += 1
            r3 = 0

        elif play == 'SAC FLY':
            runs += 1
            outs += 1
            r3 = 0
        
        elif play == 'FIELDERS CHOICE':
            outs += 1
            
        elif play == 'FORCEOUT':
            outs += 1        
        
        elif play == 'STRIKEOUT':
            outs += 1

        elif play == 'GROUNDOUT':
            outs += 1
            
        elif play == 'FIELD ERROR':
            if r1 == 0:
                r1 = 1
            elif r1 == 1:
                if r2 == 0:
                    r2 = 1
                elif r2 == 1:
                    if r3 == 0:
                        r3 = 1
                    elif r3 == 1:
                        runs +=1
        
        elif play == 'DOUBLE PLAY':
            outs += 2        
            r1, r2, r3 = 0, 0, 0
            
        elif play == 'GROUNDED INTO DP':
            outs += 2        
            r1, r2, r3 = 0, 0, 0

        if outs == 3:
            inning += 1
            outs = 0
            r1, r2, r3 = 0, 0, 0; 
         

 
    score_comparison.loc[game, 'Actual Score'] = single_game['HOMESCORE'].iloc[-1]
    score_comparison.loc[game, 'My Model'] = runs
 
        
        
        
        
        
        
        
        

score_comparison.to_excel(r'C:\Users\maxfi\Desktop\Python\baseball\Batting Order Optimizer\batting_order_back_test_results.xlsx')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        