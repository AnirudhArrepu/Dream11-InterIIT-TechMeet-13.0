from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timezone
from flask_caching import Cache

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # For production, use 'RedisCache' or 'FileSystemCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)

# # RapidAPI credentials
# RAPIDAPI_KEY = "10c8c27a68msh957ab42b76eab8cp13a77cjsn68a6f784d660"
# RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

@app.route('/api/cricket-news', methods=['POST'])
def get_cricket_news():
    try:
        # Making the request to the RapidAPI cricket news endpoint
        url = "https://cricbuzz-cricket.p.rapidapi.com/news/v1/index"

        headers = {
	        "x-rapidapi-key": "10c8c27a68msh957ab42b76eab8cp13a77cjsn68a6f784d660",
	        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
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
	    "x-rapidapi-key": "10c8c27a68msh957ab42b76eab8cp13a77cjsn68a6f784d660",
	    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
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


@app.route('/api/cricket-matches/<param>', method=['POST'])
def getMatchData(param):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/{param}"

    headers = {
        "x-rapidapi-key": "d2a20b6689msh6f097e931c446a4p145a20jsn3807682cca7d",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []

    for typematches in data["typeMatches"]:
        matchType = typematches["matchType"]
        for seriesmatch in matchType[seriesmatch]:
            for match in seriesmatch["matches"]:
                team1Name = match["team1"]
                team2Name = match["team2"]
                matchformat = match["matchFormat"]
                date = match["startDate"]
                stadium = match["venueInfo"]["ground"]
                status = match["status"]
                state = match["state"]
                matchTitle = match["matchDesc"] + " of " + match["seriesName"]
                match = {
                    "team1": team1Name,
                    "team2": team2Name,
                    "matchFormat": matchformat,
                    "date": date,
                    "stadium": stadium,
                    "status": status,
                    "state": state,
                    "matchTitle": matchTitle
                }
                matches.append(match)
    
    return jsonify({"matches: ", matches})




if __name__ == '__main__':
    app.run(debug=True, port=5000)