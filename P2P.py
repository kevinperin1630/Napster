from FrontEnd import Menu, DisplayEvents, LogCompiler
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
    try:
        for file in fileList:
            p2p.AddFileRequest(file.md5, file.name, log)
            num_copies = p2p.Read(s, log)
            print("Nella rete esistono %s copie di %s" %(num_copies, file.md5))
            log.AddLog("Offerto file %s" %file.md5)
            log.AddLog("Nella rete esistono %s copie di %s" %(num_copies, file.md5))
    except Exception as error:
        DisplayEvents.FatalError(error, log)

def Logout():
    try:
        p2p.LogoutRequest(s, log)
        deleted = p2p.Read(s, log)
        s.close()
        print("Logout. %e file rimossi dalla rete." %deleted)
        log.AddLog("Logout. %e file rimossi dalla rete." %deleted)
        exit(1)
    except Exception as error:
        DisplayEvents.FatalError(error, log)

def ChildAction(s_offer):
    s_offer.listen(10)
    log.AddLog("Figlio offerente in ascolto...")
    while True:
        conn, addr = s_offer.accept()
        log.AddLog("Accettata connessione su socket figlio.")
        pid1 = os.fork()
        if pid1 == 0:
            try:
                md5 = p2p.Read(conn, log)
                fileList = FilesInDir(pathOfferDir)
                for file in fileList:
                    if md5 == file.md5:
                        filePath = "%s\\%s" %(pathOfferDir, file.name)
                        with open(filePath, "rb") as f:
                            num_chunk = 0
                            data = []
                            while True:
                                buffer = f.read(4096)
                                if not buffer: 
                                    break
                                data.append(buffer)
                                num_chunk += 1
                            p2p.SendFile(conn, num_chunk, buffer, log)
            except Exception as error:
                DisplayEvents.FatalError(error, log)
            pid1.kill()

def Download(file_wanted):
    with open(file_wanted.nome, 'a') as f:
        try:
            num_chunk, data = p2p.Read(s_download, log)
            for i in range(num_chunk):
                f.write(data[i])
            log.AddLog("File scaricato.")
        except Exception as error:
            DisplayEvents.FatalError(error, log)

currentPath = os.path.dirname(os.path.abspath(__file__))
log = LogCompiler(currentPath)
log.AddLog("File P2P.py mandato in esecuzione.")

if (len(sys.argv) != 2):
    print("Errore! Numero di argomenti al lancio errato!")
    log.AddLog("Errore! Numero di argomenti al lancio errato!")
    exit(1)
else:
    hostname = sys.argv[1]
    log.AddLog("IP server in input: %s" %hostname)
    if Menu.CheckIp(hostname):
        server_hostname = hostname
    else:
        print("Errore! Indirizzo IP del server invalido!")
        log.AddLog("Errore! Indirizzo IP del server invalido!")
        exit(1)

dir_name = "FileOffered"
pathOfferDir = "%s\\%s" %(currentPath, dir_name)
shortMenu = True

server_port = 80

p2p_ip = socket.gethostbyname(socket.gethostname())
p2p_port = random.randint(50000, 52000)

p2p = MessagesP2P(p2p_ip, p2p_port)
log.AddLog("Peer -> Ip %s ; porta %s" %(p2p_ip, p2p_port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_hostname, int(server_port)))
log.AddLog("Connessione su socket server.")

s_offer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_offer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_offer.bind((p2p.ip, p2p.port))
log.AddLog("Bind su socket download.")

pid = os.fork()
if pid == 0:
    ChildAction(s_offer)

fileList = []

while True:
    try:
        p2p.LoginRequest(s, log)
        p2p.Read(s, log)

        if (p2p.sessionId == "0000000000000000"):
            print("Login non e' possibile...")
            log.AddLog("SessionID: %s. Login non e' possibile." %p2p.sessionId)
        else:
            print("Login effettuato.")
            log.AddLog("SessionID: %s. Login effettuato." %p2p.sessionId)
            break
    except Exception as error:
        DisplayEvents.FatalError(error, log)

if shortMenu:
    action = Menu.ShortMenu()
    log.AddLog("Selezionata opzione %s SHORT MENU." %action)
else:
    action = Menu.LongMenu()
    log.AddLog("Selezionata opzione %s LONG MENU." %action)

if action == 1:
    try:
        search_string = Menu.SearchString()
        log.AddLog("Stringa di ricerca: %s" %search_string)
        p2p.FindFileRequest(s, search_string, log)
        num_found, fileList = p2p.Read(s, log)
        if num_found != 0:
            file_wanted, p2p_hostname, p2p_port = Menu.SearchResult(fileList)
            nameError = False
            md5Error = False
            fileList = FilesInDir()
            for f in fileList:
                if file_wanted.nome == f.nome:
                    nameError = True
                elif file_wanted.md5 == f.md5:
                    md5Error = True
            if not nameError and not md5Error:
                s_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_download.connect((p2p_hostname, int(p2p_port)))
                log.AddLog("Connessione su socket peer offerente.")

                p2p.RetriveFileRequest(s_download, file_wanted.md5, log)
                Download(file_wanted)
                s_download.close()
            elif nameError:
                print("Nella cartella %s esiste un file di nome %s" %(dir_name, file_wanted.nome))
                log.AddLog("Errore! Nome file esiste nella cartella.")
            elif md5Error:
                print("Nella cartella %s esiste il file desiderato" %dir_name)
                log.AddLog("Errore! Un file con lo stesso contenuto esiste nella cartella.")
        else:
            print("La ricerca non ha prodotto risultati.")
            log.AddLog("La ricerca non ha prodotto risultati.")
    except Exception as error:
        DisplayEvents.FatalError(error, log)

elif action == 2:
    shortMenu = False
    fileList = FilesInDir(pathOfferDir)
    OfferFiles(fileList)

elif action == 3 and shortMenu:
    Logout()

elif action == 3:
    try:
        md5 = Menu.SelectFile(fileList)
        p2p.RemoveFileRequest(s, md5, log)
        num_copies = p2p.Read(s, log)
        print("Nella rete esistono %s copie di %s" %(num_copies, md5))
        log.AddLog("Terminata condivisione di %s" %md5)
        log.AddLog("Nella rete esistono %s copie di %s" %(num_copies, md5))
        for i in range(len(fileList)):
            if fileList[i].md5 == md5:
                fileList.pop(i)
                break
        if len(fileList) == 0:
            shortMenu = True
            log.AddLog("Questo peer non offre alcun file.")
    except Exception as error:
        DisplayEvents.FatalError(error, log)

elif action == 4 and not shortMenu:
    pid.kill()
    Logout()