"""
" Server for GUI 
" Author: Koustubh Saxena
" Ver 0.0
"""

import base64
import os
import sqlite3
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# TODO: Make this in its own database opening function
# TODO: Decide if one or two dbs are required
db = sqlite3.connect("Main.sqlite")
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS accounts(user TEXT,hash TEXT,salt TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS passwords(name TEXT,data TEXT,salt TEXT)')
db.commit()


def derKey (salt, key, enc):
	if enc:
		salt = os.urandom(16)
	keyb = key.encode('utf-8')
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	pash = base64.urlsafe_b64encode(kdf.derive(keyb))
	f = Fernet(pash)
	if enc:
		return f, salt
	else:
		return f


def decrypt (mess, key, non):
	f = derKey(non, key, False)
	messb = mess.encode('utf-8')
	messb = f.decrypt(messb)
	return messb.decode('utf-8')


def encrypt (mess, f):
	token = f.encrypt(mess.encode('utf-8'))
	return token.decode('utf-8')


def usrExist (user):
	cur.execute("SELECT user FROM accounts")
	for user in cur.fetchall():
		if user[0] == user:
			return True
		# print("[D]: user: ",user)
	return False


def createUsr (user, pasw):
	h = hashlib.blake2b()
	salt = os.urandom(8)
	salt = base64.urlsafe_b64encode(salt)
	h.update(pasw.encode('utf-8'))
	h.update(salt)
	pash = h.hexdigest()
	print(pash, type(salt))
	cur.execute("INSERT INTO accounts(user, hash, salt) VALUES(?, ?, ?)", (user, pash, salt))
	db.commit()


def verifyUsr (user, pasw):
	h = hashlib.blake2b()
	h.update(pasw.encode('utf-8'))
	cur.execute("SELECT salt FROM accounts WHERE user='" + user + "'")
	h.update(cur.fetchone()[0])
	cur.execute("SELECT hash FROM accounts WHERE user='" + user + "'")
	if h.hexdigest() == cur.fetchone()[0]:
		return True
	return False


# TODO: INFO: note as a csv, make an note structure
# TODO: Test
def storeCred(key, name, pasw, note = "NULL"):
	if note == "NULL":
		note = ""
		note = "pass:" + passw
	else:
		note = "pass:" + passw + ",note:" + note
	
	f, salt = derKey(0, key, True)
	note = encrypt(note,f)
	cur.execute("INSERT INTO passwords(name, data, salt) VALUES(?, ?, ?)", (name, note, salt))
	db.commit()


print("Enter the user info")
usr = str(input("Username: "))
pas = str(input("Password: "))
if usrExist(usr):
	print(" [I] user already exist going forward with verification!")
else:
	createUsr(usr, pas)
print(" [I] verifing user")
auth = verifyUsr(usr, pas)
if not auth:
	print(" [E] Authentication Failure\n [E] Wrong username or password")
	exit
print(" [I] Authentication Succesfull\n\tAcess granted!")
