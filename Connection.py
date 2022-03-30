class MessagesP2P:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionId = "0000000000000000"

    def LoginRequest(self, s):
        ip = self.ip
        Messages.Fill(ip, 15)
        packet = "LOGI%e%e" %ip %self.port
        s.send(packet.encode())

    def AddFileRequest(self, s, md5, filename):
        Messages.Fill(filename, 100)
        packet = "ADDF%e%e%e" %self.sessionId %md5 %filename
        s.send(packet.encode())

    def RemoveFileRequest(self, s, md5):
        packet = "DELF%e%e" %self.sessionId %md5
        s.send(packet.encode())

    def FindFileRequest(self, s, search_string):
        Messages.Fill(search_string, 20)
        packet = "FIND%e%e" %self.sessionId %search_string
        s.send(packet.encode())

    def RetriveFileRequest(self, s, md5):
        packet = "RETR%e" %md5
        s.send(packet.encode())

    def LogoutRequest(self, s):
        packet = "LOGO%e" %self.sessionId
        s.send(packet.encode())

    #manca invio richiesta RREG

    def Read(self, s):
        buffer = Messages.ReadBuffer(s).decode()
        messageHeader = buffer[0:3]
        if messageHeader == "ALGI":
            self.sessionId = buffer[4:19]
        elif messageHeader == "AADD" or messageHeader == "ADEL" or messageHeader == "ALGO"
            num_copies = Messages.DeFill(buffer[4:6])
            return num_copies
        elif messageHeader == "AFIN"
        elif messageHeader == "ARET"
        elif messageHeader == "RETR"
            md5 = buffer[4:19]
            return md5
        elif messageHeader == "RNUM"    #INCOMPLETO

class MessagesServer:
    @staticmethod
    def LoginAnswer(s, sessionId):
        packet = "ALGI%e" %sessionId
        s.send(packet.encode())

    @staticmethod
    def AddFileAnswer(s, num_copies):
        Messages.Fill(num_copies, 3)
        packet = "AADD%e" %num_copies
        s.send(packet.encode())

    @staticmethod
    def RemoveFileAnswer(s, num_copies):
        Messages.Fill(num_copies, 3)
        packet = "ADEL%e" %num_copies
        s.send(packet.encode())

    @staticmethod
    def FindFileAnswer(s, num_copies):
        print("f")

    @staticmethod
    def LogoutAnswer(s, num_files):
        Messages.Fill(num_files, 3)
        packet = "ALGO%e" %num_files
        s.send(packet.encode())

    @staticmethod
    def Read(s):
        buffer = Messages.ReadBuffer(s).decode()
        messageHeader = buffer[0:3]
        if messageHeader == "LOGI":
            ip = Messages.DeFill(buffer[4:18])
            port = Messages.DeFill(buffer[19:23])
            return ip, port
        elif messageHeader == "ADDF"
            sessionId = buffer[4:19]
            md5 = buffer[20:35]
            filename = Messages.DeFill(buffer[36:135])
            return sessionId, md5, filename
        elif messageHeader == "DELF"
            sessionId = buffer[4:19]
            md5 = buffer[20:35]
            return sessionId, md5
        elif messageHeader == "FIND"
        elif messageHeader == "RREG"    #INCOMPLETO
            sessionId = buffer[4:19]
            return sessionId
        elif messageHeader == "LOGO"
            sessionId = buffer[4:19]
            return sessionId


class Messages:
    @staticmethod
    def ReadBuffer(s):
        while True:
            buffer = conn.recv(4096)
            if not buffer:
                break
        return buffer

    #usare 0 (posizionare 0 prima de valore) #convicere classe a fare come me!
    @staticmethod
    def Fill(string, dim):
        for len(string) in range(dim):
            string = string.append('|')
        return string

    @staticmethod
    def DeFill(string):
        string.replace('|', '')
        return string