import pandas as pd
import numpy as np
import utm
import requests
import time

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

def trial_function(coords:list):
    df = []
    round=0
    # page=0
    for lat, lng in coords:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=500&type=restaurant&type=bakery&type=bar&type=cafe&type=meal_delivery&type=meal_takeaway&key={API}"
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
            # print(f"page: {page}")
            # page += 1
            
            time.sleep(2)
        time.sleep(4)
        round += 1
        print(f'round {round}')
        

    return df

def definitivo(*args)-> pd.DataFrame:
    data_list = [trial_function(arg) for arg in args]
    
    data_frames = [pd.json_normalize(data) for data in data_list]
    
    final_data = pd.concat(data_frames, ignore_index=True)
    
    return final_data