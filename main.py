from fastapi import FastAPI
import pandas as pd
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI() #Creacion de una instancia
#Para cambiar el nombre de nuestra aplicacion y descripcion agrego lo siguiente
app.title = "Juegos de Steam"
app.description= 'Proyecto Individual N1'
#Agrego contacto de github y mail
app.contact = {"name": "Hotcer", "url": "https://github.com/Hotcer", "email": "davisguarico27@gmail.com"}

df1 = pd.read_csv('./new_users_item.csv')
df2 = pd.read_csv('./new_users_reviews.csv')
df = pd.read_csv('./new_steam_games.csv', low_memory=False)

#creacion de los endpoint, podemos usar los tags para agrupar las rutas de la aplicacion
@app.get("/", tags=['M.V.P'])
def read_root():
    # Agregamos un retorno con un mensaje personalizado
    return {"Hello": "World", "Mensaje": "¡Bienvenidos a mi proyecto de MLOps!"}

@app.get('/PlayTime', tags=['M.V.P'])
async def playTimeGenre(genero: str):
    if not genero.istitle():
        return {"error": "El género debe comenzar con mayúscula."}

    juegos_genero = df[df['genres'].str.contains(genero)]

    df1_subset = df1[df1['item_id'].isin(juegos_genero['item_id'])][["item_id", "playtime_forever"]]

    juegos_genero = pd.merge(juegos_genero, df1_subset, on='item_id', how='left')

    # Convierte la columna "release_date" al formato de fecha y hora
    juegos_genero["release_date"] = pd.to_datetime(juegos_genero["release_date"], format='%b %Y', errors='coerce')

    # Filtra las filas con valores de fecha y hora inválidos
    juegos_genero = juegos_genero.dropna(subset=["release_date"])

    # Extrae el año de lanzamiento
    juegos_genero["release_year"] = juegos_genero["release_date"].dt.year

    horas_por_año = juegos_genero.groupby("release_year")["playtime_forever"].sum()

    año_mayor_jugadas = horas_por_año.idxmax()

    # Utiliza to_json() para convertir los valores de int32 a int
    resultado = {
        f"Año de lanzamiento con mayor cantidad de horas jugadas para el género {genero}": año_mayor_jugadas.item()
    }

    return resultado


@app.get('/UserForGenre', tags=['M.V.P'])  
def UserForGenre(genero: str):
    if not genero.istitle():
        return {"error": "El género debe comenzar con mayúscula."}

    # Filter games by genre
    juegos_genero = df[df['genres'].str.contains(genero, case=False)]  

    if juegos_genero.empty:
        return f"No games found for genre {genero}"

    # Group playtime by user and sum  
    horas_por_usuario = df1.groupby('user_id')['playtime_forever'].sum()

    if horas_por_usuario.empty:
        return "No playtime data found"   

    # Get user with most hours played
    top_user = horas_por_usuario.idxmax()

    # Extract year from games
    juegos_genero['year'] = pd.to_datetime(juegos_genero['release_date'], errors='coerce').dt.year

    # Group playtime by year and sum
    horas_por_anio = horas_por_usuario.groupby(juegos_genero['year']).sum()

    # Format hours played by year  
    horas_jugadas = [{"Año": year, "Horas": horas}  
                    for year, horas in horas_por_anio.items()]

    # Return expected output format
    return {
        "Usuario con más horas jugadas para Género": top_user,
        "Horas jugadas": horas_jugadas
    }

@app.get("/UsersRecommend/{year}", tags=['M.V.P'])
async def UsersRecommend(year: int):

  df2['clean_date'] = pd.to_datetime(df2['clean_date'])

  merged_df = pd.merge(df2, df1, on='item_id')

  # Filter for year, recommended reviews, positive/neutral sentiment
  reviews_positive = merged_df[(merged_df['clean_date'].dt.year == year) &
                               (merged_df['recommend'] == True) &
                               (merged_df['sentiment_analysis'] >= 0)] 

  games_count = reviews_positive['item_name'].value_counts()

  # Get top 3 most recommended
  top3 = games_count.nlargest(3).index.tolist()

  result = [{"Puesto " + str(i+1): game} for i, game in enumerate(top3)]

  return result



# @app.get('/Usuario por genero', tags=['General'])
@app.get("/UsersNotRecommend/{year}", tags=['M.V.P'])
async def UsersNotRecommend(year: int):

  df2['clean_date'] = pd.to_datetime(df2['clean_date'])

  # Merge para unir con tabla de juegos
  merged_df = pd.merge(df2, df1, on='item_id')

  # Filtrar por año, no recomendados y sentiment negativo
  reviews_negative = merged_df[(merged_df['clean_date'].dt.year == year) &
                               (merged_df['recommend'] == False) & 
                               (merged_df['sentiment_analysis'] == 0)]

  # Contar por nombre en lugar de ID
  games_count = reviews_negative['item_name'].value_counts()

  # Obtener top 3 menos recomendados
  top3 = games_count.nsmallest(3).index.tolist()

  result = [{"Puesto " + str(i+1) : game} for i, game in enumerate(top3)]

  return result


