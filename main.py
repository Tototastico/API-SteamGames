from fastapi import FastAPI # Imporamos nuestro constructor de apis, FastAPI
import pandas as pd
import numpy as np
from fastapi.responses import HTMLResponse # Importamos este modulo que nos permite hacer los returns como codigo HTML
#from recommendation import cosine_sim # De nuestro modelo de recomendacion (recommendation.py) importamos el coseno

app = FastAPI() # Instanciamos nuestra api

# Ahora procedemos a crear un marcador para cada funcion, con su respectiva ruta
# Ademas de crear las funciones aca mismo, previamente habian sido creadas en un archivo funciones.ipynb
# Pero decidi moverlas directamente aca en vez de importarlas.

@app.get('/userdata/{User_id}') # Creamos nuestro marcador con la ruta del mismo nombre que la funcion
def userdata(User_id: str):
    df_games = pd.read_parquet('clean_games.parquet.gzip')
    df_reviews = pd.read_parquet('clean_reviews.parquet.gzip')
    df_items = pd.read_parquet('clean_items.parquet.gzip')
    #def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario,
    #el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    user_games = df_items[df_items['user_id'] == User_id]['item_id'] # Extraemos los juegos que tiene nuestro usuario
    user_games = user_games.tolist() # Lo convertimos a lista
    total_amount = 0.0 # Instanciamos nuestro monto total
    for game in user_games: # Recorremos los juegos del usuario
        price_data = df_games.loc[df_games['id'] == game, 'price'] # Ubicamos nuestro precio de cada juego
        if not price_data.empty: # Si el precio existe
            price = price_data.values[0] # Extraemos el numero
            total_amount += float(price) # Y lo sumamos a nuestro monto
    total_amount = round(total_amount,2) # Lo redondeamos y ya tenemos el primer punto hecho
    total_games = df_items.loc[df_items['user_id'] == User_id, 'items_count'].tolist()[0] # Ubicamos los juegos totales del usuario
    user_recomendations = df_reviews[df_reviews['user_id'] == User_id]['recommend'].tolist() # Y extraemos cuantas recomendaciones tiene
    user_recomendations = sum(user_recomendations) # Extraemos la cantidad (Si pusiesemos sum() en vez de len(), 
                                                    # Extraeriamos solamente las recomendaciones positivas de nuestros juegos)
                                                    # Pero mi interpretacion de la consigna fue que eran todas las recomendaciones,
                                                    #Sin importar si eran positivas o negativas
    percentage = user_recomendations/len(total_games) # Creamos nuestro porcentaje de recomendaciones
    return f'{total_amount}, {round(percentage*100,2)}%' # Y lo retornamos

@app.get('/countreviews/{fecha_inicio},{fecha_fin}') # Aca separamos nuestros parametros en la ruta con una ','
def countreviews(fecha_inicio:str, fecha_fin:str):
    df_reviews = pd.read_parquet('clean_reviews.parquet.gzip')
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
    return f'{len(users)}, {round(percentage,2)*100}%' # Y retornamos

@app.get('/genre/{genero}')
def genre(genero: str): # Esta funcion es a que mas se demora
    df_games = pd.read_parquet('clean_games.parquet.gzip')
    df_items = pd.read_parquet('clean_items.parquet.gzip')
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
    return f'{genero} : {ranking}' # Retornamos
 
@app.get('/userforgenre/{genero}')
def userforgenre(genero: str):
    df_games = pd.read_parquet('clean_games.parquet.gzip')
    df_items = pd.read_parquet('clean_items.parquet.gzip')
    #def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado,
    #con su URL (del user) y user_id.
    genre_hours = df_items.merge(df_games, left_on='item_id', right_on='id') # Unimos los datasets de items y juegos
    genre_hours = genre_hours[genre_hours['genres'] == genero] # Tenemos nuestros datos de nuestro genero
    user_total_hours = genre_hours.groupby('user_id')['playtime_forever'].sum() # Ahora obtenemos la suma de juego por cada usuario
    top_users = user_total_hours.sort_values(ascending=False).head(5) # Conseguimos nuestro top 5
    top = '' # Este va a ser nuestro resultado
    for user_id, total_hours in top_users.items(): # Recorremos el top 5
        user_info = df_items[df_items['user_id'] == user_id].iloc[0] # Extraemos la informacion necesaria del usuario
        top+=f'{user_info.user_id}, {total_hours}, {user_info.user_url}' # Y agregamos al resultado, el user, las horas y el url
    return top # Retornamos

@app.get('/developer/{company_name}', response_class=HTMLResponse)
def developer(company_name: str):
    df_games = pd.read_parquet('clean_games.parquet.gzip')
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

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: str):
    year = int(year)
    df_reviews = pd.read_parquet('clean_reviews.parquet.gzip')
    #def sentiment_analysis( año : int ): Según el año de lanzamiento,
    #se devuelve una lista con la cantidad de registros de reseñas de usuarios
    # que se encuentren categorizados con un análisis de sentimiento.
    # Creamos una funcion que extrae el año de las fechas en las que puede hacerlo
    year_data = df_reviews[df_reviews['year'] == year] # Coseguimos los datos de nuestro año
    sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'} # Mapeamos los sentimientos con su respectiva palabra
    sentiment_counts = year_data['sentiment_analysis'].map(sentiment_mapping).value_counts().to_dict() # Contamos esos sentimientos
    return sentiment_counts # Y los retornamos

@app.get('/recomendacion_juego/{id_de_producto}')
def recomendacion_juego(id_del_producto: str):
    df_games = pd.read_parquet('clean_games.parquet.gzip')
    #def recomendacion_juego( id de producto ): Ingresando el id de producto,
    # deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
    from recommendation import cosine_sim
    item_indice = df_games[df_games['id'] == id_del_producto].index[0] # Extraemos el indice de nuestro juego en nuestro dataset de juegos
    items_similares = list(enumerate(cosine_sim[item_indice])) # Conseguimos nuestros items similares
    recommended_items = sorted(items_similares, key=lambda x: x[1], reverse=True) # Ahora ordenamos para saber nuestros items mas recomendados
    indices = [index for index, _ in recommended_items[1:10]] # Extraemos los indices de los juegos
    recommended_items = df_games.iloc[indices]['id'].tolist() # Convertimos a listas con nuestros ids, (podriamos poner nuestros app_name)
    return recommended_items # Retornamos

@app.get('/sentiment_analysis2/{year}')
def sentiment_analysis2(year: str):
    df_games = pd.read_parquet('clean_games.parquet.gzip')
    df_games.dropna(subset=['year'], inplace=True)
    df_games['year'] = df_games['year'].astype(int)
    year = int(year)
    df_sa = df_games.copy()
    year_data = df_sa[df_sa['year'] == year]
    mapeo = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    sentiment = df_games['sentiment_analysis'].map(mapeo).value_counts().to_dict()
    return sentiment
