import copy
import pandas as pd
import math
import numpy as np
import time
from collections import defaultdict

start_time = time.time()

# Current Season Index (number of years in - 1)
current_season = 1
smoothing_factor = 0  # This determines the degree of adjustment toward 0.5


# Load the CSV data
# Load the data
df = pd.read_csv('MC_games.csv')

# Define divisions and conferences
divisions = {
    'Bills': 'AFC East', 'Patriots': 'AFC East', 'Dolphins': 'AFC East', 'Jets': 'AFC East',
    'Browns': 'AFC North', 'Steelers': 'AFC North', 'Ravens': 'AFC North', 'Bengals': 'AFC North',
    'Broncos': 'AFC West', 'Chiefs': 'AFC West', 'Raiders': 'AFC West', 'Chargers': 'AFC West',
    'Texans': 'AFC South', 'Colts': 'AFC South', 'Jaguars': 'AFC South', 'Titans': 'AFC South',
    'Giants': 'NFC East', 'Eagles': 'NFC East', 'Cowboys': 'NFC East', 'Commanders': 'NFC East',
    'Rams': 'NFC West', 'Cardinals': 'NFC West', '49ers': 'NFC West', 'Seahawks': 'NFC West',
    'Lions': 'NFC North', 'Vikings': 'NFC North', 'Packers': 'NFC North', 'Bears': 'NFC North',
    'Falcons': 'NFC South', 'Panthers': 'NFC South', 'Saints': 'NFC South', 'Buccaneers': 'NFC South'
}

conferences = {
    'Bills': 'AFC', 'Patriots': 'AFC', 'Dolphins': 'AFC', 'Jets': 'AFC',
    'Browns': 'AFC', 'Steelers': 'AFC', 'Ravens': 'AFC', 'Bengals': 'AFC',
    'Broncos': 'AFC', 'Chiefs': 'AFC', 'Raiders': 'AFC', 'Chargers': 'AFC',
    'Texans': 'AFC', 'Colts': 'AFC', 'Jaguars': 'AFC', 'Titans': 'AFC',
    'Giants': 'NFC', 'Eagles': 'NFC', 'Cowboys': 'NFC', 'Commanders': 'NFC',
    'Rams': 'NFC', 'Cardinals': 'NFC', '49ers': 'NFC', 'Seahawks': 'NFC',
    'Lions': 'NFC', 'Vikings': 'NFC', 'Packers': 'NFC', 'Bears': 'NFC',
    'Falcons': 'NFC', 'Panthers': 'NFC', 'Saints': 'NFC', 'Buccaneers': 'NFC'
}

# Add division and conference columns to the DataFrame
df['home_team_division'] = df['homeTeam'].map(divisions)
df['away_team_division'] = df['awayTeam'].map(divisions)
df['home_team_conference'] = df['homeTeam'].map(conferences)
df['away_team_conference'] = df['awayTeam'].map(conferences)

# Clean the data
future_games = df[(df['stageIndex'] == 1) & (df['status'] == 1)]
test = df[(df['stageIndex'] == 1) & (df['status'] == 1)]
df = df[(df['stageIndex'] == 1) & (df['weekIndex'] < 18)]

# Create two separate dataframes for populating with games
df_current_season = df[(df['seasonIndex'] == max(df['seasonIndex']))]
df_simulated_season = df[(df['seasonIndex'] == max(df['seasonIndex']))]
current_season = max(df['seasonIndex'])  # Assuming you want to track the most recent season as the current season
print(current_season)


strength = {}

# Initialize a dictionary to store team records
team_records = {}

# Initialize a dictionary to store games
season_games = {}

# Process the data to calculate win/loss records
for index, row in df.iterrows():

    # Track game scores
    home_team = row['homeTeam']
    away_team = row['awayTeam']
    home_score = row['homeScore']
    away_score = row['awayScore']
    status = row['status']
    season_index = row['seasonIndex']

    if season_index == current_season:
        # Populate the games dictionary
        game_id = row['gameId']
        season_games[game_id] = {
            'home_team': row['homeTeam'],
            'away_team': row['awayTeam'],
            'home_score': row['homeScore'],
            'away_score': row['awayScore'],
            'season_index': row['seasonIndex'],
            'week_index':row['weekIndex'],
            'status': row['status']
        }

        
    # Create a dictionary to store team records
    if home_team not in team_records:
        team_records[home_team] = {
            'current_season': {
                'wins': 0, 'losses': 0, 'games': 0,
                'division_wins': 0, 'division_losses': 0,
                'conference_wins': 0, 'conference_losses': 0,
            },
            'previous_seasons': {'wins': 0, 'losses': 0, 'games': 0},
            'strength_of_schedule': 0,
        }
    if away_team not in team_records:
        team_records[away_team] = {
            'current_season': {
                'wins': 0, 'losses': 0, 'games': 0,
                'division_wins': 0, 'division_losses': 0,
                'conference_wins': 0, 'conference_losses': 0,
            },
            'previous_seasons': {'wins': 0, 'losses': 0, 'games': 0},
            'strength_of_schedule': 0,
        }
    if status > 1:
        # Update the records based on the scores
        if home_score > away_score:
            # Update current season records
            if season_index == current_season:
                team_records[home_team]['current_season']['wins'] += 1
                team_records[away_team]['current_season']['losses'] += 1
            elif season_index + 1 == current_season:
                team_records[home_team]['previous_seasons']['wins'] += 1
                team_records[away_team]['previous_seasons']['losses'] += 1

        elif home_score < away_score:
            if season_index == current_season:
                team_records[away_team]['current_season']['wins'] += 1
                team_records[home_team]['current_season']['losses'] += 1
            elif season_index + 1 == current_season:
                team_records[away_team]['previous_seasons']['wins'] += 1
                team_records[home_team]['previous_seasons']['losses'] += 1

        # Increment the game count for both teams
        if season_index == current_season:
            team_records[home_team]['current_season']['games'] += 1
            team_records[away_team]['current_season']['games'] += 1
        else:
            team_records[home_team]['previous_seasons']['games'] += 1
            team_records[away_team]['previous_seasons']['games'] += 1


