import random
import pandas as pd
import numpy as np

df = pd.read_csv('output_filtered_2018.csv')

df = df[df["position"] == "OL"]

df = df[df["accuracy"] >= 75]

df.rename(columns={"school": "college", "firstName": "FirstName", "lastName":"LastName", "position":"Position", "speed":"SpeedRating", "passIq":"AwarenessRating"}, inplace=True)

# print(df)
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    ranges = [
        (0, 85, "Normal"),
        (86, 94, "Star"),
        (95, 98, "Superstar"),
        (99, 100, "XFactor")
    ]
    value = int(row["potential"])
    for start, end, label in ranges:
            if start <= value <= end:
                trait = label
                break  # Move to the next value once classified
    

    # Quick adjustment to awareness
    awr = int(row["AwarenessRating"]) - 10
    if awr > 75:
        awr = int(awr * 0.925)
    # Calculations to adjust throw power
    throw_power = int(row["armStrength"])
    if throw_power > 88:
        throw_power *= 0.95
    else:
        throw_power = (throw_power + 100) * 0.509

    throw_power = int(np.random.normal(throw_power, 2))

    if throw_power > 99:
        throw_power = 99
    
    madden_throw_power = throw_power

    # Calculations to adjust the accuracy ratings
    power_factor = ((throw_power - 80) / 19) * 3  # Maps 80 to 0, 99 to 3

    madden_throw_accuracy_short = int(np.random.normal(int(row["accuracy"]) - 8, 5))
    madden_throw_accuracy_medium = int(np.random.normal(int(row["accuracy"]) - 12, 5))
    madden_throw_accuracy_deep = int(np.random.normal(int(row["accuracy"]) - 15 + power_factor, 5))

    # Calculate blocking ratings
    madden_run_blocking_power = int(np.random.normal(int(row["runBlocking"]) - 15, 5))
    madden_run_blocking_finesse = int(np.random.normal(int(row["runBlocking"]) - 15, 5))
    madden_run_blocking = int(np.random.normal(int(row["runBlocking"]) - 15, 5))
    madden_pass_blocking = int(np.random.normal(int(row["passBlocking"]) - 15, 5))
    madden_pass_blocking_finesse = int(np.random.normal(int(row["passBlocking"]) - 15, 5))
    madden_pass_blocking_power = int(np.random.normal(int(row["passBlocking"]) - 15, 5))
    madden_impact_blocking = int(np.random.normal(int(row["runBlocking"]) - 10, 10))
    madden_lead_block = int(np.random.normal(int(row["runBlocking"]) - 10, 10))

    
    if row["SpeedRating"] > 90:
        row["SpeedRating"] = 90

    df.at[index, "SpeedRating"] = int(row["SpeedRating"] + 8)
    df.at[index, "ThrowAccuracyShortRating"] = int(madden_throw_accuracy_short)
    df.at[index, "ThrowAccuracyMediumRating"] = int(madden_throw_accuracy_medium)
    df.at[index, "ThrowAccuracyDeepRating"] = int(madden_throw_accuracy_deep)
    df.at[index, "ThrowPowerRating"] = int(throw_power)
    df.at[index, "AwarenessRating"] = awr
    df.at[index, "TraitDevelopment"] = trait
    df.at[index, "RunBlockPowerRating"] = int(madden_run_blocking_power)
    df.at[index, "RunBlockFinesseRating"] = int(madden_run_blocking_finesse)
    df.at[index, "RunBlockRating"] = int(madden_run_blocking)
    df.at[index, "PassBlockPowerRating"] = int(madden_pass_blocking_power)
    df.at[index, "PassBlockFinesseRating"] = int(madden_pass_blocking_finesse)
    df.at[index, "PassBlockRating"] = int(madden_pass_blocking)
    df.at[index, "ImpactBlockingRating"] = int(madden_impact_blocking)
    df.at[index, "LeadBlockingRating"] = int(madden_lead_block)
    # Output or save'madden_attributes' as needed

print(df[["PassBlockRating", "RunBlockPowerRating", "RunBlockFinesseRating", "RunBlockRating", "PassBlockPowerRating", "PassBlockFinesseRating", "TraitDevelopment"]])
