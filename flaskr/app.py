#github test
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
from flask import Flask, flash, redirect, render_template, request, session, abort

 
popularityWhole = 0
"""similars = [["songs","music","tunes","song"],["movies","films","long form videos","motion picture"],["tv shows", "shows","television shows"], ["games", "video games"],]"""

similars = [ ["songs", "music", "tunes", "melodies"],["movies", "films", "long form videos", "motion pictures", "cinema"],["tv shows", "shows", "television shows", "series"], ["games", "video games", "electronic games", "interactive entertainment"], ["books", "novels", "literature", "publications"], ["food", "cuisine", "meals", "dishes"],["cars", "automobiles", "vehicles", "motorcars"],["clothes", "apparel", "garments", "attire"],["computers", "PCs", "desktops"],["phones", "smartphones", "mobiles", "cell phones"],["sports", "athletics", "games", "physical activities"],["art", "paintings", "sculptures", "visual arts"],["furniture", "home decor", "household items", "fixtures"],["animals", "pets", "creatures", "fauna"],["plants", "flora", "vegetation", "greenery"], ["weather", "climate", "atmospheric conditions", "meteorology"],["travel", "tourism", "journeys", "trips"],["technology", "tech", "gadgets", "devices"],["health", "wellness", "fitness", "medical"],["education", "learning", "schooling", "academics"],["finance", "money", "economics", "banking"],["history", "past events", "chronicles", "records"],["science", "research", "experiments", "studies"],["nature", "environment", "ecosystem", "wildlife"],["music instruments", "instruments", "musical tools", "sound devices"],["beverages", "drinks", "drinking liquids", "refreshments"],["holidays", "vacations", "breaks", "getaways"],["buildings", "structures", "edifices", "constructions"],["jobs", "careers", "occupations", "professions"],["languages", "tongues", "dialects", "linguistics"]]