# Calculating the total wins and losses for each team last season
for game_id, game in season_games.items():

    # Saving the home and away team names
    home_team = game['home_team']
    away_team = game['away_team']


    # Create a dictionary to store team records
    if home_team not in strength:
        strength[home_team] = {
            'wins': 0, 'losses': 0, 'games': 0,
        }
    if away_team not in strength:
        strength[away_team] = {
            'wins': 0, 'losses': 0, 'games': 0,
        }

    # Add wins and losses to strength dictionary
    strength[home_team]['wins'] += team_records[away_team]['previous_seasons']['wins']
    strength[away_team]['wins'] += team_records[home_team]['previous_seasons']['wins']
    strength[home_team]['losses'] += team_records[away_team]['previous_seasons']['losses']
    strength[away_team]['losses'] += team_records[home_team]['previous_seasons']['losses']

# Calculating the strength of schedule for each team
for team, record in team_records.items():
    record['strength_of_schedule'] += strength[team]['wins'] / (strength[team]['wins'] + strength[team]['losses'])


sorted_teams_records = sorted(
    team_records.items(), # Get items as (team, record)
    key = lambda x: x[1]['strength_of_schedule'], # Sort by strength of schedule
    reverse=True # Set reverse to True for descending order
)

# Creating a counter to list out the teams
counter = 1

# Debugging: Print Strength of Schedule
print("Strength of Schedule for Each Team:")
for team, record in sorted_teams_records:
    print(counter, f" {team}: {record['strength_of_schedule']:.3f}")
    counter += 1

print("\n\n\n")

# Initialize separate dictionaries for strength calculations
strength_early = {}
strength_late = {}

# Calculate total wins and losses for each team in two timeframes
for game_id, game in season_games.items():
    # Saving the home and away team names
    home_team = game['home_team']
    away_team = game['away_team']
    week_index = game['week_index']

    # Determine which dictionary to update
    if week_index <= 8:
        strength = strength_early
    elif 9 <= week_index <= 18:
        strength = strength_late
    else:
        continue  # Skip games outside the desired weeks

    # Initialize team records in the dictionary
    if home_team not in strength:
        strength[home_team] = {'wins': 0, 'losses': 0, 'games': 0}
    if away_team not in strength:
        strength[away_team] = {'wins': 0, 'losses': 0, 'games': 0}

    # Add wins and losses to the strength dictionary
    strength[home_team]['wins'] += team_records[away_team]['previous_seasons']['wins']
    strength[away_team]['wins'] += team_records[home_team]['previous_seasons']['wins']
    strength[home_team]['losses'] += team_records[away_team]['previous_seasons']['losses']
    strength[away_team]['losses'] += team_records[home_team]['previous_seasons']['losses']

# Update strength of schedule for each team
for timeframe, strength in [("Early Season (Weeks 0-8)", strength_early), ("Late Season (Weeks 9-18)", strength_late)]:
    for team, record in team_records.items():
        if team in strength:
            total_games = strength[team]['wins'] + strength[team]['losses']
            if total_games > 0:  # Avoid division by zero
                record[f'strength_of_schedule_{timeframe}'] = strength[team]['wins'] / total_games
            else:
                record[f'strength_of_schedule_{timeframe}'] = 0

    # Sort teams by the calculated strength of schedule
    sorted_teams_records = sorted(
        team_records.items(),
        key=lambda x: x[1].get(f'strength_of_schedule_{timeframe}', 0),
        reverse=True
    )

    # Display the results
    print(f"\nStrength of Schedule for {timeframe}:")
    counter = 1
    for team, record in sorted_teams_records:
        sos_value = record.get(f'strength_of_schedule_{timeframe}', 0)
        print(f"{counter}. {team}: {sos_value:.3f}")
        counter += 1