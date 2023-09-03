import pandas as pd
from recommendation import cosine_sim
df_games = pd.read_parquet(r'src\data\clean_games.parquet.gzip')
def recommendations(id_del_producto: str):
    item_indice = df_games[df_games['id'] == id_del_producto].index[0]
    items_similares = list(enumerate(cosine_sim[item_indice]))
    recommended_items = sorted(items_similares, key=lambda x: x[1], reverse=True)
    indices = [index for index, _ in recommended_items[1:10]]
    recommended_items = df_games.iloc[indices]['id'].tolist()
    return recommended_items
print(recommendations('749540'))