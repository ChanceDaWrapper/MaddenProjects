import pandas as pd
from collections import Counter

# Load the CSV file
df = pd.read_csv("data/MC_players.csv")

# Filter players with less than 6 years of experience
df = df[df['yearsPro'] < 6]

# Count occurrences of each last name
last_name_counts = Counter(df["lastName"])

# Filter last names that appear more than once and sort by count (descending)
duplicate_last_names = {name: count for name, count in last_name_counts.items() if count > 1}
duplicate_last_names = dict(sorted(duplicate_last_names.items(), key=lambda item: item[1], reverse=True))

# Display the results
if duplicate_last_names:
    print("Potential relatives (last names appearing multiple times, sorted by count):")
    for name, count in duplicate_last_names.items():
        print(f"{name}: {count} players")
else:
    print("No duplicate last names found.")
