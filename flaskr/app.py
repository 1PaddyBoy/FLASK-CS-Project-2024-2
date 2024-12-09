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
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, current_app
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
import base64
import socket
import sys
for path in sys.path:
		print(path)


import mytester as extrahelpers


"""similars = [["songs","music","tunes","song"],["movies","films","long form videos","motion picture"],["tv shows", "shows","television shows"], ["games", "video games"],]"""


#this is similar catagories for grouping 


extra=[]
#main routing for main page, controls the textboxes and submit button as well. 
app = Flask(__name__, static_folder='static')
@app.route("/", methods=['GET','POST'])
def hello():
	extrahelpers.printer()
	if request.method == 'POST':
		#download()
		if 'submit' in request.form:
			pos = [2,5] # change these variables to change how many boxes it checks 
			text = [['' for _ in range(pos[0])] for _ in range(pos[1])] 
			for a in range(len(text)):
				for b in range(len(text[a])):
					print('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1))
					print(request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1)))
					text[a][b] = request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1))
			print(text)
			removers = []
			for a in text:
				if len(a) < 2 or (a[0] == '') or (a[1] == ''):
					print("popping, index = " + str(text.index(a)) + " value was "+ str(a) + " reason " + str([len(a) < 2,(a[0] == ''),a[1] == ''])) 
					removers.append(a)
			text = extrahelpers.remove(text,removers)
			
			print("new combinations to be added =" + str(text))
			extrahelpers.combination.extend(text)
			extra.append("test " + str(text) + "endtest                                          test test test test test test test test test test test test test test test")
			print(extrahelpers.combination)
		elif 'results' in request.form:
			#this does the results button
			print("results")
			return redirect("/results")

		else:
			print("bad input in html submit post \\, will pretend like nothing happened")
	return render_template('entry.html',name="testername")	
	#return "Hello World!"




@app.route("/results",methods=['GET','POST'])
def results():
	if request.method == 'POST':
		checkboxes = []
		textboxes = []
		print(request.form)
		for a in range(len(extrahelpers.combination)):
			b = request.form.get("interest" + str(a))
			print("checkbox " + "insert" + str(a) + " =" + str(b))
			checkboxes.append(b == "check")
			text = request.form.get("interest" + str(a)+"t")
			textboxes.append(text)
			print("textbox = " + str(text))
		print("checkboxes =" + str(checkboxes))
		print("textboxes =" + str(textboxes))
		extrahelpers.addandinfoloop(extrahelpers.combination,checkboxes,textboxes)
		
		

	#RESULTS!!!!
	interestsa = []
	catagoriesa = []
	for a in extrahelpers.combination: #delinates double list from website 
		catagoriesa.append(a[0])
		interestsa.append(a[1])
	z = extrahelpers.loopinterest(extrahelpers.combination)
	extra = z[2]
	counter = z[1]
	other = z[0]
	people = z[3]
	peoplefor = z[4]
	print("people:")
	print(people)
	print(peoplefor)
	for a in peoplefor:
		print(len(a))
		if len(a) < 2:
			print("triggered replacement")
			a = (1,1)

	if len(peoplefor) == 0:
		peoplefor.append((1,1))
	print("popularity per:")
	print(peoplefor)
	try:
		print("popularity will be " + str((other / counter)*100))
	except:
		print("popularity none")
	extrahelpers.popularityWhole
	try:
		extrahelpers.popularityWhole = (other / counter)*100
	except:
		extrahelpers.popularityWhole = 1
	#popularityWhole = 33
	for a in extrahelpers.combination: #delinates double list from website 
		catagoriesa.append(a[0])
		interestsa.append(a[1])
	print("len = " + str(len(extrahelpers.combination)))
	print("interests = " + str(interestsa))
	return render_template("results.html",name="resultsname", len = len(extrahelpers.combination), combinations = extrahelpers.combination, interests = interestsa, catagories = catagoriesa,extraa = extra, peoplelist = people, popularitylist = peoplefor)



@app.route("/results/status", methods=['GET','POST'])
def resultsstatus():
	#print("attempted from results status ")
	statusList = {'status':extrahelpers.popularityWhole}
	#print(statusList)
	return json.dumps(statusList)

#main and runs just normal without ui 
def main():
	#app.run(host = '10.0.0.172', port=80,debug = True)
	


	print("welcome to the basic tester, there are two modes, individual interests and full percentage ")
	mode = input("enter full to do full form, otherwise right no or anything else IDC").lower()
	if mode == "full":
		extrahelpers.full()
	else:
		extrahelpers.individual()

#does not do anything right now.
@app.route('/', methods=['POST'])
def formpostre():
	text = request.form['text']
	print(text)
	return render_template('entry.html',name="testername")

#not really used right now 
#some day a seperate thread for this status would be nice. this is here made for a a seperate results page, idk if I will combine or not yet. 
@app.route('/result', methods=['GET'])
def getStatus():
	print("running for some reason")
	statusList = {'status':extrahelpers.popularityWhole}
	return json.dumps(statusList)



if __name__ == "__main__":
    main()