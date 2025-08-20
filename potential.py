import random
import math
import pandas as pd

# Load your dataset
data = pd.read_csv('Data/MC_players.csv')
# Filter for rookies (players with yearsPro == 0)
# data = data[data['yearsPro'] == 0]
# data = data[data['productionGrade'] > 70]
data = data[pd.notna(data['team'])]
data = data[data['position'] == 'LE']
# data = data[data['team'] == 'Panthers']
# Define development trait multipliers
dev_trait_multipliers = {
    '0': 2,
    '1': 5,
    '2': 8,
    '3': 12
}

# data['difference'] = 0

# Create the 'difference' column by calculating it for the entire DataFrame
data['difference'] = data['productionGrade'] - data['playerBestOvr']

# Filter rows where the absolute value of the difference is greater than 20
filtered_data = data[(data['difference'] > 20) | (data['difference'] < -10)]

data = data.sort_values(by='productionGrade', ascending=False)

# Display the first 10 rows of the filtered DataFrame
print(data[['fullName', 'team', 'playerBestOvr', 'productionGrade', 'difference']].head(50))