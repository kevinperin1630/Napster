import hashlib

class MessagesP2P:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionId = "0000000000000000"

    def LoginRequest(self, s):
        ip = self.ip
        Messages.Fill(ip, 15)
        packet = "LOGI%s%s" %(ip, self.port)
        s.send(packet.encode())

    def AddFileRequest(self, s, md5, filename):
        Messages.Fill(filename, 100)
        packet = "ADDF%s%s%s" %(self.sessionId, md5, filename)
        s.send(packet.encode())

    def RemoveFileRequest(self, s, md5):
        packet = "DELF%s%s" %(self.sessionId, md5)
        s.send(packet.encode())

    def FindFileRequest(self, s, search_string):
        Messages.Fill(search_string, 20)
        packet = "FIND%s%s" %(self.sessionId, search_string)
        s.send(packet.encode())

    def RetriveFileRequest(self, s, md5):
        packet = "RETR%s" %md5
        s.send(packet.encode())

    def LogoutRequest(self, s):
        packet = "LOGO%s" %self.sessionId
        s.send(packet.encode())

    def SendFile(self, s, chunks):
        packet = "ARET%s" %len(chunks)
        for chunk in chunks:
            dim_chunk = Messages.Fill(len(chunk), 5)
            packet += dim_chunk
            packet += chunk
        s.send(packet.encode())

    #manca invio richiesta RREG

    def Read(self, s):
        buffer = Messages.ReadBuffer(s)
        messageHeader = buffer[0:4]
        if messageHeader == "ALGI":
            self.sessionId = buffer[4:19]
        elif messageHeader == "AADD" or messageHeader == "ADEL" or messageHeader == "ALGO":
            num_copies = Messages.DeFill(buffer[4:7])
            return num_copies
        elif messageHeader == "AFIN":
            result = []
            num_found = Messages.DeFill(buffer[4:7])
            field = 7
            for i1 in range (num_found):
                md5 = buffer[field:field + 32]
                field += 32
                filename = Messages.DeFill(buffer[field:field + 100])
                field += 100
                file = File(md5, filename)
                num_offering = Messages.DeFill(buffer[field:field + 3])
                field += 3
                for i2 in range(num_offering):
                    ip = Messages.DeFill(buffer[field:field + 15])
                    field += 15
                    port = Messages.DeFill(buffer[field:field + 5])
                    field += 5
                    file.AddOfferingP2P(ip, port)
                result.append(file)
            return num_found, result
        elif messageHeader == "ARET":
            num_chunk = Messages.DeFill(buffer[4:10])
            field = 10
            content = []
            for i1 in range(num_chunk):
                len_chunk = Messages.DeFill(buffer[field:field + 5])
                field += 5
                data = buffer[field:field + len_chunk]
                content.append(data)
                field += len_chunk
            return content
        elif messageHeader == "RETR":
            md5 = buffer[4:36]
            return md5
        elif messageHeader == "RNUM":    #INCOMPLETO
            print("f")

    def CheckIP(self):
        return self.ip
    
    def CheckPort(self):
        return self.port

class MessagesServer:
    @staticmethod
    def LoginAnswer(s, sessionId):
        packet = "ALGI%s" %sessionId
        s.send(packet.encode())

    @staticmethod
    def AddFileAnswer(s, num_copies):
        Messages.Fill(num_copies, 3)
        packet = "AADD%s" %num_copies
        s.send(packet.encode())

    @staticmethod
    def RemoveFileAnswer(s, num_copies):
        Messages.Fill(num_copies, 3)
        packet = "ADEL%s" %num_copies
        s.send(packet.encode())

    @staticmethod
    def FindFileAnswer(s, num_copies):
        print("f")

    @staticmethod
    def LogoutAnswer(s, num_files):
        Messages.Fill(num_files, 3)
        packet = "ALGO%s" %num_files
        s.send(packet.encode())

    @staticmethod
    def Read(s):
        buffer = Messages.ReadBuffer(s)
        messageHeader = buffer[0:4]
        if messageHeader == "LOGI":
            ip = Messages.DeFill(buffer[4:19])
            port = Messages.DeFill(buffer[19:24])
            return ip, port
        elif messageHeader == "ADDF":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            filename = Messages.DeFill(buffer[51:151])
            return sessionId, md5, filename
        elif messageHeader == "DELF":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            return sessionId, md5
        elif messageHeader == "FIND":
            sessionId = buffer[4:19]
            search_string = Messages.DeFill(buffer[19:39])
            return sessionId, search_string
        elif messageHeader == "RREG":    #INCOMPLETO
            sessionId = buffer[4:19]
            return sessionId
        elif messageHeader == "LOGO":
            sessionId = buffer[4:19]
            return sessionId


class Messages:
    @staticmethod
    def ReadBuffer(s):
        buffer = ""
        while True:
            part = s.recv(4096).decode()
            if not part:
                break
            buffer += part
        return buffer

    #usare 0 (posizionare 0 prima de valore) #convicere classe a fare come me!
    @staticmethod
    def Fill(string, dim):
        if (len(string) < dim):
            for i in range(dim - len(string)):
                string = string.append('|')
        return string

    @staticmethod
    def DeFill(string):
        string.replace('|', '')
        return string

class File:
    def __init__(self, md5, nome):
        self.md5 = md5
        self.nome = nome
        self.peers = []

    def AddOfferingP2P(self, ip, port):
        self.peers.append(MessagesP2P(ip, port))

    def CheckPeers(self):
        return self.peers

    @staticmethod
    def FileData(path):
        with open(path, "rb") as f:
            buffer = f.read()
        return buffer

    @staticmethod
    def FileChunks(path):
        chunks = []
        with open(path, "rb") as f:
            while True:
                buffer = f.read(4096)
                if not buffer: 
                    break
                chunks.append(buffer)
        return chunks

    @staticmethod 
    def CalculateMD5(buffer):
        md5 = hashlib.md5(buffer).hexdigest()
        return md5