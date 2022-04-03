from pickle import TRUE
import ORM
import Connection
import psycopg2
import os

def disponibilitaFile(md5):
    presente = False
    conn = psycopg2.connect("host=localhost dbname=db")
    query="SELECT COUNT(*) FROM P2P_File where md5 = %e" %md5
    cur = conn.cursor()
    cur.execute(query)
    if(cur.rowcount > 0):
        presente = True
    cur.close()
    conn.close()
    return presente
   
def login(IP, porta):
    sessionID = os.random(16)
    conn = psycopg2.connect("host=localhost dbname=db")
    cur = conn.cursor()
    query = "SELECT sessionID FROM P2P where sessionID = %e" %sessionID
    cur.execute(query)
    cur.fetchall()
    if(cur.rowcount == 0):
        query = "INSERT INTO P2P (sessionID, IP, porta) VALUES ('{%e}','{%e}','{%e}')" %sessionID %IP %porta
        cur.execute(query)
        return True, sessionID
    sessionID = '0000000000000000'
    return False, sessionID

def logout(sessionID): 
    conn = psycopg2.connect("host=localhost dbname=db")
    cur = conn.cursor()
    query = "Select COUNT(*) FROM P2P_File where sessionID = %e" %sessionID
    cur.execute(query)
    mobile_records = cur.fetchall()
    for row in mobile_records:
        copy = row[0]
    query = "Delete FROM P2P where sessionID = %e" %sessionID
    cur.execute(query)
    cur.fetchall()
    if(cur.rowcount == 0):
        query = "INSERT INTO P2P (sessionID, IP, porta) VALUES ('{%e}','{%e}','{%e}')" %sessionID %IP %porta
        cur.execute(query)
        return True, sessionID
    sessionID = '0000000000000000' 

    
def ricercaPerNome(nome):
    conn = psycopg2.connect("host=localhost dbname=db")
    cur = conn.cursor()
    query = "SELECT md5,COUNT(md5) FROM P2P_File where nome = {%e} GROUP by md5" %nome
    cur.execute(query)
    mobile_records = cur.fetchall()
    for row in mobile_records:
        print("md5 = ", row[0], )
        print("copy = ", row[1], "\n")

