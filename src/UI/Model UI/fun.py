import pandas as pd
import json
from train_model import model_train
from predict_model import predict_model
# from datetime import DateTime

def getTrainingData(startDate, endDate):
    with open('../../data/raw/cricksheet/final/combined_output.csv', 'r') as file:
        df = pd.read_csv(file)
        print(df.head())  # Add this line to check the structure of the data
        df['Match Date'] = pd.to_datetime(df['Match Date'])
        filtered_df = df[(df['Match Date'] >= startDate) & (df['Match Date'] <= endDate)]
        filtered_df.to_csv('./data/train.csv', index=False)

def getTestData(startDate, endDate):
    with open('../../data/raw/cricksheet/final/combined_output.csv', 'r') as file:
        df = pd.read_csv(file)
        df['Match Date'] = pd.to_datetime(df['Match Date'])
        
        match_dict = {}

        for _, row in df.iterrows():
            teams = sorted([row["Team"], row["Opponent"]])
            match_key = f"{row['Match Date']}|{teams[0]}|{teams[1]}"
            
            if match_key not in match_dict:
                match_dict[match_key] = {
                    "date": row['Match Date'].strftime('%Y-%m-%d'),
                    "matchFormat": row['Match Type'],
                    "team1": {"name": teams[0], "players": []},
                    "team2": {"name": teams[1], "players": []},
                }
            
            if(row["Team"] == teams[0]):
                match_dict[match_key]["team1"]["players"].append({"name": row["Player"]})
            else:
                match_dict[match_key]["team2"]["players"].append({"name": row["Player"]})

        print(match_dict)  # Debug output
        with open("modelInput.json", "w") as outfile: 
            json.dump(match_dict, outfile)


def getGroundTruth(players):
    with open('../../data/raw/cricksheet/final/combined_output.csv', 'r') as file:
        df = pd.read_csv(file)
        
        points = []

        team1 = players['team1']
        team2 = players['team2']
        date = players['date']

        # Collect points for team1 players
        for player in team1["players"]:
            name = player["name"]
            row = df[(df['Player'] == name) & (df['Match Date'] == date)]

            # Ensure we are extracting 'Fantasy Points' properly
            if not row.empty:
                point = row["Fantasy Points"].values[0]
            else:
                point = 0  # Handle case where player doesn't have data

            points.append({"name": name, "points": point})

        # Collect points for team2 players
        for player in team2["players"]:
            name = player["name"]
            row = df[(df['Player'] == name) & (df['Match Date'] == date)]

            if not row.empty:
                point = row["Fantasy Points"].values[0]
            else:
                point = 0  # Handle case where player doesn't have data

            points.append({"name": name, "points": point})

        return points


def getGroundTruthBest11(players):
    points = getGroundTruth(players)
    # points = points.values()
    sorted_points = sorted(points, key=lambda x: x['points'], reverse=True)

    top_11 = sorted_points[:11]

    return top_11

import csv

def savePredictionsMAE():
    maes = []
    mapes = []
    
    # Open and read the input JSON file
    with open('modelInput.json', 'r') as jsoninput:
        data = json.load(jsoninput)
        
        # Open the CSV file in append mode
        with open('predictions.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Check if the file is empty to write the header row only once
            file_empty = csvfile.tell() == 0
            if file_empty:
                # Write the header row to the CSV file
                header = ['Date', 'Team1', 'Team2'] + \
                         [f'DreamPlayer{i}_Name' for i in range(1, 12)] + [f'DreamPlayer{i}_Points' for i in range(1, 12)] + \
                         [f'GroundPlayer{i}_Name' for i in range(1, 12)] + [f'GroundPlayer{i}_Points' for i in range(1, 12)] + ['MAE', 'MAPE']
                csv_writer.writerow(header)
            
            # Process each match in the JSON file
            for match in data.values():
                date = match['date']
                team1 = match['team1']['name']
                team2 = match['team2']['name']

                dream_team = predict_model(match)
                ground_team = getGroundTruthBest11(match)

                # Extract points from dream_team (always 11 players)
                points_list = [player['points'] for player in dream_team]
                actual_points_list = [player['points'] for player in ground_team]

                # Calculate the dream team points with the specified weighting
                if len(points_list) == 11:
                    max_value = max(points_list)
                    points_list.remove(max_value)
                    second_max_value = max(points_list)
                    
                    # Add max_value twice, second_max_value 1.5 times, and the rest normally
                    dream_team_points = (max_value * 2) + (second_max_value * 1.5) + sum(points_list)
                else:
                    # This case should not happen as there are always 11 players
                    dream_team_points = sum(points_list)

                # Calculate ground team points (assuming top 11 players from ground truth)
                ground_team_points = sum(actual_points_list)

                # Calculate MAE (Mean Absolute Error)
                mae = abs(dream_team_points - ground_team_points)
                maes.append(mae)

                # Calculate MAPE (Mean Absolute Percentage Error)
                if ground_team_points != 0:  # Prevent division by zero
                    mape = (abs(dream_team_points - ground_team_points) / ground_team_points) * 100
                    mapes.append(mape)

                # Prepare the row for the CSV file
                row = [date, team1, team2]
                
                # Add dream team players' names and points
                for player in dream_team:
                    row.append(player['name'])
                    row.append(player['points'])
                
                # Add ground team players' names and points
                for player in ground_team:
                    row.append(player['name'])
                    row.append(player['points'])

                # Add MAE and MAPE values
                row.append(mae)
                row.append(mape)
                
                # Write the row to the CSV file
                csv_writer.writerow(row)

        # Calculate averages for MAE and MAPE
        avg_mae = sum(maes) / len(maes) if maes else 0
        avg_mape = sum(mapes) / len(mapes) if mapes else 0

        return avg_mae, avg_mape


        
#choose start date and end date for train data
getTrainingData('2010-12-14', '2024-1-15')
# #then train the model
# model_train('./data/train.csv')

#choose start and end date for test data
getTestData('2023-12-14', '2023-12-15')
#get prediction
print(savePredictionsMAE())

