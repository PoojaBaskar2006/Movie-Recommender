from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import pandas as pd
import ast

app = Flask(__name__)
CORS(app)
import os
from dotenv import load_dotenv

# This searches for the .env file and loads the variables
load_dotenv()

# Now you can use the key like this:
api_key = os.getenv("TMDB_API_KEY")


# --- 1. THE API FUNCTION (Place this at the top) ---
def fetch_poster(movie_id):
    # 👇👇 PASTE YOUR KEY BELOW 👇👇
    

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            # If TMDB has an image, return the full URL
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            # If TMDB has no image, return a placeholder
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        # If the API call fails (e.g., no internet), return error image
        return "https://via.placeholder.com/500x750?text=Error"


# --- CONFIGURATION ---
print("Attempting to load dataset...")

try:
    # 2. Load the dataset
    df = pd.read_csv('movies.csv')

    # Clean column names (remove hidden spaces)
    df.columns = df.columns.str.strip()

    print("SUCCESS! Columns found:", df.columns.tolist())


    # 3. Safe parsing function for genres
    def parse_genres(x):
        try:
            if isinstance(x, str):
                return ast.literal_eval(x)
            return x
        except:
            return []


    if 'genres' in df.columns:
        df['genres'] = df['genres'].apply(parse_genres)

except Exception as e:
    print(f"CRITICAL ERROR LOADING DATA: {e}")
    df = pd.DataFrame()


@app.route('/api/genres', methods=['GET'])
def get_genres():
    if df.empty or 'genres' not in df.columns:
        return jsonify([])

    all_genres = set()
    for genre_list in df['genres']:
        if isinstance(genre_list, list):
            for g in genre_list:
                if isinstance(g, dict) and 'name' in g:
                    all_genres.add(g['name'])
                elif isinstance(g, str):
                    all_genres.add(g)
    return jsonify(sorted(list(all_genres)))


@app.route('/api/recommend', methods=['GET'])
def recommend():
    genre_query = request.args.get('genre')

    if df.empty or not genre_query:
        return jsonify([])

    # Filter logic
    def check_genre(genre_list):
        if not isinstance(genre_list, list): return False
        for g in genre_list:
            name = g['name'] if isinstance(g, dict) else g
            if name == genre_query:
                return True
        return False

    mask = df['genres'].apply(check_genre)
    filtered = df[mask]

    # Sort logic (Top 10 to make it faster, since API calls take time)
    if 'popularity' in df.columns:
        sorted_movies = filtered.sort_values(by='popularity', ascending=False).head(10)
    else:
        sorted_movies = filtered.head(10)

    results = []

    # --- MODIFIED LOOP STARTS HERE ---
    print(f"Fetching posters for {len(sorted_movies)} movies...")  # Debug print

    for _, row in sorted_movies.iterrows():
        # 1. Get the Movie ID
        movie_id = row['id']

        # 2. Call the API function to get the image
        # This is the step that connects your ID to the internet to get the jpg
        image_url = fetch_poster(movie_id)

        # 3. Get Title and Rating
        title = row.get('title', row.get('original_title', 'Unknown Title'))
        rating = row.get('vote_average', row.get('rating', 'N/A'))

        # 4. Add to results
        results.append({
            'id': int(movie_id),
            'title': title,
            'poster_url': image_url,  # <--- Using the API result here
            'vote_average': rating
        })
    # --- MODIFIED LOOP ENDS HERE ---

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=5000)