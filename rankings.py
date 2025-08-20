import pandas as pd

# Read the CSV file
df = pd.read_csv('MC_games.csv')

# Filter to get regular season games (stageIndex == 1)
# and remove unplayed games (both scores are 0)
df = df[(df['stageIndex'] == 1) & ~((df['homeScore'] == 0) & (df['awayScore'] == 0))]

# Get a list of unique teams from both homeTeam and awayTeam columns
teams = pd.unique(df[['homeTeam', 'awayTeam']].values.ravel())

# Initialize a dictionary to store wins, losses, and ties for each team
records = {team: {'wins': 0, 'losses': 0, 'ties': 0} for team in teams}

# Iterate over each game to count outcomes
for _, row in df.iterrows():
    home_team = row['homeTeam']
    away_team = row['awayTeam']
    home_score = row['homeScore']
    away_score = row['awayScore']
    
    if home_score > away_score:
        records[home_team]['wins'] += 1
        records[away_team]['losses'] += 1
    elif home_score < away_score:
        records[away_team]['wins'] += 1
        records[home_team]['losses'] += 1
    else:  # it's a tie
        records[home_team]['ties'] += 1
        records[away_team]['ties'] += 1

# Convert the results dictionary to a DataFrame for display
results_df = pd.DataFrame.from_dict(records, orient='index')

# Calculate win percentage: wins + (ties/2) divided by total games played
results_df['win_percentage'] = (results_df['wins'] + results_df['ties'] / 2) / (results_df['wins'] + results_df['losses'] + results_df['ties']) * 100

# Sort by win percentage in descending order
results_df = results_df.sort_values(by='win_percentage', ascending=False)

print(results_df)
