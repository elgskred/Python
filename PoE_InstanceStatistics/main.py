import psutil
import pickle
import os.path
from datetime import datetime
from datetime import timedelta
import pandas as pd
import atexit
import time as tm



def CheckIfRunning():
    if 'PathOfExile_x64Steam.exe' in (p.name() for p in psutil.process_iter()):
        return True
    else:
        return False

def CreateEmptyDataStructure():
    saveFile = 'stats.json'
    saveDict = {}
    saveDict['lastOpened'] = [] #datetime.strptime('2000/01/01,00:00:00', '%Y/%m/%d,%H:%M:%S')
    saveDict['deaths'] = 0
    saveDict['sessionStats'] = {}
    saveDict['totalStats'] = {}
    pickle.dump(saveDict, open(saveFile, 'wb'))
    return True
    
def OpenDataStructure():
    saveFile = 'stats.json'
    saveDict = pickle.load(open(saveFile, 'rb'))
    return saveDict

def CheckIfSaveExists():
    saveFile = 'stats.json'
    if os.path.isfile(saveFile):
        print('True')
        return True
    else:
        return False
    
def SaveDataStructure(saveDict):
    saveFile = 'stats.json'
    pickle.dump(saveDict, open(saveFile, 'wb'))

def iterateLogfile(lastUpdated):
    lines = []
    path_installLocation = 'C:\Program Files (x86)\Steam\steamapps\common\Path of Exile'
    logsLocation = '\logs\Client.txt'
    fullPath = path_installLocation + logsLocation
    if lastUpdated == []:
        for line in reversed(list(open(fullPath, encoding="utf8"))):
            if '***** LOG FILE OPENING *****' not in line:
                lines.append(line.rstrip())
            else:
                lines.append(line.rstrip())
                break
    else:
        for line in reversed(list(open(fullPath, encoding="utf8"))):
            if ('***** LOG FILE OPENING *****' in line) and (line.rstrip().split()[0:2] == lastUpdated):
                lines.append(line.rstrip())
                break
            else:
                lines.append(line.rstrip())
    return lines
        
def parseLogfile(newLines):
    
    returnList = []
    for x in range(len(newLines)-1,-1,-1):
        lineID = 0
        instance = ''
        time = datetime
        returnDict = {}
        if 'You have entered' in newLines[x]:
            instance = newLines[x].split('entered ')[1]
            instance = instance.split('.')[0]
            lineID = newLines[x].split()[2]
            time = getDateTime(newLines[x])  
            returnDict['lineID'] = lineID
            returnDict['instance'] = instance
            returnDict['time'] = time
            returnList.append(returnDict)
    return returnList


def parseLogLine(line):
    lineID = 0
    instance = ''
    time = datetime
    returnDict = {}
    if 'You have entered' in line:
        instance = line.split('entered ')[1]
        instance = instance.split('.')[0]
        lineID = line.split()[2]
        time = getDateTime(line)
    returnDict['lineID'] = lineID
    returnDict['instance'] = instance
    returnDict['time'] = time
    return returnDict


def getDateTime(line):
    time = []
    time = line.split()[0:2]
    conctime = time[0] + ',' + time[1]
    return  datetime.strptime(conctime, '%Y/%m/%d,%H:%M:%S')

def clearDF():
    columns = ['lineID', 'instance', 'time']
    df = pd.DataFrame(columns=columns)
    return df

def countOpenings(log):
    s = '***** LOG FILE OPENING *****'
    occurences = []
    for i in range(len(log)):
        if s in logData[i]:
            occurences.append(i)
    return occurences

def saveToTotalstats(df, dataStruct):
    df['timeDelta'] = df['time'].shift(-1) - df['time']
    df['timeDelta'] = df['timeDelta'].apply(lambda x: x.seconds)
    instances = {}
    
    #Instantiate/reset keyvalue pairs for dictionary
    for index, row in df.iterrows():
        if row.instance not in instances:
            instances[row.instance] = {}
            instances[row.instance]['count'] = 0
            instances[row.instance]['avgTime'] = 0
            instances[row.instance]['avgTimeCounter'] = 0
            
     #Loop through and count all the instance events    
    for index, row in df.iterrows():
        if row.instance in instances:
            instances[row.instance]['count'] += 1
            if row.timeDelta > 0:
                instances[row.instance]['avgTime'] += row.timeDelta
                instances[row.instance]['avgTimeCounter'] += 1
    #Calculate the avg time spent in each instance
    for s in instances.keys():
        if instances[s]['avgTime'] > 0:
            instances[s]['avgTime'] = int(instances[s]['avgTime'] / instances[s]['avgTimeCounter'])
        else:
            instances[s]['avgTime'] = 0
        instances[s]['avgTime'] = instances[s]['avgTime']
        instances[s].pop('avgTimeCounter')
            
    #Add to totalStats
    if len(dataStruct['totalStats']) == 0:
        for a in instances.keys():
            dataStruct['totalStats'][a] = {}
            dataStruct['totalStats'][a]['count'] = instances[a]['count']
            dataStruct['totalStats'][a]['avgTime'] = instances[a]['avgTime']
    else:
        for a in instances.keys():
            if a in dataStruct['totalStats'].keys():
                print('add count')
                dataStruct['totalStats'][a]['count'] += instances[a]['count']
                dataStruct['totalStats'][a]['avgTime'] = int((dataStruct['totalStats'][a]['avgTime'] + instances[a]['avgTime'])/2)
                
            else:
                print('insert instance')
                dataStruct['totalStats'][a] = {}
                dataStruct['totalStats'][a]['count'] = instances[a]['count']
                dataStruct['totalStats'][a]['avgTime'] = instances[a]['avgTime']
        
    SaveDataStructure(dataStruct)           

