"""
" Server Backend
" Author: Koustubh Saxena
" Ver 0.1
"""

from base64 import urlsafe_b64encode
from os import urandom
import sqlite3
import hashlib

def createUsr (user, pasw):
	h = hashlib.blake2b()
	salt = urandom(8)
	salt = urlsafe_b64encode(salt)
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

#TODO: delete user
#TODO: Change Password

db = sqlite3.connect("Main.sqlite")
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS accounts(user TEXT,hash TEXT,salt TEXT)')
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

cur.close()
db.close()