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
   
#Defines the dataframe object and it's indexes   

#Empties the dataframe and sets all columns to default
#ringDF = pd.DataFrame(columns=ringDF.columns)

#Formats the dataframe object                                            
def insertDF(df, attributes, crafted, shaperElder, ilvl, stashID, itemID, price):
    itemNums = []
    columnStrings = []
    columns = df.columns
    appendDict = {}
    isCrafted = 0

    for s in range(0, len(columns)):
        for i in range(0, len(attributes)):
            itemString = attributes[i]
            columnString = columns[s]
            if itemString.split(columnString, 1)[-1] != itemString:
                itemNums.append([float(s) for s in re.findall(r'-?\d+\.?\d*', itemString)])
                columnStrings.append(columnString)
    
    
    if crafted != 0:
        for s in range(0, len(columns)):
            for i in range(0, len(crafted)):
                craftedString = crafted[i]
                columnString = columns[s]
                if craftedString.split(columnString, 1)[-1] != craftedString:
                    itemNums.append([float(s) for s in re.findall(r'-?\d+\.?\d*', craftedString)])
                    columnStrings.append(columnString)
                    isCrafted = 1
              
    for i in range(0, len(itemNums)):
        if len(itemNums[i]) > 1:
            itemNums[i] = [np.mean(itemNums[i])]
    
    for i in range(0, len(columnStrings)):
        appendDict[columnStrings[i]] = itemNums[i][0]
    appendDict['crafted'] = isCrafted
    if shaperElder == 'shaper':
        appendDict['elder'] = 0
        appendDict['shaper'] = 1
    elif shaperElder == 'elder':
        appendDict['elder'] = 1
        appendDict['shaper'] = 0
    else:
        appendDict['elder'] = 0
        appendDict['shaper'] = 0
    appendDict['ilvl'] = ilvl
    appendDict['stashID'] = stashID
    appendDict['itemID'] = itemID
    currency = price.split('~')[1]
    numericCurrency = [float(s) for s in re.findall(r'-?\d+\.?\d*', currency)]
    if len(currency.split(' ')) >2:
        currency = currency.split(' ')[2]
    else:
        currency = 0
    if currency == 'chaos':
        if len(numericCurrency)>0:
            appendDict['price'] = numericCurrency[0]
    elif currency in currencyIndex:
        if len(numericCurrency)>0:
            appendDict['price'] = currencyIndex[currency] * numericCurrency[0]
    else:
        print(price)
        print('no match')
        appendDict['price'] = 0
    
    df = df.append(appendDict, ignore_index=True)
    return(df)

def extractItems(df, stash):
    for x in range(0, len(stash)):
        if stash[x]['public']==True:
            if stash[x]['stash'].find('~') >= 0:
                for y in range(0, len(stash[x]['items'])):
                    if stash[x]['items'][y]['frameType'] == 2:
                        if ('accessories' in stash[x]['items'][y]['category']) and (stash[x]['items'][y]['league'] == 'Bestiary'):
                            if stash[x]['items'][y]['category']['accessories'][0] == 'ring':
                                if 'craftedMods' in stash[x]['items'][y]:
                                    crafted = stash[x]['items'][y]['craftedMods']
                                else:
                                    crafted = 0
                                if ('elder' in stash[x]['items'][y]):
                                    shaperElder = 'elder'
                                if('shaper' in stash[x]['items'][y]):
                                    shaperElder = 'shaper'
                                else:
                                    shaperElder = 'normal'
                                if 'explicitMods' in stash[x]['items'][y]:
                                    df = insertDF(df=df, attributes=stash[x]['items'][y]['explicitMods'], crafted=crafted,
                                                      shaperElder=shaperElder, ilvl=stash[x]['items'][y]['ilvl'],stashID=stash[x]['id'],
                                                      itemID=stash[x]['items'][y]['id'],price=stash[x]['stash'])
                                    
    
            elif len(stash[x]['items']) >= 0:
                for y in range(0, len(stash[x]['items'])):
                    if ('note' in stash[x]['items'][y]) and (stash[x]['items'][y]['frameType'] == 2):
                        if stash[x]['items'][y]['note'].find('~') > 0:
                            if ('accessories' in stash[x]['items'][y]['category']) and (stash[x]['items'][y]['league'] == 'Bestiary'):
                                if stash[x]['items'][y]['category']['accessories'][0] == 'ring':
                                    if 'craftedMods' in stash[x]['items'][y]:
                                        crafted = stash[x]['items'][y]['craftedMods']
                                    else:
                                        crafted = 0
                                    if ('elder' in stash[x]['items'][y]):
                                        shaperElder = 'elder'
                                    if('shaper' in stash[x]['items'][y]):
                                        shaperElder = 'shaper'
                                    else:
                                        shaperElder = 'normal'
                                    if 'explicitMods' in stash[x]['items'][y]:
                                        df = insertDF(df=df, attributes=stash[x]['items'][y]['explicitMods'], crafted=crafted,
                                                      shaperElder=shaperElder, ilvl=stash[x]['items'][y]['ilvl'],stashID=stash[x]['id'],
                                                      itemID=stash[x]['items'][y]['id'],price=stash[x]['items'][y]['note'])
    
    return(df)
    
latestState = requests.get('https://www.pathofexile.com/api/trade/data/change-ids')
if latestState.status_code == 200:
    data = latestState.json()
    state = data['psapi']
#Request stash data
endpoint = 'http://www.pathofexile.com/api/public-stash-tabs'
    
currencyIndex = priceIndex('chaos')



while len(ringDF) < 10000:
    next_id =  endpoint+'?id='+state
    response = requests.get(next_id)
    if response.status_code == 200:
        data = response.json()
        state = data['next_change_id']
        stash = data['stashes']
        
    ringDF = extractItems(ringDF, stash)


   

    
LinRegression = LinearRegression()
DecRegression = DecisionTreeRegressor()
ringDF = ringDF[ringDF['price'] != 0]
ringDF = ringDF.fillna(value=0)
ringDF.info()
X = ringDF.drop(['price','stashID','itemID'],axis=1)
y = ringDF['price']
#y = ringDF.iloc[:, 63:64].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

LinRegression.fit(X_train,y_train)
DecRegression.fit(X_train,y_train)

linCDF = pd.DataFrame(LinRegression.coef_,X.columns,columns=['Coeff'])
LinearPredictions = LinRegression.predict(X_test)
plt.scatter(y_test,LinearPredictions,color = 'red')
plt.xlabel('Price in Testdata')
plt.ylabel('Predicted Price')
plt.show

print('MAE:', metrics.mean_absolute_error(y_test, LinearPredictions))
print('MSE:', metrics.mean_squared_error(y_test, LinearPredictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, LinearPredictions)))

sns.distplot((y_test-LinearPredictions),bins=50);


DecisionPredictions = DecRegression.predict(X_test)
plt.scatter(y_test,DecisionPredictions,color = 'blue')
plt.xlabel('Price in Testdata')
plt.ylabel('Predicted Price')
plt.show

t = pd.DataFrame(columns=['test','pred','diff'])
t['test'] = y_test
t['pred'] = DecisionPredictions
t['diff'] = y_test - DecisionPredictions
sns.distplot((y_test-DecisionPredictions),bins=50);

print('MAE:', metrics.mean_absolute_error(y_test, DecisionPredictions))
print('MSE:', metrics.mean_squared_error(y_test, DecisionPredictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, DecisionPredictions)))




    
    
    
    
    
    
    
    
    
    
    
    
    
