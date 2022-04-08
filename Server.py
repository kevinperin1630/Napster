from ORM import Query
from Connection import MessagesServer, MessagesP2P, File
from FrontEnd import DisplayEvents
import os
import socket
import random

def Login(ip, porta):
    if Query.PeerRegistrato(ip, porta):
        sessionID = '0000000000000000'
        return sessionID
    while True:
        sessionID = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))
        if(not Query.SessionIDpresente(sessionID)):   
            Query.EffettuaLogin(sessionID,ip, porta)
            return sessionID

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 80))
s.listen(10)

while True:
    conn, addr = s.accept()
    pid = os.fork()
    if pid==0:
        try:
            parametri = MessagesServer.Read(s)
            messageHeader = parametri[0]
            if messageHeader == "LOGI":
                result = Login(parametri[1], parametri[2])
                MessagesServer.LoginAnswer(s, result[1])
            elif messageHeader == "ADDF":
                sessionId = parametri[1]
                md5 = parametri[2]
                filename = parametri[3]
                result = Query.QueryADDF(sessionId, md5, filename)
                MessagesServer.AddFileAnswer(s, result)
            elif messageHeader == "DELF":
                sessionId = parametri[1]
                md5 = parametri[2]
                result = Query.QueryDELF(parametri[1], parametri[2])
                MessagesServer.RemoveFileAnswer(s, result)
            elif messageHeader == "FIND":
                sessionId = parametri[1]
                search_string = parametri[2]
                result = Query.QueryFIND(sessionId, search_string)
                files =[]
                for i in range(0, len(result[0])):
                    f = File(result[0][i],result[1][i],result[2][i])
                    files.append(f)
                MessagesServer.FindFileAnswer(s, files)
            elif messageHeader == "RREG":
                result = Query.QueryRREG(parametri[2], parametri[3], parametri[4])
                MessagesServer.DownloadAnswer(s, result)
            elif messageHeader == "LOGO":
                sessionID = parametri[1]
                n_fileRimossi = Query.EffettuaLogout(sessionID)
                MessagesServer.LogoutAnswer(s, n_fileRimossi)
            conn.close()
            pid.kill()
        except Exception as error:
            DisplayEvents.FatalError(error)