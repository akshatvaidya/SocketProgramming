# Name - Akshat Vaidya
# Student Id - 1001550684
# importing all the necessary libraries
# socket library is used to create and handle various sockets
# easygui library is used to create gui
# os library is used to get the file list at a specific location
import socket
import easygui
import os

# specifying the host as localhost because the server and clients both reside on the same node
host = socket.gethostname()
port = 80

# A socket is created where the first argument refers to the IPV4 addressing scheme and the second argument refers to the TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect method connects to the server on given host and port
s.connect((host, port))

# The message to be shown to the client upon connection and the title of that window
message = "Enter a username"
title = "Client"

# FieldsList keeps track of all the fields which will be used as input from the user
fieldsList = ["Username"]

# The window is created with the parameters message, title and the input fields
fieldValue = easygui.multenterbox(message, title, fieldsList)

# since the field list has only one field i.e. username, it is sent to the server
s.send(bytes(fieldValue[0], 'utf-8'))

# Menu is shown to the client and client's choice is saved in the variable
choice = easygui.buttonbox('Choose an option:', fieldValue, ["Upload A File", "Check Available Files", "Download A File", "Disconnect"], None, None, "Disconnect")

# This loop will execute as long as the user does not select Disconnect
# Once inside the loop, according to the choice of the user corresponding code will be executed
while choice != "Disconnect":
    # if upload is selected then following code block will be executed
        if choice == "Upload A File":
            # this will notify the server that upload was selected
            s.send(bytes('Upload', "utf-8"))
            # fileopenbox allows the user to select a particular file from any directory
            filename = easygui.fileopenbox()
            try:
                # filename is sent to the server
                s.send(bytes(filename, 'utf-8'))
                # file is opened in read in binary mode
                f = open(filename, 'rb')
                # reading the data from the file and saving it
                data = f.read()
                # data is sent to the sever
                s.send(data)
                # Notifying the user after uploading
                easygui.msgbox('Done Uploading')
                # Redirecting user back to the main menu
                choice = easygui.buttonbox('Choose an option:', fieldValue, ["Upload A File", "Check Available Files", "Download A File", "Disconnect"], None, None, "Disconnect")

            # if the file does not exist then user will forcefully be redirected to the main menu
            except FileExistsError as f:
                choice = easygui.buttonbox('Choose an option:', fieldValue, ["Upload A File", "Check Available Files", "Download A File", "Disconnect"], None, None, "Disconnect")

    # if check available files is selected then following code block will be executed
        elif choice == "Check Available Files":
            # listdir(path) method lists all the files present at that particular path which is sent as an argument
            easygui.msgbox(os.listdir('C:\\Users\\Akshat Vaidya\\PycharmProjects\\SocketProgramming'), "File List")
            # After showing the file list, user is sent back to the main menu
            choice = easygui.buttonbox('Choose an option:', fieldValue, ["Upload A File", "Check Available Files", "Download A File", "Disconnect"], None, None, "Disconnect")

    # if download is selected then following code block will be executed
        elif choice == "Download A File":
            # this will notify the server that download is selected
            s.send(bytes('Download', "utf-8"))
            # after the server is notified that download is selected, server shows a list of available files to the client
            # Once client clicks on a file server sends the filename to the client
            filename = s.recv(64)
            # Here the filename is prefixed with whatever folder client wants the file to be downloaded in
            file = "C:\\Users\\Akshat Vaidya\\Downloads\\" + str(filename, "utf-8")
            if file:
                # now we create a file with the same name and write all the data into it basically making a copy of the file at the server
                with open(file, 'wb') as f:
                    data = s.recv(1024)
                    f.write(data)
                    easygui.msgbox('Done Downloading')
                f.close()
            # client is redirected back to the main menu
            choice = easygui.buttonbox('Choose an option:', fieldValue, ["Upload A File", "Check Available Files", "Download A File", "Disconnect"], None, None, "Disconnect")

        else:
            # if disconnect is selected server is notified of it
            s.send(bytes('Disconnect', "utf-8"))
            #s.close()




