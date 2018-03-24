import requests
import time
import json
import mysql.connector
from datetime import date, datetime, timedelta
from mysql.connector import errorcode
from priceConverter import priceIndex
import re
import numpy as np
import pandas as pd
from pymongo import MongoClient


client = MongoClient('mongodb://poeUser:12345678@192.168.10.50/poe')

db = client.get_default_database()
print(db)
assert db.name == 'poe'
db = client.get_database()
assert db.name == 'poe'




config = {
	'user': 'poeUser',
	'password': '123456',
	'host': '192.168.10.50',
	'port': '3306',
	'database': 'poe',
	'raise_on_warnings': True
}



latestState = requests.get('https://www.pathofexile.com/api/trade/data/change-ids')
if latestState.status_code == 200:
    data = latestState.json()
    state = data['psapi']
#Request stash data
endpoint = 'http://www.pathofexile.com/api/public-stash-tabs'

currencyIndex = priceIndex('chaos')

while True:
    next_id =  endpoint+'?id='+state
    response = requests.get(next_id)
    if response.status_code == 200:
        data = response.json()
        state = data['next_change_id']
        stash = data['stashes']
