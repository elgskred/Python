import requests
import time
import json
import mysql.connector
from datetime import date, datetime, timedelta
from mysql.connector import errorcode

#Login info for mysql server - local network
config = {
	'user': 'pythonWOW',
	'password': 'pw',
	'host': '192.168.10.50',
	'port': '3306',
	'database': 'wowauctions',
	'raise_on_warnings': True
}



#While true loop
while True:

	#Request api key
	response = requests.get("https://eu.api.battle.net/wow/auction/data/frostmane?locale=en_GB&apikey=vmgmryqdpgtwggu5r3v7y9xu7dvmzszk")
	#Json the response
	if response.status_code == 200:
		data = response.json()
		#Auction data url
		url = data["files"][0]["url"]
		#When auction data was last updated
		lastModified = data["files"][0]["lastModified"]
		timeStamp = datetime.fromtimestamp(lastModified / 1e3)

		fRead = open('/home/christoffer/Documents/wowLastModified/lastModified','r')
		ff = int(fRead.read())
		fRead.close()

		if lastModified != ff:
			#IF START
			print("Not equal - Update db")
			#Writes the timestamp to a file
			fWrite = open('/home/christoffer/Documents/wowLastModified/lastModified','w')
			fWrite.write(str(lastModified))
			fWrite.close()

			#Gets the auction data json file
			r = requests.get(url)
			#Json the data
			aucData = r.json()
			#The dictionary containing all the auctions
			auctions = aucData["auctions"]
			#Amount of auctions
			auctionsLen = len(auctions)

			print("Connecting")
			cnx = mysql.connector.connect(**config)
			cursor = cnx.cursor()
			print("Connected")

			#Data insertion order
			add_auction = ("INSERT INTO auctions "
					"(aucId, itemID, name, bid, buyout, quantity, timeLeft, date)"
					"VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")


			print("Starting update")
			for x in range(0, auctionsLen):
			#for loop start
				#Data to be inserted
				data_auction = (auctions[x]["auc"], auctions[x]["item"],
				auctions[x]["owner"], auctions[x]["bid"], auctions[x]["buyout"], 
				auctions[x]["quantity"], auctions[x]["timeLeft"], timeStamp)
				#Execute query
				cursor.execute(add_auction, data_auction)
			#for loop end
			print("Update complete")


			#Make sure the data is inserted properly
			cnx.commit()
			#Close connection
			cursor.close()
			cnx.close()
			time.sleep(300)


		else:
			print("Equal")
			time.sleep(300)
			print("Woke up")
		#IF END
#While true end














##DEBUG PRINTS##
#print("Content: ")
#print(response.content)
#print("Data type: ")
#print(type(data))h
#print("Data: ")
#print(data)
#print(url)
#print(timeStamp)
#print(auctionsLen)

#print(auctions[0]["auc"])
#print(auctions[0]["item"])
#print(auctions[0]["owner"])
#print(auctions[0]["bid"])
#print(auctions[0]["buyout"])
#print(auctions[0]["quantity"])
#print(auctions[0]["timeLeft"])
#print(timeStamp)
