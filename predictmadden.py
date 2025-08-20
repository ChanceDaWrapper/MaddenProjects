import copy
import pandas as pd
import math
import numpy as np
import time
from collections import defaultdict

start_time = time.time()

# Current Season Index (number of years in - 1)
smoothing_factor = 0  # This determines the degree of adjustment toward 0.5
iterations = 1000

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
        }
    if away_team not in team_records:
        team_records[away_team] = {
            'current_season': {
                'wins': 0, 'losses': 0, 'games': 0,
                'division_wins': 0, 'division_losses': 0,
                'conference_wins': 0, 'conference_losses': 0,
            },
            'previous_seasons': {'wins': 0, 'losses': 0, 'games': 0},
        }
    if status > 1:
        # Update the records based on the scores
        if home_score > away_score:
            # Update current season records
            if season_index == current_season:
                team_records[home_team]['current_season']['wins'] += 1
                team_records[away_team]['current_season']['losses'] += 1
                if row['home_team_division'] == row['away_team_division']:
                    team_records[home_team]['current_season']['division_wins'] += 1
                    team_records[away_team]['current_season']['division_losses'] += 1
                if row['home_team_conference'] == row['away_team_conference']:
                    team_records[home_team]['current_season']['conference_wins'] += 1
                    team_records[away_team]['current_season']['conference_losses'] += 1
            else:
                team_records[home_team]['previous_seasons']['wins'] += 1
                team_records[away_team]['previous_seasons']['losses'] += 1
        elif home_score < away_score:
            if season_index == current_season:
                team_records[away_team]['current_season']['wins'] += 1
                team_records[home_team]['current_season']['losses'] += 1
                if row['home_team_division'] == row['away_team_division']:
                    team_records[away_team]['current_season']['division_wins'] += 1
                    team_records[home_team]['current_season']['division_losses'] += 1
                if row['home_team_conference'] == row['away_team_conference']:
                    team_records[away_team]['current_season']['conference_wins'] += 1
                    team_records[home_team]['current_season']['conference_losses'] += 1
            else:
                team_records[away_team]['previous_seasons']['wins'] += 1
                team_records[home_team]['previous_seasons']['losses'] += 1

        # Increment the game count for both teams
        if season_index == current_season:
            team_records[home_team]['current_season']['games'] += 1
            team_records[away_team]['current_season']['games'] += 1
        else:
            team_records[home_team]['previous_seasons']['games'] += 1
            team_records[away_team]['previous_seasons']['games'] += 1

# print("\n\n" + "-" * 40 + "\n\n")
# print(team_records)
# print("\n\n" + "-" * 40 + "\n\n")
# print(season_games)
# print("\n\n" + "-" * 40 + "\n\n")



# for team, record in team_records.items():
#     current_season_record = record['current_season']
#     previous_seasons_record = record['previous_seasons']
    
#     # Calculate current season win percentage
#     current_win_percentage = current_season_record['wins'] / current_season_record['games'] if current_season_record['games'] > 0 else 0
    
#     # Calculate past seasons win percentage
#     past_win_percentage = previous_seasons_record['wins'] / previous_seasons_record['games'] if previous_seasons_record['games'] > 0 else 0
    
#     # Store the win percentages in the record
#     record['current_win_percentage'] = current_win_percentage
#     record['past_win_percentage'] = past_win_percentage

#     # Calculate the overall win percentage as an average of the current and past win percentages
#     if current_season_record['games'] == 0:
#         record['win_percentage'] = (1 - smoothing_factor) * past_win_percentage + smoothing_factor * 0.5
#     else:
#         # Average current and past win percentages
#         initial_win_percentage = (current_win_percentage + past_win_percentage) / 2
        
#         # Adjust the win percentage slightly toward 0.5
#         record['win_percentage'] = (1 - smoothing_factor) * initial_win_percentage + smoothing_factor * 0.5

#     # Debugging print to see the adjusted win percentage
#     # print(f"Team: {team}")
#     # print(f"Initial Win Percentage: {past_win_percentage}")
#     # print(f"Adjusted Win Percentage (toward 0.5): {record['win_percentage']}")
#     # print("\n" + "-" * 40 + "\n")


