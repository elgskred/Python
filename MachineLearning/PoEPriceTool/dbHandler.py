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
import datetime



client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")


db = client['poe']
col = db.items.find()
for document in col:
    print (document)
print(col)





config = {
	'user': 'poeUser',
	'password': '123456',
	'host': '192.168.10.50',
	'port': '3306',
	'database': 'poe',
	'raise_on_warnings': True
}
#All possible fields in a document
#document = {
#        'stashID': '',
#        'itemID': '',
#        'stats': [],
#        'implicitStats': [],
#        'price': 0,
#        'currency': '',
#        'league': '',
#        'armorSlot': '',
#        'itemName': '',
#        'stashName': '',
#        'sockets': [],
#        'socketLinks': [],
#        'socketColors': [],
#        'armour' : 0,
#        'evasion': 0,
#        'energyShield': 0,
#        'ilvl': 0,
#        'lastCharName': '',
#        'shaper': 0,
#        'elder': 0,
#        'crafted': [],
#        'x': 0,
#        'y': 0
#}
document = {}
documents = []




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
        
    queryIDs = []
    #Loop through all stash pages returned by the api request    
    for x in range(0, len(stash)):
        
        #Check to see if the tab is public, no point in checking private tabs
        if stash[x]['public']==True:
            tab = stash[x]
            
            #Check to see if the stash tab is priced, if not, check to see if individual items are priced
            if tab['stash'].find('~') >= 0:
                #Loop through all items in the stash page
                for y in range(0, len(tab['items'])):
                    item = tab['items'][y]
                    #Checks to see if the rarity of the item is "rare"
                    if item['frameType'] == 2:
                        if next(iter(item['category'])) != 'maps':
                            if next(iter(item['category'])) == 'jewels':
                                document['armorSlot'] = item['typeLine']
                            else:
                                document['armorSlot'] = next(iter(item['category'].values()))[0]
                            if ('elder' in item):
                                elder = 1
                            if('shaper' in item):
                                shaper = 1
                            else:
                                shaper = 0
                                elder = 0
                            if 'craftedMods' in item:
                                document['crafted'] = item['craftedMods']
                            document['stashID'] = tab['id']
                            queryIDs.append(tab['id'])
                            document['itemID'] = item['id']
                            if 'explicitMods' in item:
                                document['stats'] = item['explicitMods']
                            if 'implicitMods' in item:
                                document['implicitMods'] = item['implicitMods']
                            currency = tab['stash'].split('~')[1]
                            numericCurrency = [float(s) for s in re.findall(r'-?\d+\.?\d*', currency)]
                            if len(currency.split(' ')) >2:
                                currency = currency.split(' ')[2]
                            else:
                                currency = 'unknown'
                            if currency in currencyIndex:
                                if len(numericCurrency)>0:
                                    document['price'] = numericCurrency[0]
                                    document['currency'] = currency
                            else:
                                document['price'] = 0
                                document['currency'] = 'unknown'
                            document['league'] = item['league']                           
                            if len(item['name']) > 1:
                                temp = [m.end() for m in re.finditer('>>',item['name'])]
                                document['name'] = item['name'][temp[len(temp)-1]:]
                            if 'sockets' in item:
                                document['sockets'] = len(item['sockets'])
                                tempLinks = []
                                tempColor = []
                                for i in range(0, len(item['sockets'])):
                                    tempLinks.append(item['sockets'][i]['group'])
                                    tempColor.append(item['sockets'][i]['sColour'])
                                document['socketLinks'] = tempLinks
                                document['socketColors'] = tempColor
                            if 'properties' in item:
                                for i in range(0, len(item['properties'])):
                                    if 'Armour' in item['properties'][i]['name']:
                                        document['armour'] = item['properties'][i]['values'][0][0]
                                    if 'Evasion Rating' in item['properties'][i]['name']:
                                        document['evasion'] = item['properties'][i]['values'][0][0]
                                    if 'Energy Shield' in item['properties'][i]['name']:
                                        document['energyShield'] = item['properties'][i]['values'][0][0]
                            document['ilvl'] = item['ilvl']
                            document['lastCharName'] = tab['lastCharacterName']
                            document['x'] = item['x']
                            document['y'] = item['y']
                            documents.append(document)
                            document = {}
                        else:
                            break
                        
                        
                        
                        
                            
            elif len(tab['items']) >= 0:
                for y in range(0, len(tab['items'])):
                    item = tab['items'][y]
                    #Check to see if 'note' key exists
                    if ('note' in item) and (item['frameType'] == 2):
                        #Check to see if the item is priced, all priced items contain '~' in the note
                        if item['note'].find('~') >= 0:
                            if next(iter(item['category'])) != 'maps':
                                if next(iter(item['category'])) == 'jewels':
                                    document['armorSlot'] = item['typeLine']
                                else:
                                    document['armorSlot'] = next(iter(item['category'].values()))[0]
                                if ('elder' in item):
                                    elder = 1
                                if('shaper' in item):
                                    shaper = 1
                                else:
                                    shaper = 0
                                    elder = 0
                                if 'craftedMods' in item:
                                    document['crafted'] = item['craftedMods']
                                document['stashID'] = tab['id']
                                queryIDs.append(tab['id'])
                                document['itemID'] = item['id']
                                if 'explicitMods' in item:
                                    document['stats'] = item['explicitMods']
                                if 'implicitMods' in item:
                                    document['implicitMods'] = item['implicitMods']
                                currency = item['note'].split('~')[1]

                                numericCurrency = [float(s) for s in re.findall(r'-?\d+\.?\d*', currency)]
                                if len(currency.split(' ')) >2:
                                    currency = currency.split(' ')[2]
                                else:
                                    currency = 'unknown'
                                if currency in currencyIndex:
                                    if len(numericCurrency)>0:
                                        document['price'] = numericCurrency[0]
                                        document['currency'] = currency
                                else:
                                    document['price'] = 0
                                    document['currency'] = 'unknown'
                                document['league'] = item['league']                           
                                if len(item['name']) > 1:
                                    temp = [m.end() for m in re.finditer('>>',item['name'])]
                                    document['name'] = item['name'][temp[len(temp)-1]:]
                                if 'sockets' in item:
                                    document['sockets'] = len(item['sockets'])
                                    tempLinks = []
                                    tempColor = []
                                    for i in range(0, len(item['sockets'])):
                                        tempLinks.append(item['sockets'][i]['group'])
                                        tempColor.append(item['sockets'][i]['sColour'])
                                    document['socketLinks'] = tempLinks
                                    document['socketColors'] = tempColor
                                if 'properties' in item:
                                    for i in range(0, len(item['properties'])):
                                        if 'Armour' in item['properties'][i]['name']:
                                            document['armour'] = item['properties'][i]['values'][0][0]
                                        if 'Evasion Rating' in item['properties'][i]['name']:
                                            document['evasion'] = item['properties'][i]['values'][0][0]
                                        if 'Energy Shield' in item['properties'][i]['name']:
                                            document['energyShield'] = item['properties'][i]['values'][0][0]
                                document['ilvl'] = item['ilvl']
                                document['lastCharName'] = tab['lastCharacterName']
                                document['x'] = item['x']
                                document['y'] = item['y']
                                documents.append(document)
                                document = {}
                            else:
                                break
        
        
        
    db.items.insert_many(documents) 
    #query = db.items.find({'stashID':})
    queryIDs2 = np.unique(queryIDs)
    df = pd.DataFrame.from_dict(data=documents)
    #test2 = test.drop_duplicates('stashID',keep='first')['stashID']

    
    queryID = ""
    queryDocuments = []
    replaceQuery = []
    insertQuery = []
    deleteQuery = []
    
    for doc in documents:
        if queryID != doc['stashID']:
            if queryID != "":
                #If there are any remaining documents in queryDocuments, delete them from the db,
                #they have been sold or is no longer in the stash tab
                if len(queryDocuments) > 0:
                    for d in queryDocuments:
                        deleteQuery.append(d)                    
            queryID = doc['stashID']
            query = db.items.find({'stashID': queryID},{'_id': False})
            queryDocuments = []
            queryItemIDs = []
            for document in query:
                queryDocuments.append(document)
                queryItemIDs.append(document['itemID'])
        if len(queryDocuments) > 0:
            for i, d in enumerate(queryDocuments):
                if doc['itemID'] == d['itemID']:
                    if doc == d:
                        #document is unchanged
                        queryDocuments.pop(i)
                        break
                    else:
                        #document is changed, replace it
                        replaceQuery.append(doc)
                        queryDocuments.pop(i)
                        break
                else:
                    #document does not exist in db, add it
                    insertQuery.append(doc)
                    break
        else:
            continue
    

        
        
        
    
    
    
    
    
    
    
    


