import csv
import os 
import hashlib
from itertools import count as crashB
from spellchecker import SpellChecker
import datetime
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, current_app, request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
import base64
import socket
import sys
import random










import json
import os
import sqlite3

import requests
import mytester as extrahelpers

# Internal imports
import db as db
from db import init_db_command

# Third party libraries
from flask import Flask, redirect, request, url_for
#import flask_login
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
print(GOOGLE_CLIENT_ID)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
#app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

devcodes = True # this prints everything to the terminal if you want to it. 
def printdev(toprint): # function to control whether stuff is printed to terminal 
	if devcodes:
		print(toprint)

def getip():
	if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
		a = request.environ['REMOTE_ADDR']
	else:
		a = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
	return [request.environ['REMOTE_ADDR'], request.environ.get('HTTP_X_REAL_IP', request.remote_addr), a]


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/",methods=['GET', 'POST'])
def index():

	print("test12")
	extrahelpers.printer()
	if request.method == 'POST':
		#download()
		if 'Submit' in request.form or 'submit interests' in request.form:
			pos = [2,5] # change these variables to change how many boxes it checks 
			text = [['' for _ in range(pos[0])] for _ in range(pos[1])] 
			for a in range(len(text)):
				for b in range(len(text[a])):
					printdev('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1))
					print(request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1)))
					text[a][b] = request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1)).lower()
			printdev(text)
			removers = []
			for a in text:
				if len(a) < 2 or (a[0] == '') or (a[1] == ''):
					printdev("popping, index = " + str(text.index(a)) + " value was "+ str(a) + " reason " + str([len(a) < 2,(a[0] == ''),a[1] == ''])) 
					removers.append(a)
			text = extrahelpers.remove(text,removers)
			print("new combinations to be added =" + str(text))
			printdev("new combinations to be added =" + str(text))
			#extrahelpers.combination.extend(text)
			writecombination(text)
			#extrahelpers.writecombination(text,getip())
			extra.append("test " + str(text) + "endtest                                          test test test test test test test test test test test test test test test")
			printdev(getcombination())
		elif 'results' in request.form:
			#this does the results button
			printdev("results")
			print(getip())
			return redirect("/results")

		else:
			printdev("bad input in html submit post \\, will pretend like nothing happened, " + str(request.form))
	try:
		return render_template('entry.html',name="testername", authentication = current_user.is_authenticated, name2 = current_user.name, email = current_user.email,image = current_user.profile_pic)	
	except:
		return render_template('entry.html',name="testername", authentication = current_user.is_authenticated)


	if current_user.is_authenticated:
		return (
    		"<p>Hello, {}! You're logged in! Email: {}</p>"
			"<div><p>Google Profile Picture:</p>"
    		'<img src="{}" alt="Google profile pic"></img></div>'
    		'<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
		)
		#current_user.name, current_user.email, current_user.profile_pic
	else:
		return '<a class="button" href="/login">Google Login</a>'


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
























#custom modules and custom path check, all dev
for path in sys.path:
		printdev(path)
import mytester as extrahelpers

writentoo = []

