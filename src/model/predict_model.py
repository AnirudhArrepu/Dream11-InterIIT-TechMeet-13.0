import os
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import logging
from lime.lime_tabular import LimeTabularExplainer
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import learning_curve
from lime.lime_tabular import LimeTabularExplainer
import joblib
import hashlib
from collections import defaultdict
from lime.lime_tabular import LimeTabularExplainer
from mistralai import Mistral

model = "mistral-large-latest"
client = Mistral(api_key="r2OC0XPdCa4VSwkarNCP53PVdlWStSJ1")


loaded_model = joblib.load('xgb_model_best.pkl')
player_encoding, team_encoding, match_date_encoding, opponent_encoding, match_type_encoding = joblib.load('encodings.pkl')


def apply_encoding(df, encoding_dict, column_name, global_mean):
    return df[column_name].map(encoding_dict).fillna(global_mean)

json_data = {
  "date": "2024-03-22",
  "matchFormat": "t20",
  "team1": {
    "name": "India",
    "players": [
        {"name": "Arshdeep Singh", "role": "Batsman"},
        {"name": "Virat Kohli", "role": "Batsman"},
        {"name": "Rohit Sharma", "role": "Batsman"},
        {"name": "Surya Yadav", "role": "Batsman"},
        {"name": "S Gill", "role": "Batsman"},
        {"name": "Jasprit Bumrah", "role": "Bowler"},
        {"name": "Rishabh Pant", "role": "Wicket-Keeper"},
        {"name": "Hardik Pandya", "role": "All-Rounder"},
        {"name": "Ravindra Jadeja", "role": "All-Rounder"},
        {"name": "Bhuvneshwar Kumar", "role": "Bowler"},
        {"name": "Yuzvendra Chahal", "role": "Bowler"}
    ]
  },
  "team2": {
    "name": "Australia",
    "players": [
      {"name": "Travis Head", "role": "Batsman"},
      {"name": "Maxwell Maxwell", "role": "All-Rounder"},
      {"name": "David Warner", "role": "Batsman"},
      {"name": "Mitchell Starc", "role": "Bowler"},
      {"name": "Adam Zampa", "role": "Bowler"},
      {"name":"Marcus Stoinis","role":"All-Rounder"},
      {"name":"Mitchell Marsh","role":"All-Rounder"},
      {"name":"Josh Hazlewood","role":"Bowler"},
      {"name":"Sean Abbott","role":"Bowler"},
      {"name":"Tim David","role":"Batsman"},
      {"name": "Josh Inglis", "role": "Wicket-Keeper"}

    ]
  }
}


