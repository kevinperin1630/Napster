from Connection import MessagesP2P
import psycopg2

class Query:
    conn_string = "user=postgres password=tpsi host=localhost dbname=db"

    @staticmethod
    def SessionIDpresente(sessionID):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM P2P WHERE sessionID = '%s'" %sessionID
        cur.execute(query)
        cur.fetchall()
        righe = cur.rowcount
        cur.close()
        conn.close()
        if(righe == 0):
               return False
        return True

    @staticmethod
    def PeerRegistrato(ip, porta):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM P2P WHERE ip = '%s' AND porta = '%s'" %(ip, porta)
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
            conn = psycopg2.connect(Query.conn_string)
            cur = conn.cursor()
            query = "INSERT INTO P2P (sessionID, ip, porta) VALUES ('{%s}','{%s}','{%s}')" %(sessionID, ip, porta)
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
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        #query = "SELECT * FROM P2P_File where sessionID = %s" %sessionID
        #cur.execute(query)
        #cur.fetchall()
        #n_fileRimossi = cur.rowcount
        query = "DELETE FROM P2P_File WHERE sessionID = '%s'" %sessionID
        cur.execute(query)
        n_fileRimossi = cur.rowcount
        conn.commit()
        query = "DELETE FROM P2P WHERE sessionID = '%s'" %sessionID
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return n_fileRimossi
        
    @staticmethod
    def QueryADDF(sessionId, md5, filename):
        try:
            conn = psycopg2.connect(Query.conn_string)
            cur = conn.cursor()
            query = "INSERT INTO File (md5) VALUES ('{%s}')" %md5
            cur.execute(query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            if not "duplicate key value" in str(error):
                if conn:
                    cur.close()
                    conn.close()
                return 0
        conn.rollback()
        query = "INSERT INTO P2P_File (md5, sessionID, nome) VALUES ('{%s}','{%s}','{%s}')" %(md5, sessionId, filename)
        cur.execute(query)
        conn.commit()
        query = "SELECT * FROM P2P_File WHERE md5 = '%s'" %md5
        cur.execute(query)
        cur.fetchall()
        copie = cur.rowcount
        cur.close()
        conn.close()
        return copie

    @staticmethod
    def QueryDELF(sessionId, md5):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "DELETE FROM P2P_File WHERE sessionID = '%s' AND md5 = '%s'" %(sessionId, md5)
        cur.execute(query)
        conn.commit()  
        cur.close()
        conn.close()
        n_filePresenti = Query.ControlloFileOfferto(md5)
        if(n_filePresenti == 0):
            conn = psycopg2.connect(Query.conn_string)
            cur = conn.cursor()
            query = "DELETE FROM File WHERE md5 = '%s'" %md5
            cur.execute(query)
            conn.commit()  
            cur.close()
            conn.close()
        return n_filePresenti

    @staticmethod
    def QueryFIND(sessionId, search_string):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT DISTINCT md5 FROM P2P_File WHERE nome LIKE '%s%s%s'" %('%', search_string, '%')
        cur.execute(query)
        md5Array = cur.fetchall()
        peersLList = []
        filenameLList = []
        for md5 in md5Array:
            query = "SELECT ip, porta FROM P2P JOIN P2P_File ON P2P_File.sessionID = P2P.sessionID AND P2P_File.md5 = '%s' AND NOT P2P.sessionID = '%s' " %(md5, sessionId)
            cur.execute(query)
            ipPorta = cur.fetchall()
            peers = []
            for row in ipPorta:
                peer = MessagesP2P(row[0], row[1])
                peers.append(peer)
            peersLList.append(peers)
            query = "SELECT DISTINCT nome FROM P2P_File WHERE P2P_File.md5 = '%s'" %(md5)
            cur.execute(query)
            filename = cur.fetchone()
            filenameLList.append(filename)
            cur.close()
            conn.close()         
        return md5Array, filenameLList, peersLList

    @staticmethod
    def QueryRREG(md5, ip_p2p, port_p2p):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT sessionID FROM P2P WHERE ip_p2p = '%s' AND port_p2p = '%s'" %(ip_p2p, port_p2p)
        cur.execute(query)
        sessionID = cur.fetchone()
        query = "UPDATE P2P_File SET n_download = n_download + 1 WHERE sessionID = '%s' AND md5 = '%s'" %(sessionID, md5)
        cur.execute(query)
        conn.commit()
        query = "SELECT n_download FROM P2P_File WHERE sessionID = '%s' AND md5 = '%s'" %(sessionID, md5)
        cur.execute(query)
        n_download = cur.fetchone()
        cur.close()
        conn.close()
        return n_download

    
    @staticmethod
    def ControlloFileOfferto(md5):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM P2P_File WHERE md5 = '%s'" %md5
        cur.execute(query)
        cur.fetchall()
        n_copieRimaste = cur.rowcount
        cur.close()
        conn.close()
        return n_copieRimaste