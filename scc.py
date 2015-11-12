# telnet program example
import os
import socket
import select
import string
import getpass
import sys
from cipher import algorithm
 
def prompt() :
    print " ~ ",

def clear():
    if "linux" in sys.platform:
        os.system("clear")
    elif "win" in sys.platform:
        os.system("cls")
 
#main function
if __name__ == "__main__":

    clear()

    print "|-- Crypto chat client 1.0\n"

    try:
     
        if(len(sys.argv) < 3) :
            print ' ~ Usage : python client.py hostname port'
            sys.exit()
     
        host = sys.argv[1]
        port = int(sys.argv[2])
     
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
     
        # connect to remote host
        try :
            s.connect((host, port))
        except :
            print ' ~ Unable to connect'
            sys.exit()

        nickname = raw_input(' ~ Secure chat nickname: ')
        password = ""

        # to prevent an empty key
        while password == "":
            password  = getpass.getpass(" ~ Secure chat password: ")
            vpassword = getpass.getpass(" ~ Confirm password: ")

            if password != vpassword:
                print "\n ~ [FAIL] Keys do not match!\n"
                password = ""
     
        print " ~ Connected to remote host"
        print " ~ Start sending messages"
        #prompt()
     
        while 1:
            socket_list = [sys.stdin, s]
         
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
            for sock in read_sockets:
                #incoming message from remote server
                if sock == s:
                    data = sock.recv(4096)
                    if not data :
                        print '\n Disconnected from chat server'
                        sys.exit()
                    else :

                        try:
                            type, data = data.split(':')
                        except:
                            continue

                        if type == 'message':

                            try:

                                print algorithm.decode(data, password)

                            except:

                                print "<unknow message>"

                        elif type == 'sys':

                            print data

                        #prompt()
             
                #user entered a message
                else:

                    msg = raw_input()

                    if msg == '\\clear':
                        clear()
                    elif msg == '\\quit':
                        s.close()
                        sys.exit()

                    else:
                    
                        s.send(algorithm.encode(nickname + ": " + msg, password))
                        
                    #prompt()

    except KeyboardInterrupt:

        print "\n\n|-- bye"