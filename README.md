# Movie Recommendation System 🎬

A full-stack movie recommendation application built with **React (Vite)** and **Python (Flask)**, utilizing the **TMDB Dataset** and **TMDB API**.

## 🚀 Features
- **Movie Search:** Real-time search using the TMDB API.
- **Content-Based Filtering:** Suggests similar movies using Cosine Similarity logic.
- **Dynamic UI:** Modern interface displaying high-quality posters and metadata.
- **Efficient Asset Loading:** Fast performance powered by Vite.

## 🛠️ Tech Stack
- **Frontend:** React.js, Vite, Axios, CSS3
- **Backend:** Python, Flask, Scikit-learn, Pandas
- **Data:** TMDB API & TMDB 5000 Movies Dataset (CSV)

## 📊 Dataset & Machine Learning
- **Dataset:** I used the TMDB 5000 Movie Dataset to extract features like genres, keywords, and cast.
- **Processing:** Data cleaning and tags creation were performed using Pandas.
- **Algorithm:** The system calculates the distance between movie vectors using **Cosine Similarity** to provide the most accurate recommendations.

## 🌐 API Integration
- This project fetches real-time movie details (posters, descriptions, and ratings) using the **TMDB API**. 
- A custom fetching function maps the local movie IDs to the TMDB database to retrieve visuals.

## 🛡️ Security
- **Sensitive Info:** All API keys are stored in a `.env` file.
- **Gitignore:** The `.env`, `node_modules`, and `venv` folders are excluded from this repository to ensure security and light weight.

## 🔧 Setup & Installation

### Frontend
1. `cd movie-project` (or your root folder)
2. `npm install`
3. `npm run dev`

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create a `.env` file to add api
4. `python app.py`

---