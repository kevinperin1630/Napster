import FrontEnd
from Connection import MessagesP2P, File
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
    s.close()
    print("Logout. %e file rimossi dalla rete" %deleted)
    exit(1)

def ChildAction(s_offer):
    s_offer.listen()
    while True:
        conn, addr = s_offer.accept()
        pid1 = os.fork()
        if pid1 == 0:
            md5 = p2p.Read(conn)
            fileList = FilesInDir(pathOfferDir)
            for file in fileList:
                if md5 == file.md5:
                    filePath = "%s\\%s" %(pathOfferDir, file.name)
                    with open(filePath, "rb") as f:
                        num_chunk = 0
                        while True:
                            buffer = f.read(4096)
                            if not buffer: 
                                break
                            num_chunk += 1
                            p2p.SendFile(conn, num_chunk, buffer)
            pid1.kill()

def Download(file_wanted):
    with open(file_wanted.nome, 'a') as f:
        while True:
            chunk = p2p.Read(s_download)
            f.write(chunk[0])
            if len(chunk[0]) < 4096:
                break

if (len(sys.argv) != 2):
    print("Errore! Numero di argomenti al lancio errato!")
    exit(1)
else:
    hostname = sys.argv[1]
    if FrontEnd.CheckIp(hostname):
        server_hostname = hostname
    else:
        print("Errore! Indirizzo IP invalido")
        exit(1)

dir_name = "FileOffered"
pathOfferDir = "%s\\%s" %(os.path.dirname(os.path.abspath(__file__)), dir_name)
shortMenu = True

server_port = 80
p2p = MessagesP2P(socket.gethostname(), random.randint(50000, 52000))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_hostname, int(server_port)))

s_offer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_offer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_offer.bind((p2p.ip, p2p.port))

pid = os.fork()
if pid == 0:
    ChildAction(s_offer)

fileList = []

while True:
    p2p.LoginRequest(s)
    p2p.Read(s)

    if (p2p.sessionId == "0000000000000000"):
        print("Login non e' possibile")
    else:
        print("Login effettuato")
        break

if shortMenu:
    action = FrontEnd.ShortMenu()
else:
    action = FrontEnd.LongMenu()

if action == 1:
    search_string = FrontEnd.SearchString()
    p2p.FindFileRequest(s, search_string)
    num_found, fileList = p2p.Read(s)
    file_wanted, p2p_hostname, p2p_port = FrontEnd.SearchResult()

    s_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_download.connect((p2p_hostname, int(p2p_port)))

    p2p.RetriveFileRequest(s_download, file_wanted.md5)
    Download(file_wanted)
    s_download.close()

elif action == 2:
    shortMenu = False
    fileList = FilesInDir(pathOfferDir)
    OfferFiles(fileList)

elif action == 3 and shortMenu:
    Logout()

elif action == 3:
    md5 = FrontEnd.SelectFile(fileList)
    p2p.RemoveFileRequest(s, md5)
    num_copies = p2p.Read(s)
    print("Nella rete esistono %s copie di %s" %(num_copies, md5))
    fileNames = os.listdir(pathOfferDir)
    if len(fileNames) == 0:
        shortMenu = True

elif action == 4 and not shortMenu:
    pid.kill()
    Logout()