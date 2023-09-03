import pandas as pd
import pickle

with open('clean_items_genreFunction.pkl', 'rb') as f:
    df_items = pickle.load(f)
with open('clean_games_genreFunction.pkl', 'rb') as f:
    df_games = pickle.load(f)

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
    return f'{genero} : {ranking}' # Retornamos
