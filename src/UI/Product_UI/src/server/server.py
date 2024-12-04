from flask import Flask, request, jsonify, make_response, render_template, session, flash, redirect, url_for
from flask_cors import CORS
import requests
from datetime import datetime, timezone, timedelta
from flask_caching import Cache
import jwt
from functools import wraps
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

MONGO_URI = "mongodb+srv://shankhesh01:qRxyuHlQGRL0BrpA@team97sudo.fkb7v.mongodb.net/?retryWrites=true&w=majority&appName=Team97sudo"
client = MongoClient(MONGO_URI)
db = client["team97db"]  # Replace with your database name
users_collection = db["Users"]  # Replace with your collection name
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SasaankJaiminAyushMokshitAnirudh97SudoShankhesh'
CORS(app)  # Enable CORS for all routes

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # For production, use 'RedisCache' or 'FileSystemCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)

# # RapidAPI credentials
RAPIDAPI_KEY = "10c8c27a68msh957ab42b76eab8cp13a77cjsn68a6f784d660"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

@app.route('/api/cricket-news', methods=['POST'])
@cache.cached(timeout=1800)
def get_cricket_news():
    print("getting news")
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
@cache.cached(timeout=7200)
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

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated

@app.route('/auth')
@token_required
def auth(): 
    return 'JWT is verified. Welcome to your dashboard!'

@app.route('/matches', methods=['POST','GET'])
@token_required
def auth_matches():
    pass

@app.route('/api/cricket-matches/<param>', methods=['POST'])
# @token_required  # Protect this route with the token_required decorator
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
        if matchType=="Domestic":
            continue
        for series_match in type_match["seriesMatches"]:
            series_info = series_match.get("seriesAdWrapper", {})
            for match in series_info.get("matches", []):
                match_info = match["matchInfo"]

                # Extract required details
                matchid = match_info["matchId"]
                # team1_id = match_info["team1"]["teamId"]
                team1_name = match_info["team1"]["teamSName"]
                team1id = match_info["team1"]["imageId"]
                
                # team2_id = match_info["team2"]["teamId"]
                team2_name = match_info["team2"]["teamSName"]
                team2id = match_info["team2"]["imageId"]
                
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
                    "team1id": team1id,
                    "team2": team2_name,
                    "team2id": team2id,
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

@app.route('/login', methods=['POST'])
def login_page():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Retrieve the user from the database
    user = users_collection.find_one({"username": username})

    if user and check_password_hash(user['password'], password):
        # Generate JWT token
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(seconds=3600)  # 1 hour expiration
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token, 'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/SignUp', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    # print(username)
    password = data.get('password')
    # print(password)

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Check if username already exists in the database
    if users_collection.find_one({"username": username}):
        return jsonify({'message': 'Username already exists! Please choose a different one.'}), 409

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the new user into the database
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({'message': 'Signup successful! Please log in.'}), 201

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/app/model/predict', methods=['POST'])
def get_prediction():
    data = request.get_json()

    player_names = data['player_names']

    predictions = [getFantasyPoints(name) for name in player_names]

    return jsonify({"predictions": predictions}), 200

def getFantasyPoints():
    pass

@app.route('/api/cricket-matches/<matchid>/players', methods=['GET'])
@cache.cached(timeout=7200)
def getPlayerData(matchid):
    # print(matchid)
    url = f"https://www.cricbuzz.com/cricket-match-squads/{matchid}/as"
    # print(url)

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
            name = name_div.get_text(separator='~', strip=True).split('~')[0].strip()
            name = name.split(' (')[0]
            role = name_div.find('span', class_='cb-font-12')
            role_text = role.text.strip() if role else 'Role not specified'
            players_left.append({'name': name, 'role': role_text})

    # Extract player name and role for Team 2 (right)
    for card in player_cards_right:
        name_div = card.find('div', class_='cb-player-name-right')
        if name_div:
            name = name_div.get_text(separator='~', strip=True).split('~')[0].strip()
            name = name.split('(')[0]
            role = name_div.find('span', class_='cb-font-12')
            role_text = role.text.strip() if role else 'Role not specified'
            if "Coach" in role:
                continue
            players_right.append({'name': name, 'role': role_text})

    # # Print the results
    # print("Team 1 Players:")
    # for player in players_left:
    #     print(f"Name: {player['name']}, Role: {player['role']}")

    # print('---------------------------------')

    # print("Team 2 Players:")
    # for player in players_right:
    #     print(f"Name: {player['name']}, Role: {player['role']}")

    return jsonify({"team1": players_left, "team2": players_right})

if __name__ == '__main__':
    app.run(debug=True, port=5000)