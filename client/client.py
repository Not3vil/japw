import secrets
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

def encryptMsg (pasw: str, note: str) -> str:
	msg = pasw + ":" + note
	key = urlsafe_b64encode(secrets.token_bytes(32))
	f = Fernet(key)
	encMsg = f.encrypt(msg.encode('utf-8'))
	return encMsg.decode('utf-8'), key.decode('utf-8')

def decryptMsg (encMsg: str, key: str):
	f = Fernet(key.encode('utf-8'))
	mesg = f.decrypt(encMsg.encode('utf-8'))
	return mesg.decode('utf-8')
	
def newAccount(name: str, pasw: str, note: str = ""):
	# TODO: Check if same name account exists
	mesg, key = encryptMsg(pasw, note)
	with open("account.csv",'a') as f:
		f.write(name.lower().lstrip() + ":")
		f.write(mesg)
		f.write("\n")
		f.close()
	
	# TODO: the user.csv should be encrypted
	with open("user.csv",'a') as f:
		f.write(name.lower().lstrip() + ":")
		f.write(key)
		f.write('\n')
		f.close()
	
def retriveAccount(name: str):
	encMsg = ""
	with open("account.csv") as f:
		lines = f.readlines()
		for line in lines:
			if line.split(":")[0] == name.lower():
				encMsg = line.split(":")[1]
				break

	key = ""
	with open("user.csv") as f:
		lines = f.readlines()
		for line in lines:
			if line.split(":")[0] == name.lower():
				key = line.split(":")[1]
				break
	
	decMsg = decryptMsg(encMsg, key)
	pasw = decMsg.split(":")[0]
	note = decMsg.split(":")[1]
	return pasw, note

# TODO: Make a function that extracts all accounts into a csv file.

# TESTS
# import sys
# # TEST 1:
# msg, key = encryptMsg("badfacebook", "Never Ever use This!!")
# demsg = decryptMsg(msg, key)
# if demsg.split(':')[0] == "badfacebook":
# 	print("Test Msg encryption and decryption succedded!")
# else:
# 	print("Test Msg encryption and decryption Failed!",file=sys.stderr)

# # TEST 2:
# import os
# newAccount("fb", "badpassword","Never use this!")
# newAccount("insta", "verygoodpassword","But i will use this!")
# accPass, accNote = retriveAccount("fb")
# if accPass == "badpassword" and accNote == "Never use this!":
# 	print("Test Account Storing And retriving succedded!")
# else:
# 	print("Test Account Storing And retriving  Failed!",file=sys.stderr)
# os.remove("user.csv")
# os.remove("account.csv")
