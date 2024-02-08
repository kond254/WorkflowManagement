# WBIG

Server Configuration:
1. Login onto wfm server with username: "wfm" and password: "mnFD6dfd"
2. Install Git if it isnt on the server 
3. Clone the repository https://github.com/kond254/WorkflowManagement with "git clone 	https://github.com/kond254/WorkflowManagement"
4. Install npm and pip
5. install and activate venv in WorkflowManagement/Code and WorkflowManagement/Backend and type in "pip install -r requirements.txt"
6. Move to the frontend repository with cd WorkflowManagement/GUI/src/app and install nodejs v20.x with 
	"curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - &&\
	sudo apt-get install -y nodejs"
7. Move to cd WorkflowManagement/GUI and install Angular/CLI with "npm install -g @angular/cli"


Server Start-Instruction:
1. Login onto wfm server with username: "wfm" and password: "mnFD6dfd"
2. To start the System type cd WorkflowManagement/Backend and type "python3 backend.py" 
3. Then type cd WorkflowManagement/GUI/src/app and type "ng serve --host=0.0.0.0
4. Finally move to cd WorkflowManagement/Code and type "python3 main.py"
5. The frontend can be accessed via the URL: http:141.26.157.71:4200


Installation Locally:
	Note: Change the URL in Line 119 from GUI the data.service.ts to the URL the backend runs on locally!
1. Install Python by using the follwing command: sudo apt-get install python3-pip
2. Check if Python is installed successfullyby using: python --version
3. Install node: https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi -> standard intallation (recommended to install via browser)
4. Check if node is installed successfully: node --version
5. Install Angular CLI globally with the npm-command: npm install -g @angular/cli
6. Install this Angular needed add-on: npm install --save-dev @angular-devkit/build-angular 
   Otherwise you can try the command: npm install @angular/cli
7. Check if angular installed successfully by using: ng version
8. Here you can check again Angular version, Node version, Package Manager (npm) version Angular
9. Install flask: pip install flask
10. Install flask cors: pip install flask_cors
11. Install flask socketio: pip install flask_socketio
12. Check if flask was installed successfully: pip show flask
13. Install pyzeebe: pip install pyzeebe
14. Check if pyzeebe was installed successfully: pip show pyzeebe

Start-Instruction Locally:
1. Download project as zip via github: https://github.com/kond254/WorkflowManagement
2. Unpack zip folder
3. Start the one console for backend
4. Call up path for backend file: cd  ..\WorkflowManagement\Backend
5. Execute backend file: python backend.py
6. Backend file should now be running
7. Start new console for frontend
8. Call up path for frontend file: cd ..\WorkflowManagement\GUI\src\app
9. Run fronend with: ng serve --o 
10. Frontend should now be running
11. Now a browser should open automatically with the gui. If not, then manually open the generated link in the frontend console: http://localhost:4200/ (by default)
12. Now start the camunda operator to display the process: http://141.26.157.71:8081/login
13. Login with the data: username: demo, password: demo
14. Click the tab "dashboard and you can the process instances
15. Next, login a user via login button in browser (see the login data in chapter "right")


#############################################################################

All used API-Links are in the Backend Folder under backend.py from line 185

#############################################################################
Access-Rights:
These following rights have been defined and can be entered in the login window

username: hrdepartment, password: 1234
username: hrmanager, password: 1234
username: accounting, password: 1234
username: admin, password: 1234

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
