import streamlit as st
import pandas as pd
import requests
import pickle

moviesdata = pickle.load(open('moviesdata.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetchposters(movieid):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movieid))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/{}'.format(data['poster_path'])



def recommend(movie):
    movie_index = moviesdata[moviesdata['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list_sims = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    mvindex = [movie_list_sims[i][0] for i in range(0,5)]
    mvmovie = [moviesdata.iloc[i].title for i in mvindex]
    mvid = [int(moviesdata.iloc[i].id) for i in mvindex]
    mvposters = []
    for j in mvid:
        mvposters.append(fetchposters(j))
    return mvmovie,mvposters


st.title('movie recommender')
selected_movie = st.selectbox('Select Movie',moviesdata['title'].values)
if st.button('recommend'):
    titles,posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(titles[0])
        st.image(posters[0])
    with col2:
        st.text(titles[1])
        st.image(posters[1])
    with col3:
        st.text(titles[2])
        st.image(posters[2])
    with col4:
        st.text(titles[3])
        st.image(posters[3])
    with col5:
        st.text(titles[4])
        st.image(posters[4])