custom_win_percentages = {
    'Bills': 0.88,
    'Patriots': 0.77,
    'Dolphins': 0.24,
    'Jets': 0.65,
    'Browns': 0.77,
    'Steelers': 0.24,
    'Ravens': 0.41,
    'Bengals': 0.12,
    'Broncos': 0.29,
    'Chiefs': 0.59,
    'Raiders': 0.47,
    'Chargers': 0.71,
    'Texans': 0.24,
    'Colts': 0.47,
    'Jaguars': 0.9,
    'Titans': 0.35,
    'Giants': 0.82,
    'Eagles': 0.41,
    'Cowboys': 0.24,
    'Commanders': 0.65,
    'Rams': 0.1,
    'Cardinals': 0.47,
    '49ers': 0.1,
    'Seahawks': 0.88,
    'Lions': 0.59,
    'Vikings': 0.47,
    'Packers': 0.65,
    'Bears': 0.35,
    'Falcons': 0.65,
    'Panthers': 0.35,
    'Saints': 0.53,
    'Buccaneers': 0.53,
}


for team, record in team_records.items():
    current_season_record = record['current_season']
    previous_seasons_record = record['previous_seasons']
    
    # Get custom win percentage if available
    custom_win_pct = custom_win_percentages.get(team, None)
    
    if custom_win_pct is not None:
        # Use the custom win percentage
        record['win_percentage'] = custom_win_pct
    else:
        # Calculate current season win percentage
        current_win_percentage = (
            current_season_record['wins'] / current_season_record['games']
            if current_season_record['games'] > 0 else 0
        )
        
        # Calculate past seasons win percentage
        past_win_percentage = (
            previous_seasons_record['wins'] / previous_seasons_record['games']
            if previous_seasons_record['games'] > 0 else 0
        )
        
        # Store the win percentages in the record
        record['current_win_percentage'] = current_win_percentage
        record['past_win_percentage'] = past_win_percentage
        
        # Calculate the overall win percentage as an average of the current and past win percentages
        if current_season_record['games'] == 0:
            record['win_percentage'] = (
                (1 - smoothing_factor) * past_win_percentage + smoothing_factor * 0.5
            )
        else:
            # Average current and past win percentages
            initial_win_percentage = (
                current_win_percentage + past_win_percentage
            ) / 2
            
            # Adjust the win percentage slightly toward 0.5
            record['win_percentage'] = (
                (1 - smoothing_factor) * initial_win_percentage + smoothing_factor * 0.5
            )




def point_sort(tied_teams, season_games):

    # Initialize a dictionary to store points totals for each team in tied_teams
    team_points = {team[0]: 0 for team in tied_teams}

    # Iterate over each game row in the DataFrame to accumulate points
    for index, row in df_current_season.iterrows():
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        home_score = row['homeScore']
        away_score = row['awayScore']

        # Add points only for teams in tied_teams
        if home_team in team_points:
            team_points[home_team] += home_score
        if away_team in team_points:
            team_points[away_team] += away_score

    # Sort tied teams by their total points scored in descending order
    sorted_tied_teams = sorted(tied_teams, key=lambda x: team_points[x[0]], reverse=True)

    # print("\n\n" + "-" * 40 + "\n\n")
    # print("Sorted by Point Total:\n", team_points)
    # print("\n\n" + "-" * 40 + "\n\n")

    return sorted_tied_teams


def conference_sort(tied_teams, season_games):
    # Sort teams by conference win percentage
    sorted_teams = sorted(
        tied_teams,
        key=lambda x: (
            x[1].get('conference', 0) / 
            (x[1].get('conference_wins', 0) + x[1].get('conference_losses', 0))
            if (x[1].get('conference_wins', 0) + x[1].get('conference_losses', 0)) > 0
            else 0
        ),
        reverse=True
    )
    # print("\n\n" + "-" * 40 + "\n\n")
    # print("Sorted by conference Win Percentage:\n", sorted_teams)
    # print("\n\n" + "-" * 40 + "\n\n")

    # Check for ties in conference win percentage
    conference_ties = {}
    for team, stats in sorted_teams:
        conference_win_percentage = (
            stats.get('conference_wins', 0) / 
            (stats.get('conference_wins', 0) + stats.get('conference_losses', 0))
            if (stats.get('conference_wins', 0) + stats.get('conference_losses', 0)) > 0
            else 0
        )
        if conference_win_percentage not in conference_ties:
            conference_ties[conference_win_percentage] = []
        conference_ties[conference_win_percentage].append((team, stats))

    # Process each group of tied teams with common_games_sort if needed
    final_sorted_teams = []
    for conference_win_percentage, tied_group in conference_ties.items():
        if len(tied_group) > 1:  # Only process further if there is a tie
            sorted_group = point_sort(tied_group, season_games)
            final_sorted_teams.extend(sorted_group)
        else:
            final_sorted_teams.extend(tied_group)
    
    return final_sorted_teams

