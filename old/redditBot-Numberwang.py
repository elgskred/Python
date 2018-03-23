import praw
import pdb
import re
import os
import random
import time

#Creating the reddit instance
reddit = praw.Reddit('numberwang')

l = []
author = []
numberwangAuthor = ""
numberwang = []
multiple = []
numberwangAmount = 10
lastNumberwang = None

#Getting the subreddit to look in
sub = "funny"
subreddit = reddit.subreddit(sub)


def getNumberwangs(amount, number):
	tempList = []
	if number is None:
		number = random.randrange(-1000, 1000)
	
	#Finding what numbers are "numberwang" based on supplied number or generated number	
	for x in range(0, amount):
		tempList.append(x)
		numType = int(round(random.random()))
		if numType == 0:
			#Float
			variable = round(random.uniform(-5000, 5000), random.randrange(1, 8))
		elif numType == 1:
			variable = random.randrange(-5000, 5000)
		variable = abs(variable)
		if variable == 0:
			variable = variable + random.randrange(1, 13000)
		tempList[x] = variable
	return tempList

def getMultiple(amount):
	tempList = []
	for x in range(0, amount):
		tempList.append(x)
		multiple = abs(random.randrange(-500, 500))
		if multiple == 0:
			multiple = multiple + random.randrange(1, 3000)
		tempList[x] = multiple
	return tempList
	
def checkIfNumberwang(list):
	length = len(list)
	for x in range(0, length):
		if abs(list[x]) in numberwang:
			print("Number: ", list[x])
			lastNumberwang = abs(list[x])
			numberwangAuthor = author[x]
			return list[x]
		elif checkIfMultiple(abs(list[x])) is True:
			lastNumberwang = abs(list[x])
			return list[x]
	return 0

def checkIfMultiple(number):
	for x in range(0, numberwangAmount):
		testVarDiv = number / float(numberwang[x])
		testVarMult = number * float(numberwang[x])
		#print("number : ", number, "numberwang : ", numberwang[x])
		#print("Testvar: ", testVar)
		if testVarDiv in multiple:
			print("Testvar: ", testVarDiv)
			numberwangAuthor = author[x]
			return True
		elif testVarMult in multiple:
			print("Testvar: ", testVarMult)
			numberwangAuthor = author[x]
			return True
		else:
			return False

numberwang = getNumberwangs(numberwangAmount, lastNumberwang)
print("numberwangs: ", numberwang)
multiple = getMultiple(numberwangAmount)
print multiple


#Getting all new comments in the selected subreddit
for comment in subreddit.stream.comments():
	if comment.author != "a_numberwang_bot":
		#print(comment.body)
		#print comment.author
		string = comment.body
		for t in string.split():
			try:
				l.append(int(t))
			except ValueError:
				try:
					l.append(float(t))
				except ValueError:
					pass
			author.append(comment.author)
		if len(l) > 1:
			print l
			if checkIfNumberwang(l) != 0:
				num = checkIfNumberwang(l)
				print "NUMBERWANG"
				reply = numberwangAuthor + ": Number " + str(num) + "!  \n" + "That's NUMBERWANG!"
				print reply
				#comment.reply(reply)
				numberwang = getNumberwangs(numberwangAmount, lastNumberwang)
				multiple = getMultiple(numberwangAmount)
				print ("numberwangs: ", numberwang)
				print multiple
				print "Sleeping for 9mins"
				time.sleep(541)
			l = []
			author = []
#except:
	#print "Something went wrong
	#pass



	