def full():
	print("full,\n nothing here dude")
	print("in this you can enter alot of your favorite things and then it will calculate a ")
	
	counter = 0 
	using = 0
	end = False
	while end == False:
		z = asks()
		file = z[3]
		catagory = z[0]
		lines = z[1]
		interest = z[2]
		
		dictable = True
		for a in lines:
			if len(a) != 2:
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
		if hashinterest in Dlines:
			print("amount of people with your interest are" + str(Dlines[hashinterest]))
			popularity = moreinfo(hashinterest,Dlines) / len(Twolines)
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


		
		end = isInsert(input("more or stop? type yes for end"))
	print("using = " + str(using) + " counter = " + str(counter))
	print("popularity percent = " + str((using / counter)*100) + "%")
	
	outputfile = open("output.txt", 'w')
	outputfile.write("result of full test " + str(datetime.datetime.now()) + " \n Interest popularity percent =" + str((using / counter)*100) + "%" + " \n total amount of answers given: " + str(counter) + " \n Thanks for testing with us today")
	print("output file written")
		
	
	

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
	print("catagory =" + str(catagory))
	hashcatagory = hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	#print("hash 1 " + str(hashlib.sha384(str.encode(catagory)).hexdigest()) + " \n the second eariler method =" + str(hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()))
	print("catagory chosen is " + str(catagory))
	try:
		file = open(hashcatagory + ".csv","r+")
		lines = list(csv.reader(file,))
		interest = input("interest b").lower()

		"""misspelled  = spell.unknown([interest])
		if len(mispelled) > 0:
			interest = spell.correction(interest)"""
		

	except:
		try:
			file = open(hashcatagory + ".csv","w")
		except:
			print("file permissions lost, probably open somewhere else")
		interest = input("interest a").lower()
		
		"""misspelled  = spell.unknown([interest])
		if len(mispelled) > 0:
			interest = spell.correction(interest)"""

		lines = ["nothing here"]
	return [catagory,lines,interest,file]
	

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
		if len(a) != 2:
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
	if hashinterest in Dlines:
		print("amount of people with your interest are" + str(Dlines[hashinterest]))
		moreinfo(hashinterest,Dlines)
		print("percent that have your interest = " + str(int(Dlines[hashinterest])/total))

		if yinsert:
			
			if hashinterest in Dlines:
				Dlines[hashinterest] = int(Dlines[hashinterest])
				#this is where encyrption of the number could take place 
				Dlines[hashinterest] += 1
				print(Dlines[hashinterest])
				print("D lines = " + str(Dlines))
				file.close()
				#file.truncate()
				hashcatagory = hashlib.sha384(catagory.encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
				newDlines = Dlines.items()
				newDlines = [list(a) for a in newDlines]

				if newDlines != []:
					os.remove(hashcatagory+".csv")
					#csv.writer(file).writerows(Dlines)
					file = open(hashcatagory + ".csv","w")	
					print("new Dlines = " + str(newDlines))
					for a in Dlines:
						if a != []:
							print("line to be printed" + str(a))
							csv.writer(file).writerow([a,Dlines[a]])
					print("should have rewriten")
					file.close()
				
			else:
				print("wasn't there so didn't update")
		
		
	else:
		print("interest not found")
		#Dlines[hashinterest] = 1
		#file.close()
		csv.writer(file).writerow([hashinterest,1])
	
def addinfo(newDlines):
	print("a")
		
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
	


yeses = list(map(lambda x: x.lower(), ["Yes", "Sure", "Absolutely", "Definitely", "Of course", "Certainly", "Indeed", "Affirmative", "For sure", "Without a doubt", "No doubt", "Sure thing", "You bet", "By all means", "Naturally", "Positively", "Undoubtedly", "Yep", "Yeah", "Yup", "Uh-huh", "Right", "Agreed", "Okay", "Alright", "Fine", "Sounds good", "I agree", "I do", "I will", "I can", "I am", "I have", "I did", "I shall", "I accept", "I consent", "I approve", "I confirm", "I acknowledge", "I concur", "I endorse", "I support", "I back", "I second", "I validate", "I verify", "I affirm", "I assent","Yes", "Yeah", "Yep", "Yup", "Sure", "Absolutely", "Definitely", "Of course", "Certainly", "Affirmative", "Indeed", "Naturally", "Sure thing", "You bet", "For sure", "Without a doubt", "Totally", "Alright", "Okay", "Ok", "Fine", "Agreed", "Roger", "Aye", "Uh-huh", "Yessir", "Yup yup", "Right on", "Surely", "By all means", "Indubitably", "Positively", "Unquestionably", "Undoubtedly", "I do", "I will", "I can", "I agree", "I accept", "I consent", "I approve", "I concur", "I understand", "I acknowledge", "I recognize", "I confirm", "I support", "I endorse", "I assent","y","Absolutely", "Affirmative", "All right", "Alrighty", "Amen", "Assuredly", "Aye aye", "Beyond a doubt", "By all means", "Can do", "Certainly", "Clearly", "Completely", "Correct", "Count on it", "Definitely", "Doubtless", "Easily", "Exactly", "Fine by me", "Gladly", "Good", "Got it", "Granted", "Happily", "I am", "I approve", "I believe so", "I can", "I do", "I got you", "I have", "I know", "I shall", "I suppose", "I think so", "I understand", "I will", "I would", "I'm in", "I'm on it", "I'm with you", "Indeed", "Indubitably", "Naturally", "No problem", "No question", "Of course", "Okay", "Okie dokie", "Positively", "Precisely", "Right", "Right away", "Righto", "Roger that", "Sure", "Sure thing", "Surely", "Totally", "True", "Uh-huh", "Undoubtedly", "Unquestionably", "Very well", "Willingly", "Without fail", "Without question", "Y", "Yas", "Yass", "Yasss", "Yea", "Yeah", "Yep", "Yes indeed", "Yes please", "Yes sir", "Yes ma'am", "Yes, I do", "Yes, I will", "Yes, of course", "Yes, please", "Yes, sure", "Yes, totally", "Yes, yes", "Yessir", "Yesss", "Yup", "Yup yup", "You bet", "You got it", "You know it", "You said it", "You’re right", "You’re on", "You’re correct", "You’re absolutely right", "You’re spot on", "You’re right on","Sí", "Oui", "Ja", "Sì", "Sim", "はい", "네", "是的", "Да", "نعم", "ใช่", "हाँ", "Evet", "Bəli", "Ano", "Jah", "Kyllä", "Ναι", "Igen", "Já", "Bai", "Haa", "Ndiyo", "Ewe", "Ee", "Da", "Iva", "Tak", "Vâng", "Áno", "Ja", "Ano", "Ja", "Jah", "Kyllä", "Oui", "Ja", "Ναι", "Igen", "Já", "Sì", "Ja", "Tak", "Sim", "Da", "Sí", "Ja", "Evet", "Так", "Vâng", "Bəli", "Bai", "Ano", "Ja", "Jah", "Kyllä", "Oui", "Ja", "Ναι", "Igen", "Já", "Sì", "Ja", "Tak", "Sim", "Da", "Sí", "Ja", "Evet", "Так", "Vâng"
]))
#print(yeses)

def isInsert(inner):
	inner = inner.lower() 
	return inner in yeses


alphabet = "abcdefghijklmnopqrstuvwxyz"
app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		text = [['' for _ in range(2)] for _ in range(2)]
		for a in range(len(text)):
			for b in range(len(text[a])):
				print('textarea' + str(alphabet[a]) + str(b + 1))
				print(request.form.get('textarea' + str(alphabet[a]) + str(b + 1)))
				text[a][b] = request.form.get('textarea' + str(alphabet[a]) + str(b + 1))
		print(text)
	return render_template('entry.html',name="testername")	
	#return "Hello World!"


	
def main():
	#app.run(host = '10.0.0.172', port=80,debug = True)
	


	print("welcome to the basic tester, there are two modes, individual interests and full percentage ")
	mode = input("enter full to do full form, otherwise right no or anything else IDC").lower()
	if mode == "full":
		full()
	else:
		individual()


@app.route('/', methods=['POST'])
def formpostre():
	text = request.form['text']
	print(text)
	return render_template('entry.html',name="testername")


#some day a seperate thread for this status would be nice. this is here made for a a seperate results page, idk if I will combine or not yet. 
@app.route('/result', methods=['GET'])
def getStatus():
	statusList = {'status':status}
	return json.dumps(statusList)



if __name__ == "__main__":
    main()