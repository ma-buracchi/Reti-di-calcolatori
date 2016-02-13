'''
Created on 18/nov/2014

@author: Marco
'''
import socket

with open('testGM', 'r') as test:
    result = ""
    for line in test:
        serverName = 'localhost'
        serverPort = 8080
        clientSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        clientSocket.connect( (serverName , serverPort) )
        clientSocket.sendall( line + '\r\n' )                                                                
        modifiedMessage = clientSocket.recv( 2048 )
        result = result + modifiedMessage
        clientSocket.close() # close socket
    print result