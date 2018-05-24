import numpy as np
import pandas as pd
import re
from priceConverter import priceIndex
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
import dataframes
import pickle
from sklearn.preprocessing import StandardScaler

#df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

def saveModels(item, df):
    DecRegression = DecisionTreeRegressor()
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = df.drop(['price'],axis=1)
    X = pd.DataFrame(sc_X.fit_transform(X),columns=X.columns)
    print(X.head())
    filename = './models/' + item + '-xScale.sav'
    pickle.dump(sc_X,open(filename, 'wb'))
    y = df['price']
    y = y.values.reshape(-1,1)
    y = sc_y.fit_transform(y)
    filename = './models/' + item + '-yScale.sav'
    pickle.dump(sc_y,open(filename, 'wb'))
    DecRegression.fit(X,y)
    filename = './models/' + item + '.sav'
    pickle.dump(DecRegression,open(filename, 'wb'))


def showEstimatedPriceFromTestdata(slotList, DFofDF):
    DecRegression = DecisionTreeRegressor()
    for item in slotList:
        X = DFofDF[item].drop(['price'],axis=1)
        y = DFofDF[item]['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
        
        DecRegression.fit(X_train,y_train)
        DecisionPredictions = DecRegression.predict(X_test)
        plt.figure()
        plt.scatter(y_test,DecisionPredictions,color = 'blue')
        plt.title(item)
        plt.xlabel('Price in Testdata')
        plt.ylabel('Predicted Price')
        plt.show
        
        t = pd.DataFrame(columns=['test','pred','diff'])
        t['test'] = y_test
        t['pred'] = DecisionPredictions
        t['diff'] = y_test - DecisionPredictions
        plt.figure()
        sns.distplot((y_test-DecisionPredictions),bins=50);

def insertToDF(df, doc):
    columns = df.columns
    appendDict = {}
    itemNums = []
    columnStrings = []
    
    for c in range(0, len(columns)):
        if 'stats' in doc:
            for i in range(0, len(doc['stats'])):
                itemString = doc['stats'][i]
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
    if 'crafted' in doc:
        for c in range(0, len(columns)):
            for i in range(0, len(doc['crafted'])):
                craftedString = doc['crafted'][i]
                columnString = columns[c]
                findStrings = columnString.split(' ')
                if craftedString == 'Can have multiple Crafted Mods':
                    itemNums.append([1])
                    columnStrings.append('Can have multiple Crafted Mods')
                elif re.match(columnString,craftedString):
                    num = [float(s) for s in re.findall(r'-?\d+\.?\d*', craftedString)]
                    if len(num) > 0:
                        itemNums.append(num)
                    else:
                        itemNums.append([1])
                    columnStrings.append(columnString)
                elif craftedString.split(columnString, 1)[-1] != craftedString:
                    num = [float(s) for s in re.findall(r'-?\d+\.?\d*', craftedString)]
                    if len(num) > 0:
                        itemNums.append(num)
                    else:
                        itemNums.append([1])
                    columnStrings.append(columnString)
                elif all(s in itemString for s in findStrings):
                    num = [float(s) for s in re.findall(r'-?\d+\.?\d*', craftedString)]
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
    appendDict['ilvl'] = doc['ilvl']
    if 'currency' in doc:
        if doc['currency'] in currencyIndex:
            appendDict['price'] = currencyIndex[doc['currency']] * doc['price']
        else:
            appendDict['price'] = 0
    else:
        appendDict['price'] = 0
    if 'shaper' in doc:
        if doc['shaper'] == 1:
            appendDict['shaper'] = 1
            appendDict['elder'] = 0
    elif 'elder' in doc:
        if doc['elder']== 1 :
            appendDict['shaper'] = 0
            appendDict['elder'] = 1
    else:
        appendDict['shaper'] = 0
        appendDict['elder'] = 0
    #df = df.loc[~df.index.duplicated(keep='first')]
    return(df.append(appendDict, ignore_index=True))


#Find all the different itemSlots(helm, boots, etc.) and the itemTypes(Zealot helmet, opal ring, etc.)
client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")
db = client['poe']
itemTypes = {}
itemSlot = db.items.distinct('armorSlot')
print('Getting the currencyIndex\n')
currencyIndex = priceIndex('chaos')

for item in itemSlot:
    query = db.items.distinct('typeLine',{'armorSlot':item})
    itemTypes[item] = query
for item in itemSlot:
    documents = []
    query = db.items.find({'armorSlot':'Dagger'},{'_id': False})
    for q in query:
        documents.append(q)
t = ['Fishing Rod']

league = 'Bestiary'
DFofDF = {}

for item in itemSlot:
    print(item)
    lowercaseItem = item.lower()
    lowercaseItem = lowercaseItem.replace(' ', '_')
    try:
        getattr(dataframes,lowercaseItem)()
    except AttributeError:
        continue
    else:
        func = getattr(dataframes, lowercaseItem)()
        documents = []
        itemNums = []
        columnStrings = []
        columns = func.columns
        query = db.items.find({'armorSlot':item,'league':league},{'_id': False}).limit(5000)
        for q in query:
            documents.append(q)
        print('Starting dataframe processing for item:', item)
        for doc in documents:
            func = insertToDF(func, doc)
        func = func[func['price'] != 0]
        func = func.fillna(value=0)
        DFofDF[item] = func
        print('Training and saving model for item:', item)
        print('\n')
        saveModels(item, func)

#showEstimatedPriceFromTestdata(itemSlot, DFofDF)






