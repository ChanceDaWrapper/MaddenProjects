import pandas as pd
import numpy as np

# Read the CSV file
passing = pd.read_csv('Data/MC_passing.csv')
rushing = pd.read_csv('Data/MC_rushing.csv')
receiving = pd.read_csv('Data/MC_receiving.csv')
defense = pd.read_csv('Data/MC_defense.csv')
df = pd.read_csv('Data/MC_players.csv')


df_rec = receiving
df_pass = passing
df_rush = rushing
df_def = defense

print("\n\nIn the regression system\n\n")
#Renaming columns in the receiving for WRs dataframe
df_rec_adjust = df_rec[['player__fullName', 'recTotalTDs', 'recTotalYds', 'recTotalCatches', 'player__position']]
df_rec_adjust = df_rec_adjust.rename(columns={"player__fullName" : "fullName"})

#Renaming columns in the passing dataframe
df_pass = df_pass[['player__fullName', 'passTotalTDs', 'passTotalYds', 'passTotalInts', 'passerAvgRating', 'passAvgCompPct', 'passTotalAtt']]
df_pass = df_pass.rename(columns={"player__fullName" : "fullName"})

#Renaming columns in the rushing dataframe
df_rush = df_rush[['player__fullName', 'player__position', 'rushTotalYds', 'rushTotalTDs']]
df_rush = df_rush.rename(columns={"player__fullName" : "fullName"})


#Renaming columns in the defense dataframe
#Some slight adjustments for each specific position will be done later one
df_def = df_def[['player__fullName', 'player__position', 'defTotalDeflections', 'defTotalForcedFum', 'defTotalInts', 'defTotalSacks', 'defTotalTDs', 'defTotalTackles']]
df_def = df_def.rename(columns={"player__fullName" : "fullName"})


"""
QUARTERBACKS
"""


df2 = df[df['position'] == 'QB']  # Selecting rows where position is 'QB'
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']]  # Selecting relevant columns for QBs

# Merging the players' names (for dev traits) and the passing stats dataframes
df_QB_merged = pd.merge(df_pass, df2)  # Merging passing stats with QB player names

# Importing the rushing data so we can also look at QB rushing stats
df_rushQB = df_rush[df_rush['player__position'] == 'QB']  # Splitting the rushing dataframe
df_rushQB = df_rushQB[['fullName', 'rushTotalYds', 'rushTotalTDs']]  # Selecting relevant columns

# Merging the QB passing and rushing stats into the main dataframe
df_QB_merged = pd.merge(df_QB_merged, df_rushQB)  # Merging QB passing and rushing stats with QB player names

# Define weights for QB performance metrics
weights = {
    'passTotalYds': 0.2,     # Weight for passing yards
    'passTotalTDs': 0.3,     # Weight for passing touchdowns
    'passTotalInts': -0.25,   # Negative weight for interceptions
    'passerAvgRating': 0.15,  # Weight for passer rating
    'passAvgCompPct': 0.01,  # Weight for completion percentage
    'passTotalAtt': -0.01,   # Weight for passing attempts
    'rushTotalYds': 0.1,     # Weight for rushing yards
    'rushTotalTDs': 0.15      # Weight for rushing touchdowns
}

# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_QB_merged.columns:
        min_val = df_QB_merged[stat].min()
        max_val = df_QB_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_QB_merged[f'{stat}_score'] = (df_QB_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_QB_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_QB_merged['All_Pro_Score'] = sum(
    df_QB_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_QB_merged.columns
)

# Rank QBs by All-Pro Score
df_QB_merged = df_QB_merged.sort_values(by='All_Pro_Score', ascending=False)

# Rename columns for better readability
df_QB_merged = df_QB_merged.rename(columns={
    'fullName': 'Full Name',
    'team': 'Team',
    'passTotalYds': 'Passing Yards',
    'passTotalTDs': 'Passing TDs',
    'passTotalInts': 'Passing INTs',
    'passerAvgRating': 'Passer Rating',
    'rushTotalYds': 'Rushing Yards',
    'rushTotalTDs': 'Rushing TDs'
})

# Select the top 5 QBs for the All-Pro list
all_pro_qbs = df_QB_merged[['Full Name', 'Team', 'Passing Yards', 'Passing TDs', 'Passing INTs', 
                            'Passer Rating', 'Rushing Yards', 'Rushing TDs', 'All_Pro_Score']].head(10)

# Display the All-Pro Quarterbacks
print("\n\nAll-Pro Quarterbacks:\n\n")
print(all_pro_qbs)



"""
RUNNNINGBACKS
"""

df2 = df[df['position'] == 'HB'] # Selecting rows where position is 'HB'
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']] # Selecting relevant columns for HBs

# Merging the players' names (for dev traits) and the passing stats dataframes
df_HB_merged = pd.merge(df_rush, df2)  # Merging passing stats with HB player names

# Importing the rushing data so we can also look at HB rushing stats
df_recHB = df_rec_adjust[df_rec_adjust['player__position'] == 'HB']  # Splitting the rushing dataframe

df_recHB = df_recHB[['fullName', 'recTotalCatches', 'recTotalYds', 'recTotalTDs']]  # Selecting relevant columns

# Merging the HB passing and rushing stats into the main dataframe
df_HB_merged = pd.merge(df_HB_merged, df_recHB)  # Merging HB passing and rushing stats with HB player names

weights = {
    'rushTotalYds': 0.35,     # Heavier weight for rushing yards
    'rushTotalTDs': 0.30,     # More focus on rushing touchdowns
    'recTotalYds': 0.10,      # Reduced emphasis on receiving yards
    'recTotalTDs': 0.10       # Reduced emphasis on receiving touchdowns
}


# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_HB_merged.columns:
        min_val = df_HB_merged[stat].min()
        max_val = df_HB_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_HB_merged[f'{stat}_score'] = (df_HB_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_HB_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_HB_merged['All_Pro_Score'] = sum(
    df_HB_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_HB_merged.columns
)

# Rank QBs by All-Pro Score
df_HB_merged = df_HB_merged.sort_values(by='All_Pro_Score', ascending=False)

# Select the top 10
all_pro_hbs = df_HB_merged[['fullName', 'team', 'rushTotalYds', 'rushTotalTDs', 'recTotalCatches', 'recTotalYds', 'recTotalTDs', 'All_Pro_Score']]

print("\n\nAll-Pro Runningbacks:\n\n")
print(all_pro_hbs)

""" 
WIDE RECEIVERS
"""

df2 = df[df['position'] == 'WR']  # Selecting rows where position is 'QB'
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']]  # Selecting relevant columns for QBs

# Merging the players' names (for dev traits) and the passing stats dataframes
df_WR_merged = pd.merge(df_rec_adjust, df2)  # Merging passing stats with QB player names

# Importing the rushing data so we can also look at QB rushing stats
df_rushWR = df_rush[df_rush['player__position'] == 'WR']  # Splitting the rushing dataframe
df_rushWR = df_rushWR[['fullName', 'rushTotalYds', 'rushTotalTDs']]  # Selecting relevant columns

# Merging the QB passing and rushing stats into the main dataframe
df_WR_merged = pd.merge(df_WR_merged, df_rushWR)  # Merging QB passing and rushing stats with QB player names

# Define weights for QB performance metrics
weights = {
    'recTotalCatches': 0.05,   # Reduce catches if reliability is less critical
    'recTotalYds': 0.40,       # Small reduction for more balanced grading
    'recTotalTDs': 0.40,       # Balance touchdowns with yards
    'rushTotalYds': 0.075,     # Increase rushing contribution slightly
    'rushTotalTDs': 0.075      # Reward rushing touchdowns more
}


# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_WR_merged.columns:
        min_val = df_WR_merged[stat].min()
        max_val = df_WR_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_WR_merged[f'{stat}_score'] = (df_WR_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_WR_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_WR_merged['All_Pro_Score'] = sum(
    df_WR_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_WR_merged.columns
)

# Rank QBs by All-Pro Score
df_WR_merged = df_WR_merged.sort_values(by='All_Pro_Score', ascending=False)

# Select the top 5 QBs for the All-Pro list
all_pro_wrs = df_WR_merged[['fullName', 'team', 'recTotalCatches', 'recTotalYds', 'recTotalTDs', 
                            'rushTotalYds', 'rushTotalTDs', 'All_Pro_Score']].head(10)

# Display the All-Pro Quarterbacks
print("\n\nAll-Pro Wide Receivers:\n\n")
print(all_pro_wrs)



""" 
TIGHT ENDS
"""

df2 = df[df['position'] == 'TE']  # Selecting rows where position is 'QB'
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']]  # Selecting relevant columns for QBs

# Merging the players' names (for dev traits) and the passing stats dataframes
df_TE_merged = pd.merge(df_rec_adjust, df2)  # Merging passing stats with QB player names

# Importing the rushing data so we can also look at QB rushing stats
df_rushTE = df_rush[df_rush['player__position'] == 'TE']  # Splitting the rushing dataframe
df_rushTE = df_rushTE[['fullName', 'rushTotalYds', 'rushTotalTDs']]  # Selecting relevant columns

# Merging the QB passing and rushing stats into the main dataframe
df_TE_merged = pd.merge(df_TE_merged, df_rushTE)  # Merging QB passing and rushing stats with QB player names

# Define weights for QB performance metrics
weights = {
    'recTotalCatches': 0.1,   # Reduce catches if reliability is less critical
    'recTotalYds': 0.425,       # Small reduction for more balanced grading
    'recTotalTDs': 0.45,       # Balance touchdowns with yards
    'rushTotalYds': 0.05,     # Increase rushing contribution slightly
    'rushTotalTDs': 0.05      # Reward rushing touchdowns more
}


# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_TE_merged.columns:
        min_val = df_TE_merged[stat].min()
        max_val = df_TE_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_TE_merged[f'{stat}_score'] = (df_TE_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_TE_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_TE_merged['All_Pro_Score'] = sum(
    df_TE_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_TE_merged.columns
)

# Rank QBs by All-Pro Score
df_TE_merged = df_TE_merged.sort_values(by='All_Pro_Score', ascending=False)

# Select the top 5 QBs for the All-Pro list
all_pro_tes = df_TE_merged[['fullName', 'team', 'recTotalCatches', 'recTotalYds', 'recTotalTDs', 
                            'rushTotalYds', 'rushTotalTDs', 'All_Pro_Score']].head(10)

# Display the All-Pro Quarterbacks
print("\n\nAll-Pro Tight Ends:\n\n")
print(all_pro_tes)

"""
EDGE RUSHERS
"""

# Filter the main dataframe for edge rushers
df2 = df[df['position'].isin(['LE', 'RE'])]  # Selecting rows where position is DE or OLB
# df2 = df2[df2['weight'] < 285]
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']]  # Selecting relevant columns

# Merge the defensive stats with player data
df_edge_merged = pd.merge(df_def, df2, left_on='fullName', right_on='fullName')  # Merge by player name

# Define weights for edge rusher performance metrics
weights = {
    'defTotalSacks': 0.4,       # Heavily weight sacks as primary metric
    'defTotalForcedFum': 0.2,   # Significant weight for forced fumbles
    'defTotalTackles': 0.2,     # Reward total tackles as a measure of activity
    'defTotalTDs': 0.1,         # Smaller weight for rare defensive touchdowns
    'defTotalDeflections': 0.1  # Smaller weight for pass deflections
}

# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_edge_merged.columns:
        min_val = df_edge_merged[stat].min()
        max_val = df_edge_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_edge_merged[f'{stat}_score'] = (df_edge_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_edge_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_edge_merged['All_Pro_Score'] = sum(
    df_edge_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_edge_merged.columns
)

# Rank edge rushers by All-Pro Score
df_edge_merged = df_edge_merged.sort_values(by='All_Pro_Score', ascending=False)

# Select the top edge rushers for the All-Pro list
all_pro_des = df_edge_merged[[
    'fullName', 'team', 'defTotalSacks', 'defTotalForcedFum', 
    'defTotalTackles', 'defTotalTDs', 'defTotalDeflections', 'All_Pro_Score']].head(10)

# Display the All-Pro Edge Rushers
print("\n\nAll-Pro Defensive Ends:\n\n")
print(all_pro_des)


"""
EDGE RUSHERS
"""

# Filter the main dataframe for edge rushers
df2 = df[df['position'].isin(['DT'])]  # Selecting rows where position is DE or OLB
# df2 = df2[df2['weight'] < 285]
df2 = df2[['portraitId', 'fullName', 'team', 'position', 'age']]  # Selecting relevant columns

# Merge the defensive stats with player data
df_dt_merged = pd.merge(df_def, df2, left_on='fullName', right_on='fullName')  # Merge by player name

# Define weights for edge rusher performance metrics
weights = {
    'defTotalSacks': 0.4,       # Heavily weight sacks as primary metric
    'defTotalForcedFum': 0.2,   # Significant weight for forced fumbles
    'defTotalTackles': 0.2,     # Reward total tackles as a measure of activity
    'defTotalTDs': 0.1,         # Smaller weight for rare defensive touchdowns
    'defTotalDeflections': 0.1  # Smaller weight for pass deflections
}

# Normalize stats to a 0-100 scale
for stat in weights.keys():
    if stat in df_dt_merged.columns:
        min_val = df_dt_merged[stat].min()
        max_val = df_dt_merged[stat].max()
        if max_val != min_val:  # Avoid division by zero
            df_dt_merged[f'{stat}_score'] = (df_dt_merged[stat] - min_val) / (max_val - min_val) * 100
        else:
            df_dt_merged[f'{stat}_score'] = 0  # Assign zero if all values are the same

# Calculate composite scores for All-Pro ranking
df_dt_merged['All_Pro_Score'] = sum(
    df_dt_merged[f'{stat}_score'] * weight for stat, weight in weights.items() if f'{stat}_score' in df_dt_merged.columns
)

# Rank edge rushers by All-Pro Score
df_dt_merged = df_dt_merged.sort_values(by='All_Pro_Score', ascending=False)

# Select the top edge rushers for the All-Pro list
all_pro_dts = df_dt_merged[[
    'fullName', 'team', 'defTotalSacks', 'defTotalForcedFum', 
    'defTotalTackles', 'defTotalTDs', 'defTotalDeflections', 'All_Pro_Score']].head(10)

# Display the All-Pro Edge Rushers
print("\n\nAll-Pro Defensive Tackles:\n\n")
print(all_pro_dts)

