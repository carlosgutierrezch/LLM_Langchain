import pandas as pd
import requests
from dotenv import load_dotenv,dotenv_values
from copy import deepcopy as dc

API = dotenv_values('GOOGLE_API_KEY')
r = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&keyword=cruise&key={API}')
print(r)