def saveToSession(df, dataStruct):
    df['timeDelta'] = df['time'].shift(-1) - df['time']
    df['timeDelta'] = df['timeDelta'].apply(lambda x: x.seconds)

    #Calculate the session length
    lastOpened = dataStruct['lastOpened'][0] + ',' + dataStruct['lastOpened'][1]
    dateTime_object = datetime.strptime(lastOpened, '%Y/%m/%d,%H:%M:%S')
    sessionLength = datetime.now() - dateTime_object
    instances = {}
    
    #Instantiate/reset keyvalue pairs for dictionary
    for index, row in df.iterrows():
        if row.instance not in instances:
            instances[row.instance] = {}
            instances[row.instance]['count'] = 0
            instances[row.instance]['avgTime'] = 0
            instances[row.instance]['avgTimeCounter'] = 0
            
    #Loop through and count all the instance events    
    for index, row in df.iterrows():
        if row.instance in instances:
            instances[row.instance]['count'] += 1
            if row.timeDelta > 0:
                instances[row.instance]['avgTime'] += row.timeDelta
                instances[row.instance]['avgTimeCounter'] += 1
    #Calculate the avg time spent in each instance
    for s in instances.keys():
        if instances[s]['avgTime'] > 0:
            instances[s]['avgTime'] = int(instances[s]['avgTime'] / instances[s]['avgTimeCounter'])
        else:
            instances[s]['avgTime'] = 0
        instances[s]['avgTime'] = instances[s]['avgTime']
        instances[s].pop('avgTimeCounter')
        
    #Save session statistics
    instances['sessionLength'] = sessionLength
    dataStruct['sessionStats'] = instances
    SaveDataStructure(dataStruct)

def saveSessionToTotal(dataStruct):
    print('ss')



#Main program#
if not CheckIfSaveExists():
    if CreateEmptyDataStructure():
        print('Savefile created')
        dataStruct = OpenDataStructure()
    else:
        print('Something went wrong when creating a empty savefile')
else:
    dataStruct = OpenDataStructure()   

savedStatistics = 'stats.json'

defaultDateTime = []
lastLength = 0
columns = ['lineID', 'instance', 'time']
df = pd.DataFrame(columns=columns)

t = dataStruct['lastOpened']
dataStruct['lastOpened'] = t

while True:
    
    dataStruct = OpenDataStructure()
    logData = iterateLogfile(dataStruct['lastOpened'])
    print(countOpenings(logData))
    #First time the logger is run. If PoE is running, find the latest ** log file opening ** and go from there.
    if dataStruct['lastOpened'] == defaultDateTime:
        print('First time exe is run.')
        if CheckIfRunning():
            print('PoE is running')
            logData = iterateLogfile(dataStruct['lastOpened'])
            dataStruct['lastOpened'] = logData[-1].split()[0:2]
            df = clearDF()
            df = df.append(pd.DataFrame(parseLogfile(logData)))
            
            lastLength = len(logData)
        #If PoE is not running. Save the timestamp of last ** log file opening **.
        else:
            print('PoE is not running')
            logData = iterateLogfile(dataStruct['lastOpened'])
            dataStruct['lastOpened'] = logData[-1].split()[0:2]
            df = clearDF()
            SaveDataStructure(dataStruct)
            lastLength = len(logData)
    #If countOpenings = 1, means PoE is either running or has not been started since last check, should either expect a new log opened or parse new lines.
    #If countOpenings is greater than 1, means PoE has been opened at least once since last check, parse new info and save it to our datastruct.
    elif len(countOpenings(logData)) > 1:
        print('lastOpened has been updated. Parse new data.')
        if CheckIfRunning():
            print('PoE is running')
            occurences = countOpenings(logData)
            dataStruct['lastOpened'] = logData[occurences[0]].split()[0:2]
            df = clearDF()
            df = df.append(pd.DataFrame(parseLogfile(logData[occurences[1]:occurences[-2]])))
            saveToTotalstats(df,dataStruct)
            df = clearDF()
            df = df.append(pd.DataFrame(parseLogfile(logData[0:occurences[1]])))
            saveToSession(df, dataStruct)
            lastLength = len(logData)
        else:
            print('PoE is not running')
            occurences = countOpenings(logData)
            dataStruct['lastOpened'] = logData[occurences[0]].split()[0:2]
            df = clearDF()
            df = df.append(pd.DataFrame(parseLogfile(logData[0:occurences[-2]])))
            saveToTotalstats(df, dataStruct)
            lastLength = len(logData)
    #If logdata length has increased, but no new log file opened has beeen found, meaning poe is runnning and there is new info to parse.
    elif len(logData) > lastLength:
        print('New lines to parse')
        if CheckIfRunning():
            print('PoE is running')
            occurences = countOpenings(logData)
            dataStruct['lastOpened'] = logData[occurences[0]].split()[0:2]
            df = df.append(pd.DataFrame(parseLogfile(logData[0:(len(logData)-lastLength+1)])))
            saveToSession(df, dataStruct)
            lastLength = len(logData)
    else:
        tm.sleep(10)
        print('Sleep')
    print(dataStruct)
            

 
    
    
    
    
    
    
    
