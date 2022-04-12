from ORM import Query
from Connection import MessagesServer, File
from FrontEnd import DisplayEvents, LogCompiler
import os
import socket
import random

def Login(ip, porta, log):
    if Query.PeerRegistrato(ip, porta):
        sessionID = '0000000000000000'
        log.AddLog("Errore! Il peer %s %s era registrato." %(ip, porta))
        return sessionID
    while True:
        sessionID = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))
        if Query.SessionIDpresente(sessionID):
            log.AddLog("Errore! SessionID %s presente nel database. Riprovare..." %sessionID)
        else:
            Query.EffettuaLogin(sessionID,ip, porta)
            log.AddLog("Login di peer %s %s effettuato." %(ip, porta))
            return sessionID

currentPath = os.path.dirname(os.path.abspath(__file__))
log = LogCompiler(currentPath)
log.AddLog("File Server.py mandato in esecuzione.")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 80))
s.listen(10)
log.AddLog("Server in ascolto...")

while True:
    conn, addr = s.accept()
    log.AddLog("Accettata connessione su socket.")
    pid = os.fork()
    if pid == 0:
        try:
            parametri = MessagesServer.Read(s, log)
            messageHeader = parametri[0]
            if messageHeader == "LOGI":
                result = Login(parametri[1], parametri[2], log)
                MessagesServer.LoginAnswer(s, result[1], log)
            elif messageHeader == "ADDF":
                sessionId = parametri[1]
                md5 = parametri[2]
                filename = parametri[3]
                result = Query.QueryADDF(sessionId, md5, filename)
                MessagesServer.AddFileAnswer(s, result, log)
            elif messageHeader == "DELF":
                sessionId = parametri[1]
                md5 = parametri[2]
                result = Query.QueryDELF(parametri[1], parametri[2])
                MessagesServer.RemoveFileAnswer(s, result, log)
            elif messageHeader == "FIND":
                sessionId = parametri[1]
                search_string = parametri[2]
                result = Query.QueryFIND(sessionId, search_string)
                files = []
                for i in range(len(result[0])):
                    f = File(result[0][i], result[1][i][0])
                    for peer in result[2][i]:
                        f.AddOfferingP2P(peer.ip, peer.port)
                    files.append(f)
                MessagesServer.FindFileAnswer(s, files, log)
            elif messageHeader == "RREG":
                result = Query.QueryRREG(parametri[2], parametri[3], parametri[4])
                MessagesServer.DownloadAnswer(s, result, log)
            elif messageHeader == "LOGO":
                sessionID = parametri[1]
                n_fileRimossi = Query.EffettuaLogout(sessionID)
                MessagesServer.LogoutAnswer(s, n_fileRimossi, log)
            conn.close()
            pid.kill()
            log.AddLog("Connessione chiusa.")
        except Exception as error:
            DisplayEvents.FatalError(error, log)