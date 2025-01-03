import streamlit as st
from datetime import date
import pandas as pd
import json
import sys
sys.path.append('./model_')
from train_model import model_train
from predict_model import predict_model
# from datetime import DateTime

def getTrainingData(startDate, endDate):
    with open('../../data/raw/cricksheet/final/combined_output.csv', 'r') as file:
        df = pd.read_csv(file)
        df['Match Date'] = pd.to_datetime(df['Match Date'])

        filtered_df = df[(df['Match Date'] >= startDate) & (df['Match Date'] <= endDate)]
        
        # filtered_df = filtered_df.sort_values(by="Match Date")

        filtered_df.to_csv('./data/train.csv', index=False)

        # print(filtered_df.head())

def getTestData(startDate, endDate):
    with open('../../data/raw/cricksheet/final/combined_output.csv', 'r') as file:
        df = pd.read_csv(file)
        df['Match Date'] = pd.to_datetime(df['Match Date'])

        filtered_df = df[(df['Match Date'] >= startDate) & (df['Match Date'] <= endDate)]
        
        match_dict = {}

        format_match = {
            "date": "",
            "matchFormat": "",
            "team1":{
                "name": "",
                "players": [

                ]
            },
            "team2":{
                "name": "",
                "players": [
                    
                ]
            }
        }

        for _, row in filtered_df.iterrows():
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


        # for match, players in match_dict.items():
        #     print(f"Match: {match}, Players: {players}")

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


# Page Title
st.title("Dream11 Fantasy Team Predictor")
st.markdown("""
    **Welcome to the Dream11 Fantasy Team Predictor!**

    Use this tool to train a model, predict fantasy teams, and evaluate the model's performance.
""")

# Select Training Date Range
st.header("Training Data")
st.subheader("Choose a date range for training data")
train_start_date = st.date_input("Training Start Date", date(2010, 1, 1))
train_end_date = st.date_input("Training End Date", date.today())

if train_start_date > train_end_date:
    st.error("Training start date must be before the end date.")
else:
    if st.button("Generate Training Data"):
        getTrainingData(train_start_date, train_end_date)
        model_train('./data/train.csv')  # Train the model with the generated data
        st.success("Training data generated and model trained!")

# Select Test Date Range
st.header("Test Data")
st.subheader("Choose a date range for test data")
test_start_date = st.date_input("Test Start Date", date(2023, 1, 1))
test_end_date = st.date_input("Test End Date", date.today())

if test_start_date > test_end_date:
    st.error("Test start date must be before the end date.")
else:
    if st.button("Generate Test Data"):
        getTestData(test_start_date, test_end_date)
        st.success("Test data generated!")

# Run Predictions and Display Results
if st.button("Run Predictions and Evaluate"):
    avg_mae, avg_mape = savePredictionsMAE()  # Get predictions and evaluation metrics
    st.write(f"**Mean Absolute Error (MAE):** {avg_mae}")
    st.write(f"**Mean Absolute Percentage Error (MAPE):** {avg_mape}")
    st.success("Predictions and evaluation completed!")

# Footer
st.markdown("---")
st.caption("Developed for the Dream11 Fantasy Cricket Prediction Challenge.")