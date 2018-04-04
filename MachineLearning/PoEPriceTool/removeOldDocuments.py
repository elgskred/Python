from datetime import datetime, timedelta
from pymongo import MongoClient

def removeOld():
    client = MongoClient("mongodb://poeUser:12345678@192.168.10.50/poe")
    #client = MongoClient("mongodb://poeUser:12345678@localhost/poe")
    db = client['poe']
    
    #Remove documents that are 3 days or older
    t = datetime.now() - timedelta(days=3)
    day = t.day
    month = t.month
    year = t.year
    query = db.items.delete_many({
            'timeStamp': {"$lte": datetime(year,month,day)} 
            })