# def common_games_sort(tied_teams, season_games):
#     # Initialize dictionary to store common games results alongside original stats
#     common_games_results = {team[0]: {'wins': 0, 'games': 0, 'original_stats': team[1]} for team in tied_teams}

#     # Step 1: Identify common opponents for all tied teams
#     for i in range(len(tied_teams)):
#         team_a = tied_teams[i][0]
#         common_opponents = set()
        
#         # Collect all opponents that each tied team has faced
#         for game_id, game in season_games.items():
#             if game['home_team'] == team_a:
#                 common_opponents.add(game['away_team'])
#             elif game['away_team'] == team_a:
#                 common_opponents.add(game['home_team'])

#         # Step 2: Filter games where each tied team played against any common opponent
#         for team in [t[0] for t in tied_teams]:
#             for game_id, game in season_games.items():
#                 if (game['home_team'] == team and game['away_team'] in common_opponents) or \
#                    (game['away_team'] == team and game['home_team'] in common_opponents):
                    
#                     # Determine the winner
#                     home_team = game['home_team']
#                     away_team = game['away_team']
#                     home_score = game['home_score']
#                     away_score = game['away_score']

#                     if home_score > away_score:
#                         winner = home_team
#                     elif away_score > home_score:
#                         winner = away_team
#                     else:
#                         winner = None  # Tie game

#                     # Record win/loss for the current team
#                     if winner == team:
#                         common_games_results[team]['wins'] += 1

#                     # Increment games count for the team
#                     common_games_results[team]['games'] += 1

#     # Step 3: Calculate win percentages for each team against common opponents
#     for team in common_games_results:
#         games = common_games_results[team]['games']
#         wins = common_games_results[team]['wins']
#         common_games_results[team]['original_stats']['common_games_win_percentage'] = wins / games if games > 0 else 0

#     # Step 4: Sort tied teams by the calculated win percentage for common games
#     sorted_teams = sorted(common_games_results.items(), key=lambda x: x[1]['original_stats']['common_games_win_percentage'], reverse=True)

#     # Step 5: Check for ties in win percentage and group them
#     grouped_by_percentage = {}
#     for team, stats in sorted_teams:
#         win_percentage = stats['original_stats']['common_games_win_percentage']
#         if win_percentage not in grouped_by_percentage:
#             grouped_by_percentage[win_percentage] = []
#         grouped_by_percentage[win_percentage].append((team, stats['original_stats']))

#     # Step 6: Process each group; sort by conference if win percentages are tied
#     final_sorted_teams = []
#     for win_percentage, teams_with_same_percentage in grouped_by_percentage.items():
#         if len(teams_with_same_percentage) > 1:
#             # Call conference_sort if there is a tie in win percentages
#             sorted_group = conference_sort(teams_with_same_percentage, season_games)
#             final_sorted_teams.extend(sorted_group)
#         else:
#             final_sorted_teams.extend(teams_with_same_percentage)

#     # Remove common_games_win_percentage after sorting
#     for _, data in common_games_results.items():
#         if 'common_games_win_percentage' in data['original_stats']:
#             del data['original_stats']['common_games_win_percentage']

#     # Return final sorted list
#     return final_sorted_teams





