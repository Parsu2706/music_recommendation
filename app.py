import pickle
import streamlit as st 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "7d7b84865ce9403a83575cccf6319aa6"
CLIENT_SECRET = "63582662a5d0431ab4ef2e80e1d8a3d0"

# Initializing client credentials 
client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

def get_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        recommended_music_posters.append(get_album_cover_url(song_name, artist))
        recommended_music_names.append(song_name)

    return recommended_music_posters, recommended_music_names

st.header("Music Recommendation System")

# Fix: Use `pickle.load()`, not `pickle.loaf()`
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_li = music['song'].values

selected_music = st.selectbox(
    'Type or select a song from the dropdown',
    music_li
)

if st.button("Show Recommendation"):
    recommended_music_posters, recommended_music_names = recommend(selected_music)  
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])



