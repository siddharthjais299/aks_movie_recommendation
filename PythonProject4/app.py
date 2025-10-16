import streamlit as st
import pandas as pd
import pickle
import requests
import zipfile
import os

# ------------------- Fetch Poster Function -------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------- Recommendation Function -------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# ------------------- Load Data -------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Ensure 'data' folder exists
if not os.path.exists('data'):
    os.makedirs('data')

# Extract the ZIP file and load similarity
with zipfile.ZipFile('similarity.zip', 'r') as zip_ref:
    zip_ref.extractall('data')

# Find the pickle file inside extracted folder
similarity = None
for file in os.listdir('data'):
    if file.endswith('.pkl') or file.endswith('.pickle'):
        with open(os.path.join('data', file), 'rb') as f:
            similarity = pickle.load(f)
        break

if similarity is None:
    st.error("No .pkl file found inside similarity.zip")

# ------------------- Streamlit UI -------------------
st.title('🎬 AKS - Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