def divisional_sort(tied_teams, season_games):
    # Sort teams by divisional win percentage
    sorted_teams = sorted(
        tied_teams,
        key=lambda x: (
            x[1].get('division_wins', 0) / 
            (x[1].get('division_wins', 0) + x[1].get('division_losses', 0))
            if (x[1].get('division_wins', 0) + x[1].get('division_losses', 0)) > 0
            else 0
        ),
        reverse=True
    )
    # print("\n\n" + "-" * 40 + "\n\n")
    # print("Sorted by Divisional Win Percentage:\n", sorted_teams)
    # print("\n\n" + "-" * 40 + "\n\n")

    # Check for ties in divisional win percentage
    divisional_ties = {}
    for team, stats in sorted_teams:
        division_win_percentage = (
            stats.get('division_wins', 0) / 
            (stats.get('division_wins', 0) + stats.get('division_losses', 0))
            if (stats.get('division_wins', 0) + stats.get('division_losses', 0)) > 0
            else 0
        )
        if division_win_percentage not in divisional_ties:
            divisional_ties[division_win_percentage] = []
        divisional_ties[division_win_percentage].append((team, stats))

    # Process each group of tied teams with common_games_sort if needed
    final_sorted_teams = []
    for division_win_percentage, tied_group in divisional_ties.items():
        if len(tied_group) > 1:  # Only process further if there is a tie
            sorted_group = conference_sort(tied_group, season_games)
            final_sorted_teams.extend(sorted_group)
        else:
            final_sorted_teams.extend(tied_group)
    
    return final_sorted_teams


def head_to_head(tied_teams, season_games):
    head_to_head_results = {team[0]: {'wins': 0, 'games': 0} for team in tied_teams}
    
    # Loop through each pair of tied teams
    for i in range(len(tied_teams)):
        team_a = tied_teams[i][0]
        for j in range(i + 1, len(tied_teams)):
            team_b = tied_teams[j][0]
            
            # Find games where team_a and team_b played each other in season_games
            for game_id, game in season_games.items():
                home_team = game['home_team']
                away_team = game['away_team']
                home_score = game['home_score']
                away_score = game['away_score']
                
                # Check if this game was a head-to-head matchup between team_a and team_b
                if (home_team == team_a and away_team == team_b) or (home_team == team_b and away_team == team_a):
                    # Determine the winner
                    if home_score > away_score:
                        winner = home_team
                    elif away_score > home_score:
                        winner = away_team
                    else:
                        winner = None  # In case of a tie

                    # Record win/loss
                    if winner == team_a:
                        head_to_head_results[team_a]['wins'] += 1
                    elif winner == team_b:
                        head_to_head_results[team_b]['wins'] += 1
                    
                    # Increment games count for both teams
                    head_to_head_results[team_a]['games'] += 1
                    head_to_head_results[team_b]['games'] += 1
    
    # Calculate win percentages for each team
    for team in head_to_head_results:
        games = head_to_head_results[team]['games']
        wins = head_to_head_results[team]['wins']
        head_to_head_results[team]['win_percentage'] = wins / games if games > 0 else 0

    # Sort tied teams by win percentage
    sorted_teams = sorted(head_to_head_results.items(), key=lambda x: x[1]['win_percentage'], reverse=True)

    # print("\n\n" + "-" * 40 + "\n\n")
    # print("Sorted by Head to Head Win Percentage:\n", sorted_teams)
    # print("\n\n" + "-" * 40 + "\n\n")

    # Identify remaining ties by win percentage
    ties = {}
    for team, stats in sorted_teams:
        win_percentage = stats['win_percentage']
        if win_percentage not in ties:
            ties[win_percentage] = []
        ties[win_percentage].append((team, tied_teams[[t[0] for t in tied_teams].index(team)][1]))  # Include full stats here

    # Process each group of tied teams with divisional_sort if needed
    final_sorted_teams = []
    for win_percentage, tied_group in ties.items():
        if len(tied_group) > 1:  # Only process further if there is a tie
            # Run divisional_sort on tied teams with full stats
            sorted_group = divisional_sort(tied_group, season_games)
            final_sorted_teams.extend(sorted_group)
        else:
            final_sorted_teams.extend(tied_group)
    
    return final_sorted_teams



