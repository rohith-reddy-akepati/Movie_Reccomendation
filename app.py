import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e93990d2f63fa35f0bd58759247ca52d&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movie_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity1.pkl', 'rb'))

# Streamlit app configuration
st.set_page_config(page_title="HollyBox - Movie Recommender", layout="wide", page_icon="🎬")

# Custom CSS for Amazon Prime Theme
st.markdown("""
    <style>
    body {
        background-color: #232F3E; /* Dark navy background */
        font-family: 'Arial', sans-serif;
        color: #FFFFFF; /* White text */
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #131A22; /* Darker navy for navbar */
        color: #00A8E1; /* Light blue for navbar text */
        font-size: 18px;
        font-weight: bold;
    }
    .navbar div {
        cursor: pointer;
        margin: 0 10px;
    }
    .navbar div:hover {
        text-decoration: underline;
        color: #1E90FF; /* Hover effect with brighter blue */
    }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #00A8E1; /* Amazon Prime blue */
        margin: 20px 0;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #D1D5DB; /* Light gray subtitle */
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #00A8E1;
        margin: 20px 0 10px;
    }
    .movie-title {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #FFFFFF; /* White text for movie titles */
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Navbar styled for Amazon Prime Theme
st.markdown("""
    <div class="navbar">
        <div style="font-size: 30px; font-weight: bold;">🎬 HollyBox</div>
        <div style="display: flex;">
            <div>About</div>
            <div>Recommendations</div>
            <div>Privacy Settings</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="title">Discover Your Next Favorite Movie</div>', unsafe_allow_html=True)

# Subtitle
st.markdown('<div class="subtitle">Your personalized movie platform</div>', unsafe_allow_html=True)

# Search bar for recommendations
st.markdown("<h4 style='color: #00A8E1;'>Find Movies You'll Love</h4>", unsafe_allow_html=True)
selected_movie_name = st.selectbox(
    'Select a movie you like to get recommendations:',
    movies['title'].values)

if st.button('Get Recommendations'):
    st.markdown('<div class="subtitle">Recommended Movies:</div>', unsafe_allow_html=True)
    names, posters = recommend(selected_movie_name)

    if not names:
        st.error("Sorry, no recommendations found. Try another movie.")
    else:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.image(posters[idx], use_container_width=True)
                st.markdown(f'<div class="movie-title">{names[idx]}</div>', unsafe_allow_html=True)

# Trending Now Section
st.markdown('<div class="section-title">Trending Now</div>', unsafe_allow_html=True)

# Trending Movies Data with Verified URLs
trending_movies = [
    {"title": "Oppenheimer", "poster": "https://image.tmdb.org/t/p/w500/8WUVHemHFH2ZIP6NWkwlHWsyrEL.jpg"},
    {"title": "Barbie", "poster": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"},
    {"title": "Spider-Man: Across the Spider-Verse", "poster": "https://image.tmdb.org/t/p/w500/uVJmRHngHHcGGxIqST93VblfHIS.jpg"},
    {"title": "John Wick: Chapter 4", "poster": "https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg"},
    {"title": "Avatar: The Way of Water", "poster": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"},
    {"title": "The Batman", "poster": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg"},
    {"title": "Black Panther: Wakanda Forever", "poster": "https://image.tmdb.org/t/p/w500/sv1xJUazXeYqALzczSZ3O6nkH75.jpg"},
    {"title": "Doctor Strange in the Multiverse of Madness", "poster": "https://image.tmdb.org/t/p/w500/9Gtg2DzBhmYamXBS1hKAhiwbBKS.jpg"}
]

# Create a scrollable horizontal container for trending movies
for i in range(0, len(trending_movies), 5):  # Display 5 movies per row
    cols = st.columns(5)
    for j, col in enumerate(cols):
        if i + j < len(trending_movies):
            movie = trending_movies[i + j]
            with col:
                # Display fallback if the poster is missing
                poster_url = movie["poster"] if movie["poster"] else "https://via.placeholder.com/500?text=No+Image"
                st.image(poster_url, use_container_width=True)
                st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)


# Watch Again Section
st.markdown('<div class="section-title">Watch Again</div>', unsafe_allow_html=True)
watch_again = [
    {"title": "The Dark Knight", "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"},
    {"title": "Inception", "poster": "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg"},
    {"title": "Interstellar", "poster": "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg"},
    {"title": "Avengers: Endgame", "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"},
    {"title": "Titanic", "poster": "https://image.tmdb.org/t/p/w500/kHXEpyfl6zqn8a6YuozZUujufXf.jpg"}
]
cols = st.columns(5)
for idx, col in enumerate(cols):
    with col:
        st.image(watch_again[idx]["poster"], use_container_width=True)
        st.markdown(f'<div class="movie-title">{watch_again[idx]["title"]}</div>', unsafe_allow_html=True)

# Categories Section
st.markdown('<div class="section-title">Categories</div>', unsafe_allow_html=True)
categories = ["Action", "Drama", "Comedy", "Sci-Fi", "Romance"]
cols = st.columns(len(categories))
for idx, col in enumerate(cols):
    with col:
        st.button(categories[idx])

# Footer styled in Amazon Prime Theme
st.markdown("""
    <hr style="margin-top: 50px; border: 1px solid #ddd;">
    <div style="text-align: center; font-size: 14px; color: #00A8E1; background-color: #232F3E; padding: 20px; border-radius: 5px;">
        <p><strong>Contact Information:</strong></p>
        <p><strong>Name:</strong> Rohith Reddy</p>
        <p><strong>Email:</strong> <a href="mailto:rakepat@clemson.edu" style="color: #00A8E1;">rakepat@clemson.edu</a></p>
        <p><strong>Phone:</strong> 9876543210</p>
        <p><strong>GitHub:</strong> <a href="https://github.com/rakepat" target="_blank" style="color: #00A8E1;">https://github.com/rakepat</a></p>
        <p style="margin-top: 10px; color: #FFFFFF;">&copy; 2024 HollyBox. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
