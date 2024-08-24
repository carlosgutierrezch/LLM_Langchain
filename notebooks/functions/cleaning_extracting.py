import pandas as pd
import numpy as np
import utm
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