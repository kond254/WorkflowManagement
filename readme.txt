Step-by-Step-Installation:

1.
2.
3.
4.
5.
6.
....



#############################################################################
Features:
- WBIG GUI has a realistic login function implemented
	- Multiple users can log in and out -> use different tabs
	- In addition, already logged-in users cannot log in again. 
	- Certain users can also only access certain pages
	- The role rights are stored in a JSON file with boolean values
	- also the authorized users with name, password are also stored in a JSON file
	- The password is recorded as plain text via the UI and converted into a hash value and compared with the hash value from the JSON file
	- If the person is authorized, this person can logged in and the login status is also removed when the person log out.