def sort_teams(teams, season_games):
    # print("\n\n--- Initial Teams List ---\n", teams)

    # Step 1: Sort teams by wins
    teams_sorted = sorted(teams.items(), key=lambda x: x[1]['wins'], reverse=True)
    # print("\n--- Sorted by Wins ---\n", teams_sorted)
    
    # Step 2: Identify ties by wins
    ties = {}
    for team, stats in teams_sorted:
        wins = stats['wins']
        if wins not in ties:
            ties[wins] = []
        ties[wins].append((team, stats))

    # Step 3: Process each group of tied teams with head_to_head for further tiebreaking
    final_sorted_teams = []
    for win_count, tied_teams in ties.items():
        if len(tied_teams) > 1:  # Only process if there is a tie
            # print(f"\n--- Tie Found in Wins: {win_count} ---\n", tied_teams)
            sorted_group = head_to_head(tied_teams, season_games)
            final_sorted_teams.extend(sorted_group)
        else:
            final_sorted_teams.extend(tied_teams)
    
    # Convert back to dictionary format for the final sorted dictionary
    final_sorted_dict = dict((team, stats) for team, stats in final_sorted_teams)
    
    # Final debug print for sorted output
    # print("\n--- Final Sorted Teams ---\n", final_sorted_dict)
    return final_sorted_dict




