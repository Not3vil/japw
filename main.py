#!/usr/bin/env python
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

db = sqlite3.connect("Pass.sqlite")
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS accounts(user TEXT,hash TEXT,salt TEXT)')


# def storeCred(name, pasw, note):

def derKey(salt, key, enc):
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


def decrypt(mess, key, non):
    f = derKey(non, key, False)
    messb = mess.encode('utf-8')
    messb = f.decrypt(messb)
    return messb.decode('utf-8')


def encrypt(mess, key):
    f, salt = derKey(0, key, True)
    token = f.encrypt(mess.encode('utf-8'))
    return token.decode('utf-8'), salt


def createUsr(usr, pas):
    h = hashlib.blake2b()
    salt = os.urandom(8)
    salt = base64.urlsafe_b64encode(salt)
    h.update(pas.encode('utf-8'))
    h.update(salt)
    pash = h.hexdigest()
    print(pash, type(salt))
    cur.execute("INSERT INTO accounts(user, hash, salt) VALUES(?, ?, ?)", (usr, pash, salt))
    db.commit()


# def verifyUsr(usr,pass):

pas = str(input("Pass: "))
usr = str(input("Mes: "))
createUsr(usr, pas)

cur.close()
db.close()
