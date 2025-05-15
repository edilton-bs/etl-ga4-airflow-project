from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Carregar o CSV (o caminho depende de onde o arquivo CSV está armazenado)
df = pd.read_csv('static/movies-dataset.csv')  # Ajuste o caminho conforme necessário

# remove todas as linhas que tiver algum valor nulo/NaN
df.dropna(inplace=True)

df['Year'] = pd.to_datetime(df['Release_Date'], errors='coerce').dt.year

# Gerar preços aleatórios para os filmes
df['Price'] = df['Title'].apply(lambda x: round(10 + (len(x) % 5) * 2 + (len(x) % 3), 2))




@app.route('/')
def index():
    return render_template('index.html')

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
    films = data[['Title', 'Poster_Url', 'Genre', 'Year', 'Price', 'Overview', 'Vote_Average']].to_dict(orient='records')
    return jsonify(films)

if __name__ == '__main__':
    app.run(debug=True)
