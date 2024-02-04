# WorkflowManagement

1.
2.
3.
4.
5.
6.
....



#############################################################################
Features:

LogIn Feature
- WBIG GUI has a realistic login function implemented
	- several authorized users can log in and log out -> e.g. us different tabs or browser
	- in addition, users who are already logged in cannot log in again
	- due to that, certain users habe certain access rights
	- the role right are stored in a json file
	- also the username, hash password and role are stored in a json file
	- during a login, the plain text is converted into a hash and this hash is compared with the hash form the json file
	- only if the username and password are correct, the user can login
	- the login process is also logged in the console, there are several log messages
		- the username 
		- the role
		- successful or not
		- someone is logged in