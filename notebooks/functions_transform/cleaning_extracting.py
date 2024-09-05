import pandas as pd
import numpy as np
import utm
import requests
import time
from math import radians, sin, cos, sqrt, atan2
import folium.map
from dotenv import dotenv_values,load_dotenv
import os
# API = os.getenv('GOOGLE_API_KEY')

#Funcion para visualizar mapas dados ciertos parametros

def map_madrid(df:pd.DataFrame,latitud:str,longitud:str,name:str)->folium.map:
    """_summary_

    Args:
        df (pd.DataFrame): dataframe with the data
        latitud (str): name of the column in string format where the latitud is
        longitud (str): name of the column in string format where the longitud is
        name (str): name of the name column in string format

    Returns:
        _type_: _description_
    """
    map_m = folium.Map(location=[40.4168, -3.7038], zoom_start=14)

    for (index, row) in df.iterrows():
        folium.Marker(location = [row.loc[latitud], row.loc[longitud]],popup = row.loc[name],tooltip = "click").add_to(map_m)
    return map_m

#funcion para calcular distancia entre 2 coordenadas geograficas
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371000  
    return r * c

def grid(start_lat:float,start_lng:float,lat_diff:float,lng_diff:float)->list[tuple]:
    
    lat_range = np.arange(start_lat - 0.060, start_lat + 0.060, lat_diff) 
    lng_range = np.arange(start_lng - 0.060, start_lng + 0.060, lng_diff)  
    coordinates = [(lat, lng) for lat in lat_range for lng in lng_range]
    
    return coordinates

#funcion para detectar columnas con valores NaN
def list_of_columns_function(df):
    x=[]
    for column in df.columns:
        if df[column].isna().any():
           x.append(column)
    return x

#funcion para visualizar la cantidad de nan por columnas
def visualization_of_nan(df):
    for column in df.columns:
        if df[column].isna().any():
            nan_count = df[column].isna().sum()
            print(f"Column '{column}' has {nan_count} NaN values.")
        # else:
        #     print(f"Column `{column}´ has no NaN values.")  
        
def cleaner(df:pd.DataFrame)-> pd.DataFrame:
    new_df= []
    for _,row in df.iterrows():
        if row["coordenada_x_local_x"] != 0:
            new_df.append(row.to_dict())
    return pd.DataFrame(new_df)

def hourglass(x, y):
    lat, lon = utm.to_latlon(x, y, 30, 'N')
    return pd.Series({'latitud': lat, 'longitud': lon})

def features_ing(total:pd.DataFrame)->pd.DataFrame:
    np.random.seed(42)
    cuisine= ['Española','India','China','Japonesa','Italiana','Latina']
    total['tipo_de_cocina']= np.random.choice(cuisine,size=len(total))
    total['delivery']= np.random.choice(['si','no'], size= len(total))
    total['reservable']= np.random.choice(['si','no'], size= len(total))
    total['desayuno']= np.random.choice(['si','no'], size= len(total))
    total['brunch']= np.random.choice(['si','no'], size= len(total))
    total['almuerzo']= np.random.choice(['si','no'], size= len(total))
    total['cena']= np.random.choice(['si','no'], size= len(total))
    total['para_llevar']= np.random.choice(['si','no'], size= len(total))
    total['comida_vegetariana']= np.random.choice(['si','no'], size= len(total))
    total['rango_de_precio']= np.random.randint(0,5,size=len(total))
    total['rating']= np.random.uniform(0,5,size=len(total)).round(1)
    return total

# Function to make the extraction from Google API 
def data_extraction(coords:list):
    df = []
    round=0
    for lat, lng in coords:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=500&type=restaurant&type=bakery&type=bar&type=cafe&type=meal_delivery&type=meal_takeaway&key={os.getenv('GOOGLE_API_KEY')}"
        params = {'pagetoken': ''}
        
        while True:
            response = requests.get(url, params)
            if response.status_code != 200:
                print("There is a problem, please confirm the requests")
                break
            
            data = response.json()
            df.extend(data.get('results', []))
            next_page_token = data.get('next_page_token')
            
            if not next_page_token:
                break
            
            params['pagetoken'] = next_page_token
            time.sleep(2)
    

        time.sleep(4)
        round += 1
        print(f'Round {round} complete.')
        

    return df