def simulate_season(team_records, season_games, iterations):
    # Initialize playoff counts and Super Bowl wins
    total_wins = {team: 0 for team in team_records}
    playoff_counts = {team: 0 for team in team_records}
    first_counts = {team: 0 for team in team_records}
    super_bowl_wins = {team: 0 for team in team_records}

    # Helper function to simulate a playoff game
    def simulate_playoff_game(team_a, team_b, win_pct_a, win_pct_b):
        """Simulate a playoff game based on win percentages."""
        total_prob = win_pct_a + win_pct_b
        adjusted_prob_a = win_pct_a / total_prob
        return team_a if np.random.rand() < adjusted_prob_a else team_b

    # Main simulation loop
    for iteration in range(iterations):
        if (iteration + 1) % 1000 == 0:
            print(f"\n--- Iteration {(iteration + 1) / 1000} ---\n")
            print("\n\n--- %s seconds ---" % (time.time() - start_time))
        
        # Copy initial records for a fresh start in each iteration
        simulated_records = copy.deepcopy(team_records)
        
        # Loop through each game in season_games for this iteration
        for game_id, game in season_games.items():
            if game['status'] != 1:
                continue  # Skip already played games
            
            home_team = game['home_team']
            away_team = game['away_team']
            home_win_pct = simulated_records[home_team]['win_percentage']
            away_win_pct = simulated_records[away_team]['win_percentage']
            
            # Retrieve division and conference info directly from predefined dictionaries
            home_team_division = divisions[home_team]
            away_team_division = divisions[away_team]
            home_team_conference = conferences[home_team]
            away_team_conference = conferences[away_team]

            # print("\n" + "-" * 40 + "\n")  # Separator for readability
            
            # # Print team information and win percentages
            # print(f"Game ID: {game_id}")
            # print(f"{home_team} vs. {away_team}")
            # print(f"{home_team} Win Percentage: {home_win_pct}")
            # print(f"{away_team} Win Percentage: {away_win_pct}")
            
            # Determine winner based on adjusted home win probability
            total_prob = home_win_pct + away_win_pct
            # print(f"Total Probability (Home + Away): {total_prob}")
            
            adjusted_home_win_prob = home_win_pct / total_prob
            # print(f"Adjusted Home Win Probability: {adjusted_home_win_prob}")
            
            random_number = np.random.rand()
            # print(f"Random Number for Comparison: {random_number}")
                
            # Update scores and win/loss records
            if random_number < adjusted_home_win_prob:
                # Home team wins
                simulated_records[home_team]['current_season']['wins'] += 1
                simulated_records[away_team]['current_season']['losses'] += 1
                game['home_score'] = 10
                game['away_score'] = 0
            else:
                # Away team wins
                simulated_records[away_team]['current_season']['wins'] += 1
                simulated_records[home_team]['current_season']['losses'] += 1
                game['home_score'] = 0
                game['away_score'] = 10

            # print(team_records)
            
            # Debug print statements to verify correct access
            # print(f"{home_team} Division: {home_team_division}, Conference: {home_team_conference}")
            # print(f"{away_team} Division: {away_team_division}, Conference: {away_team_conference}")
            # print("\n" + "-" * 40 + "\n")  # Separator for readability

            # Check and update division records
            if home_team_division == away_team_division:
                if random_number < adjusted_home_win_prob:
                    simulated_records[home_team]['current_season']['division_wins'] += 1
                    simulated_records[away_team]['current_season']['division_losses'] += 1
                else:
                    simulated_records[away_team]['current_season']['division_wins'] += 1
                    simulated_records[home_team]['current_season']['division_losses'] += 1

            # Check and update conference records
            if home_team_conference == away_team_conference:
                if random_number < adjusted_home_win_prob:
                    simulated_records[home_team]['current_season']['conference_wins'] += 1
                    simulated_records[away_team]['current_season']['conference_losses'] += 1
                else:
                    simulated_records[away_team]['current_season']['conference_wins'] += 1
                    simulated_records[home_team]['current_season']['conference_losses'] += 1

            # Update total games played for each team
            simulated_records[home_team]['current_season']['games'] += 1
            simulated_records[away_team]['current_season']['games'] += 1

        # # Print simulated records for each iteration to check updates
        # print(f"Simulated records for iteration {iteration + 1}:\n")
        # for team, record in simulated_records.items():
        #     print(f"{team}: {record['current_season']}")

        for team, record in simulated_records.items():
            total_wins[team] += record['current_season']['wins']

        # Separate the simulated records by AFC and NFC
        afc_team_records = {team: simulated_records[team]['current_season'] for team in simulated_records if conferences[team] == 'AFC'}
        nfc_team_records = {team: simulated_records[team]['current_season'] for team in simulated_records if conferences[team] == 'NFC'}

        # Convert sorted dictionaries to lists of tuples for AFC and NFC
        afc_sorted_teams = list(sort_teams(afc_team_records, season_games).items())
        nfc_sorted_teams = list(sort_teams(nfc_team_records, season_games).items())

        # print(f"Simulated records for iteration {iteration + 1}:\n")
        # for team, record in afc_sorted_teams:
        #     print(f"{team}: {record}")
        # print(f"Simulated records for iteration {iteration + 1}:\n")
        # for team, record in nfc_sorted_teams:
        #     print(f"{team}: {record}")

        # Function to select division winners and wildcard teams with correct seeding
        def select_playoff_teams_with_seeding(sorted_teams):
            # Counters and collections for division winners and wildcards
            division_winners = []
            wildcards = []
            divisions_seen = set()
            
            # Separate division winners and wildcards
            for team, record in sorted_teams:
                division = divisions[team]
                
                # Check if the team is a division winner and hasn't been selected yet
                if division not in divisions_seen and len(division_winners) < 4:
                    division_winners.append((team, record))  # Add as a division winner
                    divisions_seen.add(division)
                elif len(wildcards) < 3:
                    wildcards.append((team, record))  # Add as a wildcard
                
                # Stop if we have all 4 division winners and 3 wildcards
                if len(division_winners) == 4 and len(wildcards) == 3:
                    break
            
            # Sort division winners and wildcards individually by win percentage (already sorted from `sorted_teams`)
            seeded_playoff_teams = division_winners + wildcards  # Division winners are seeds 1-4, wildcards are 5-7
            return seeded_playoff_teams

        # Select and seed AFC and NFC playoff teams
        afc_playoff_teams = select_playoff_teams_with_seeding(afc_sorted_teams)
        nfc_playoff_teams = select_playoff_teams_with_seeding(nfc_sorted_teams)


        # First-ranked team in each conference for the first seed
        first_afc_team = afc_playoff_teams[0]
        first_nfc_team = nfc_playoff_teams[0]

        # Display results for debugging
        # print("\n" + "-" * 40 + "\n")  # Separator for readability
        # print("AFC Playoff Teams with Seeding:", afc_playoff_teams)
        # print("\n" + "-" * 40 + "\n")  # Separator for readability
        # print("NFC Playoff Teams with Seeding:", nfc_playoff_teams)

        # Add first-seed teams to the count
        first_counts[first_afc_team[0]] += 1
        first_counts[first_nfc_team[0]] += 1

        # Update playoff counts for each team in the playoff bracket
        for team, _ in afc_playoff_teams + nfc_playoff_teams:
            playoff_counts[team] += 1

        # Calculate playoff chances
        firstSeed = {team: first_counts[team] / iterations for team in first_counts}


            # Simulate the AFC and NFC playoffs
        for conference, teams in [('AFC', afc_playoff_teams), ('NFC', nfc_playoff_teams)]:
            advancing_teams = [team[0] for team in teams]

            # print("\n\n" + "-" * 40 + "\n\n")
            # print("Advancing Teams:\n", advancing_teams)
            # print("\n\n" + "-" * 40 + "\n\n")

            # First Round
            round_1_winners = [
                simulate_playoff_game(advancing_teams[1], advancing_teams[6], team_records[advancing_teams[1]]['win_percentage'], team_records[advancing_teams[6]]['win_percentage']),
                simulate_playoff_game(advancing_teams[2], advancing_teams[5], team_records[advancing_teams[2]]['win_percentage'], team_records[advancing_teams[5]]['win_percentage']),
                simulate_playoff_game(advancing_teams[3], advancing_teams[4], team_records[advancing_teams[3]]['win_percentage'], team_records[advancing_teams[4]]['win_percentage'])
            ]

             
            # Second Round
            highest_seeded_winner = advancing_teams[0]
            round_2_teams = [highest_seeded_winner] + sorted(round_1_winners, key=lambda team: advancing_teams.index(team))
            round_2_winners = [
                simulate_playoff_game(round_2_teams[0], round_2_teams[3], team_records[round_2_teams[0]]['win_percentage'], team_records[round_2_teams[3]]['win_percentage']),
                simulate_playoff_game(round_2_teams[1], round_2_teams[2], team_records[round_2_teams[1]]['win_percentage'], team_records[round_2_teams[2]]['win_percentage'])
            ]
            
            # Conference Championship
            conference_champion = simulate_playoff_game(round_2_winners[0], round_2_winners[1], team_records[round_2_winners[0]]['win_percentage'], team_records[round_2_winners[1]]['win_percentage'])
            
            # Track Super Bowl contenders
            # playoff_counts[conference_champion] += 1
            if conference == 'AFC':
                afc_champion = conference_champion
            else:
                nfc_champion = conference_champion

        # Simulate the Super Bowl
        super_bowl_winner = simulate_playoff_game(afc_champion, nfc_champion, team_records[afc_champion]['win_percentage'], team_records[nfc_champion]['win_percentage'])
        super_bowl_wins[super_bowl_winner] += 1
    
    # Calculate playoff chances
    playoff_chances = {team: playoff_counts[team] / iterations for team in playoff_counts}
    super_bowl_percentages = {team: (super_bowl_wins[team] / iterations) * 100 for team in super_bowl_wins}

    return playoff_chances, firstSeed, super_bowl_percentages, total_wins




