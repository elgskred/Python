import requests
from datetime import date, datetime, timedelta
from priceConverter import priceIndex
from removeOldDocuments import removeOld
import re
from pymongo import MongoClient


def preprocessing(stash):
    document = {}
    documents = []
    t = datetime.now()
    day = t.day
    month = t.month
    year = t.year
    print(datetime(year, month, day))
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
                        if (next(iter(item['category'])) != 'maps') and (next(iter(item['category'])) != 'monsters'):
                            if next(iter(item['category'])) == 'jewels':
                                document['armorSlot'] = 'jewel'
                            elif next(iter(item['category'])) == 'weapons':
                                document['armorSlot'] = item['properties'][0]['name']
                            else:
                                document['armorSlot'] = next(iter(item['category'].values()))[0]
                            if ('elder' in item):
                                document['elder'] = 1
                            elif('shaper' in item):
                                document['shaper'] = 1
                            else:
                                document['elder'] = 0
                                document['shaper'] = 0
                            if 'craftedMods' in item:
                                document['crafted'] = item['craftedMods']
                            document['stashID'] = tab['id']
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
                            if 'typeLine' in item:
                                document['typeLine'] = item['typeLine']
                            document['timeStamp'] = datetime(year, month, day)
                            documents.append(document)
                            document = {}
                        else:
                            continue
                        
                        
                        
                        
                            
            elif len(tab['items']) >= 0:
                for y in range(0, len(tab['items'])):
                    item = tab['items'][y]
                    #Check to see if 'note' key exists
                    if ('note' in item) and (item['frameType'] == 2):
                        #Check to see if the item is priced, all priced items contain '~' in the note
                        if item['note'].find('~') >= 0:
                            if (next(iter(item['category'])) != 'maps') and (next(iter(item['category'])) != 'monsters'):
                                if next(iter(item['category'])) == 'jewels':
                                    document['armorSlot'] = 'jewel'
                                elif next(iter(item['category'])) == 'weapons':
                                    document['armorSlot'] = item['properties'][0]['name']
                                else:
                                    document['armorSlot'] = next(iter(item['category'].values()))[0]
                                if ('elder' in item):
                                    document['elder'] = 1
                                elif('shaper' in item):
                                    document['shaper'] = 1
                                else:
                                    document['elder'] = 0
                                    document['shaper'] = 0
                                if 'craftedMods' in item:
                                    document['crafted'] = item['craftedMods']
                                document['stashID'] = tab['id']
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
                                if 'typeLine' in item:
                                    document['typeLine'] = item['typeLine']
                                document['timeStamp'] = datetime(year, month, day)
                                documents.append(document)
                                document = {}
                            else:
                                continue
    return documents


def dbhandling(documents):
    client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")
    #client = MongoClient("mongodb://poeUser:12345678@localhost/poe")
    db = client['poe']
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
                        print('deleteQ')
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
                        print('doc unchanged')
                        queryDocuments.pop(i)
                        break
                    else:
                        #document is changed, replace it
                        print('replace')
                        replaceQuery.append(doc)
                        queryDocuments.pop(i)
                        break
                else:
                    #document does not exist in db, add it
                    print('insert new')
                    insertQuery.append(doc)
                    break
        else:
            #itemID or stashID is not in the itemDB, add it
            insertQuery.append(doc)
            continue
    

        
    #Insert new items:
    db.items.insert_many(insertQuery) 
    #Delete sold or removed items:
    if len(deleteQuery) > 0:
        for doc in deleteQuery:
            db.items.delete_one({'itemID':doc['itemID']})
    #Update changed items
    if len(replaceQuery) > 0:
        for doc in replaceQuery:
            db.inventory.replace_one({'itemID':doc['itemID']}, doc)
    client.close()




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
#        'y': 0,
#        'timeStamp': date
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
        if (state != data['next_change_id']) and (len(data['stashes'])>0):
            state = data['next_change_id']
            stash = data['stashes']
            #Loop through all stash pages returned by the api request    
            documents = preprocessing(stash)
            dbhandling(documents)
            removeOld()
            print('done preprocessing and handling db functions')
    

    
    
        
    
    
    
    
    
    
    
    


