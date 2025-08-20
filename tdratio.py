import pandas as pd


df = pd.read_csv('MC_passing.csv')

df['TD/INT Ratio'] = 0  # Initialize the column
for _, row in df.iterrows():
    if row['passTotalInts'] == 0:
        df.loc[row.name, 'TD/INT Ratio'] = row['passTotalTDs']
    else:
        df.loc[row.name, 'TD/INT Ratio'] = row['passTotalTDs'] / row['passTotalInts']


df_sorted = df.sort_values(by='TD/INT Ratio', ascending=False)

for _, row in df_sorted.iterrows():
    print(f"{row['player__fullName']} has a TD/INT Ratio of -- **{row['TD/INT Ratio']:.2f}**")