# Define AFC and NFC teams lists
afc_teams_list = ['Patriots', 'Bills', 'Dolphins', 'Jets', 'Ravens', 'Steelers', 'Browns', 'Bengals', 'Texans', 'Colts', 'Jaguars', 'Titans', 'Broncos', 'Chiefs', 'Raiders', 'Chargers']

nfc_teams_list = ['Cowboys', 'Giants', 'Eagles', 'Commanders', 'Packers', 'Bears', 'Vikings', 'Lions', 'Falcons', 'Panthers', 'Saints', 'Buccaneers', 'Cardinals', 'Rams', '49ers', 'Seahawks']

# Simulate season and calculate playoff chances
playoff_chances, firstSeed, super_bowl_chances, total_wins = simulate_season(team_records, season_games, iterations)
super_bowl_chances = dict(sorted(super_bowl_chances.items(), key=lambda item: item[1], reverse=True))

# Sort playoff chances in descending order
sorted_playoff_chances = dict(sorted(playoff_chances.items(), key=lambda item: item[1], reverse=True))
firstSeed = dict(sorted(firstSeed.items(), key=lambda item: item[1], reverse=True))

# Filter for AFC teams
afc_playoff_chances = {team: chance for team, chance in sorted_playoff_chances.items() if team in afc_teams_list}
afc_firstSeed = {team: chance for team, chance in firstSeed.items() if team in afc_teams_list}

