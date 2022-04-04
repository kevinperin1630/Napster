import hashlib

class MessagesP2P:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionId = "0000000000000000"

    def LoginRequest(self, s):
        ip = self.ip
        ip = Messages.Fill(ip, 15)
        packet = "LOGI%s%s" %(ip, self.port)
        s.send(packet.encode())

    def AddFileRequest(self, s, md5, filename):
        filename = Messages.Fill(filename, 100)
        packet = "ADDF%s%s%s" %(self.sessionId, md5, filename)
        s.send(packet.encode())

    def RemoveFileRequest(self, s, md5):
        packet = "DELF%s%s" %(self.sessionId, md5)
        s.send(packet.encode())

    def FindFileRequest(self, s, search_string):
        search_string = Messages.Fill(search_string, 20)
        packet = "FIND%s%s" %(self.sessionId, search_string)
        s.send(packet.encode())

    def RetriveFileRequest(self, s, md5):
        packet = "RETR%s" %md5
        s.send(packet.encode())

    def LogoutRequest(self, s):
        packet = "LOGO%s" %self.sessionId
        s.send(packet.encode())

    def SendFile(self, s, chunk_id, chunk):
        len_chunk = len(chunk)
        chunk_id = Messages.Fill(chunk_id, 6)
        len_chunk = Messages.Fill(len_chunk)
        packet = "ARET%s%s%s" %(chunk_id, len_chunk, chunk)
        s.send(packet.encode())

    def RegisterRequest(self, s, md5, ip_p2p, port_p2p):
        ip_p2p = Messages.Fill(ip_p2p, 15)
        port_p2p = Messages.Fill(port_p2p, 5)
        packet = "RREG%s%s%s%s" %(self.sessionId, md5, ip_p2p, port_p2p)
        s.send(packet.encode())

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
            len_chunk = Messages.DeFill(buffer[10:15])
            field = int(len_chunk)
            chunk = buffer[15:15 + field]
            return num_chunk, chunk
        elif messageHeader == "RETR":
            md5 = buffer[4:36]
            return md5
        elif messageHeader == "ARRE":
            num_download = Messages.DeFill(buffer[4:9])
            return num_download

class MessagesServer:
    @staticmethod
    def LoginAnswer(s, sessionId):
        packet = "ALGI%s" %sessionId
        s.send(packet.encode())

    @staticmethod
    def AddFileAnswer(s, num_copies):
        num_copies = Messages.Fill(num_copies, 3)
        packet = "AADD%s" %num_copies
        s.send(packet.encode())

    @staticmethod
    def RemoveFileAnswer(s, num_copies):
        num_copies = Messages.Fill(num_copies, 3)
        packet = "ADEL%s" %num_copies
        s.send(packet.encode())

    @staticmethod
    def FindFileAnswer(s, files):
        num_result = len(files)
        num_result = Messages.Fill(num_result, 3)
        packet = "AFIN%s" %num_result
        for f in files:
            md5 = f.md5
            nome = f.nome
            num_copies = len(f.peers)
            nome = Messages.Fill(nome, 100)
            num_copies = Messages.Fill(num_copies, 3)
            packet += md5
            packet += nome
            packet += num_copies
        s.send(packet.encode())

    @staticmethod
    def LogoutAnswer(s, num_files):
        num_files = Messages.Fill(num_files, 3)
        packet = "ALGO%s" %num_files
        s.send(packet.encode())

    @staticmethod
    def DownloadAnswer(s, num_download):
        num_download = Messages.Fill(num_download, 5)
        packet = "ARRE%s" %num_download
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
        elif messageHeader == "RREG":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            ip_p2p = Messages.DeFill(buffer[51:66])
            port_p2p = Messages.DeFill(buffer[66:71])
            return sessionId, md5, ip_p2p, port_p2p
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
                string += '|'
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

    @staticmethod
    def FileData(path):
        with open(path, "rb") as f:
            buffer = f.read()
        return buffer

    @staticmethod 
    def CalculateMD5(buffer):
        md5 = hashlib.md5(buffer).hexdigest()
        return md5