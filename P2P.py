import FrontEnd
import Connection
import socket

p2p = Connection.MessagesP2P(socket.gethostname(), o)
server_hostname = 
server_port = 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_hostname,int(server_port))) 

#LOGIN
p2p.LoginRequest(s)
p2p.Read(s)

if (p2p.sessionId == "0000000000000000"):
    print("ERRORE")

#MENU'
#1. Scarica file
#2. Fornire file
    #Apri istanza "server"
    #Posibilità di rimuovere
#3. Logout