#while True:
#    
#    logData = iterateLogfile(dataStruct['lastOpened'])
#    logDataLength = len(logData)
#    #Log file opening should be the last entry in the list, if not run through the entire list to find it.
#    if '***** LOG FILE OPENING *****' in logData[-1]:
#        tempString = logData[-1]
#    else:
#        for lines in logData:
#            if '***** LOG FILE OPENING *****' in lines:
#                tempString = lines
#    #Getting the date of the last time PathOfExile was started and storing it as a datetime object
#    lastOpened = tempString.split()[0:2]
#    lastOpened = lastOpened[0] + ',' + lastOpened[1]
#    dateTime_object = datetime.strptime(lastOpened, '%Y/%m/%d,%H:%M:%S')
#    
#    #If lastOpened == default, means this is the first time the script is run. Save the last opening of path
#    if dataStruct['lastOpened'] == defaultDateTime:
#        dataStruct['lastOpened'] = dateTime_object
#        print('lastOpened set')
#        #Parse log data
#        df = clearDF()
#        df = df.append(pd.DataFrame(parseLogfile(logData)))
#        lastLength = logDataLength
#    #If lastOpened is unequal to the last time the variable was checked, save it and the length of the new logs - Means a new session is started
#    elif (dataStruct['lastOpened'] != dateTime_object):
#        dataStruct['lastOpened'] = dateTime_object
#        print('lastOpened updated')
#        df = clearDF()
#        df = df.append(pd.DataFrame(parseLogfile(logData)))
#        lastLength = logDataLength
#    #If lastOpened is equal to the datetime object, check to see if there are any new lines added to the logfile.
#    else:
#        if lastLength < logDataLength:
#            print('New lines added to logfile')
#            #Append new instance events to dataframe
#            df = df.append(pd.DataFrame(parseLogfile(logData[0:(logDataLength-lastLength+1)])))
#            lastLength = logDataLength
#        else:
#            clearDF()
#    
#    #Get the timeDelta for the instance events
#    df['timeDelta'] = df['time'].shift(-1) - df['time']
#    df['timeDelta'] = df['timeDelta'].apply(lambda x: x.seconds)
#
#    #Calculate the session length
#    sessionLength = datetime.now() - dataStruct['lastOpened']
#    instances = {}
#    
#    #Instantiate/reset keyvalue pairs for dictionary
#    for index, row in df.iterrows():
#        if row.instance not in instances:
#            instances[row.instance] = {}
#            instances[row.instance]['count'] = 0
#            instances[row.instance]['avgTime'] = 0
#            instances[row.instance]['avgTimeCounter'] = 0
#            
#    #Loop through and count all the instance events    
#    for index, row in df.iterrows():
#        if row.instance in instances:
#            instances[row.instance]['count'] += 1
#            if row.timeDelta > 0:
#                instances[row.instance]['avgTime'] += row.timeDelta
#                instances[row.instance]['avgTimeCounter'] += 1
#    #Calculate the avg time spent in each instance
#    for s in instances.keys():
#        if instances[s]['avgTime'] > 0:
#            instances[s]['avgTime'] = int(instances[s]['avgTime'] / instances[s]['avgTimeCounter'])
#        else:
#            instances[s]['avgTime'] = 0
#        instances[s]['avgTime'] = divmod(instances[s]['avgTime'], 60)
#        instances[s].pop('avgTimeCounter')
#        
#    #Save session statistics
#    instances['sessionLength'] = sessionLength
#    dataStruct['sessionStats'] = instances
#    SaveDataStructure(dataStruct)
#    
#    
#
#print(dataStruct['totalStats']["Lioneye's Watch"]) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    