# Filter for NFC teams
nfc_playoff_chances = {team: chance for team, chance in sorted_playoff_chances.items() if team in nfc_teams_list}
nfc_firstSeed = {team: chance for team, chance in firstSeed.items() if team in nfc_teams_list}

# Print playoff chances for AFC teams
print("\n\nAFC Teams Playoff Chances:")
for team, chance in afc_playoff_chances.items():
    print(f":{team}: {chance * 100:.2f}%")

# Print playoff chances for NFC teams
print("\n\nNFC Teams Playoff Chances:")
for team, chance in nfc_playoff_chances.items():
    print(f":{team}: {chance * 100:.2f}%")

# Print playoff chances for AFC teams
print("\n\nAFC Teams 1st Seed Chances:")
for team, chance in afc_firstSeed.items():
    print(f":{team}: {chance * 100:.2f}%")

# Print playoff chances for NFC teams
print("\n\nNFC Teams 1st Seed Chances:")
for team, chance in nfc_firstSeed.items():
    print(f":{team}: {chance * 100:.2f}%")

print("\nSuper Bowl Win Percentages:")
for team, pct in super_bowl_chances.items():
    print(f":{team}: {pct:.2f}%")


print("\n\n--- %s seconds ---" % (time.time() - start_time))

# Define function to convert percentage to American odds
def percentage_to_american_odds(percentage):
    if percentage == 100.0:
        return '0'  # Represents 100% certainty (no payout in betting terms)
    elif percentage == 0.0:
        return 'No odds'  # Represents 0% chance
    else:
        decimal_odds = 100 / percentage
        if decimal_odds >= 2:
            return f"+{int((decimal_odds - 1) * 100)/2}"
        else:
            return f"{int(-100 / (decimal_odds - 1))/2}"

# Convert all percentages to American odds
afc_playoff_odds = {team: percentage_to_american_odds(pct) for team, pct in afc_playoff_chances.items()}
nfc_playoff_odds = {team: percentage_to_american_odds(pct) for team, pct in nfc_playoff_chances.items()}
afc_seed_odds = {team: percentage_to_american_odds(pct) for team, pct in afc_firstSeed.items()}
nfc_seed_odds = {team: percentage_to_american_odds(pct) for team, pct in nfc_firstSeed.items()}
super_bowl_odds = {team: percentage_to_american_odds(pct) for team, pct in super_bowl_chances.items()}

# Create dataframes for organized display
afc_playoff_odds_df = pd.DataFrame(list(afc_playoff_odds.items()), columns=['AFC Team', 'Playoff Odds'])
nfc_playoff_odds_df = pd.DataFrame(list(nfc_playoff_odds.items()), columns=['NFC Team', 'Playoff Odds'])
afc_seed_odds_df = pd.DataFrame(list(afc_seed_odds.items()), columns=['AFC Team', '1st Seed Odds'])
nfc_seed_odds_df = pd.DataFrame(list(nfc_seed_odds.items()), columns=['NFC Team', '1st Seed Odds'])
super_bowl_odds_df = pd.DataFrame(list(super_bowl_odds.items()), columns=['Team', 'Super Bowl Odds'])


print("\nSuper Bowl Win Odds:")
for index, row in super_bowl_odds_df.iterrows():
    try:
        # Attempt to convert to float and round to the nearest 50
        rounded_odds = round(float(row['Super Bowl Odds']) / 50) * 50
        print(f":{row['Team']}: +{rounded_odds}")
    except ValueError:
        # If conversion fails, print the original string
        print(f":{row['Team']}: {row['Super Bowl Odds']}")

print("\n\n" + "-" * 40 + "\n\n")

average_wins = {team: total_wins[team] / iterations for team in total_wins}
print("Average Wins per Team:")
for team, avg_wins in sorted(average_wins.items(), key=lambda x: -x[1]):
    rounded_wins = round(avg_wins * 2) / 2
    print(f"{team}: {rounded_wins:.2f}")