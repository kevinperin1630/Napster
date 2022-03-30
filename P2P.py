import FrontEnd
import Connection
import socket
import sys
import random

if (len(sys.argv) != 2):
    print("Errore! Numero di argomenti al lancio errato!")
    exit(1)
else:
    server_hostname = sys.argv[1]   #risolvere caso in cui si scriva male indirizzo ip

server_port = 80
p2p = Connection.MessagesP2P(socket.gethostname(), random.randint(50000, 52000))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_hostname,int(server_port)))

#LOGIN
while True:
    p2p.LoginRequest(s)
    p2p.Read(s)

    if (p2p.sessionId == "0000000000000000"):
        print("Login non è possibile")
    else:
        break

#MENU'
#1. Scarica file
#2. Fornire file
    #Apri istanza "server"
    #Posibilità di rimuovere
#3. Logout
