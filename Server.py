from ORM import Query 
from Connection import MessagesServer, File
import os

def login(ip, porta):
    if(Query.PeerRegistrato(ip, porta)):
        sessionID = '0000000000000000'
        return False, sessionID
    while(True):
        sessionID = os.random(16)
        if(not Query.SessionIDpresente(sessionID)):    
            return True, sessionID

def logout(sessionID): 
    n_fileRimossi=Query.EffettuaLogout(sessionID)
    return n_fileRimossi


risposta = MessagesServer.Read(s)
messageHeader = risposta[0]
if messageHeader == "LOGI":
    result = login(risposta[1], risposta[2])
    MessagesServer.LoginAnswer(s, result[1])
elif messageHeader == "ADDF":
    result = logout(sessionID)
    MessagesServer.LogoutAnswer(s,result)
elif messageHeader == "DELF":
elif messageHeader == "FIND":
elif messageHeader == "RREG":
elif messageHeader == "LOGO":
    result = 
MessagesServer.LoginAnswer(s, sessionId):


def disponibilitaFile(md5):
    presente = False
    conn = psycopg2.connect("host=localhost dbname=db")
    query="SELECT COUNT(*) FROM P2P_File where md5 = %s" %(md5)
    cur = conn.cursor()
    cur.execute(query)
    if(cur.rowcount > 0):
        presente = True
    cur.close()
    conn.close()
    return presente
   


def aggiuntaFile(nome):
    
def rimozioneFile():
def ricercaPerNome(nome):
    conn = psycopg2.connect("host=localhost dbname=db")
    cur = conn.cursor()
    query = "SELECT md5,COUNT(md5) FROM P2P_File where nome = {%s} GROUP by md5" %nome
    cur.execute(query)
    mobile_records = cur.fetchall()
    for row in mobile_records:
        print("md5 = ", row[0], )
        print("copy = ", row[1], "\n")