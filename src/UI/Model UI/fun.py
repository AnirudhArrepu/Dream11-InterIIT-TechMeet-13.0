import pandas as pd
import json
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
                match_dict[match_key] = format_match
                match_dict[match_key]["date"] = row['Match Date'].strftime('%Y-%m-%d')
                match_dict[match_key]["matchFormat"] = row['Match Type']
                match_dict[match_key]["team1"]["name"] = teams[0]
                match_dict[match_key]["team2"]["name"] = teams[1]
            
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

        for player in team1["players"]:
            name = player["name"]

            row = df[df['Player']==name & df['Match Date']==date]

            point = row["Fantasy Points"]

            points.append({name: point})

        for player in team2["players"]:
            name = player["name"]

            row = df[df['Player']==name & df['Match Date']==date]

            point = row["Fantasy Points"]

            points.append({"name": name, "points": point})

        return points

def getGroundTruthBest11(players):
    points = getGroundTruth(players)

    sorted_points = sorted(points, key=lambda x: x['points'], reverse=True)

    top_11 = sorted_points[:11]

    return top_11


def savePredictionsMAE():
    with open('modelInput.json', 'r') as jsoninput:
        maes = []
        for match in jsoninput:
            date = match['date']
            team1 = match['team1']['name']
            team2 = match['team2']['name']

            dream_team = predict_model(match)
            ground_team = getGroundTruthBest11(match)

            dream_team_points = sum(player['points'] for player in dream_team)
            ground_team_points = sum(player['points'] for player in ground_team)

            mae = abs(dream_team_points - ground_team_points)

            maes.append(mae)

        return maes


        
#choose start date and end date for train data
getTrainingData('2023-12-14', '2023-12-15')
#then train the model
model_train('./data/train.csv')

#choose start and end date for test data
getTestData('', '')
#get prediction
print(savePredictionsMAE())

