import FrontEnd
import Connection
import socket
import sys
import random
import os

def FilesInDir(pathOfferDir):
    fileList = []
    fileNames = os.listdir(pathOfferDir)
    for name in fileNames:
        filePath = "%s\\%s" %(pathOfferDir, name)
        buffer = File.FileData(filePath)
        md5 = File.CalculateMD5(buffer)
        file = File(md5, name)
        fileList.append(file)
    return fileList

def OfferFiles(fileList):
    for file in fileList:
        p2p.AddFileRequest(file.md5, file.name)
        num_copies = p2p.Read(s)
        print("Nella rete esistono %s copie di %s" %(num_copies, file.md5))

def Logout():
    p2p.LogoutRequest(s)
    deleted = p2p.Read(s)
    print("Logout. %e file rimossi dalla rete" %deleted)
    exit(1)

if (len(sys.argv) != 2):
    print("Errore! Numero di argomenti al lancio errato!")
    exit(1)
else:
    server_hostname = sys.argv[1]   #risolvere caso in cui si scriva male indirizzo ip

dir_name = "FileOffered"
pathOfferDir = "%s\\%s" %(os.path.dirname(os.path.abspath(__file__)), dir_name)
shortMenu = True

server_port = 80
p2p = Connection.MessagesP2P(socket.gethostname(), random.randint(50000, 52000))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_hostname,int(server_port)))

s_offer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_offer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_offer.bind((p2p.ip, p2p.port))

fileList = []

while True:
    p2p.LoginRequest(s)
    p2p.Read(s)

    if (p2p.sessionId == "0000000000000000"):
        print("Login non è possibile")
    else:
        print("Login effettuato")
        break

if shortMenu:
    action = TDmainmenu()
else:
    action = TDmainmenu2()

if action == 1:
    search_string = TDinputscreen()
    p2p.FindFileRequest(s, search_string)
    p2p.Read(s)
elif action == 2:
    shortMenu = False
    fileList = FilesInDir(pathOfferDir)
    OfferFiles(fileList)

    #apri istanza "server"
    s_offer.listen()
    while True:
        conn, addr = s_offer.accept()
        pid = os.fork()
        if pid == 0:
            md5 = p2p.Read(conn)
            for file in fileList:
                if md5 == file.md5:
                    filePath = "%s\\%s" %(pathOfferDir, file.name)
                    chunks = File.FileChunks(filePath)
                    p2p.SendFile(conn, chunks)
            pid.kill()

elif action == 3 and shortMenu:
    Logout()
elif action == 3:
    md5 = TDsearchFile()
    p2p.RemoveFileRequest(s, md5)
    num_copies = p2p.Read(s)
    print("Nella rete esistono %s copie di %s" %(num_copies, md5))
    fileNames = os.listdir(pathOfferDir)
    if len(fileList) == 0:
        shortMenu = True
        #chiudi istanza "sever"
        #conn.close()
elif action == 4 and not shortMenu:
    Logout()