def writewrittentoo(stuff):
	hashedip = hashlib.sha384(str(getip()[2]).encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	for a in writentoo:
		if a[0] == hashedip:
			a.extend(stuff)
			return True
	writentoo.append([hashedip] + stuff)
	return True


def getwrittentoo():
	hashedip = hashlib.sha384(str(getip()[2]).encode(encoding = "UTF-8", errors='xmlcharrefreplace')).hexdigest()
	for a in writentoo:
		if a[0] == hashedip:
			return a[1:]
	printdev("none yet")
	return []


def decrypting(key, message):
	code_bytes = key.encode("utf-8")
	key = base64.urlsafe_b64encode(code_bytes.ljust(32)[:32]) # properly encodes and lengthens or shortenes the input string to be used as a key 
	f = Fernet(key)
	return f.decrypt(message)
def encrypting(key,message):
	code_bytes = key.encode("utf-8")
	key = base64.urlsafe_b64encode(code_bytes.ljust(32)[:32]) # properly encodes and lengthens or shortenes the input string to be used as a key 
	f = Fernet(key)
	return f.encrypt(message.encode("utf-8"))

#use the above with lamdas for ultimate street cred | f = lambda key, message : encrypting(key,message)

def getcombination():
	f = lambda key, message : decrypting(key,message)
	key = getip()
	try:
		return [[str(f(str(key),a))[2:-1] for a in message] for message in extrahelpers.getcombination(getip())]
	except:
		return []
	#return extrahelpers.getcombination(getip()

def writecombination(inputinfo):
	print(inputinfo)
	for message in inputinfo:
		print(message)

	f = lambda key, message : encrypting(key,message)
	key = getip()
	a = [[f(str(key),a) for a in message] for message in inputinfo]
	#return extrahelpers.writecombination(inputinfo,getip())
	return extrahelpers.writecombination(a,getip())

def deletecombination():
	return extrahelpers.deletecombination(getip())

extra=[] #holds extra information between functions, not that necessary 

#main routing for main page, controls the textboxes and submit button as well. 

#@app.route("/", methods=['GET','POST'])
def hello():
	print("test123")
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
					text[a][b] = request.form.get('textarea' + str(extrahelpers.alphabet[a]) + str(b + 1)).lower()
			printdev(text)
			removers = []
			for a in text:
				if len(a) < 2 or (a[0] == '') or (a[1] == ''):
					printdev("popping, index = " + str(text.index(a)) + " value was "+ str(a) + " reason " + str([len(a) < 2,(a[0] == ''),a[1] == ''])) 
					removers.append(a)
			text = extrahelpers.remove(text,removers)
			
			printdev("new combinations to be added =" + str(text))
			#extrahelpers.combination.extend(text)
			writecombination(text)
			#extrahelpers.writecombination(text,getip())
			extra.append("test " + str(text) + "endtest                                          test test test test test test test test test test test test test test test")
			printdev(getcombination())
		elif 'results' in request.form:
			#this does the results button
			printdev("results")
			print(getip())
			return redirect("/results")

		else:
			printdev("bad input in html submit post \\, will pretend like nothing happened, " + str(request.form))
	return render_template('entry.html',name="testername", authentication = current_user.is_authenticated)	
	#return "Hello World!"



@app.route("/clubs", methods=['GET','POST'])
def clubs():
	if request.method == 'POST':
		if request.form.get("return") == "return":
			printdev("returned button2")
			return redirect("/")
		
	print("in function")
	return render_template("clubs.html",name = "clubspage")
	

#results page, this controls the results page, its forms and the like, loaded information however still from other url 
@app.route("/results",methods=['GET','POST'])
def results():
	bullshit = ""
	writtenstuff = False
	nowrittenstuff = False
	if request.method == 'POST':
		if request.form.get("return") == "return":
			printdev("returned button2")
			return redirect("/")
		elif request.form.get("clubs") == "clubs":
			printdev("clubs button3")
			return redirect("/clubs")
		else:
			printdev("stuff happens")
			checkboxes = []
			textboxes = []
			printdev(request.form)
			#for a in range(len(extrahelpers.combination)):
			for a in range(len(getcombination())):
				b = request.form.get("interest" + str(a + 1))
				printdev("checkbox " + "insert" + str(a + 1) + " =" + str(b))
				checkboxes.append(b == "check")
				text = request.form.get("interest" + str(a + 1)+"t")
				textboxes.append(text)
				printdev("textbox = " + str(text))
			printdev("checkboxes =" + str(checkboxes))
			printdev("textboxes =" + str(textboxes))
			combinations = getcombination()
			interestsforwrite = []
			intereststotal = []
			for d in range(len(combinations)):
				if checkboxes[d] == True:
					interestsforwrite.append(combinations[d][1])
				intereststotal.append(combinations[d][1])
			writtentoo = getwrittentoo()
			printdev("interestsforwrite =" + str(interestsforwrite))
			printdev(writtentoo)
			for a in range(len(interestsforwrite)):
				if interestsforwrite[a] in writtentoo:
					checkboxes[intereststotal.index(interestsforwrite[a])] = False
					printdev("interest " + str(interestsforwrite[a]) +"already done")

			interestsforwrite = []
			for d in range(len(combinations)):
				if checkboxes[d] == True:
					interestsforwrite.append(combinations[d][1])
			printdev("interests to be rewritten = " + str(interestsforwrite) + " , checkboxes are now" + str(checkboxes))
			writewrittentoo(interestsforwrite)

			#extrahelpers.addandinfoloop(extrahelpers.combination,checkboxes,textboxes)
			extrahelpers.addandinfoloop(getcombination(),checkboxes,textboxes)
			writtenstuff = False
			nowrittenstuff = True
			for x in checkboxes: 
				if x == True:
					writtenstuff = True
					nowrittenstuff = False
			

				
	else:
		printdev("elsed button")
		
		

	#RESULTS!!!!
	interestsa = []
	catagoriesa = []
	#for a in extrahelpers.combination: #delinates double list from website
	for a in getcombination(): #delinates double list from website 
		catagoriesa.append(a[0])
		interestsa.append(a[1])
	#z = extrahelpers.loopinterest(extrahelpers.combination)
	z = extrahelpers.loopinterest(getcombination())
	extra = z[2]
	counter = z[1]
	other = z[0]
	people = z[3]
	peoplefor = z[4]
	for a in range(len(peoplefor)):
		printdev(peoplefor[a][1])
		printdev(peoplefor[a][0])
		try:
			peoplefor[a] = (peoplefor[a][1] - peoplefor[a][0],peoplefor[a][1]) 
		except:
			peoplefor[a] = peoplefor[a]

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
	#for a in extrahelpers.combination: #delinates double list from website 
	for a in getcombination(): #delinates double list from website 
		catagoriesa.append(a[0])
		interestsa.append(a[1])
	printdev("len = " + str(len(extrahelpers.combination)))
	printdev("len = " + str(len(getcombination())))
	printdev("interests = " + str(interestsa))
	extrare = []
	printdev("extrastuffs")
	printdev(extra)
	cwd = os.getcwd()
	print("file thing = " + str(cwd))
	try:
		dir_list = os.listdir("/mysite/static/data")
		print("mysite static data")
	except:
		try:
			dir_list = os.listdir("/static/data")
			print("static data")
		except:
			try:
				dir_list = os.listdir("/static/")
				print("static")
			except:
				try:
					dir_list = os.listdir("/data/")
				except:
					try:
						dir_list = os.listdir(str(cwd) + "/static/data/")
					except:		
						print("none")
	
	for i in range(40):
		file = open("static\\data\\" + random.choice(dir_list),"r")
		#lines = list(csv.reader(file,))
		newlist = []
		for a in list((csv.reader(file,))):
			if len(a) >= 1:
				newlist.append(str(a[0]))
		print(newlist)
		bullshit += str("\n".join(newlist))
		#bullshit = ""
		#for a in newlist:
		#	bullshit += str(a) + "\n"
		file.close()
	print("bullshit =" + str(bullshit))

	printdev(extrare)
	extrare = []
	for a in extra:
		extrare.append(' ;\n '.join(a))
	printdev(extrare)
	print("stuffs")
	print(getcombination())
	#return render_template("results.html",name="resultsname", len = len(extrahelpers.combination), combinations = extrahelpers.combination, interests = interestsa, catagories = catagoriesa,extraa = extrare, peoplelist = people, popularitylist = peoplefor)
	return render_template("results.html",name="resultsname", len = len(getcombination()), combinations = getcombination(), interests = interestsa, catagories = catagoriesa,extraa = extrare, peoplelist = people, popularitylist = peoplefor, success = writtenstuff, failure = nowrittenstuff, stuff = bullshit)


#api page for the results page, not for viewers really just used for json return 
@app.route("/results/status", methods=['GET','POST'])
def resultsstatus():
	#printdev("attempted from results status ")
	statusList = {'status':extrahelpers.popularityWhole}
	#printdev(statusList)
	return json.dumps(statusList)

@app.route("/test")
def test():
	return render_template("test.html",name="test")

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

if __name__ == "__main__":
	app.run()
	print("test1")
#runs main function if run as main file and not as module like with flask. 
#if __name__ == "__main__":
 #   main()