def process_json_to_dataframe(json_data):
    match_date = json_data["date"]
    match_format = json_data["matchFormat"]
    team1 = json_data["team1"]["name"]
    team2 = json_data["team2"]["name"]
    players_team1 = json_data["team1"]["players"]
    players_team2 = json_data["team2"]["players"]
    player_role_mapping = {}
    rows = []
    for player in players_team1:
        player_name = player["name"]
        player_role = player["role"]
        player_role_mapping[player_name] = player_role
        row = {
            "Player": player_name,
            "Match Date": match_date,
            "Team": team1,
            "Opponent": team2,
            "Match Type": match_format,
            "Role": player_role
        }
        rows.append(row)
    for player in players_team2:
        player_name = player["name"]
        player_role = player["role"]
        player_role_mapping[player_name] = player_role
        row = {
            "Player": player_name,
            "Match Date": match_date,
            "Team": team2,
            "Opponent": team1,
            "Match Type": match_format,
            "Role": player_role
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df = df[["Player", "Match Date", "Team", "Opponent", "Match Type", "Role"]]
    return df, player_role_mapping

X, player_role_mapping = process_json_to_dataframe(json_data)
X_original = X.copy()
X = X.iloc[:, :-1]

all_teams = set(X['Team'].unique())
all_teams = list(all_teams)

global_mean_player = np.mean(list(player_encoding.values()))
global_mean_team = np.mean(list(team_encoding.values()))
global_mean_match_date = np.mean(list(match_date_encoding.values()))
global_mean_opponent = np.mean(list(opponent_encoding.values()))
global_mean_match_type = np.mean(list(match_type_encoding.values()))

X['Player'] = apply_encoding(X, player_encoding, 'Player', global_mean_player)
X['Team'] = apply_encoding(X, team_encoding, 'Team', global_mean_team)
X['Match Date'] = apply_encoding(X, match_date_encoding, 'Match Date', global_mean_match_date)
X['Opponent'] = apply_encoding(X, opponent_encoding, 'Opponent', global_mean_opponent)
X['Match Type'] = apply_encoding(X, match_type_encoding, 'Match Type', global_mean_match_type)
X = X.values

predictions = loaded_model.predict(X)
chosen_players = []
roles = {
    "Batsman": {},
    "Bowler": {},
    "All-Rounder": {},
    "Wicket-Keeper": {}
}

team_A_players = set()
team_B_players = set()

for i, player_name in enumerate(player_role_mapping):
    role = player_role_mapping[player_name]
    prediction_score = predictions[i]
    team = X_original.loc[X_original['Player'] == player_name, 'Team'].values[0]
    roles[role][player_name] = prediction_score
    if team == all_teams[0]:
        team_A_players.add(player_name)
    else:
        team_B_players.add(player_name)

selected_roles = set()  
selected_teams = set()  

for role, players in roles.items():
    if len(chosen_players) < 11:
        top_player = max(players, key=players.get)
        chosen_players.append((top_player, players[top_player]))
        selected_roles.add(role)
        team = X_original.loc[X_original['Player'] == top_player, 'Team'].values[0]
        selected_teams.add(team)
        del players[top_player]  

if len(selected_teams) < 2:
 
    if "Team A" not in selected_teams:
        team_a_candidates = [player for player in team_A_players if player not in [p[0] for p in chosen_players]]
        top_team_a_player = max(team_a_candidates, key=lambda x: roles[player_role_mapping[x]].get(x))
        chosen_players.append((top_team_a_player, roles[player_role_mapping[top_team_a_player]].get(top_team_a_player)))
        selected_teams.add("Team A")

    if "Team B" not in selected_teams:
        team_b_candidates = [player for player in team_B_players if player not in [p[0] for p in chosen_players]]
        top_team_b_player = max(team_b_candidates, key=lambda x: roles[player_role_mapping[x]].get(x))
        chosen_players.append((top_team_b_player, roles[player_role_mapping[top_team_b_player]].get(top_team_b_player)))
        selected_teams.add("Team B")

remaining_players = []
for role, players in roles.items():
    remaining_players.extend([(player, score) for player, score in players.items() if player not in [p[0] for p in chosen_players]])

remaining_players = sorted(remaining_players, key=lambda x: x[1], reverse=True)

for player, score in remaining_players:
    if len(chosen_players) < 11:
        chosen_players.append((player, score))

chosen_player_names = [player[0] for player in chosen_players]
chosen_players_scores = [player[1] for player in chosen_players]
chosen_players_encoded = X[X_original['Player'].isin(chosen_player_names)]
feature_names = [ 'Player' , 'Match Date', 'Team', 'Opponent', 'Match Type']
total_score = sum(chosen_players_scores)


explainer = LimeTabularExplainer(
    training_data=X,         # The model was trained on this data (X with encodings)
    mode='regression',       # Assuming your model is a regression model, change to 'classification' if needed
    training_labels=None,    # For regression, it's not required
    feature_names=feature_names,  # Feature names are the same as the columns of your X
    class_names=['Prediction'],  # Only for regression
    discretize_continuous=True  # Discretizing continuous features
)

all_explanations = []
for i, player_data_values in enumerate(chosen_players_encoded):
    player_name = chosen_player_names[i] 
    prediction = chosen_players_scores[i]

    exp = explainer.explain_instance(
        player_data_values,  # Player data (features)
        loaded_model.predict,  # The model to explain
        num_features=10 # Number of top features to show (can adjust)
    )
    feature_contributions = exp.as_list()
    formatted_feature_contributions = ', '.join([f"{cond}: {val:.2f}" for cond, val in feature_contributions])
    explanation_text = f"""
    Explanation for {player_name} (Prediction: {prediction}):
    LIME Output: [{formatted_feature_contributions}]
    Predicted value: {prediction}
    """
    all_explanations.append(explanation_text)

all_explanations_text = "\n".join(all_explanations)

# prompt = f"""
# I am building a fantasy cricket app with an ML model to predict the best players. Here are the explanations for the top 11 players, predicted to perform well based on their fantasy points. The following explanations are generated using LIME for the model's prediction:

# {all_explanations_text}

# Write a human-interpretable summary of why these players were predicted, mentioning the features that have positively or negatively impacted their fantasy points. Exclude numerical values and focus on the key factors that influenced the prediction.
# """

prompt = f"""
I am building a fantasy cricket app with an ML model to predict the best players. Below is a summary of the top 11 players selected based on LIME explanations:

{all_explanations_text}

For each player, focus on the key factors that influenced their selection. Do not include any numerical values. For each player, describe in one sentence which features had a positive effect on their selection and which features had a negative effect. For example: "Player X's selection was positively influenced by feature A, while feature B had a negative impact." 

If two or more players have similar explanations, combine them into a single sentence. For example: "Player X and Player Y's selection was positively influenced by feature A, while feature B had a negative impact."

Write all of this in paragraph form, without headings, and ensure the information is clear and concise. All dont give all sentences in same formta try to rephrase them
"""
chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
)
print(chat_response.choices[0].message.content)