def get_review_counts_for_year(df, year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    df_filtered = df[(df['clean_date'] >= start_date) & (df['clean_date'] <= end_date)]

    positive_reviews = len(df_filtered[df_filtered['sentiment_analysis'] == 2])
    neutral_reviews = len(df_filtered[df_filtered['sentiment_analysis'] == 1])
    negative_reviews = len(df_filtered[df_filtered['sentiment_analysis'] == 0])

    return {
        "Positive Reviews": positive_reviews,
        "Neutral Reviews": neutral_reviews,
        "Negative Reviews": negative_reviews
    }
    

@app.get('/Analisis de sentimiento', tags=['M.V.P'])
def sentiment_analysis(anio:str):
    countreviews = df2[['user_id', 'clean_date', 'sentiment_analysis']].copy()
    countreviews['clean_date'] = pd.to_datetime(countreviews['clean_date'], errors='coerce')
    countreviews['clean_date'] = countreviews['clean_date'].dt.strftime('%Y-%m-%d')
    countreviews_clean = countreviews.dropna(subset=['clean_date'])
    review_counts = get_review_counts_for_year(countreviews_clean, anio)

    result = {(f"Positivo: {review_counts['Positive Reviews']}"),
            (f"Neutral: {review_counts['Neutral Reviews']}"),
            (f"Negativo: {review_counts['Negative Reviews']}")}
    return result

@app.get("/recomendacion_usuario/{id_de_usuario}", tags=['Machine Learning'])
def recomendacion_usuario(id_usuario: int):
    # Cargar el archivo CSV
    df1 = pd.read_csv('new_users_item.csv')

    # Muestra aleatoria de datos (ajusta el tamaño según sea necesario)
    df_sample = df1.sample(n=1000, random_state=42)  # Por ejemplo, tomar una muestra de 1000 filas

    # Eliminar duplicados en df_sample si es necesario
    df_sample = df_sample.drop_duplicates(subset=['user_id', 'item_name'])

    df_sample['user_id_numerico'] = range(len(df_sample))

    # Pivotear datos
    matriz_usuarios_items = df_sample.pivot(index='user_id_numerico', columns='item_name', values='playtime_forever').fillna(0)

    # Calcular similitud coseno entre usuarios
    similitudes = cosine_similarity(matriz_usuarios_items)

    # Obtener los índices de los usuarios más parecidos
    indices_similares = similitudes[id_usuario].argsort()[-6:][::-1]

    # Quitar el índice del usuario actual
    indices_similares = indices_similares[1:]

    # Obtener items de usuarios similares
    items_similares = matriz_usuarios_items.iloc[indices_similares] 

    # Obtener items no interactuados por el usuario
    items_no_interactuados = items_similares.columns[~items_similares.columns.isin(matriz_usuarios_items.columns[matriz_usuarios_items.loc[id_usuario] > 0])]

    # Ordenar items por promedio de tiempo en usuarios similares
    items_recomendados = items_similares[items_no_interactuados].mean().sort_values(ascending=False)

    # Devolver las top 5 recomendaciones
    return list(items_recomendados.index)[:5]
  
@app.get("/recomendacion_juego/{id_juego}", tags=['Machine Learning'])
def recomendacion_juego(id_juego):

  # Leer datos
  df1 = pd.read_csv('new_users_item.csv')
  df_sample = df1.sample(n=1000, random_state=42)

  # Eliminar duplicados en df_sample si es necesario 
  df_sample = df_sample.drop_duplicates(subset=['item_name', 'user_id'])

  # Pivotear datos
  matriz_items = df_sample.pivot(index='item_name', columns='user_id', values='playtime_forever').fillna(0)

  # Calcular similitud coseno entre items
  similitudes = cosine_similarity(matriz_items)

  # Convertir id_juego a int porque inicialmente es string
  id_juego = int(id_juego)

  # Verificar que id_juego está dentro del rango de índices de similitudes
  if id_juego >= len(similitudes):
    return []
  
  # Obtener índices de items más similares
  indices_similares = similitudes[id_juego].argsort()[-6:][::-1]

  # Quitar el índice del item actual
  indices_similares = indices_similares[1:]

  # Obtener los IDs de los ítems similares
  items_similares = list(matriz_items.index[indices_similares][:5])

  return items_similares

  
  

