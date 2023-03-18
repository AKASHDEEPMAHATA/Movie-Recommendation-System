from flask import *
import pickle
import pandas as pd
import requests
from patsy import dmatrices

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w300/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7]
    recommended_movies = []
    recommended_poster = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_poster

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                recommended_movies,recommended_poster = recommend(movies_name)

                status = True

                return render_template("index.html",movies_name = recommended_movies , poster = recommended_poster , movie_list = movie_list , status = status)

        except Exception as e:
            error = {'error':e}
            return render_template("index.html", error = error , movie_list = movie_list, status = status)
        
    else:
        return render_template("index.html", movie_list = movie_list, status = status)
    
if __name__ == '__main__':
    app.run(debug=False , host="0.0.0.0")
