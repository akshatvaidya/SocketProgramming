# SocketProgramming
This is a client server app designed in Python in which a client is able do 4 things:
1. Upload A File
2. Download A File
3. See Available Files from all the clients on the server
4. Disconnect

The connection to the server remains open until the client explicitely chooses to disconnect. 

The aplication has a very basic UI. 

Before running the program:
Go to line no. 66 in Client.py and change the directory path to where you want the files to be downloaded. 
Upload works from all the directories. All the files for all the clients will be downloaded to this path specified at line no. 66.
Also, easygui library is required to run the program.
‘Pip install easygui’ is the command to install it.
The program sometimes does not work with the command line so the last option would be to install Pycharm and run the program in it.
Just open pycharm and select open project in file menu. Select the entire SocketProgramming folder.


References:
Easygui docs - http://easygui.sourceforge.net/tutorial.html
Multithreading and basic api for client and server - http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
Easygui - http://easygui.sourceforge.net/api.html
String encoding with bytes - https://github.com/mitsuhiko/phpserialize/issues/15


Bugs:
After running each client, a new window opens which lists all the connected clients at that point. 
Please close that window before doing any operation with any client.


