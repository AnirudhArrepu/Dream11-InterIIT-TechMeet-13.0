player_info = {
    "John": {"points": 100, "role": "Batsman"},
    "Alice": {"points": 80, "role": "Bowler"},
    "Bob": {"points": 90, "role": "All_Rounder"},
    "Charlie": {"points": 70, "role": "Wicket_Keeper"},
    "David": {"points": 85, "role": "Batsman"},
    "Eva": {"points": 95, "role": "Bowler"},
    "Frank": {"points": 75, "role": "All_Rounder"},
    "George": {"points": 65, "role": "Wicket_Keeper"},
    "Hannah": {"points": 60, "role": "Batsman"},
    "Ivan": {"points": 55, "role": "Bowler"},
    "Julia": {"points": 50, "role": "All_Rounder"},
    "Kevin": {"points": 45, "role": "Wicket-Keeper"},
    "Lily": {"points": 40, "role": "Batsman"},
    "Mike": {"points": 35, "role": "Bowler"},
    "Nina": {"points": 30, "role": "All_Rounder"},
    "Oliver": {"points": 25, "role": "Wicket_Keeper"},
    "Pamela": {"points": 20, "role": "Batsman"},
    "Quincy": {"points": 15, "role": "Bowler"},
    "Rachel": {"points": 10, "role": "All_Rounder"},
    "Samuel": {"points": 5, "role": "Wicket_Keeper"},
    "Tessa": {"points": 0, "role": "Batsman"},
    "Uma": {"points": 110, "role": "Bowler"},
    "Victor": {"points": 105, "role": "All_Rounder"},
    "Wendy": {"points": 100, "role": "Wicket_Keeper"},
    "Xavier": {"points": 95, "role": "Batsman"},
    "Yvonne": {"points": 90, "role": "Bowler"},
    "Zoe": {"points": 85, "role": "All_Rounder"}
}
# Organize players into roles
All_Rounder = {}
Batsman = {}
Bowler = {}
Wicket_Keeper = {}

for name, info in player_info.items():
    role = info['role']
    if role == "All_Rounder":
        All_Rounder[name] = info["points"]
    elif role == "Batsman":
        Batsman[name] = info["points"]
    elif role == "Bowler":
        Bowler[name] = info["points"]
    elif role == "Wicket_Keeper":
        Wicket_Keeper[name] = info["points"]

# Sort each role's players by points in descending order
All_Rounder = dict(sorted(All_Rounder.items(), key=lambda x: x[1], reverse=True))
Batsman = dict(sorted(Batsman.items(), key=lambda x: x[1], reverse=True))
Bowler = dict(sorted(Bowler.items(), key=lambda x: x[1], reverse=True))
Wicket_Keeper = dict(sorted(Wicket_Keeper.items(), key=lambda x: x[1], reverse=True))

# Choose players
chosen_players = []

# Select the best Wicket-Keeper
best_wicket_keeper = next(iter(Wicket_Keeper))
chosen_players.append((best_wicket_keeper, Wicket_Keeper[best_wicket_keeper]))
del Wicket_Keeper[best_wicket_keeper]

# Select the top 2 All-Rounders
for _ in range(2):
    best_all_rounder = next(iter(All_Rounder))
    chosen_players.append((best_all_rounder, All_Rounder[best_all_rounder]))
    del All_Rounder[best_all_rounder]

# Select the top 3 Batsmen
for _ in range(3):
    best_batsman = next(iter(Batsman))
    chosen_players.append((best_batsman, Batsman[best_batsman]))
    del Batsman[best_batsman]

# Select the top 4 Bowlers
for _ in range(4):
    best_bowler = next(iter(Bowler))
    chosen_players.append((best_bowler, Bowler[best_bowler]))
    del Bowler[best_bowler]

# Display chosen players
print("Chosen Players: ")
for player, points in chosen_players:
    print(f"{player}: {points} points")

