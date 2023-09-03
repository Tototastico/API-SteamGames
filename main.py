from fastapi import FastAPI
import pandas as pd
import numpy as np
from fastapi.responses import HTMLResponse
from recommendation import cosine_sim
#pip intall fastparquet

df_games = pd.read_parquet(r'src\data\clean_games.parquet.gzip')
df_items = pd.read_parquet(r'src\data\clean_items.parquet.gzip')
df_reviews = pd.read_parquet(r'src\data\clean_reviews.parquet.gzip')

app = FastAPI()

@app.get('/userdata/{User_id}', response_class=HTMLResponse)
def userdata(User_id: int):
    User_id = str(User_id)
    user_games = df_items[df_items['user_id'] == User_id]['item_id']
    user_games = user_games.tolist()
    total_amount = 0.0
    for game in user_games:
        price_data = df_games.loc[df_games['id'] == game, 'price']
        if not price_data.empty:
            price = price_data.values[0]
            total_amount += float(price)
    total_amount = round(total_amount,2)
    total_games = df_items.loc[df_items['user_id'] == User_id, 'items_count'].tolist()[0]
    user_recomendations = df_reviews[df_reviews['user_id'] == User_id]['recommend'].tolist()
    user_recomendations = sum(user_recomendations)
    percentage = user_recomendations/total_games
    return f'{total_amount}, {round(percentage*100,2)}%'

@app.get('/countreviews/{fecha_inicio},{fecha_fin}', response_class=HTMLResponse)
def countreviews(fecha_inicio:str, fecha_fin:str):
    users = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                       (df_reviews['posted'] <= fecha_fin)]['user_id'].unique()

    pos = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                     (df_reviews['posted'] <= fecha_fin) &
                     (df_reviews['recommend'] == 1)]['recommend'].count()
                     
    total_r = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                     (df_reviews['posted'] <= fecha_fin)]['recommend'].count()
    percentage = pos/total_r
    return f'{len(users)}, {round(percentage,2)*100}%'

@app.get('/genre/{genero}', response_class=HTMLResponse)
def genre(genero: str):
    generos_unicos = df_games['genres'].unique()
    sumas_por_genero = {}
    genero = 'Action'
    for gen in generos_unicos:
        lista_ids = df_games[df_games['genres'] == gen]['id'].drop_duplicates().tolist()
        suma = df_items.loc[df_items['item_id'].isin(lista_ids)]['playtime_forever'].sum()
        sumas_por_genero[gen] = suma
    sumas_por_genero_ordenado = dict(sorted(sumas_por_genero.items(), key=lambda item: item[1], reverse=True))
    ranking = list(sumas_por_genero_ordenado.keys()).index(genero) + 1
    return f'{genero} : {ranking}'

@app.get('/userforgenre/{genero}', response_class=HTMLResponse)
def userforgenre(genero: str):
    genre_hours = df_items.merge(df_games, left_on='item_id', right_on='id')
    genre_hours = genre_hours[genre_hours['genres'] == genero]
    user_total_hours = genre_hours.groupby('user_id')['playtime_forever'].sum()
    top_users = user_total_hours.sort_values(ascending=False).head(5)
    top = ''
    for user_id, total_hours in top_users.items():
        user_info = df_items[df_items['user_id'] == user_id].iloc[0]
        top+=f'{user_info.user_id}, {total_hours}, {user_info.user_url}'
    return top

@app.get('/developer/{company_name}', response_class=HTMLResponse)
def developer(company_name: str):
    frees = df_games[(df_games.publisher == company_name) & ((df_games.price == 0) | df_games.price.isnull())].drop_duplicates(subset=['id'])
    frees = frees.groupby('year')['app_name'].nunique()

    alls = df_games[df_games.publisher == company_name].groupby('year')['app_name'].nunique()

    answer_matrix = (frees/alls).fillna(0)
    answer = f'<p>| {company_name} | | |</p><p>|-----|---------------------|</p><p>| Año | Contenido Free |</p>'
    for year, percentage in answer_matrix.items():
        answer += f"<p>| {year} | {percentage*100:.0f}% |</p>"
    return answer

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    year = int(year)
    df = df_reviews.copy()
    df['year'] = df['posted'].dt.year
    year_data = df[df['year'] == year]
    sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    sentiment_counts = year_data['sentiment_analysis'].map(sentiment_mapping).value_counts().to_dict()
    return sentiment_counts

@app.get('/recomendacion_juego/{id_de_producto}')
def recommendations(id_del_producto: str):
    item_indice = df_games[df_games['id'] == id_del_producto].index[0]
    items_similares = list(enumerate(cosine_sim[item_indice]))
    recommended_items = sorted(items_similares, key=lambda x: x[1], reverse=True)
    indices = [index for index, _ in recommended_items[1:10]]
    recommended_items = df_games.iloc[indices]['id'].tolist()
    return recommended_items