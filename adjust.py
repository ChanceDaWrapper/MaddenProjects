import json
import csv
import pandas as pd

# Importing the JSON file
with open('FCCD - Getting Draft Files (2022 Export).json', 'r') as json_file:
    data = json.load(json_file)



with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Set header row for players (adjust as necessary)
    headers = ["team", "position", "firstName", "lastName", "hsGradYear", 
            "archetype", "jerseyNumber", 
            "durability", "potential", "height", "weight", "speed", 
                "evasion", "strength", "armStrength", "accuracy", "passIq", 
                "catching", "routeRunning", "ballSecurity", "ballCarrierVision", 
                "runBlocking", "passBlocking", "tackling", "manCoverage", 
                "zoneCoverage", "blockShedding", "pursuit", "defensiveIq", 
                "kickPower", "kickAccuracy", "puntPower", "puntAccuracy" 
            ]
    writer.writerow(headers)

    # Iterate through players and add rows
    for player in data["players"]:
        row = [
            player["team"], 
            player["position"], 
            player["firstName"], 
            player["lastName"], 
            player["hsGradYear"], 
            player["archetype"], 
            player["jerseyNumber"],
            player["attributes"]["durability"],
            player["attributes"]["potential"],
            player["attributes"]["height"],
            player["attributes"]["weight"],
            player["attributes"]["speed"],
            player["attributes"]["evasion"],
            player["attributes"]["strength"],
            player["attributes"]["armStrength"],
            player["attributes"]["accuracy"],
            player["attributes"]["passIq"],
            player["attributes"]["catching"],
            player["attributes"]["routeRunning"],
            player["attributes"]["ballSecurity"],
            player["attributes"]["ballCarrierVision"],
            player["attributes"]["runBlocking"],
            player["attributes"]["passBlocking"],
            player["attributes"]["tackling"],
            player["attributes"]["manCoverage"],
            player["attributes"]["zoneCoverage"],
            player["attributes"]["blockShedding"],
            player["attributes"]["pursuit"],
            player["attributes"]["defensiveIq"],
            player["attributes"]["kickPower"],
            player["attributes"]["kickAccuracy"],
            player["attributes"]["puntPower"],
            player["attributes"]["puntAccuracy"]
        ]
        writer.writerow(row)

df = pd.read_csv('output.csv')

df = df[df["hsGradYear"] == 2018]

df.to_csv('output_filtered_2018.csv', index=False)
