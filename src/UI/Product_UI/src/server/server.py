from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timezone
from flask_caching import Cache
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # For production, use 'RedisCache' or 'FileSystemCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)

# # RapidAPI credentials
RAPIDAPI_KEY = "10c8c27a68msh957ab42b76eab8cp13a77cjsn68a6f784d660"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

@app.route('/api/cricket-news', methods=['POST'])
def get_cricket_news():
    try:
        # Making the request to the RapidAPI cricket news endpoint
        url = "https://cricbuzz-cricket.p.rapidapi.com/news/v1/index"

        headers = {
	        "x-rapidapi-key": RAPIDAPI_KEY,
	        "x-rapidapi-host": RAPIDAPI_HOST
        }

        # Sending GET request to the RapidAPI endpoint
        response = requests.get(url, headers=headers)
        
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the response
        data = response.json()
        # print(data)

        # Extracting the latest news stories
        story_list = data.get("storyList", [])
        formatted_stories = []

        for item in story_list:
            story = item.get("story")
            if story:
                headline = story.get("hline", "No headline")
                intro = story.get("intro", "No intro")
                pub_time = story.get("pubTime", 0)
                source = story.get("source", "No source")
                cover_image = story.get("coverImage", {})
                caption = cover_image.get("caption", "No caption")
                image_source = cover_image.get("source", "No image source")
                id = story.get("id", "")

                # url = getURL(id)
                
                # Convert pub_time to an integer if it's a string
                if isinstance(pub_time, str):
                    pub_time = int(pub_time)

                # Convert publish time from timestamp to a readable format (UTC)
                if pub_time:
                    pub_time = datetime.fromtimestamp(pub_time / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                
                # Append formatted story
                formatted_stories.append({
                    "headline": headline,
                    "intro": intro,
                    "published_on": pub_time,
                    "source": source,
                    "caption": caption,
                    "image_source": image_source,
                    "id": id,
                })

        # Return the formatted news stories as JSON
        if formatted_stories:
            return jsonify({"news": formatted_stories})
        else:
            return jsonify({"message": "No news found."}), 404
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error fetching data from the RapidAPI"}), 500

@app.route('/api/cricket-news/<id>', methods=['GET'])
@cache.cached()
def getNewsURL(id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/news/v1/detail/{id}"

    headers = {
	    "x-rapidapi-key": RAPIDAPI_KEY,
	    "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    urlWrapper = data.get("appIndex", "NotFound")

    if urlWrapper == "NotFound":
        return jsonify({"url": "https://cricbuzz.com"})
    else:
        url = urlWrapper.get("webURL", "https://cricbuzz.com")
        print(url)
        return jsonify({"url": url})


@app.route('/api/cricket-matches/<param>', methods=['POST'])
def getMatchData(param):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/{param}"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)

    matches = []

    for type_match in data["typeMatches"]:
        matchType = type_match["matchType"]
        if matchType=="Women" or matchType=="Domestic":
            continue
        
        for series_match in type_match["seriesMatches"]:
            series_info = series_match.get("seriesAdWrapper", {})
            for match in series_info.get("matches", []):
                match_info = match["matchInfo"]

                # Extract required details
                matchid = match_info["matchId"]
                team1_name = match_info["team1"]["teamSName"]
                # team1_id = match_info["team1"]["teamId"]
                team2_name = match_info["team2"]["teamSName"]
                # team2_id = match_info["team2"]["teamId"]
                match_format = match_info["matchFormat"]
                start_date = match_info["startDate"]
                stadium = match_info["venueInfo"]["ground"]
                status = match_info["status"]
                state = match_info["state"]
                match_title = match_info["matchDesc"] + " of " + match_info["seriesName"]

                # Convert startDate from timestamp to readable format
                if isinstance(start_date, str):
                    start_date = int(start_date)

                if start_date:
                    dt = datetime.fromtimestamp(start_date / 1000, tz=timezone.utc)
                    formatted_date = dt.strftime('%Y-%m-%d')
                    formatted_time = dt.strftime('%H:%M:%S')
                else:
                    formatted_date = None
                    formatted_time = None

                match = {
                    "matchid": matchid,
                    "team1": team1_name,
                    # "team1id": team1_id,
                    "team2": team2_name,
                    # "team2id": team2_id,
                    "matchFormat": match_format,
                    "date": formatted_date,
                    "time": formatted_time,
                    "stadium": stadium,
                    "status": status,
                    "state": state,
                    "matchTitle": match_title,
                }
                matches.append(match)

    return jsonify({"matches": matches})


@app.route('/app/model/predict', methods=['POST'])
def get_prediction():
    data = request.get_json()

    player_names = data['player_names']

    predictions = [getFantasyPoints(name) for name in player_names]

    return jsonify({"predictions": predictions}), 200

def getFantasyPoints():
    pass

@app.route('/api/matches/<matchid>/players', methods=['GET'])
def getPlayerData(matchid):
    url = f"https://www.cricbuzz.com/cricket-match-squads/{matchid}/as"
    
    response = requests.get(url=url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all player card elements
    player_cards_left = soup.find_all('a', class_='cb-player-card-left')
    player_cards_right = soup.find_all('a', class_='cb-player-card-right')

    # Initialize a list to store player info
    players_left = []
    players_right = []

    # Extract player name and role for Team 1 (left)
    for card in player_cards_left:
        name_div = card.find('div', class_='cb-player-name-left')
        if name_div:
            name = name_div.get_text(separator='', strip=True).split('')[0].strip()
            name = name.split(' (')[0]
            role = name_div.find('span', class_='cb-font-12')
            role_text = role.text.strip() if role else 'Role not specified'
            players_left.append({'Name': name, 'Role': role_text})

    # Extract player name and role for Team 2 (right)
    for card in player_cards_right:
        name_div = card.find('div', class_='cb-player-name-right')
        if name_div:
            name = name_div.get_text(separator='', strip=True).split('')[0].strip()
            name = name.split('(')[0]
            role = name_div.find('span', class_='cb-font-12')
            role_text = role.text.strip() if role else 'Role not specified'
            players_right.append({'Name': name, 'Role': role_text})

    # Print the results
    print("Team 1 Players:")
    for player in players_left:
        print(f"Name: {player['Name']}, Role: {player['Role']}")

    print('---------------------------------')

    print("Team 2 Players:")
    for player in players_right:
        print(f"Name: {player['Name']}, Role: {player['Role']}")


if __name__ == '__main__':
    app.run(debug=True, port=5000)