from Connection import MessagesP2P
import psycopg2

class Query:
    conn_string = "user=postgres password=tpsi host=localhost dbname=db"

    @staticmethod
    def SessionIDpresente(sessionID):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM P2P WHERE sessionID = '%s'" %sessionID
        fetched, righe = Query.ExecuteQuery(conn, cur, query, True)
        if conn:
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
        fetched, righe = Query.ExecuteQuery(conn, cur, query, True)
        if conn:
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
            query = "INSERT INTO P2P (sessionID, ip, porta) VALUES ('%s', '%s', '%s')" %(sessionID, ip, porta)
            Query.ExecuteQuery(conn, cur, query, True)
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
        query = "SELECT FROM P2P_File WHERE sessionID = '%s'" %sessionID
        fetched, n_fileRimossi = Query.ExecuteQuery(conn, cur, query, True)
        query = "DELETE FROM P2P_File WHERE sessionID = '%s'" %sessionID
        Query.ExecuteQuery(conn, cur, query, True)
        query = "DELETE FROM P2P WHERE sessionID = '%s'" %sessionID
        Query.ExecuteQuery(conn, cur, query, True)
        if conn:
            cur.close()
            conn.close()
        return n_fileRimossi
        
    @staticmethod
    def QueryADDF(sessionId, md5, filename):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "INSERT INTO File (md5) VALUES ('%s')" %md5
        fetched, num = Query.ExecuteQuery(conn, cur, query, True)
        if num == 0 and conn:
            cur.close()
            conn.close()
            return num
        query = "SELECT * FROM P2P_File WHERE md5 = '%s' AND sessionID = '%s'" %(md5, sessionId)
        fetched, num = Query.ExecuteQuery(conn, cur, query, True)
        if num == 0:
            query = "INSERT INTO P2P_File (md5, sessionID, nome, n_download) VALUES ('%s', '%s', '%s', %s)" %(md5, sessionId, filename, 0)
            Query.ExecuteQuery(conn, cur, query, True)
        query = "SELECT * FROM P2P_File WHERE md5 = '%s'" %md5
        fetched, copie = Query.ExecuteQuery(conn, cur, query, True)
        if conn:
            cur.close()
            conn.close()
        return copie

    @staticmethod
    def QueryDELF(sessionId, md5):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "DELETE FROM P2P_File WHERE sessionID = '%s' AND md5 = '%s'" %(sessionId, md5)
        Query.ExecuteQuery(conn, cur, query, True)
        if conn:
            cur.close()
            conn.close()
        n_filePresenti = Query.ControlloFileOfferto(md5)
        if(n_filePresenti == 0):
            conn = psycopg2.connect(Query.conn_string)
            cur = conn.cursor()
            query = "DELETE FROM File WHERE md5 = '%s'" %md5
            Query.ExecuteQuery(conn, cur, query, True)
            if conn:
                cur.close()
                conn.close()
        return n_filePresenti

    @staticmethod
    def QueryFIND(sessionId, search_string):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT DISTINCT md5 FROM P2P_File WHERE nome LIKE '%s%s%s'" %('%', search_string, '%')
        md5Array, num = Query.ExecuteQuery(conn, cur, query, True)
        peersLList = []
        filenameLList = []
        for md5 in md5Array:
            query = "SELECT ip, porta FROM P2P JOIN P2P_File ON P2P_File.sessionID = P2P.sessionID AND P2P_File.md5 = '%s' AND NOT P2P.sessionID = '%s'" %(md5[0], sessionId)
            ipPorta, num = Query.ExecuteQuery(conn, cur, query, True)
            peers = []
            for row in ipPorta:
                peer = MessagesP2P(row[0], row[1])
                peers.append(peer)
            peersLList.append(peers)
            query = "SELECT DISTINCT nome FROM P2P_File WHERE P2P_File.md5 = '%s'" %(md5)
            filename, num = Query.ExecuteQuery(conn, cur, query, False)
            filenameLList.append(filename)
            if conn:
                cur.close()
                conn.close()         
        return md5Array, filenameLList, peersLList

    @staticmethod
    def QueryRREG(md5, ip_p2p, port_p2p):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT sessionID FROM P2P WHERE ip = '%s' AND porta = '%s'" %(ip_p2p, port_p2p)
        sessionID, num = Query.ExecuteQuery(conn, cur, query, False)
        query = "UPDATE P2P_File SET n_download = n_download + 1 WHERE sessionID = '%s' AND md5 = '%s'" %(sessionID[0], md5)
        Query.ExecuteQuery(conn, cur, query, True)
        query = "SELECT n_download FROM P2P_File WHERE sessionID = '%s' AND md5 = '%s'" %(sessionID[0], md5)
        n_download, num = Query.ExecuteQuery(conn, cur, query, False)
        if conn:
            cur.close()
            conn.close()
        return n_download[0]

    
    @staticmethod
    def ControlloFileOfferto(md5):
        conn = psycopg2.connect(Query.conn_string)
        cur = conn.cursor()
        query = "SELECT * FROM P2P_File WHERE md5 = '%s'" %md5
        fetched, n_copieRimaste = Query.ExecuteQuery(conn, cur, query, True)
        if conn:
            cur.close()
            conn.close()
        return n_copieRimaste

    @staticmethod
    def ExecuteQuery(conn, cur, query, fetchall):
        try:
            cur.execute(query)
        except psycopg2.InterfaceError as e:
            conn = psycopg2.connect(Query.conn_string)
            cur = conn.cursor()
            cur.execute(query)
        except psycopg2.Error as e:
            if "duplicate key value" in str(e):
                conn.rollback()
                cur.execute(query)
            else:
                return False, 0
        finally:
            if not "SELECT" in query:
                conn.commit()
            try:
                if fetchall:
                    return cur.fetchall(), cur.rowcount
                else:
                    return cur.fetchone(), cur.rowcount
            except:
                return False, cur.rowcount
