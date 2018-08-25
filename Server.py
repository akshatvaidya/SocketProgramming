# Name - Akshat Vaidya
# Student Id - 1001550684
# importing all the necessary libraries
# socket library is used to create and handle various sockets
# Threading library is used to create threads which help in multithreading
# easygui library is used to create gui
# os library is used to get the file list at a specific location
import socket
from threading import Thread
import easygui
import os

# specifying the host as localhost because the server and clients both reside on the same node
host = socket.gethostname()
port = 80


# A class is created for clients so that easch thread will be its object and have the same particular mechanism as other threads
class ClientThread(Thread):
    # A list of usernames of all the connected clients is maintained with each client
    usernames = []

    # This is the constructor which assigns the ip address, port number and socket to each client
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock

    # This method prints all the connected clients to GUI
    def listusers(self):
        # First argument is the text to be shown and the second argument is the title of the window
        easygui.msgbox(self.usernames, 'Connected Clients:')

    # This is the code which will run from the server side for each and every client
    def run(self):
        # Username of the connected client is received from the client
        username = self.sock.recv(64)
        # username is saved in the usernames[] list
        ClientThread.usernames.append(str(username, "utf-8"))
        # After every client connects the listuser() method is called so it will display the connected clients
        self.listusers()

        # This loop will execute till the current client thread is running
        while True:
            # Server will receive either upload, download or disconnect command from the client
            command = self.sock.recv(64)
            # if the command is upload then following code block will be executed
            if str(command, "utf-8") == 'Upload':
                # name of the file which the client wants to upload is received
                filename = self.sock.recv(64)
                # filename is sent with UTF-8 encoding so decoding it here and saving the filename
                file = str(filename, "utf-8")
                # Since the client sends the complete filename which includes the path to that file too, server splits the filename
                # Server splits the filename based on \ in address path
                temp = file.split("\\")
                # After saving the separate parts after each \, server will only save the last part which is the filename
                file = temp[len(temp) - 1]
                if file:
                    # creating a file with the same filename at the server and copying all the data into it i.e. basically copying the file at the client side to the server side
                    with open(file, 'wb') as f:
                        data = self.sock.recv(1024)
                        f.write(data)
                    f.close()

            # if download is the command received then following code block will be executed
            elif str(command, "utf-8") == 'Download':
                # server will first show a list of all the available files to the client and client's choice will be saved
                filename = easygui.choicebox("Choose a file to download:", "Download A File", os.listdir())
                try:
                    # filename is sent to the client
                    self.sock.send(bytes(filename, 'utf-8'))
                    # file is opened and all the data is sent to the client
                    f = open(filename, 'rb')
                    data = f.read()
                    self.sock.send(data)
                except:
                    # if client decides to close the download window then this message is shown
                    easygui.msgbox('Canceled the operation')
            # if client decides to disconnect then server will terminate that thread and close the socket
            else:
                self.sock.close()
                print('Connection Closed')
                break


# A socket is created where the first argument refers to the IPV4 addressing scheme and the second argument refers to the TCP protocol
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This line makes sure that sockets do not use the same port number again
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# This binds the server to the given host address and port number so that it can listen to incoming requests
tcpsock.bind((host, port))

while True:
    # 5 specifies that server will wait for 5 connections if it busy and the 6th connection will be refused
    tcpsock.listen(5)
    # This line will accept a particuar incoming request and save the address and port number of that client from which the request is coming from
    (conn, (ip, port)) = tcpsock.accept()
    # A new thread is created for each and every client request which is accepted that too on the exact same address and port number
    newthread = ClientThread(ip, port, conn)
    # start() method starts the client thread and calls the run method of that thread
    newthread.start()

# Exit from the code
exit(0)




