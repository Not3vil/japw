"""
= Client Backend (non-UI)
= Author: Koustubh Saxena
= Ver 0.0
"""

import sqlite3
from base64 import urlsafe_b64encode
from os import urandom
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#TODO: Make a function that can decrypt and rencrypt every website in case of password change
#TODO: make class with the three function below us.
def derKey (salt, key, enc):
	'''Set up Cryptography parameters and returns a pakage uset to encrypt or decrypt'''
	if enc:
		salt = urandom(16)
	keyb = key.encode('utf-8')
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	pash = urlsafe_b64encode(kdf.derive(keyb))
	f = Fernet(pash)
	if enc:
		return f, salt
	else:
		return f

def decrypt (mess, key, non):
	'''It Decrypts the mess (str) using key(str) and non (str) returns plaintext'''
	f = derKey(non, key, False)
	messb = mess.encode('utf-8')
	messb = f.decrypt(messb)
	return messb.decode('utf-8')

def encrypt (mess, f):
	'''It Encrypts the mess (str) using the derKey (func) returns ciphertext'''
	token = f.encrypt(mess.encode('utf-8'))
	return token.decode('utf-8')

def storeCred(key, name, pasw, note = "NULL"):
	'''Stores the password (passw) for website (name) with master_password (key) into the database'''
	#TODO: Check if the same name already exist in database
	if note == "NULL":
		note = "pass:" + pasw
	else:
		note = "pass:" + pasw + ",note:" + note
	
	f, salt = derKey(0, key, True)
	note = encrypt(note,f)
	cur.execute("INSERT INTO passwords(name, data, salt) VALUES(?, ?, ?)", (name, note, salt))
	db.commit()

def displayCred (key, name):
	'''Returns the password and note [if any] for the website (name) secured with master_passord (key)'''
	cur.execute("SELECT salt FROM passwords WHERE name='" + name + "'")
	salt = cur.fetchone()
	if salt == None:
		#TODO: see that this error is handeled in UI
		raise Exception("name does not exist")
	salt = salt[0]
	cur.execute("SELECT data FROM passwords WHERE name='" + name + "'")
	data = cur.fetchone()
	if data == None:
		#TODO: see that this error is handeled in UI
		# This means database is corrupt
		raise Exception("can't find password")
	data = data[0]
	data = decrypt(data, key, salt)
	data = data.split(',')
	if len(data) == 2:
		note = data[1].split(':')[1]
	else:
		note = ''
	password = data[0].split(':')[1]
	return password, note

# TODO: Create a class with all the above funC and make the above two public.
# 		The code below will go into the constructor  
db = sqlite3.connect("Pass.sqlite")
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS passwords(name TEXT,data TEXT,salt TEXT)')
db.commit()
#test
storeCred("Hello","LOOK","password","Something")
displayCred("Hello","LOOK")
# Destructor
cur.close()
db.close()