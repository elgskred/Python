from priceConverter import priceIndex
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
import pickle
import pyperclip
import re
import dataframes
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

#Find all the different itemSlots(helm, boots, etc.) and the itemTypes(Zealot helmet, opal ring, etc.)
client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")
db = client['poe']
itemTypes = {}
itemSlot = db.items.distinct('armorSlot')

for item in itemSlot:
    query = db.items.distinct('typeLine',{'armorSlot':item})
    itemTypes[item] = query

#Get the item data
lines = pyperclip.paste().split('\n')
for x in range(0,len(lines)):
    lines[x] = lines[x].rstrip()

#Find the itemType
itemType = lines[2]

for item in itemTypes.keys():
    if itemType in itemTypes[item]:
        parsedItemType = item

itemType = parsedItemType.lower()
itemType = itemType.replace(' ', '_')
#Get the stats
stats = []
linebreaks = []
  
if 'Shaper Item' in lines:
    lastLine = lines.index('Shaper Item') - 2
    for x in range(lastLine, 0, -1):
        if lines[x] != '--------':
            stats.append(lines[x])
        else:
            break
elif 'Elder Item' in lines:
    lastLine = lines.index('Elder Item') - 2
    for x in range(lastLine, 0, -1):
        if lines[x] != '--------':
            stats.append(lines[x])
        else:
            break
elif 'Corrupted' in lines:
    lastLine = lines.index('Corrupted') - 2
    for x in range(lastLine, 0, -1):
        if lines[x] != '--------':
            
            stats.append(lines[x])
        else:
            break
elif 'Note:' in lines[-1]:
    index = [i for i, s in enumerate(lines) if 'Note:' in s]
    lastLine = index[-1] - 2
    for x in range(lastLine, 0, -1):
        if lines[x] != '--------':
            stats.append(lines[x])
        else:
            break
else:
    lastLine = len(lines) - 1
    for x in range(lastLine, 0, -1):
        if lines[x] != '--------':
            print(lines[x])
            print(x)
            print('\n')
            stats.append(lines[x])
        else:
            break
        
ilvl = [i for i, s in enumerate(lines) if 'Item Level:' in s]
ilvl = [float(s) for s in re.findall(r'-?\d+\.?\d*', lines[ilvl[-1]])][-1]



df = getattr(dataframes, itemType)()
columns = df.columns
appendDict = {'ilvl':0,'elder':0,'shaper':0}
itemNums = []
columnStrings = []
for c in range(0, len(columns)):
    for i in range(0, len(stats)):
        itemString = stats[i]
        columnString = columns[c]
        findStrings = columnString.split(' ')
        if re.match(columnString,itemString):
            num = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)]
            if len(num) > 0:
                itemNums.append(num)
            else:
                itemNums.append([1])
            columnStrings.append(columnString)
        elif itemString.split(columnString, 1)[-1] == '':
            num = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)]
            if len(num) > 0:
                itemNums.append(num)
            else:
                itemNums.append([1])
            columnStrings.append(columnString)
        elif all(s in itemString for s in findStrings):
            num = [float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)]
            if len(num) > 0:
                itemNums.append(num)
            else:
                itemNums.append([1])
            columnStrings.append(columnString)
            
for i in range(0, len(itemNums)):
        if len(itemNums[i]) > 1:
            itemNums[i] = [np.mean(itemNums[i])]
if (len(itemNums) > 0) and (len(columnStrings) > 0):
        for i in range(0, len(columnStrings)):
            appendDict[columnStrings[i]] = itemNums[i][0] 

if 'Shaper Item' in lines:
    appendDict['ilvl'] = ilvl
    appendDict['shaper'] = 1
    appendDict['elder'] = 0
elif 'Elder Item' in lines:
    appendDict['ilvl'] = ilvl
    appendDict['shaper'] = 0
    appendDict['elder'] = 1
else:
    appendDict['ilvl'] = ilvl
    appendDict['shaper'] = 0
    appendDict['elder'] = 0
print('Item understood as:\n')
print(appendDict)
df = df.append(appendDict, ignore_index=True)
df = df.fillna(value=0)
    
#load model
print('\n')
print(parsedItemType)
print('\n')
filename = './models/' + parsedItemType + '.sav'
loaded_model = pickle.load(open(filename, 'rb'))
filename = './models/' + parsedItemType + '-xScale.sav'
sc_X = pickle.load(open(filename, 'rb'))
X = sc_X.transform(df)
predictions = loaded_model.predict(X)
filename = './models/' + parsedItemType + '-yScale.sav'
sc_y = pickle.load(open(filename, 'rb'))
predict_scaled = sc_y.inverse_transform(predictions)
print(predict_scaled)
    
    
    
    
    
    
    
        