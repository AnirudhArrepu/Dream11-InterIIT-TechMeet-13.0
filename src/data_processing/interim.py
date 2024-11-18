import json
import pandas as pd
import os
from datetime import datetime


directory = '../data/raw/cricksheet/cricsheet-raw'
output_directory = "../data/raw/cricksheet/interim"
os.makedirs(output_directory, exist_ok=True)    

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # Check if the file is a JSON file
        file_path = os.path.join(directory, filename)
        print(filename)

        # if(filename!='1160280.json'):
        #     continue
        
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

            match_date = data['info']['dates'][0]
            check_date = "2014-01-01"
            last_date = "2024-06-30"

            # Parse the dates using the correct format
            date1 = datetime.strptime(match_date, "%Y-%m-%d")
            date2 = datetime.strptime(check_date, "%Y-%m-%d")
            date3 = datetime.strptime(last_date, "%Y-%m-%d")

            # Move the file if the match date is after the check date
            if date1 > date2 and date1 < date3:


# Initialize a dictionary to store player stats
                players_stats = {}

                # Helper function to initialize player stats
                def initialize_player(player_name, player_team, sub):
                    if player_name not in players_stats:
                        players_stats[player_name] = {
                            "runs": 0,
                            "balls_faced": -1,
                            "run_per_over": [],
                            "4": 0,
                            "6": 0,
                            "caught": 0,
                            "wickets": 0,
                            "bowled": 0,
                            "run_outs": 0,
                            "lbw": 0,
                            "indirect_run_out": 0,
                            "maiden_overs": 0,
                            "team_name": player_team,
                            "substitute": sub,
                        }

                player_list = data["info"]["players"]
                print(player_list)
                for team in player_list:
                    print(team)
                    for player in player_list[team]:
                        print(player)
                        initialize_player(player, team, False)

                # Parse innings
                for inning in data.get("innings", []):
                    for over_data in inning.get("overs", []):
                        over_number = over_data["over"]
                        runs_in_over = {}
                        total_runs_in_over = 0  # Track total runs conceded in the over

                        for delivery in over_data["deliveries"]:
                            # Batting stats
                            batter = delivery["batter"]
                            # initialize_player(batter)

                            # Increment balls faced for the batter
                            players_stats[batter]["balls_faced"] += 1

                            # Runs scored by batter
                            runs_scored = delivery["runs"]["batter"]
                            players_stats[batter]["runs"] += runs_scored
                            if runs_scored == 4:
                                players_stats[batter]["4"] += 1
                            elif runs_scored == 6:
                                players_stats[batter]["6"] += 1

                            # Track runs per over for the batter
                            if batter not in runs_in_over:
                                runs_in_over[batter] = 0
                            runs_in_over[batter] += runs_scored

                            # Bowling stats
                            bowler = delivery["bowler"]
                            # initialize_player(bowler)
                            bowlers_runs = delivery["runs"]["total"]
                            total_runs_in_over += bowlers_runs  # Track total runs in the over

                            if len(players_stats[bowler]["run_per_over"]) <= over_number:
                                players_stats[bowler]["run_per_over"].extend([0] * (over_number + 1 - len(players_stats[bowler]["run_per_over"])))
                            players_stats[bowler]["run_per_over"][over_number] += bowlers_runs

                            # Process wicket information if present
                            if "wickets" in delivery:
                                for wicket in delivery["wickets"]:
                                    dismissal_kind = wicket["kind"]
                                    if dismissal_kind == "caught":
                                        # Credit the fielder with a catch
                                        fielders = wicket.get("fielders", [])
                                        if fielders and "name" in fielders[0]:
                                            fielder_name = fielders[0]["name"]
                                            # initialize_player(fielder_name)
                                            if fielder_name not in players_stats:
                                                initialize_player(fielder_name, players_stats[bowler]["team_name"], True)

                                            players_stats[fielder_name]["caught"] += 1
                                        else:
                                            # Log or handle cases where 'name' is not present
                                            print(f"Warning: Malformed fielder data in delivery: {delivery}")

                                        # initialize_player(fielder_name)
                                        if fielder_name not in players_stats:
                                            initialize_player(fielder_name, players_stats[bowler]["team_name"], True)
                                        players_stats[fielder_name]["caught"] += 1

                                        # Credit the bowler with a wicket
                                        players_stats[bowler]["wickets"] += 1

                                    elif dismissal_kind == "bowled":
                                        players_stats[bowler]["wickets"] += 1
                                        players_stats[bowler]["bowled"] += 1

                                    elif dismissal_kind == "lbw":
                                        players_stats[bowler]["wickets"] += 1
                                        players_stats[bowler]["lbw"] += 1

                                    elif dismissal_kind == "run out":
                                        fielders = wicket.get("fielders", [])
                                        if len(fielders) > 1:
                                            # Indirect run-out for multiple fielders
                                            for fielder in fielders:
                                                if "name" in fielders:
                                                    fielder_name = fielder["name"]
                                                    if fielder_name not in players_stats:
                                                        initialize_player(fielder_name, players_stats[bowler]["team_name"], True)
                                                    # initialize_player(fielder_name)
                                                    players_stats[fielder_name]["indirect_run_out"] += 1
                                        elif len(fielders)==1:
                                            if "name" in fielders[0]:
                                                fielder_name = fielders[0]["name"]
                                                if fielder_name not in players_stats:
                                                    initialize_player(fielder_name, players_stats[bowler]["team_name"], True)
                                                # initialize_player(fielder_name)  # Ensure the fielder is initialized
                                                players_stats[fielder_name]["run_outs"] += 1
                                        else:
                                            players_stats[bowler]["run_outs"]+=1


                        # Check if the over is a maiden over
                        if total_runs_in_over == 0:
                            players_stats[bowler]["maiden_overs"] += 1

                        # Append run_per_over for batters in the current over
                        for player, runs in runs_in_over.items():
                            # initialize_player(player)
                            if len(players_stats[player]["run_per_over"]) <= over_number:
                                players_stats[player]["run_per_over"].extend([0] * (over_number + 1 - len(players_stats[player]["run_per_over"])))
                            players_stats[player]["run_per_over"][over_number] += runs

                # Result
                # print(players_stats)


                fantasy_points = {
                    't20': {
                        'runs': 1,
                        'boundary': 1,
                        'six': 2,
                        'thirty_run_bonus': 4,
                        'half_century_bonus': 8,
                        'century_bonus': 16,
                        'duck': -2,
                        'wicket': 25,
                        'bonus_wicket': 8,
                        'wicket_3_bonus': 4,
                        'wicket_4_bonus': 8,
                        'wicket_5_bonus': 16,
                        'maiden_over': 12,
                        'catch': 8,
                        'catch_3_bonus': 4,
                        'lbw': 8,
                        'bowled': 8,
                        'stumped': 12,
                        'run_out_direct': 12,
                        'run_out_non_direct': 6,
                        'economy_rate': {
                            'below_5': 6,
                            '5_to_5_99': 4,
                            '6_to_7': 2,
                            '10_to_11': -2,
                            '11_01_to_12': -4,
                            'above_12': -6,
                        },
                        'strike_rate': {
                            'above_170': 6,
                            '150_to_170': 4,
                            '130_to_150': 2,
                            '60_to_70': -2,
                            '50_to_59_99': -4,
                            'below_50': -6,
                        }
                    },
                    'test': {
                        'runs': 1,
                        'boundary': 1,
                        'six': 2,
                        'thirty_run_bonus': 0,
                        'half_century_bonus': 4,
                        'century_bonus': 8,
                        'duck': -4,
                        'wicket': 16,
                        'bonus_wicket': 8,
                        'wicket_3_bonus': 0,
                        'wicket_4_bonus': 4,
                        'wicket_5_bonus': 8,
                        'maiden_over': 0,
                        'catch': 8,
                        'catch_3_bonus': 0,
                        'lbw': 8,
                        'bowled': 8,
                        'stumped': 12,
                        'run_out_direct': 12,
                        'run_out_non_direct': 6,
                        'economy_rate': {
                            'below_5': 0,
                            '5_to_5_99': 0,
                            '6_to_7': 0,
                            '10_to_11': 0,
                            '11_01_to_12': 0,
                            'above_12': 0,
                        },
                        'strike_rate': {
                            'above_170': 0,
                            '150_to_170': 0,
                            '130_to_150': 0,
                            '60_to_70': 0,
                            '50_to_59_99': 0,
                            'below_50': 0,
                        }
                    },
                    'odi': {
                        'runs': 1,
                        'boundary': 1,
                        'six': 2,
                        'thirty_run_bonus': 0,
                        'half_century_bonus': 4,
                        'century_bonus': 8,
                        'duck': -3,
                        'wicket': 25,
                        'bonus_wicket': 8,
                        'wicket_3_bonus': 0,
                        'wicket_4_bonus': 4,
                        'wicket_5_bonus': 8,
                        'maiden_over': 4,
                        'catch': 8,
                        'catch_3_bonus': 4,
                        'lbw': 8,
                        'bowled': 8,
                        'stumped': 12,
                        'run_out_direct': 12,
                        'run_out_non_direct': 6,
                        'economy_rate': {
                            'below_2.5': 6,
                            '2.5_to_3.49': 4,
                            '3.5_to_4.5': 2,
                            '7_to_8': -2,
                            '8.01_to_9': -4,
                            'above_9': -6,
                        },
                        'strike_rate': {
                            'above_140': 6,
                            '120_to_140': 4,
                            '100_to_120': 2,
                            '40_to_50': -2,
                            '30_to_40': -4,
                            'below_30': -6,
                        }
                    }
                }

                def calculate_fantasy_points(players_stats, fantasy_points, match_name):
                    player_fantasy_points = {}
                    print(match_name)

                    for player, stats in players_stats.items():
                        if(players_stats[player]["substitute"]):
                            continue
                    
                        points = 0
                        # Map the match type to valid keys in fantasy_points
                        match_name = match_name.lower()
                        match_type_mapping = {"odm": "odi"}  # Add more mappings if necessary
                        match_name = match_type_mapping.get(match_name, match_name)  # Default to original if no mapping exists

                        # Check if match_name exists in fantasy_points
                        if match_name not in fantasy_points:
                            raise ValueError(f"Unsupported match type: {match_name}")
                            continue

                        scoring = fantasy_points[match_name]


                        # Points for runs scored
                        points += stats['runs'] * scoring['runs']

                        # Points for boundaries and sixes
                        points += stats['4'] * scoring['boundary']
                        points += stats['6'] * scoring['six']

                        # Bonus points for runs milestones
                        if stats['runs'] >= 100:
                            points += scoring['century_bonus']
                        elif stats['runs'] >= 50:
                            points += scoring['half_century_bonus']
                        elif stats['runs'] >= 30:
                            points += scoring['thirty_run_bonus']

                        # Duck penalty (assuming duck means no runs and minimum balls faced)
                        if stats['runs'] == 0 and stats['balls_faced'] > 0:
                            points += scoring['duck']

                        # Points for wickets taken
                        points += stats['wickets'] * scoring['wicket']

                        # Bonus points for bowled and lbw dismissals
                        points += stats['bowled'] * scoring['bowled']
                        points += stats['lbw'] * scoring['lbw']

                        # Bonus for taking 3, 4, or 5 wickets
                        if stats['wickets'] >= 5:
                            points += scoring['wicket_5_bonus']
                        elif stats['wickets'] >= 4:
                            points += scoring['wicket_4_bonus']
                        elif stats['wickets'] >= 3:
                            points += scoring['wicket_3_bonus']

                        # Points for maiden overs
                        points += stats['maiden_overs'] * scoring['maiden_over']

                        # Points for catches
                        points += stats['caught'] * scoring['catch']

                        # Bonus for taking 3 or more catches
                        if stats['caught'] >= 3:
                            points += scoring['catch_3_bonus']

                        # Points for run-outs
                        points += stats['run_outs'] * scoring['run_out_direct']
                        points += stats['indirect_run_out'] * scoring['run_out_non_direct']

                        # Points for economy rate (only if the player has bowled)
                        if stats["balls_faced"] > 0:
                            overs_bowled = stats['balls_faced'] / 6
                            if overs_bowled > 0:
                                economy_rate = sum(stats['run_per_over']) / overs_bowled

                                if match_name != "odi":
                                    if economy_rate < 5:
                                        points += scoring['economy_rate']['below_5']
                                    elif 5 <= economy_rate < 6:
                                        points += scoring['economy_rate']['5_to_5_99']
                                    elif 6 <= economy_rate < 7:
                                        points += scoring['economy_rate']['6_to_7']
                                    elif 10 <= economy_rate < 11:
                                        points += scoring['economy_rate']['10_to_11']
                                    elif 11 <= economy_rate < 12:
                                        points += scoring['economy_rate']['11_01_to_12']
                                    elif economy_rate >= 12:
                                        points += scoring['economy_rate']['above_12']
                                else:
                                    if economy_rate < 2.5:
                                        points += scoring['economy_rate']['below_2.5']
                                    elif 2.5 <= economy_rate < 3.5:
                                        points += scoring['economy_rate']['2.5_to_3.49']
                                    elif 3.5 <= economy_rate < 4.5:
                                        points += scoring['economy_rate']['3.5_to_4.5']
                                    elif 7 <= economy_rate < 8:
                                        points += scoring['economy_rate']['7_to_8']
                                    elif 8 <= economy_rate < 9:
                                        points += scoring['economy_rate']['8.01_to_9']
                                    elif economy_rate >= 9:
                                        points += scoring['economy_rate']['above_9']

                        # Points for strike rate (only if the player has faced balls)
                        if stats["balls_faced"] > 0:
                            strike_rate = (stats['runs'] / stats['balls_faced']) * 100

                            if match_name != "odi":
                                if strike_rate > 170:
                                    points += scoring['strike_rate']['above_170']
                                elif 150 <= strike_rate <= 170:
                                    points += scoring['strike_rate']['150_to_170']
                                elif 130 <= strike_rate < 150:
                                    points += scoring['strike_rate']['130_to_150']
                                elif 60 <= strike_rate < 70:
                                    points += scoring['strike_rate']['60_to_70']
                                elif 50 <= strike_rate < 60:
                                    points += scoring['strike_rate']['50_to_59_99']
                                elif strike_rate < 50:
                                    points += scoring['strike_rate']['below_50']
                            else:
                                if strike_rate > 140:
                                    points += scoring['strike_rate']['above_140']
                                elif 120 <= strike_rate <= 140:
                                    points += scoring['strike_rate']['120_to_140']
                                elif 100 <= strike_rate < 120:
                                    points += scoring['strike_rate']['100_to_120']
                                elif 40 <= strike_rate < 50:
                                    points += scoring['strike_rate']['40_to_50']
                                elif 30 <= strike_rate < 40:
                                    points += scoring['strike_rate']['30_to_40']
                                elif strike_rate < 30:
                                    points += scoring['strike_rate']['below_30']

                        player_fantasy_points[player] = points

                    return player_fantasy_points

                if data["info"]["match_type"].lower() not in fantasy_points:
                    continue

                # Calculate fantasy points
                fantasy_points_result = calculate_fantasy_points(players_stats, fantasy_points, data["info"]["match_type"].lower())
                # print(fantasy_points_result)


                # Convert the dictionary to a DataFrame
                df_fantasy_points = pd.DataFrame.from_dict(fantasy_points_result, orient='index', columns=['Fantasy Points'])

                # Reset the index to have player names as a separate column
                df_fantasy_points.reset_index(inplace=True)
                df_fantasy_points.rename(columns={'index': 'Player'}, inplace=True)

                match_date = data["info"]["dates"][0]
                match_city = data["info"]["venue"]

                df_fantasy_points["Match Date"] = match_date

                team_names = []
                for player in fantasy_points_result:
                    team_names.append(players_stats[player]["team_name"])

                df_fantasy_points["Team"] = team_names

                df_fantasy_points["City"] = match_city
                df_fantasy_points["Match Type"] = data["info"]["match_type"].lower()
                # Display the DataFrame
                # print(df_fantasy_points)


                #add colomns to this df based on what features to be considered about the match


                output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_fantasy_points.csv")
                df_fantasy_points.to_csv(output_path, index=False)