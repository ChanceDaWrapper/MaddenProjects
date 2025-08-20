import copy
import pandas as pd
import math
import numpy as np
import time
from collections import defaultdict
import pandas as pd

start_time = time.time()

# Current Season Index (number of years in - 1)
smoothing_factor = 0  # This determines the degree of adjustment toward 0.5
selected_week = int(input("Input the week you'd like check:\n"))  # For example, set to the week number you want to process


# Create a folder for generated images
import os
if not os.path.exists("predictions_images"):
    os.makedirs("predictions_images")

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
df = df[(df['stageIndex'] > 0) & (df['weekIndex'] < 24)]
df = df[(df['seasonIndex'] > (df['seasonIndex'] - 1))]
current_season = max(df['seasonIndex'])  # Assuming you want to track the most recent season as the current season
print(current_season)
# Example selected week
selected_week -= 1
# Initialize dictionaries for team records and all games
team_records = {}
season_games = {}
# Initialize counters for home and away wins
home_wins = 0
away_wins = 0

# Process data to calculate PPG and PAPG using all games
for index, row in df.iterrows():
    home_team = row['homeTeam']
    away_team = row['awayTeam']
    home_score = row['homeScore']
    away_score = row['awayScore']
    status = row['status']
    season_index = row['seasonIndex']

    game_id = row['gameId']
    season_games[game_id] = {
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score,
        'season_index': season_index,
        'status': status,
        'week_index': row['weekIndex']
    }

    # Initialize team records if not already present
    if home_team not in team_records:
        team_records[home_team] = {'points_scored': 0, 'points_allowed': 0, 'games': 0}
    if away_team not in team_records:
        team_records[away_team] = {'points_scored': 0, 'points_allowed': 0, 'games': 0}

    # Update stats only if the game was played
    if status > 1:
        team_records[home_team]['points_scored'] += home_score
        team_records[home_team]['points_allowed'] += away_score
        team_records[away_team]['points_scored'] += away_score
        team_records[away_team]['points_allowed'] += home_score
        team_records[home_team]['games'] += 1
        team_records[away_team]['games'] += 1
        if home_score > away_score:
            home_wins += 1
        elif away_score > home_score:
            away_wins += 1

# Calculate PPG and PAPG for each team using all games
for team, record in team_records.items():
    games_played = record['games']
    if games_played > 0:
        record['ppg'] = record['points_scored'] / games_played
        record['papg'] = record['points_allowed'] / games_played
    else:
        record['ppg'] = 0
        record['papg'] = 0

    

# Function to calculate weighted prediction
def weighted_prediction(ppg_a, papg_b, ppg_b, papg_a, previous_games, weight=1.5):
    if previous_games > 0:
        return (
            (ppg_a + papg_b) * weight / (weight + 1),
            (ppg_b + papg_a) * weight / (weight + 1)
        )
    else:
        return (ppg_a + papg_b) / 2, (ppg_b + papg_a) / 2



# Function to calculate scores from all previous matchups
def calculate_scores_from_matchups(home_team, away_team, previous_games):
    """Aggregate all previous matchups between two teams."""
    home_points_scored = 0
    away_points_scored = 0
    games_played = 0

    for game in previous_games:
        # Check if the two teams were participants in the game
        if (
            (game['home_team'] == home_team and game['away_team'] == away_team) or
            (game['home_team'] == away_team and game['away_team'] == home_team)
        ) and game['status'] > 1:
            # Accumulate scores, aligning with the current home/away roles
            if game['home_team'] == home_team:
                home_points_scored += game['home_score']
                away_points_scored += game['away_score']
            else:
                home_points_scored += game['away_score']
                away_points_scored += game['home_score']
            games_played += 1

    # Calculate averages from previous matchups if they exist
    if games_played > 0:
        home_ppg = home_points_scored / games_played
        away_ppg = away_points_scored / games_played
    else:
        home_ppg, away_ppg = 0, 0  # No previous matchups found

    return home_ppg, away_ppg, games_played





# Initialize a list to store game predictions
game_predictions = []

# Predict scores for the selected week
for game_id, game in season_games.items():
    # Include scheduled games for prediction
    if game['week_index'] == selected_week and game['season_index'] == current_season:
        home_team = game['home_team']
        away_team = game['away_team']

        # Check for previous matchups and calculate matchup-specific scores
        prev_home_ppg, prev_away_ppg, prev_games = calculate_scores_from_matchups(home_team, away_team, season_games.values())

        # Get season-wide PPG and PAPG
        home_ppg, home_papg = team_records[home_team]['ppg'], team_records[home_team]['papg']
        away_ppg, away_papg = team_records[away_team]['ppg'], team_records[away_team]['papg']

        # Blend previous matchups with season-wide stats
        if prev_games > 0:
            weight_prev = 2  # Weight for previous matchups
            weight_season = 1  # Weight for season-wide stats
            total_weight = weight_prev + weight_season  # Total weight for normalization
            
            # Blend PPG values
            predicted_home_score = ((home_ppg * weight_season) + (prev_home_ppg * weight_prev)) / total_weight
            predicted_away_score = ((away_ppg * weight_season) + (prev_away_ppg * weight_prev)) / total_weight
            
        else:
            predicted_home_score, predicted_away_score = weighted_prediction(
                home_ppg, away_papg, away_ppg, home_papg, prev_games
            )

        # Calculate the expected spread
        expected_spread = predicted_home_score - predicted_away_score

        # Save the game prediction in a list
        game_predictions.append({
            'game_id': game_id,
            'home_team': home_team,
            'away_team': away_team,
            'predicted_home_score': predicted_home_score,
            'predicted_away_score': predicted_away_score,
            'expected_spread': expected_spread,
        })

# Sort predictions by closest spreads
sorted_predictions = sorted(game_predictions, key=lambda x: abs(x['expected_spread']), reverse=True)

# Display the sorted predictions
print("\nPredicted Games Sorted by Closest Spreads:")
for prediction in sorted_predictions:
    home_team = prediction['home_team']
    away_team = prediction['away_team']
    predicted_home_score = prediction['predicted_home_score']
    predicted_away_score = prediction['predicted_away_score']
    expected_spread = prediction['expected_spread']

    favored_team = home_team if expected_spread > 0 else away_team
    rounded_spread = round(expected_spread * 2) / 2
    rounded_over_under = round((predicted_home_score + predicted_away_score) * 2) / 2

    print(f"Game: {away_team} @ {home_team}")
    print(f"Predicted Score - {away_team}: {predicted_away_score:.2f}, {home_team}: {predicted_home_score:.2f}")
    print(f"Expected Spread: {favored_team} by -{abs(rounded_spread):.1f}")
    print(f"Over/Under Spread: {rounded_over_under}")
    print("\n" + "-" * 40 + "\n")


