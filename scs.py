import os
import sys
import socket
import select
from cipher import algorithm

def clear():
    if "linux" in sys.platform:
        os.system("clear")
    elif "win" in sys.platform:
        os.system("cls")
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":

    clear()

    print "|-- Crypto chat server 1.0\n"

    try:
     
        # List to keep track of socket descriptors
        CONNECTION_LIST = []
        RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    
        ADDR = raw_input(" ~ IP: ")
        PORT = int(raw_input(" ~ Port: "))
     
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this has no effect, why ?
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ADDR, PORT))
        server_socket.listen(10)
 
        # Add server socket to the list of readable connections
        CONNECTION_LIST.append(server_socket)
 
        print " ~ Chat server started on %s:%s " % (ADDR, PORT)
 
        while 1:
            # Get the list sockets which are ready to be read through select
            read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
            for sock in read_sockets:
                #New connection
                if sock == server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = server_socket.accept()
                    CONNECTION_LIST.append(sockfd)
                 
                    broadcast_data(sockfd, "sys:(%s) entered room" % addr[0])

                    print " ~ Client (%s, %s) connected" % addr
             
                #Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        #In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            broadcast_data(sock, "message:" + data)
                 
                    except:

                        broadcast_data(sock, "sys:(%s) is offline" % addr[0])
                        
                        print " ~ Client (%s, %s) is offline" % addr
                        
                        try:
                            sock.close()
                            CONNECTION_LIST.remove(sock)
                        except:
                            pass
                        
                        continue
     
        server_socket.close()

    except KeyboardInterrupt:

        print "\n\n|-- bye"