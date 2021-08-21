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
rockies = ['Garrett Hampson','Raimel Tapia', 'Charlie Blackmon','Elias Diaz',  \
            'Ryan McMahon', 'C.J. Cron','Brendan Rodgers',  'Trevor Story']
#rockies player data frame  
rockies_df = pd.DataFrame(index = rockies, columns = ['1st', '2nd', '3rd', '4th'])


for rocky in rockies:    
    #creates a dataframe of the players appearances
    player_df = df2.loc[df2['BATTER'] == rocky]
    #creates a list of the game id's that they've played
    player_games = pd.Series(player_df['GAME ID']).drop_duplicates().to_list()
    #a blank df to collect all of their games and appearances
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
        
        
array = list(range(0, 32))      
pot_lup = pd.DataFrame()
lup_counter = 0
pot_lup_eval = pd.Series()
test_lup = pd.Series(index = array, dtype = float)
lup_df = pd.DataFrame()

for egt in rockies:
    test_lup[0], test_lup[8], test_lup[16], test_lup[24] = rockies_df.loc[egt, '1st'], rockies_df.loc[egt, '2nd'], rockies_df.loc[egt, '3rd'], rockies_df.loc[egt, '4th']
    sev_left = [x for x in rockies if x != egt]
    
    for sev in sev_left:
        test_lup[1], test_lup[9], test_lup[17], test_lup[25] = rockies_df.loc[sev, '1st'], rockies_df.loc[sev, '2nd'], rockies_df.loc[sev, '3rd'], rockies_df.loc[sev, '4th']
        six_left = [x for x in sev_left if x != sev]
        
        for six in six_left:
            test_lup[2], test_lup[10], test_lup[18], test_lup[26] = rockies_df.loc[six, '1st'], rockies_df.loc[six, '2nd'], rockies_df.loc[six, '3rd'], rockies_df.loc[six, '4th']
            fiv_left = [x for x in six_left if x != six]

            for fiv in fiv_left:
                test_lup[3], test_lup[11], test_lup[19], test_lup[27] = rockies_df.loc[fiv, '1st'], rockies_df.loc[fiv, '2nd'], rockies_df.loc[fiv, '3rd'], rockies_df.loc[fiv, '4th']
                frr_left = [x for x in fiv_left if x != fiv]

                for frr in frr_left:
                    test_lup[4], test_lup[12], test_lup[20], test_lup[28] = rockies_df.loc[frr, '1st'], rockies_df.loc[frr, '2nd'], rockies_df.loc[frr, '3rd'], rockies_df.loc[frr, '4th']
                    tre_left = [x for x in frr_left if x != frr]

                    for tre in tre_left:
                        test_lup[5], test_lup[13], test_lup[21], test_lup[29] = rockies_df.loc[tre, '1st'], rockies_df.loc[tre, '2nd'], rockies_df.loc[tre, '3rd'], rockies_df.loc[tre, '4th']
                        two_left = [x for x in tre_left if x != tre]

                        for two in two_left:
                            test_lup[6], test_lup[14], test_lup[22], test_lup[30] = rockies_df.loc[two, '1st'], rockies_df.loc[two, '2nd'], rockies_df.loc[two, '3rd'], rockies_df.loc[two, '4th']
                            one_left =  [x for x in two_left if x != two]
                            
                            for one in one_left:
                                test_lup[7], test_lup[15], test_lup[23], test_lup[31] = rockies_df.loc[one, '1st'], rockies_df.loc[one, '2nd'], rockies_df.loc[one, '3rd'], rockies_df.loc[one, '4th']
                                evaluation = 0                                                                                                                             
                                lup = [egt, sev, six, fiv, frr, tre, two, one]
                               
                                for i in list(range(0, 31)):
                                        evaluation += test_lup.iloc[i]*test_lup.iloc[i+1]                                
                               
                                pot_lup.insert(lup_counter, lup_counter, test_lup)
                                pot_lup_eval.loc[lup_counter] = evaluation                            
                                lup_df.insert(lup_counter, lup_counter, lup)
                                lup_counter+=1

best_lup_idx = pot_lup_eval.idxmax()
best_lup_s = pot_lup[best_lup_idx]

FINAL_LUP = pd.DataFrame(index = lup_df[best_lup_idx], columns = ['1st', '2nd', '3rd', '4th'])
r1 = best_lup_s[0:8].to_list()
r2 = best_lup_s[8:16].to_list()
r3 = best_lup_s[16:24].to_list()
r4 = best_lup_s[24: :].to_list()
FINAL_LUP['1st'] = r1
FINAL_LUP['2nd'] = r2
FINAL_LUP['3rd'] = r3
FINAL_LUP['4th'] = r4


FINAL_LUP.to_excel(r'C:\Users\maxfi\Desktop\Python\baseball\Batting Order Optimizer\batting_order_optimizer_results.xlsx')
print(FINAL_LUP)