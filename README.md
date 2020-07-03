# JAPW :: Just an Another Password Manager

## Roadmap

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
 - [X] Encrypt User's Accounts
	:: Where Accounts refer to user's individual accounts on different sites.
 - [X] Store User's Accounts.
 - [X] Decrypt's User's Accounts.
 - [ ] Make User's Accounts Only Accesible to them.
 - [ ] (Feature) Accounts can be exported.
 - [ ] (Feature) In-memory database.

:: How?
 - [ ] Accounts DB
	* CSV database: (of Accounts)
		* Name => Twitter,facebook,e.t.c..
		* Username => emailID, ID, e.t.c..
		* Password => 
		* Note => Something.
 - [X] Encrypt Using individual accounts Keys
	* Each key is derived through PBKDF2-HMAC-SHA256 and store in a database like UserDB at sever.
	* We encrypt individual acounts using these keys
 - [ ] The database containing Accounts keys is Encrypted using the master key.

:: UserExperience
 - [ ] First Time
 - [ ] Start APP:Enter Password ->Decrypt KEYS DB (CSV) with password->Put it into memory
 - [ ] Asking Account info:Enter 
