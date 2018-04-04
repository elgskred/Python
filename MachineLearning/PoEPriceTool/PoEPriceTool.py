import requests
import numpy as np
import pandas as pd
import re
from priceConverter import priceIndex
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
from pymongo import MongoClient
import dataframes
import pyperclip

s = pyperclip.paste()
lines = s.splitlines()


#Find all the different itemSlots(helm, boots, etc.) and the itemTypes(Zealot helmet, opal ring, etc.)
client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")
db = client['poe']
itemTypes = {}
itemSlot = db.items.distinct('armorSlot')
for item in itemSlot:
    query = db.items.distinct('typeLine',{'armorSlot':item})
    itemTypes[item] = query


#Get the dataframe containing all the possible stats for each itemSlot
DF = {}
t = ['dagger','claw','wand']
league = 'Bestiary'
lowercaseItemSlots = [x.lower() for x in itemSlot]
lowercaseItemSlots = [x.replace(' ', '_') for x in lowercaseItemSlots]
for item in t:
    func = getattr(dataframes, item)()
    documents = []
    itemNums = []
    columnStrings = []
    columns = func.columns
    query = db.items.find({'armorSlot':'Dagger','league':league},{'_id': False})
    for q in query:
        documents.append(q)
    for doc in documents:
        for c in range(0, len(columns)):
            if 'stats' in doc:
                for i in range(0, len(doc['stats'])):
                    itemString = doc['stats'][i]
                    columnString = columns[c]
                    if itemString.split(columnString, 1)[-1] != itemString:
                        itemNums.append([float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)])
                        columnStrings.append(columnString)
        if 'crafted' in doc:
            for s in range(0, len(columns)):
                for i in range(0, len(doc['crafted'])):
                    craftedString = doc['crafted'][i]
                    columnString = columns[c]
                    if craftedString.split(columnString, 1)[-1] != craftedString:
                        itemNums.append([float(s) for s in re.findall(r'-?\d+\.?\d*', craftedString)])
                        columnStrings.append(columnString)
                        isCrafted = 1
    


regex = "Gain ..% of Physical Damage as Extra Fire Damage"
l = ['Socketed Gems are Supported by Level 22 Added Fire Damage','Socketed Gems are Supported by Level 16 Added Fire Damage','235 to Accuracy Rating']
l2 = ["+28 to Dexterity", "Gain 33% of Physical Damage as Extra Fire Damage", "Gain 18% of Physical Damage as Extra Cold Damage","+275 to Accuracy Rating",'Socketed Gems are Supported by Level 16 Added Fire Damage',"5% chance to gain Onslaught for 4 seconds on Kill",'Socketed Gems are Supported by Level 18 Faster Attacks']
matches = [string for string in l2 if re.match(regex, string)]
t = dataframes.dagger()
col = t.columns
for c in range(0, len(col)):
    for i in range(0, len(l2)):
        matches = [string for string in l2 if re.match(col[c], string)]
        if len(matches) > 0:
            print(matches)
        itemString = l2[i]
        columnString = col[c]
        if itemString.split(columnString, 1)[-1] != itemString:
            #print(itemString.split(columnString, 1)[-1])
            #print(columnString)
            continue








    
for item in itemSlot:
    documents = []
    query = db.items.find({'armorSlot':'Dagger'},{'_id': False})
    for q in query:
        documents.append(q)
        

    
    for s in range(0, len(columns)):
        for i in range(0, len(attributes)):
            itemString = attributes[i]
            columnString = columns[s]
            if itemString.split(columnString, 1)[-1] != itemString:
                itemNums.append([float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)])
                columnStrings.append(columnString)


