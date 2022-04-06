from fileinput import filename
from hashlib import md5
import psycopg2

class Query:
    @staticmethod
    def SessionIDpresente(sessionID):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "SELECT * FROM P2P where sessionID = %s" %sessionID
        cur.execute(query)
        cur.fetchall()
        righe = cur.rowcount
        cur.close()
        conn.close()
        if(cur.rowcount == 0):
               return False
        return True

    @staticmethod
    def PeerRegistrato(ip, porta):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "SELECT * FROM P2P where ip = %s and porta = %s" %(ip, porta)
        cur.execute(query)
        cur.fetchall()
        righe = cur.rowcount
        cur.close()
        conn.close()
        if(righe == 0):
               return False
        return True

    @staticmethod
    def EffettuaLogin(sessionID,ip, porta):
        try:
            conn = psycopg2.connect("host=localhost dbname=db")
            cur = conn.cursor()
            query = "INSERT INTO P2P (sessionID, ip, porta) VALUES ('{%s}','{%s}','{%s}')" %(sessionID,ip,porta)
            cur.execute(query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into p2p table", error)
        finally:
            if conn:
                cur.close()
                conn.close()

    @staticmethod
    def EffettuaLogout(sessionID):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "SELECT * FROM P2P_File where sessionID = %s" %sessionID
        cur.execute(query)
        cur.fetchall()
        n_fileRimossi = cur.rowcount
        query = "Delete From P2P_File where sessionID = %s" %sessionID
        cur.execute(query)
        conn.commit()
        query = "Delete From P2P where sessionID = %s" %sessionID
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return n_fileRimossi
    @staticmethod
    def QueryADDF(sessionId, md5, filename):
        try:
            conn = psycopg2.connect("host=localhost dbname=db")
            cur = conn.cursor()
            query = "INSERT INTO File (md5) VALUES ('{%s}')" %md5
            cur.execute(query)
            conn.commit()
            query = "INSERT INTO P2P_File (md5, sessionID, nome) VALUES ('{%s}','{%s}','{%s}')" %(md5,sessionId, filename)
            cur.execute(query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into file table", error)
        finally:
            if conn:
                cur.close()
                conn.close()

    @staticmethod
    def QueryDELF(sessionId, md5):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "Select * From P2P_File where sessionID = %s and md5 = %s" %(sessionId,md5)
        cur.execute(query)
        cur.fetchall()
        n_fileRimossi = cur.rowcount
        query = "Delete From P2P_File where sessionID = %s and md5 = %s" %(sessionId,md5)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return n_fileRimossi

    @staticmethod
    def QueryFIND(sessionId, search_string):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "SELECT distinct md5 FROM P2P_File"
        cur.execute(query)
        records=cur.fetchall()
        md5array=[]
        for md5 in records:
            if (search_string in md5):
                md5array.append(md5)
        ipPortaArray=[]
        filenameArray = []
        for md5 in md5array:
            query = "SELECT ip, porta FROM P2P, P2P_File where P2P.sessionID = %s and P2P_File.sessionID = %s" %(sessionId)
            cur.execute(query)
            ipPorta = cur.fetchall()
            ipPortaArray.append(ipPorta)
            query = "SELECT nome FROM File, P2P_File where File.md5 = %s and P2P_File.md5 = %s" %(md5)
            cur.execute(query)
            filename = cur.fetchone()
            filenameArray.append(filename)
            cur.close()
            conn.close()         
        return md5array,filenameArray,ipPortaArray

    @staticmethod
    def QueryRREG(md5, ip_p2p, port_p2p):
        conn = psycopg2.connect("host=localhost dbname=db")
        cur = conn.cursor()
        query = "SELECT sessionID FROM P2P where ip_p2p = %s and port_p2p = %s" %(ip_p2p,port_p2p)
        cur.execute(query)
        sessionID=cur.fetchone()
        query = "UPDATE P2P_File SET n_download = (n_download+1) where sessionID = %s and md5 = %s" %(sessionID,md5)
        cur.execute(query)
        conn.commit()
        query = "Select n_download FROM P2P_File where sessionID = %s and md5 = %s" %(sessionID,md5)
        cur.execute(query)
        n_download=cur.fetchone()
        cur.close()
        conn.close()
        return n_download