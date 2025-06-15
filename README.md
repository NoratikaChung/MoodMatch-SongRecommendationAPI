# MoodMatch-SongRecommendationAPI
An image based song recommendation API, fetches you songs based on the image uploaded as well as your preferences

This is the backend API for the **MoodMatch** mobile application — an AI-powered platform that recommends songs and captions based on the mood and content of an uploaded image.

---

## 🌟 Features

- 🎶 **AI-Powered Song Recommendation**
  Analyzes image content using CLIP and maps it to the closest Spotify genres.

- ✍️ **Automatic Caption Generation**
  Generates captions that match the detected mood or theme of the image.

- 📡 **REST API with FastAPI**
  Built with FastAPI, optimized for performance and quick development.

- 🔒 **Environment-secured credentials**
  Uses `.env` file to store sensitive credentials (e.g., Spotify API keys).

---

## 🛠️ Tech Stack

- Python 3.12+
- FastAPI
- Uvicorn
- HuggingFace Transformers
- CLIP Model (via `transformers`)
- Spotify Web API (via `spotipy`)
- Python-dotenv

---

## 🚀 Getting Started

### 🔐 Prerequisites

- Python installed
- Spotify Developer Account (Client ID and Secret)
- Git & virtual environment setup

### 📥 Clone & Setup

```bash
git clone https://github.com/YourUsername/MoodMatch-SongRecommendationAPI.git
cd MoodMatch-SongRecommendationAPI
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
