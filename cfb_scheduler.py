import random

acc_teams = [
    "Florida State",
    "Notre Dame",
    "Auburn",
    "Clemson",
    "Miami",
    "LSU",
    "Louisville",
    "South Carolina"
]

big_ten_teams = [
    "Kentucky",
    "Ohio State",
    "Michigan",
    "Penn State",
    "USC",
    "Oregon",
    "UCLA",
    "Nebraska"
]

big_12_teams = [
    "Arizona",
    "Missouri",
    "West Virginia",
    "Kansas State",
    "Utah",
    "UCF",
    "Kansas",
    "Colorado"
]

sec_teams = [
    "Florida",
    "Texas",
    "Alabama",
    "Oklahoma",
    "Georgia",
    "Ole Miss",
    "Tennessee",
    "Texas A&M"
]

# Initialize the schedule dictionary
schedule = {team: [] for team in acc_teams + big_ten_teams + big_12_teams + sec_teams}

# Helper function to find a valid opponent
def find_opponent(team, candidates, schedule):
    random.shuffle(candidates)
    for opponent in candidates:
        if opponent not in schedule[team] and team not in schedule[opponent] and len(schedule[opponent]) < 4:
            return opponent
    return None

# Function to create the schedules by matching randomized lists
def create_schedules():
    # Randomize the order of the teams within each conference
    random.shuffle(acc_teams)
    random.shuffle(big_ten_teams)
    random.shuffle(big_12_teams)
    random.shuffle(sec_teams)
    
    # Match SEC teams with ACC teams
    for i in range(len(sec_teams)):
        schedule[sec_teams[i]].append(acc_teams[i])
        schedule[acc_teams[i]].append(sec_teams[i])
    
    # Match SEC teams with Big Ten teams (two matchups each)
    for i in range(len(sec_teams)):
        schedule[sec_teams[i]].append(big_ten_teams[i])
        schedule[big_ten_teams[i]].append(sec_teams[i])
        second_match = (i + len(sec_teams) // 2) % len(sec_teams)
        schedule[sec_teams[i]].append(big_ten_teams[second_match])
        schedule[big_ten_teams[second_match]].append(sec_teams[i])
    
    # Match SEC teams with Big 12 teams
    random.shuffle(big_12_teams)
    for i in range(len(sec_teams)):
        schedule[sec_teams[i]].append(big_12_teams[i])
        schedule[big_12_teams[i]].append(sec_teams[i])
    
    # Reset and re-randomize the ACC and Big 12 teams for their matchups
    random.shuffle(acc_teams)
    random.shuffle(big_12_teams)
    
    # Match ACC teams with Big Ten teams
    for i in range(len(acc_teams)):
        schedule[acc_teams[i]].append(big_ten_teams[i])
        schedule[big_ten_teams[i]].append(acc_teams[i])
    
    # Match ACC teams with Big 12 teams (two matchups each)
    for i in range(len(acc_teams)):
        schedule[acc_teams[i]].append(big_12_teams[i])
        schedule[big_12_teams[i]].append(acc_teams[i])
        second_match = (i + len(acc_teams) // 2) % len(acc_teams)
        schedule[acc_teams[i]].append(big_12_teams[second_match])
        schedule[big_12_teams[second_match]].append(acc_teams[i])
    
    # Match Big Ten teams with Big 12 teams
    random.shuffle(big_ten_teams)
    random.shuffle(big_12_teams)
    for i in range(len(big_ten_teams)):
        schedule[big_ten_teams[i]].append(big_12_teams[i])
        schedule[big_12_teams[i]].append(big_ten_teams[i])


create_schedules()

print("Hello")
# Display the schedule
for team, opponents in schedule.items():
    print(f"{team}: {', '.join(opponents)}" + "\n")
