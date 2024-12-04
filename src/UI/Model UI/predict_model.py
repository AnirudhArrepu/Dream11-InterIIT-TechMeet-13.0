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




def load_models():
    loaded_model = joblib.load('xgb_model_best.pkl')
    encodings = joblib.load('encodings.pkl')
    return loaded_model,encodings


def apply_encoding(df, encoding_dict, column_name, global_mean):
    return df[column_name].map(encoding_dict).fillna(global_mean)


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
        row = {
            "Player": player_name,
            "Match Date": match_date,
            "Team": team1,
            "Opponent": team2,
            "Match Type": match_format,
        }
        rows.append(row)
    for player in players_team2:
        player_name = player["name"]
        row = {
            "Player": player_name,
            "Match Date": match_date,
            "Team": team2,
            "Opponent": team1,
            "Match Type": match_format
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df = df[["Player", "Match Date", "Team", "Opponent", "Match Type"]]
    return df


def predict_players(X, loaded_model, X_original, encodings):
    player_encoding, team_encoding, match_date_encoding, opponent_encoding, match_type_encoding = encodings
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
    return predictions

def select_top_players(predictions, X_original, all_teams):
    # Initialize lists to store selected player names and their scores
    chosen_player_names = []
    chosen_players_scores = []
    
    # Dictionary to track the top player from each team
    team_players = {team: [] for team in all_teams}
    
    # Group players by team
    for i, player_name in enumerate(X_original['Player']):
        team = X_original.loc[i, 'Team']
        team_players[team].append((player_name, predictions[i]))

    # First, select one player from each team
    for team in all_teams:
        # Sort players of the current team by their prediction scores
        team_players[team].sort(key=lambda x: x[1], reverse=True)
        # Select the top player for this team
        chosen_player_names.append(team_players[team][0][0])
        chosen_players_scores.append(team_players[team][0][1])
        # Remove the selected player from the team's list
        team_players[team].pop(0)
    
    # Now, select the remaining 9 players based on the highest remaining scores
    remaining_players = []
    for team in all_teams:
        remaining_players.extend(team_players[team])
    
    remaining_players.sort(key=lambda x: x[1], reverse=True)
    
    # Select the top 9 remaining players
    for player_name, score in remaining_players[:9]:
        chosen_player_names.append(player_name)
        chosen_players_scores.append(score)

    return chosen_player_names, chosen_players_scores

def predict_model(json_data):
    loaded_model, encodings = load_models()
    X= process_json_to_dataframe(json_data)
    X_original = X.copy()
    all_teams = set(X['Team'].unique())
    all_teams = list(all_teams)
    predictions = predict_players(X, loaded_model, X_original, encodings)
    X = X.values
    chosen_player_names, chosen_players_scores = select_top_players(predictions, X_original, all_teams)
    
    best11 = [
        {"name": chosen_player_names[i], "points": chosen_players_scores[i]} for i in range(11)
    ]

    return best11
