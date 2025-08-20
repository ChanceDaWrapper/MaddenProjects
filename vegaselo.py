import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the CSV data
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

# Map divisions and conferences
df['home_team_division'] = df['homeTeam'].map(divisions)
df['away_team_division'] = df['awayTeam'].map(divisions)

# Clean the data
df = df[(df['stageIndex'] > 0) & (df['weekIndex'] < 24)]

# Initialize ELO Ratings (start with 1500 for all teams)
elo_ratings = {team: 1500 for team in divisions.keys()}
k_factor = 20  # Determines how much a game affects ratings

def update_elo(home_team, away_team, home_score, away_score):
    # Calculate expected scores
    home_elo = elo_ratings[home_team]
    away_elo = elo_ratings[away_team]
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home

    # Calculate actual results
    actual_home = 1 if home_score > away_score else 0.5 if home_score == away_score else 0
    actual_away = 1 - actual_home

    # Update ELO ratings
    elo_ratings[home_team] += k_factor * (actual_home - expected_home)
    elo_ratings[away_team] += k_factor * (actual_away - expected_away)

# Process games to update ELO ratings
for _, row in df.iterrows():
    if row['status'] > 1:  # Only process completed games
        update_elo(row['homeTeam'], row['awayTeam'], row['homeScore'], row['awayScore'])

# Add ELO ratings to the dataframe
df['home_elo'] = df['homeTeam'].map(elo_ratings)
df['away_elo'] = df['awayTeam'].map(elo_ratings)

# Feature Engineering
df['elo_diff'] = df['home_elo'] - df['away_elo']
df['point_diff'] = df['homeScore'] - df['awayScore']

# Train/Test Split
features = ['elo_diff']
target = 'point_diff'
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and Evaluate
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f}")

# Example Prediction
def predict_week(week_index, season_index):
    week_games = df[(df['weekIndex'] == week_index) & (df['seasonIndex'] == season_index)]
    predictions = []
    for _, game in week_games.iterrows():
        home_team = game['homeTeam']
        away_team = game['awayTeam']
        elo_diff = elo_ratings[home_team] - elo_ratings[away_team]
        predicted_point_diff = model.predict([[elo_diff]])[0]
        # Calculate win probability using ELO difference
        win_probability = 1 / (1 + 10 ** (-elo_diff / 400))
        predictions.append({
            'home_team': home_team,
            'away_team': away_team,
            'predicted_point_diff': predicted_point_diff,
            'home_team_win_probability': win_probability * 100,
            'away_team_win_probability': (1 - win_probability) * 100
        })
    return predictions

# Predict a week
selected_week = 6
selected_season = max(df['seasonIndex'])
week_predictions = predict_week(selected_week-1, selected_season)
for prediction in week_predictions:
    print(f"Game: {prediction['home_team']} vs {prediction['away_team']}, Predicted Point Difference: {prediction['predicted_point_diff']:+.1f}")
    print(f"Win Probability - {prediction['home_team']}: {prediction['home_team_win_probability']:.1f}%, {prediction['away_team']}: {prediction['away_team_win_probability']:.1f}%")
