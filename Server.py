from ORM import Query 
from Connection import MessagesServer, MessagesP2P
import os

def login(ip, porta):
    if(Query.PeerRegistrato(ip, porta)):
        sessionID = '0000000000000000'
        return False, sessionID
    while(True):
        sessionID = os.random(16)
        if(not Query.SessionIDpresente(sessionID)):   
            Query.EffettuaLogin(sessionID,ip, porta)
            return True, sessionID

def logout(sessionID): 
    n_fileRimossi=Query.EffettuaLogout(sessionID)
    return n_fileRimossi

def aggiungiFile(sessionId, md5, filename):
    result = MessagesServer.QueryADDF(sessionId, md5, filename)
    return result

def rimuoviFile(sessionId, md5):
    result = MessagesServer.QueryDELF(sessionId, md5)
    return result

def researchFile(sessionId, search_string):
    result = MessagesServer.QueryFIND(sessionId, search_string)
    return result

parametri = MessagesServer.Read(s)
messageHeader = parametri[0]
if messageHeader == "LOGI":
    result = login(parametri[1], parametri[2])
    MessagesServer.LoginAnswer(s, result[1])
elif messageHeader == "ADDF":
    result = aggiungiFile(parametri[1], parametri[2], parametri[3])
    MessagesServer.AddFileAnswer(s, result)
elif messageHeader == "DELF":
    result = MessagesServer.QueryDELF(parametri[1], parametri[2])
    MessagesServer.RemoveFileAnswer(s, result)
elif messageHeader == "FIND":
    result = MessagesServer.QueryFIND(parametri[1], parametri[2])
    files =[]
    for i in range(0, len(result[0])):
        f = File(result[0][i],result[1][i],result[2][i])
        files.append(f)
    MessagesServer.FindFileAnswer(s, files)
elif messageHeader == "RREG":
    result = MessagesServer.QueryRREG(parametri[2], parametri[3], parametri[4])
    MessagesServer.DownloadAnswer(s, result)
elif messageHeader == "LOGO":
    result = logout(parametri[1])
    MessagesServer.LogoutAnswer(s,result)