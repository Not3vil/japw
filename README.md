# JAPW :: Just an Another Password Manager

## Features

### Server (Optional)

:: Used to verify a User,
:: There is no way to recover user's master password (i.e. ALL is lost).
:: May not be required.
:: (Feature) Use it to sync different clients of the same user.

- [ ] User DB
	* A Normal SQL DB?
	* Table User:
		* Hashe
		* Salts
		* Iteration
- [ ] Hashed Using HMAC-PBKDF2 or HMAC-SHA-128
- [ ] An API to deal with the client
	* Use express.js to make this
	* Goals: 
		1. [ ] Learn node and npm
		2. [ ] Deploying node Server's

### Client

:: What it Does?
	- [ ] Encrypt User's Accounts
		:: Where Accounts refer to user's individual accounts on different sites.
	- [ ] Store User's Accounts.
	- [ ] Decrypt's User's Accounts.
	- [ ] (Feature) Accounts can be exported.  

:: How?
	- [ ] Accounts DB
		* CSV database: (of Accounts)
			* Name => Twitter,facebook,e.t.c..
			* Username => emailID, ID, e.t.c..
			* Password => 
			* Note => Something.
