import pandas as pd
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
