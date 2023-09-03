#import pandas as pd
#from sklearn.feature_extraction.text import CountVectorizer
#import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import linear_kernel

#df_games = pd.read_parquet('src/data/clean_games.parquet.gzip')

#df_games.dropna(subset=['publisher'], inplace=True)

#df_games['publisher'].fillna('', inplace=True)
#df_games['genres'].fillna('', inplace=True)
#df_games['app_name'].fillna('', inplace=True)

#df_games = df_games[df_games['genres'] != '[]']

#tfidf_vectorizer = TfidfVectorizer()
#tfidf_matrix = tfidf_vectorizer.fit_transform(df_games['publisher']+' '+df_games['genres']+' '+df_games['app_name'])

#cosine_sim = cosine_similarity(tfidf_matrix,tfidf_matrix)

import pandas as pd
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
df_games = pd.read_parquet('clean_games.parquet.gzip')
games = df_games

generos_a_excluir = [
 'Simulation',
 'Strategy',
 'Free to Play',
 'RPG',
 'Sports',
 '[]',
 'Racing',
 'Early Access',
 'Massively Multiplayer',
 'Animation &amp; Modeling',
 'Video Production',
 'Utilities',
 'Web Publishing',
 'Education',
 'Software Training',
 'Design &amp; Illustration',
 'Audio Production',
 'Photo Editing',
 'Accounting']
for i in generos_a_excluir:
    games = games[games['genres'] != i]
games.dropna(inplace=True)
co = CountVectorizer(max_features=7000, stop_words='english')
vector = co.fit_transform(games['genres']).toarray()
co.get_feature_names_out()
cosine_sim = cosine_similarity(vector)
