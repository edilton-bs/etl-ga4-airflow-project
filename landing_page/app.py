from flask import Flask, render_template, jsonify, request
import pandas as pd
import requests
import base64
import os
# from tmdbv3api import TMDbs

app = Flask(__name__)

# Carregar o CSV 
# df = pd.read_csv('static/filmes_tmdb.csv')  
df = pd.read_csv('static/movies_final.csv')

# dar Gêneros aleatórios para os filmes
# generos = ['Ação', 'Aventura', 'Comédia', 'Drama', 'Terror', 'Ficção Científica', 'Romance', 'Animação']
# df['Genre'] = df['Title'].apply(lambda x: generos[len(x) % len(generos)])

# dar pontuação aleatória para os filmes
# df['Vote_Average'] = df['Title'].apply(lambda x: round(5 + (len(x) % 5) * 2 + (len(x) % 3), 1))

# remove todas as linhas que tiver algum valor nulo/NaN
# df.dropna(inplace=True)

# df['Year'] = pd.to_datetime(df['Release_Date'], errors='coerce').dt.year

# Gerar preços aleatórios para os filmes
# df['Price'] = df['Title'].apply(lambda x: round(10 + (len(x) % 5) * 2 + (len(x) % 3), 2))

# Resetar índice para usar como id único
# df = df.reset_index().rename(columns={'index': 'id'})

TMDB_API_KEY = 'ad4fb9197822289cfcb5b3b145474b3f'
BASE_URL = 'https://api.themoviedb.org/3'



@app.route('/')
def index():
    # 1) Buscar os 5 filmes trending da semana
    trending_url = f"{BASE_URL}/trending/movie/week"
    params = {'api_key': TMDB_API_KEY, 'language': 'pt-BR'}
    resp = requests.get(trending_url, params=params)
    results = resp.json().get('results', [])[:10]

    movies = []
    for m in results:
        movie = {
            'title': m.get('title'),
            'poster': f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get('poster_path') else None,
            'rating': m.get('vote_average'),
            'trailer': None
        }
        # 2) Buscar vídeos e encontrar o trailer no YouTube
        videos_url = f"{BASE_URL}/movie/{m['id']}/videos"
        vids = requests.get(videos_url, params=params).json().get('results', [])
        for v in vids:
            if v.get('type') == 'Trailer' and v.get('site') == 'YouTube':
                movie['trailer'] = f"https://www.youtube.com/watch?v={v.get('key')}"
                break
        movies.append(movie)

    return render_template('index.html', movies=movies)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

# 2) Rota que retorna JSON de filmes, opcionalmente filtrado por gênero
@app.route('/films')
def get_films():
    genre = request.args.get('genre')
    data = df.copy()
    if genre and genre != 'Todos':
        data = data[data['Genre'].str.contains(genre, case=False, na=False)]
    # Garante as colunas corretas
    films = data[['Title', 'Poster_Url', 'Genre', 'Year', 'Price', 'Overview', 'Vote_Average', 'id', 'Original_Language', 'Director']].to_dict(orient='records')
    return jsonify(films)


# Rota de detalhe
@app.route('/film/<int:film_id>')
def film_detail(film_id):
    # Busca o filme pelo id
    film = df[df['id'] == film_id]
    if film.empty:
        # opcional: 404 customizado
        return "Filme não encontrado", 404
    # Converte para dict simples
    film = film.iloc[0].to_dict()

    # supondo que 'film' seja um dict vindo do seu DataFrame ou API
    # film['Trailer'] = film.get('Trailer') or ''  # substitui None/NaN/float por string vazia
    return render_template('film_details.html', film=film)

@app.route('/list/<encoded_ids>')
def list(encoded_ids):
    try:
        ids_str = base64.b64decode(encoded_ids).decode()
        id_list = [int(x) for x in ids_str.split(',') if x.isdigit()]
    except Exception:
        id_list = []
    selected_films = df[df['id'].isin(id_list)]
    films = selected_films.to_dict(orient='records')
    return render_template('list.html', films=films)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
