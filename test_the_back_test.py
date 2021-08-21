#test the back-test


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
#home_games = df3[df3['HM_TEAM'] == 'COL']
home_games = df3[df3['INNING'] == 'B']



list_of_games = pd.Series(home_games['GAME ID']).drop_duplicates().tail(n=200).to_list()



score_comparison = pd.DataFrame(index = list_of_games, columns = ['Actual Score', 'My Model'])

for game in list_of_games:
    single_game = home_games[home_games['GAME ID'] == game]
    
    score_comparison.loc[game, 'Actual Score'] = single_game['HOMESCORE'].iloc[-1]
    
    inning = 1
    runs = 0
    outs = 0
    r1, r2, r3 = 0, 0, 0; 
    plays = single_game['PLAYTYPE']
    

    
    for play in plays:       
        
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
            
            
        if outs >= 3:
            inning += 1
            outs = 0
            r1, r2, r3 = 0, 0, 0; 
         
    score_comparison.loc[game, 'My Model'] = runs


difference = (score_comparison['Actual Score'] - score_comparison['My Model'])
print(difference.mean(), difference.std())


         