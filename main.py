from fastapi import FastAPI # Imporamos nuestro constructor de apis, FastAPI
import pandas as pd
import numpy as np
import functions as fn
from fastapi.responses import HTMLResponse # Importamos este modulo que nos permite hacer los returns como codigo HTML
#from recommendation import cosine_sim # De nuestro modelo de recomendacion (recommendation.py) importamos el coseno

app = FastAPI() # Instanciamos nuestra api

# Ahora procedemos a crear un marcador para cada funcion, con su respectiva ruta
# Ademas de crear las funciones aca mismo, previamente habian sido creadas en un archivo funciones.ipynb
# Pero decidi moverlas directamente aca en vez de importarlas.

df_reviews = pd.read_parquet('clean_reviews.parquet.gzip')
df_games = pd.read_parquet('clean_games.parquet.gzip')
df_items = pd.read_parquet('clean_items_functions.parquet.gzip')

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
    return f'<p>{total_amount} : {round(percentage*100,2)}%</p>'

@app.get('/countreviews/{fecha_inicio},{fecha_fin}', response_class=HTMLResponse) # Aca separamos nuestros parametros en la ruta con una ','
def countreviews(fecha_inicio:str, fecha_fin:str):
    #def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ): Cantidad de usuarios que realizaron reviews entre las fechas dadas
    #y, el porcentaje de recomendación de los mismos en base a reviews.recommend.
    users = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                       (df_reviews['posted'] <= fecha_fin)]['user_id'].unique() # Conseguimos los usuarios entre las fechas dadas

    pos = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                     (df_reviews['posted'] <= fecha_fin) &
                     (df_reviews['recommend'] == 1)]['recommend'].count() # Conseguimos las recomendaciones positivas
                     
    total_r = df_reviews[(df_reviews['posted'] >= fecha_inicio) &
                     (df_reviews['posted'] <= fecha_fin)]['recommend'].count() # Y aca las recomendaciones sin importar cual son
    percentage = pos/total_r # Hacemos el porcentaje
    return f'<p>{len(users)} : {round(percentage,2)*100}%</p>' # Y retornamos

@app.get('/genre/{genero}', response_class=HTMLResponse)
def genre(genero: str): # Esta funcion es a que mas se demora
    #def genre( género : str ): Devuelve el puesto en el que se encuentra un género
    #sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.
    generos_unicos = df_games['genres'].unique() # Extraemos nuestros generos unicos
    sumas_por_genero = {} # Instanciamos un diccionario
    for gen in generos_unicos: # Recorremos nuestros generos
        lista_ids = df_games[df_games['genres'] == gen]['id'].drop_duplicates().tolist() # Y conseguimos los juegos de nuesto genero
        suma = df_items.loc[df_items['item_id'].isin(lista_ids)]['playtime_forever'].sum() # Extraemos las horas/minutos de juego y la sumamos
        sumas_por_genero[gen] = suma #Obtenemos la suma de ese genero y la agregamos al diccionario
    sumas_por_genero_ordenado = dict(sorted(sumas_por_genero.items(), key=lambda item: item[1], reverse=True)) # Creamos el ranking
    ranking = list(sumas_por_genero_ordenado.keys()).index(genero) + 1 # Conseguimos el puesto de nuestro genero
    return f'<p>{genero} : {ranking}</p>' # Retornamos

@app.get('/userforgenre/{genero}', response_class=HTMLResponse)
def userforgenre(genero: str):
    df_games = pd.read_parquet('clean_games_functions.parquet.gzip')
    #def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado,
    #con su URL (del user) y user_id.
    genre_hours = df_items.merge(df_games, left_on='item_id', right_on='id') # Unimos los datasets de items y juegos
    genre_hours = genre_hours[genre_hours['genres'] == genero] # Tenemos nuestros datos de nuestro genero
    user_total_hours = genre_hours.groupby('user_id')['playtime_forever'].sum() # Ahora obtenemos la suma de juego por cada usuario
    top_users = user_total_hours.sort_values(ascending=False).head(5) # Conseguimos nuestro top 5
    top = '' # Este va a ser nuestro resultado
    for user_id, total_hours in top_users.items(): # Recorremos el top 5
        user_info = df_items[df_items['user_id'] == user_id].iloc[0] # Extraemos la informacion necesaria del usuario
        top+=f'<p>{user_info.user_id}, {round(total_hours/60,2)}, {user_info.user_url}</p>' # Y agregamos al resultado, el user, las horas y el url
    return top # Retornamos

@app.get('/developer/{company_name}', response_class=HTMLResponse)
def developer(company_name: str):
    df_games = pd.read_parquet('clean_games_functions.parquet.gzip')
    #def developer( desarrollador : str ): Cantidad de items y porcentaje
    # de contenido Free por año según empresa desarrolladora.
    frees = df_games[(df_games.publisher == company_name) & ((df_games.price == 0) | df_games.price.isnull())].drop_duplicates(subset=['id'])
    # Extraemos los juegos gratis de la compañia
    frees = frees.groupby('year')['app_name'].nunique() # Y aca tenemos el total de juegos gratis unicos 

    alls = df_games[df_games.publisher == company_name].groupby('year')['app_name'].nunique() # Ahora el total de juegos de esa compañia

    answer_matrix = (frees/alls).fillna(0) # Creamos la division como una matriz
    answer = f'<p>| {company_name} | | |</p><p>|-----|---------------------|</p><p>| Año | Contenido Free |</p>' # Nuestra respuesta HTML
    for year, percentage in answer_matrix.items(): # Recorremos la matriz
        answer += f"<p>| {year} | {percentage*100:.0f}% |</p>" # Sumamos a nuestra respuesta, la informacion por año
    return answer # Retornamos

@app.get('/sentiment_analysis/{year}', response_class=HTMLResponse)
def sentiment_analysis(year: str):
    #def sentiment_analysis( año : int ): Según el año de lanzamiento,
    #se devuelve una lista con la cantidad de registros de reseñas de usuarios
    # que se encuentren categorizados con un análisis de sentimiento.
    # Creamos una funcion que extrae el año de las fechas en las que puede hacerlo
    year_data = df_reviews[df_reviews['year'] == year] # Coseguimos los datos de nuestro año
    sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'} # Mapeamos los sentimientos con su respectiva palabra
    sentiment_counts = year_data['sentiment_analysis'].map(sentiment_mapping).value_counts().to_dict() # Contamos esos sentimientos
    return f'<p>{sentiment_counts}</p>' # Y los retornamos

@app.get('/recomendacion_juego/{id_de_producto}', response_class=HTMLResponse)
def recomendacion_juego(id_del_producto: str):
    #def recomendacion_juego( id de producto ): Ingresando el id de producto,
    # deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
    from recommendation import cosine_sim
    df_games = pd.read_parquet('clean_games_functions.parquet.gzip')
    item_indice = df_games[df_games['id'] == id_del_producto].index[0] # Extraemos el indice de nuestro juego en nuestro dataset de juegos
    items_similares = list(enumerate(cosine_sim[item_indice])) # Conseguimos nuestros items similares
    recommended_items = sorted(items_similares, key=lambda x: x[1], reverse=True) # Ahora ordenamos para saber nuestros items mas recomendados
    indices = [index for index, _ in recommended_items[1:10]] # Extraemos los indices de los juegos
    recommended_items = df_games.iloc[indices]['id'].tolist() # Convertimos a listas con nuestros ids, (podriamos poner nuestros app_name)
    recomedations = ""
    for i in recommended_items[:5]:
        recomedations+=f'<p>{i}</p>'
    return recomedations # Retornamos los primeros 5
