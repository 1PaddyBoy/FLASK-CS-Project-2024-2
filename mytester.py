import csv
import os 
#import pandas as pd
import hashlib
#from playsound import playsound
from itertools import count as crashB
from spellchecker import SpellChecker
#from cryptography.fernet import Fernet
import datetime
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, current_app
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
import base64
import socket
import sys

popularityWhole = 30
combination = []
def printer():
        print("helpers worked")

similars = [ ["songs", "music", "tunes", "melodies"],["movies", "films", "long form videos", "motion pictures", "cinema"],["tv shows", "shows", "television shows", "series"], ["games", "video games", "electronic games", "interactive entertainment"], ["books", "novels", "literature", "publications"], ["food", "cuisine", "meals", "dishes"],["cars", "automobiles", "vehicles", "motorcars"],["clothes", "apparel", "garments", "attire"],["computers", "PCs", "desktops"],["phones", "smartphones", "mobiles", "cell phones"],["sports", "athletics", "games", "physical activities"],["art", "paintings", "sculptures", "visual arts"],["furniture", "home decor", "household items", "fixtures"],["animals", "pets", "creatures", "fauna"],["plants", "flora", "vegetation", "greenery"], ["weather", "climate", "atmospheric conditions", "meteorology"],["travel", "tourism", "journeys", "trips"],["technology", "tech", "gadgets", "devices"],["health", "wellness", "fitness", "medical"],["education", "learning", "schooling", "academics"],["finance", "money", "economics", "banking"],["history", "past events", "chronicles", "records"],["science", "research", "experiments", "studies"],["nature", "environment", "ecosystem", "wildlife"],["music instruments", "instruments", "musical tools", "sound devices"],["beverages", "drinks", "drinking liquids", "refreshments"],["holidays", "vacations", "breaks", "getaways"],["buildings", "structures", "edifices", "constructions"],["jobs", "careers", "occupations", "professions"],["languages", "tongues", "dialects", "linguistics"]]
alphabet = "abcdefghijklmnopqrstuvwxyz"
# input of multiple catagories and interests 
def full():
	print("full,\n nothing here dude")
	print("in this you can enter alot of your favorite things and then it will calculate a ")
	
	output = looptake()
	using = output[0]
	counter = output[1]

	
	outputfile = open("output.txt", 'w')
	outputfile.write("result of full test " + str(datetime.datetime.now()) + " \n Interest popularity percent =" + str((using / counter)*100) + "%" + " \n total amount of answers given: " + str(counter) + " \n Thanks for testing with us today")
	print("output file written")

#this loops the asks function and handles reviewing and inputing all the information for the command line full survey 		
def looptake():
	counter = 0 
	using = 0
	end = False
	while end == False:
		z = asks()
		file = z[3]
		catagory = z[0]
		lines = z[1]
		interest = z[2]
		
		output = processes(lines,interest,file,)
		using += output[0]
		counter += output[1]	


		
		end = isInsert(input("more or stop? type yes for end"))
	print("using = " + str(using) + " counter = " + str(counter))
	print("popularity percent = " + str((using / counter)*100) + "%")
	return [using, counter]

