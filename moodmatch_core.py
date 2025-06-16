import os
import torch
import spotipy
from PIL import Image
from dotenv import load_dotenv
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load models once
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

genres = ["pop", "indie-pop", "rock", "hip-hop", "rap", "trap", "r-n-b", "soul", "jazz", "classical",
          "electronic", "ambient", "folk", "funk", "blues", "reggaeton", "country", "punk", "k-pop",
          "metal", "techno", "lo-fi", "alternative"]

def run_moodmatch(image: Image.Image, language=None, mood=None):
    # Generate caption
    inputs = blip_processor(image, return_tensors="pt").to(device)
    caption_ids = blip_model.generate(**inputs)
    caption = blip_processor.decode(caption_ids[0], skip_special_tokens=True)

    # CLIP genre prediction
    clip_inputs = clip_processor(text=genres, images=image, return_tensors="pt", padding=True).to(device)
    clip_outputs = clip_model(**clip_inputs)
    probs = clip_outputs.logits_per_image.softmax(dim=1).squeeze()
    genre_scores = {genres[i]: float(probs[i]) for i in range(len(genres))}
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    predicted_genre = sorted_genres[0][0]

    # Query logic
    search_queries = []
    if language and mood:
        search_queries.append(f"{mood} {language}")
    elif mood:
        search_queries.append(mood)
    elif language:
        search_queries.append(f"{predicted_genre} {language}")
    else:
        search_queries.append(f"{predicted_genre} {caption}")
    search_queries.append(caption)

    # 👉 Simulate Spotify failure for testing fallback (uncomment the next line):

    # Try Spotify search
    for query in search_queries:
        try:
            results = sp.search(q=query, type="track", limit=10)
            if results['tracks']['items']:
                tracks = results['tracks']['items']
                return {
                    "caption": caption,
                    "predicted_genre": predicted_genre,
                    "top_genres": sorted_genres[:3],
                    "tracks": [
                        {
                            "name": t['name'],
                            "artists": ", ".join([a['name'] for a in t['artists']]),
                            "url": t['external_urls']['spotify']
                        }
                        for t in tracks
                    ]
                }
        except Exception as e:
            print("⚠️ Spotify error:", e)

    # Fallback to local DB
    try:
        db = sqlite3.connect("fallback_songs.db")
        cur = db.cursor()
        cur.execute("""
            SELECT name, artists, url FROM songs
            WHERE genre = ? AND language = ?
            ORDER BY RANDOM() LIMIT 10
        """, (predicted_genre, language or "english"))
        fallback_tracks = cur.fetchall()
        db.close()

        print("📀 Using fallback DB!")  # ✅ Debug print to confirm fallback is used

        return {
            "caption": caption,
            "predicted_genre": predicted_genre,
            "top_genres": sorted_genres[:3],
            "tracks": [
                {
                    "name": row[0],
                    "artists": row[1],
                    "url": row[2]
                }
                for row in fallback_tracks
            ]
        }

    except Exception as e:
        print("❌ Fallback DB error:", e)
        return {
            "caption": caption,
            "predicted_genre": predicted_genre,
            "top_genres": sorted_genres[:3],
            "tracks": []
        }
