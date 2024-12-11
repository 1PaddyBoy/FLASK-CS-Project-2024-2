import csv
import os 
import hashlib
from itertools import count as crashB
from spellchecker import SpellChecker
import datetime
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, current_app
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
import base64
import socket
import sys

devcodes = False # this prints everything to the terminal if you want to it. 
def printdev(toprint): # function to control whether stuff is printed to terminal 
	if devcodes:
		printdev(toprint)
#custom modules and custom path check, all dev
for path in sys.path:
		printdev(path)
import mytester as extrahelpers


extra=[] #holds extra information between functions, not that necessary 

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
					printdev('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1))
					printdev(request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1)))
					text[a][b] = request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1))
			printdev(text)
			removers = []
			for a in text:
				if len(a) < 2 or (a[0] == '') or (a[1] == ''):
					printdev("popping, index = " + str(text.index(a)) + " value was "+ str(a) + " reason " + str([len(a) < 2,(a[0] == ''),a[1] == ''])) 
					removers.append(a)
			text = extrahelpers.remove(text,removers)
			
			printdev("new combinations to be added =" + str(text))
			extrahelpers.combination.extend(text)
			extra.append("test " + str(text) + "endtest                                          test test test test test test test test test test test test test test test")
			printdev(extrahelpers.combination)
		elif 'results' in request.form:
			#this does the results button
			printdev("results")
			return redirect("/results")

		else:
			printdev("bad input in html submit post \\, will pretend like nothing happened")
	return render_template('entry.html',name="testername")	
	#return "Hello World!"



#results page, this controls the results page, its forms and the like, loaded information however still from other url 
@app.route("/results",methods=['GET','POST'])
def results():
	if request.method == 'POST':
		if request.form.get("return") == "return":
			printdev("returned button2")
			return redirect("/")
		else:
			checkboxes = []
			textboxes = []
			printdev(request.form)
			for a in range(len(extrahelpers.combination)):
				b = request.form.get("interest" + str(a))
				printdev("checkbox " + "insert" + str(a) + " =" + str(b))
				checkboxes.append(b == "check")
				text = request.form.get("interest" + str(a)+"t")
				textboxes.append(text)
				printdev("textbox = " + str(text))
			printdev("checkboxes =" + str(checkboxes))
			printdev("textboxes =" + str(textboxes))
			extrahelpers.addandinfoloop(extrahelpers.combination,checkboxes,textboxes)
	else:
		printdev("elsed button")
		
		

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
	printdev("people:")
	printdev(people)
	printdev(peoplefor)
	for a in peoplefor:
		printdev(len(a))
		if len(a) < 2:
			printdev("triggered replacement")
			a = (1,1)

	if len(peoplefor) == 0:
		peoplefor.append((1,1))
	printdev("popularity per:")
	printdev(peoplefor)
	try:
		printdev("popularity will be " + str((other / counter)*100))
	except:
		printdev("popularity none")
	extrahelpers.popularityWhole
	try:
		extrahelpers.popularityWhole = (other / counter)*100
	except:
		extrahelpers.popularityWhole = 1
	#popularityWhole = 33
	for a in extrahelpers.combination: #delinates double list from website 
		catagoriesa.append(a[0])
		interestsa.append(a[1])
	printdev("len = " + str(len(extrahelpers.combination)))
	printdev("interests = " + str(interestsa))
	return render_template("results.html",name="resultsname", len = len(extrahelpers.combination), combinations = extrahelpers.combination, interests = interestsa, catagories = catagoriesa,extraa = extra, peoplelist = people, popularitylist = peoplefor)


#api page for the results page, not for viewers really just used for json return 
@app.route("/results/status", methods=['GET','POST'])
def resultsstatus():
	#printdev("attempted from results status ")
	statusList = {'status':extrahelpers.popularityWhole}
	#printdev(statusList)
	return json.dumps(statusList)

#main and runs just normal without ui if called without flask
def main():
	#app.run(host = '10.0.0.172', port=80,debug = True)
	


	printdev("welcome to the basic tester, there are two modes, individual interests and full percentage ")
	mode = input("enter full to do full form, otherwise right no or anything else IDC").lower()
	if mode == "full":
		extrahelpers.full()
	else:
		extrahelpers.individual()

#just used for testing, doesn't really do anything 
@app.route('/', methods=['POST'])
def formpostre():
	text = request.form['text']
	printdev(text)
	printdev("running for some reason, // ")
	return render_template('entry.html',name="testername")

#not really used right now, just for testing 
#some day a seperate thread for this status would be nice. this is here made for a a seperate results page, idk if I will combine or not yet. 
@app.route('/result', methods=['GET'])
def getStatus():
	printdev("running for some reason // results ")
	statusList = {'status':extrahelpers.popularityWhole}
	return json.dumps(statusList)


#runs main function if run as main file and not as module like with flask. 
if __name__ == "__main__":
    main()