#processes the information inputed to return using and counter for popularity annalsys
def processes(lines,interest,file): 
		people = 0
		using = 0
		counter = 0
		popularityfor = (1,1)
		dictable = True
		for a in lines:
			if len(a) < 2:
				lines.pop(lines.index(a))

		Twolines = []
		for a in lines:
			if len(a) >= 2:
				Twolines.append(a[0:2])#new isolation piece
		print("two lines = " + str(Twolines))
		Dlines = dict(Twolines)

		total = 0
		for a in Dlines.values():
			try: 
				total += int(a)
			except: 
				total += 0
		print(total)
		hashinterest = hashlib.sha384(interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
		if hashinterest in Dlines.keys():
			print("amount of people with your interest are" + str(Dlines[hashinterest]))
			people = Dlines[hashinterest]
			popularity = moreinfo(hashinterest,Dlines) / len(Twolines)
			popularityfor = ( - (moreinfo(hashinterest,Dlines) - len(Dlines)), len(Dlines))  # popular out of number 
			print("popularity = " + str(popularity))
			using += popularity
			counter += 1
		else:
			
			print("interest not found")
			#Dlines[hashinterest] = 1
			#file.close()
			csv.writer(file).writerow([hashinterest,1])
			using += 0
			counter += 1
			people = 0
			popularityfor = ( - (moreinfo(hashinterest,Dlines) - len(Dlines)), len(Dlines))
		return [using,counter,people,popularityfor] # this returns alot of information, so going in order, using is the amount a popularity counter which along with counter, which records the amount of resources can give the average popularity (using/counter). people returns a list in the order of the interests of how many people have that interest. popularit for returns a similar list that contains tuples organized like this, (order in list of popularities, amount of interests in catagory), this tuple together shows you how popular that interest is. 

#this loops on an existing list of catagories and interests gathering information 
def loopinterest(combination):
	interests = []
	catagories = []
	for a in combination: #delinates double list from website 
		catagories.append(a[0])
		interests.append(a[1])

	people = []
	peoplefor = []
	extraInformation = []
	counter = 0 
	using = 0
	for a in range(len(catagories)):
		catagory = catagories[a]
		interest = interests[a]
		for a in similars:
			if catagory in a:
				catagory = a[0]
				break
		z = asksfileProcessing(catagory,interest)

		
		file = z[3]
		catagory = z[0]
		lines = z[1]
		interest = z[2]

		hashinterest = hashlib.sha384(interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
		for a in lines:
			if len(a) < 2:
				lines.pop(lines.index(a))
		Twolines = []
		for a in lines:
			print(a)
			if len(a) >= 2:
				Twolines.append(a[0:2])#new isolation piece
		print("two lines = " + str(Twolines))
		Dlines = dict(Twolines) #Dlines and Twolines like this only takes the info about the numbers and other stuff into a dictionary 

		try:
		#if True:
			innie = list(Dlines.keys()).index(hashinterest)
			if len(lines[innie]) > 2:
				extra = lines[innie][2:]
				
				print("\n encyrpted extra =" + str(extra))
				print("unencyrpted extra =" + str(decrypt(extra,interest)))
				extraInformation.append(str(decrypt(extra,interest)))
			else:
				print("no extra information stored")
				print(lines[innie])
			

			output = processes(lines,interest,file)
			using += output[0]
			counter += output[1]
			people.append(output[2]) # these last two are just directly passed,
			print("people to be appened =" + str(output[2])) 
			peoplefor.append(output[3])
			print("people for =" + str(peoplefor))
		except:
			using += 1
			counter += 1 
			print(hashinterest in Dlines.keys())
			print("new interest")
			people.append(0)
			peoplefor.append(("least",len(Twolines)))
		
	return [using,counter,extraInformation, people, peoplefor]



	
#crashes program
def crash():
    playsound("Microsoft Windows XP Error - Sound Effect (HD) [ ezmp3.cc ].mp3")
    list(crashB(0))
    x = {}
    for i in range(1000000):
    	x = {1: x}
    repr(x)
    try:
        crash()
    except:
        crash()


#asks individually for each interest and catagory, can be seperately spread out 
def asks():
	catagory = input("enter catagory").lower()
	spell = SpellChecker()
	mispelled  = spell.unknown(catagory.split(" "))
	#print(mispelled)
	if len(mispelled) > 0:
		catagory = spell.correction(catagory)
		
	for a in similars:
		if catagory in a:
			catagory = a[0]
			break
	interest = input("interest b").lower()
	return asksfileProcessing(catagory, interest)


#this does all the file processing and ecetera 
def asksfileProcessing(catagory, interesta):
	print("catagory =" + str(catagory))
	hashcatagory = hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	#print("hash 1 " + str(hashlib.sha384(str.encode(catagory)).hexdigest()) + " \n the second eariler method =" + str(hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()))
	print("catagory chosen is " + str(catagory))
	try:
		file = open("static\\data\\" + hashcatagory + ".csv","r+")
		lines = list(csv.reader(file,))
		interest = interesta

		"""misspelled  = spell.unknown([interest])
		if len(mispelled) > 0:
			interest = spell.correction(interest)"""
		

	except:
		try:
			file = open("static\\data\\" + hashcatagory + ".csv","w")
			
		except:
			print("file permissions lost, probably open somewhere else")
		interest = interesta
		
		"""misspelled  = spell.unknown([interest])
		if len(mispelled) > 0:
			interest = spell.correction(interest)"""

		lines = ["nothing here"]
	return [catagory,lines,interest,file]


#gives individual data for each catagory and interest
def individual():
	print("individual")

	z = asks()
	file = z[3]
	catagory = z[0]
	lines = z[1]
	interest = z[2]
	
	hashinterest = hashlib.sha384(interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	print("lines = " + str(lines))
	if catagory == "crash":
		for i in range(3):
			playsound("Microsoft Windows XP Error - Sound Effect (HD) [ ezmp3.cc ].mp3")
		for i in range(100):
			print("error, crash immenant")
			crash()
	yinsert = isInsert(input("would you like your response to be recorded?"))
	print("response recorded on =" + str(yinsert))
	#print(lines[0][0])
	print(lines)
	dictable = True
	for a in lines:
		if len(a) < 2:
			lines.pop(lines.index(a))	

	Twolines = []
	for a in lines:
		print(a)
		if len(a) >= 2:
			Twolines.append(a[0:2])#new isolation piece
	print("two lines = " + str(Twolines))
	Dlines = dict(Twolines) #Dlines and Twolines like this only takes the info about the numbers and other stuff into a dictionary 

	total = 0
	for a in Dlines.values():
		try: 
			total += int(a)
		except: 
			total += 0
	print(total)
	print(Dlines.keys())
	if hashinterest in Dlines.keys():
		print("amount of people with your interest are" + str(Dlines[hashinterest]))
		moreinfo(hashinterest,Dlines)
		print("percent that have your interest = " + str(int(Dlines[hashinterest])/total))
		print("other recorded information:")
		innie = list(Dlines.keys()).index(hashinterest)
		if len(lines[innie]) > 2:
			extra = lines[innie][2:]
			print("encyrpted extra =" + str(extra))
			print("unencyrpted extra =" + str(decrypt(extra,interest)))
		else:
			print("no extra information stored")

		if yinsert:# this goes into if they want to add to it. you need to record your answer if you are going to add information
			
			if hashinterest in Dlines:
				Dlines[hashinterest] = int(Dlines[hashinterest])
				#this is where encyrption of the number could take place 
				Dlines[hashinterest] += 1
				print(Dlines[hashinterest])
				print("D lines = " + str(Dlines))
				file.close()
				#file.truncate()
				hashcatagory = hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
				#newDlines = Dlines.items()
				#newDlines = [list(a) for a in newDlines]
				#scratch:
				newDlines = lines
				newDlines[innie][1] = int(newDlines[innie][1]) + 1
				
				newDlines = addinfo(newDlines,innie,interest) # this adds the information into the section

				if newDlines != []:
					os.remove("static\\data\\" + hashcatagory+".csv")
					#csv.writer(file).writerows(Dlines)
					file = open("static\\data\\" + hashcatagory + ".csv","w")	
					print("new Dlines = " + str(newDlines))
					for a in newDlines:
						if a != []:
							print("line to be printed" + str(a))
							csv.writer(file).writerow(a)
					print("should have rewriten")
					file.close()
				
			else:
				print("wasn't there so didn't update")
		
		
	else:
		print("interest not found")
		#Dlines[hashinterest] = 1
		#file.close()
		csv.writer(file).writerow([hashinterest,1])
	

#decrypts symmetric infos stored seperately 
def decrypt(infos, interest):
	
	"""if len(interest) > 64:
		interest = interest[0:64]
	else:
		interest = interest + "".join(["x" for _ in range(64 - interest)])"""
	#hashinterest = hashlib.sha256(interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()

	code_bytes = interest.encode("utf-8")
	key = base64.urlsafe_b64encode(code_bytes.ljust(32)[:32]) # properly encodes and lengthens or shortenes the input string to be used as a key 
	print(len(key))
	print(key)

	"""encoded = hashinterest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')
	key = encoded[0:2*(len(encoded)//3)]
	iv = encoded[len(encoded)//3:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	
	print("infos lens =" + str(len(infos)) + " and they are =" + str(infos))"""
	decrypted = []
	f = Fernet(key) #encodes with fernet library, its great just takes 1 key 
	#ct = f.encrypt(message)
	print(f.decrypt(f.encrypt(b"a")))
	for a in infos:
		#decryptor = cipher.decryptor()
		print(a)
		print(f.decrypt(str(a)[2:len(a)-1].encode(encoding = "UTF-8", errors='xmlcharrefreplace')))
		decrypted.append(f.decrypt(str(a)[2:len(a)-1].encode(encoding = "UTF-8", errors='xmlcharrefreplace'))) # appends encyrpted and encoded piece. 
		print(a[2:len(a)-1])
		#print("try basic =" + str(f.decrypt(a.encode(encoding = "UTF-8", errors='xmlcharrefreplace'))) + " try with removed = " + str(f.decrypt(a[2:len(a)-1].encode(encoding = "UTF-8", errors='xmlcharrefreplace'))))
	print("looped through all")
	print("decryption done, data = " + str(decrypted))
	return decrypted	

def addandinfoloop(combinations,checks,infos):
	interests = []
	catagories = []
	for a in combinations: #delinates double list from website 
		catagories.append(a[0])
		interests.append(a[1])
	for a in range(len(catagories)):
		print("looping for " + str(combinations[a]))
		print(checks[a]) #adds data and all 
		if checks[a]:# this goes into if they want to add to it. you need to record your answer if you are going to add information	
			catagory = catagories[a]
			interest = interests[a]
			for x in similars:
				if catagory in x:
					catagory = x[0]
					break
			z = asksfileProcessing(catagory,interest)

			
			file = z[3]
			catagory = z[0]
			lines = z[1]
			interest = z[2]

			hashinterest = hashlib.sha384(interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()

			#dictable = True
			for x in lines:
				if len(x) < 2:
					lines.pop(lines.index(x))

			Twolines = []
			for b in lines:
				print(b)
				if len(b) >= 2:
					Twolines.append(b[0:2])#new isolation piece
			print("two lines = " + str(Twolines))
			Dlines = dict(Twolines) #Dlines and Twolines like this only takes the info about the numbers and other stuff into a dictionary 

			
			hashcatagory = hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
		
			if hashinterest in Dlines.keys():
				innie = list(Dlines.keys()).index(hashinterest)
				Dlines[hashinterest] = int(Dlines[hashinterest])
				#this is where encyrption of the number could take place 
				Dlines[hashinterest] += 1
				print(Dlines[hashinterest])
				print("D lines = " + str(Dlines))
				file.close()
				#file.truncate()
				
				#newDlines = Dlines.items()
				#newDlines = [list(a) for a in newDlines]
				#scratch:
				newDlines = lines
				try:
					newDlines[innie][1] = int(newDlines[innie][1]) + 1
				except:
					newDlines[innie][1] = 1
				if infos[a] != None and infos[a] != "":
					newDlines = addinfofixed(newDlines,innie,interest,infos[a]) # this adds the information into the section

				
				
			else:
				file.close()
				newDlines = lines
				print("wasn't there so didn't update")
				newDlines.append([hashinterest,1])
				print("mystery list is " + str(a))
				if infos[a] != None and infos[a] != "":
					newDlines = addinfofixed(newDlines,len(newDlines)-1,interest,infos[a])
				
			if newDlines != []:
					os.remove("static\\data\\" + hashcatagory+".csv")
					#csv.writer(file).writerows(Dlines)
					file = open("static\\data\\" + hashcatagory + ".csv","w")	
					print("new Dlines = " + str(newDlines))
					for a in newDlines:
						if a != []:
							print("line to be printed" + str(a))
							csv.writer(file).writerow(a)
					print("should have rewriten")
					file.close()
		

	

#asks about adding information to the sheet
def addinfo(newDlines,innie, interest):

	insert = isInsert(input("would you like to add any information for others to see?"))
	if insert:
		return addencryptinfos(newDlines,innie,interest)	
	else:
		print("information not added")
		return newDlines
	#print("finished")

def addinfofixed(newDlines,innie, interest,info):

		insert = info
	
		message = insert

		#method for taking good numbers
		"""if len(interest) > 48:
			interest = interest[0:48]
		else:
			interest = interest + "".join(["x" for _ in range(48 - len(interest))])"""
		

		code_bytes = interest.encode("utf-8")
		key = base64.urlsafe_b64encode(code_bytes.ljust(32)[:32])
		print(len(key))
		print(key)

		"""encoded = hashinterest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')

		encoded = interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')
		key = encoded[0:2 * (len(encoded)//3)]
		iv = encoded[len(encoded)//3:]

		cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
		encryptor = cipher.encryptor()
		ct = encryptor.update(message.encode(encoding = "UTF-8", errors='xmlcharrefreplace')) + encryptor.finalize()"""
		f = Fernet(key)
		ct = f.encrypt(message.encode(encoding = "UTF-8", errors='xmlcharrefreplace'))

		#newDlines[innie].append(message) # unencrypted right now
		newDlines[innie].append(str(ct)) # encrypted right now
		print(newDlines[innie])
		print("information added")
		return newDlines	


		print("information not added")
		return newDlines
	#print("finished")

#actually adds the info passed instead of just playing and testing for it like addinfo
def addencryptinfos(newDlines,innie,interest):
		message = input("enter message to be encrypted")

		#method for taking good numbers
		"""if len(interest) > 48:
			interest = interest[0:48]
		else:
			interest = interest + "".join(["x" for _ in range(48 - len(interest))])"""
		

		code_bytes = interest.encode("utf-8")
		key = base64.urlsafe_b64encode(code_bytes.ljust(32)[:32])
		print(len(key))
		print(key)

		"""encoded = hashinterest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')

		encoded = interest.encode(encoding = "UTF-8", errors='xmlcharrefreplace')
		key = encoded[0:2 * (len(encoded)//3)]
		iv = encoded[len(encoded)//3:]

		cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
		encryptor = cipher.encryptor()
		ct = encryptor.update(message.encode(encoding = "UTF-8", errors='xmlcharrefreplace')) + encryptor.finalize()"""
		f = Fernet(key)
		ct = f.encrypt(message.encode(encoding = "UTF-8", errors='xmlcharrefreplace'))

		#newDlines[innie].append(message) # unencrypted right now
		newDlines[innie].append(str(ct)) # encrypted right now
		print(newDlines[innie])
		print("information added")
		return newDlines


#this gives more info, statistics etc from a specific interest, here it returns how popular as a number of all interests of that catagory it is 
def moreinfo(hashinterest, Dlines):
	print("moreinfo, Dlines is " + str(Dlines))	
	total = 0
	for a in Dlines.values():
		try: 
			total += int(a)
		except: 
			total += 0
	print(sorted(list(list(Dlines.values())), reverse = True) )
	popularity = sorted(list(list(Dlines.values())), reverse = True).index(Dlines[hashinterest])
	print(str(popularity + 1) + " most popular response out of :" + str(len(Dlines)))
	popularityPer = (len(Dlines) - (popularity))
	print("popularity per " + str( popularityPer))
	return popularityPer
	

#any answer that means yes:
yeses = list(map(lambda x: x.lower(), ["Yes", "Sure", "Absolutely", "Definitely", "Of course", "Certainly", "Indeed", "Affirmative", "For sure", "Without a doubt", "No doubt", "Sure thing", "You bet", "By all means", "Naturally", "Positively", "Undoubtedly", "Yep", "Yeah", "Yup", "Uh-huh", "Right", "Agreed", "Okay", "Alright", "Fine", "Sounds good", "I agree", "I do", "I will", "I can", "I am", "I have", "I did", "I shall", "I accept", "I consent", "I approve", "I confirm", "I acknowledge", "I concur", "I endorse", "I support", "I back", "I second", "I validate", "I verify", "I affirm", "I assent","Yes", "Yeah", "Yep", "Yup", "Sure", "Absolutely", "Definitely", "Of course", "Certainly", "Affirmative", "Indeed", "Naturally", "Sure thing", "You bet", "For sure", "Without a doubt", "Totally", "Alright", "Okay", "Ok", "Fine", "Agreed", "Roger", "Aye", "Uh-huh", "Yessir", "Yup yup", "Right on", "Surely", "By all means", "Indubitably", "Positively", "Unquestionably", "Undoubtedly", "I do", "I will", "I can", "I agree", "I accept", "I consent", "I approve", "I concur", "I understand", "I acknowledge", "I recognize", "I confirm", "I support", "I endorse", "I assent","y","Absolutely", "Affirmative", "All right", "Alrighty", "Amen", "Assuredly", "Aye aye", "Beyond a doubt", "By all means", "Can do", "Certainly", "Clearly", "Completely", "Correct", "Count on it", "Definitely", "Doubtless", "Easily", "Exactly", "Fine by me", "Gladly", "Good", "Got it", "Granted", "Happily", "I am", "I approve", "I believe so", "I can", "I do", "I got you", "I have", "I know", "I shall", "I suppose", "I think so", "I understand", "I will", "I would", "I'm in", "I'm on it", "I'm with you", "Indeed", "Indubitably", "Naturally", "No problem", "No question", "Of course", "Okay", "Okie dokie", "Positively", "Precisely", "Right", "Right away", "Righto", "Roger that", "Sure", "Sure thing", "Surely", "Totally", "True", "Uh-huh", "Undoubtedly", "Unquestionably", "Very well", "Willingly", "Without fail", "Without question", "Y", "Yas", "Yass", "Yasss", "Yea", "Yeah", "Yep", "Yes indeed", "Yes please", "Yes sir", "Yes ma'am", "Yes, I do", "Yes, I will", "Yes, of course", "Yes, please", "Yes, sure", "Yes, totally", "Yes, yes", "Yessir", "Yesss", "Yup", "Yup yup", "You bet", "You got it", "You know it", "You said it", "You’re right", "You’re on", "You’re correct", "You’re absolutely right", "You’re spot on", "You’re right on","Sí", "Oui", "Ja", "Sì", "Sim", "はい", "네", "是的", "Да", "نعم", "ใช่", "हाँ", "Evet", "Bəli", "Ano", "Jah", "Kyllä", "Ναι", "Igen", "Já", "Bai", "Haa", "Ndiyo", "Ewe", "Ee", "Da", "Iva", "Tak", "Vâng", "Áno", "Ja", "Ano", "Ja", "Jah", "Kyllä", "Oui", "Ja", "Ναι", "Igen", "Já", "Sì", "Ja", "Tak", "Sim", "Da", "Sí", "Ja", "Evet", "Так", "Vâng", "Bəli", "Bai", "Ano", "Ja", "Jah", "Kyllä", "Oui", "Ja", "Ναι", "Igen", "Já", "Sì", "Ja", "Tak", "Sim", "Da", "Sí", "Ja", "Evet", "Так", "Vâng"
]))
#print(yeses)

#if an answer is correct or yes or sometthing 
def isInsert(inner):
	inner = inner.lower() 
	return inner in yeses
 
#does not work right now but attempts to download a file, just a test but can be utilized to download the extra information each person adds. 
def download():
	name = socket.gethostname() + " " + socket.gethostbyname(socket.gethostname())
	print(" download started for " + name)
	hashedname = hashlib.sha384(name.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	
	file = open("static\\UPLOAD_FOLDER\\" + str(hashedname) + ".txt", "w")
	file.write(" file to be downloaded" + str(hashedname))
	file.close()
	print(current_app.root_path)
	#uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
	#return send_from_directory(uploads, hashedname)
	return send_from_directory(app.static_folder, hashedname, as_attachment=True)

#doesn't check just removes all removers from before
def remove(before,removers):
	#adjust = 0
	for a in removers:
		before.pop(before.index(a))
		#adjust += 1
	return before