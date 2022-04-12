import hashlib

class MessagesP2P:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionId = "0000000000000000"

    def LoginRequest(self, s, log):
        ip = self.ip
        ip = Messages.FillIP(ip, 15)
        packet = "LOGI%s%s" %(ip, self.port)
        s.send(packet.encode())
        log.AddLog("Invio richiesta di login (LOGI)")

    def AddFileRequest(self, s, md5, filename, log):
        filename = Messages.Fill(filename, 100, '|')
        packet = "ADDF%s%s%s" %(self.sessionId, md5, filename)
        s.send(packet.encode())
        log.AddLog("Invio richiesta di aggiunta file (ADDF)")

    def RemoveFileRequest(self, s, md5, log):
        packet = "DELF%s%s" %(self.sessionId, md5)
        s.send(packet.encode())
        log.AddLog("Invio richiesta di rimozione file (DELF)")

    def FindFileRequest(self, s, search_string, log):
        search_string = Messages.Fill(search_string, 20, '|')
        packet = "FIND%s%s" %(self.sessionId, search_string)
        s.send(packet.encode())
        log.AddLog("Invio stringa di ricerca (FIND)")

    def RetriveFileRequest(self, s, md5, log):
        packet = "RETR%s" %md5
        s.send(packet.encode())
        log.AddLog("Invio richiesta di download (RETR)")

    def LogoutRequest(self, s, log):
        packet = "LOGO%s" %self.sessionId
        s.send(packet.encode())
        log.AddLog("Invio richiesta di logout (LOGO)")

    def SendFile(self, s, chunk_num, data, log):
        chunk_num = str(chunk_num)
        chunk_num = Messages.Fill(chunk_num, 6, '0')
        packet = "ARET%s" %chunk_num
        for chunk in data:
            len_chunk = str(len(chunk))
            len_chunk = Messages.Fill(len_chunk, 5, '0')
            packet += "%s%s" %(len_chunk, chunk)
        s.send(packet.encode())
        log.AddLog("Invio dati del file (ARET)")

    def RegisterRequest(self, s, md5, ip_p2p, port_p2p, log):
        ip_p2p = Messages.FillIP(ip_p2p, 15)
        port_p2p = str(port_p2p)
        port_p2p = Messages.Fill(port_p2p, 5, '0')
        packet = "RREG%s%s%s%s" %(self.sessionId, md5, ip_p2p, port_p2p)
        s.send(packet.encode())
        log.AddLog("Invio dati per registrazione download avvenuto (RREG)")

    def Read(self, s, log):
        buffer = Messages.ReadBuffer(s)
        messageHeader = buffer[0:4]
        log.AddLog("Ricezione pacchetto %s" %messageHeader)
        if messageHeader == "ALGI":
            self.sessionId = buffer[4:19]
        elif messageHeader == "AADD" or messageHeader == "ADEL" or messageHeader == "ALGO":
            num_copies = Messages.DeFill(buffer[4:7], '0')
            return int(num_copies)
        elif messageHeader == "AFIN":
            result = []
            num_found = Messages.DeFill(buffer[4:7], '0')
            field = 7
            for i1 in range (num_found):
                md5 = buffer[field:field + 32]
                field += 32
                filename = Messages.DeFill(buffer[field:field + 100], '|')
                field += 100
                file = File(md5, filename)
                num_offering = Messages.DeFill(buffer[field:field + 3], '0')
                field += 3
                for i2 in range(num_offering):
                    ip = Messages.DeFillIP(buffer[field:field + 15])
                    field += 15
                    port = Messages.DeFill(buffer[field:field + 5], '0')
                    port = int(port)
                    field += 5
                    file.AddOfferingP2P(ip, port)
                result.append(file)
            return int(num_found), result
        elif messageHeader == "ARET":
            num_chunk = int(Messages.DeFill(buffer[4:10], '0'))
            field = 10
            data = []
            for i in range(num_chunk):
                len_chunk = int(Messages.DeFill(buffer[field:field+5], '0'))
                field += 5
                chunk = Messages.DeFill(buffer[field:field+len_chunk], '0')
                data.append(chunk)
                field += len_chunk
            return num_chunk, data
        elif messageHeader == "RETR":
            md5 = buffer[4:36]
            return md5
        elif messageHeader == "ARRE":
            num_download = Messages.DeFill(buffer[4:9], '0')
            return int(num_download)
        elif messageHeader == "ERRO":
            raise Exception("Il destinatario ha risposto con un messaggio di errore")
        else:
            Messages.SendError(s)
            log.AddLog("Pacchetto non riconosciuto. Invio risposta: messaggio di errore (ERRO)")

class MessagesServer:
    @staticmethod
    def LoginAnswer(s, sessionId, log):
        packet = "ALGI%s" %sessionId
        s.send(packet.encode())
        log.AddLog("Invio risposta a login (ALGI)")

    @staticmethod
    def AddFileAnswer(s, num_copies, log):
        num_copies = str(num_copies)
        num_copies = Messages.Fill(num_copies, 3, '0')
        packet = "AADD%s" %num_copies
        s.send(packet.encode())
        log.AddLog("Invio risposta ad aggiunta file (AADD)")

    @staticmethod
    def RemoveFileAnswer(s, num_copies, log):
        num_copies = str(num_copies)
        num_copies = Messages.Fill(num_copies, 3, '0')
        packet = "ADEL%s" %num_copies
        s.send(packet.encode())
        log.AddLog("Invio risposta a rimozione file (ADEL)")

    @staticmethod
    def FindFileAnswer(s, files, log):
        num_result = str(len(files))
        num_result = Messages.Fill(num_result, 3, '0')
        packet = "AFIN%s" %num_result
        for f in files:
            md5 = f.md5
            nome = f.nome
            num_copies = str(len(f.peers))
            nome = Messages.Fill(nome, 100, '|')
            num_copies = Messages.Fill(num_copies, 3, '0')
            packet += md5
            packet += nome
            packet += num_copies
        s.send(packet.encode())
        log.AddLog("Invio risultati ricerca (AFIN)")

    @staticmethod
    def LogoutAnswer(s, num_files, log):
        num_files = str(num_files)
        num_files = Messages.Fill(num_files, 3, '0')
        packet = "ALGO%s" %num_files
        s.send(packet.encode())
        log.AddLog("Invio risposta a logout (ALGO)")

    @staticmethod
    def DownloadAnswer(s, num_download, log):
        num_download = str(num_download)
        num_download = Messages.Fill(num_download, 5, '0')
        packet = "ARRE%s" %num_download
        s.send(packet.encode())
        log.AddLog("Invio statistica download (ARRE)")

    @staticmethod
    def Read(s, log):
        buffer = Messages.ReadBuffer(s)
        messageHeader = buffer[0:4]
        log.AddLog("Ricezione pacchetto %s" %messageHeader)
        if messageHeader == "LOGI":
            ip = Messages.DeFillIP(buffer[4:19])
            port = Messages.DeFill(buffer[19:24], '0')
            return messageHeader, ip, int(port)
        elif messageHeader == "ADDF":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            filename = Messages.DeFill(buffer[51:151], '|')
            return messageHeader, sessionId, md5, filename
        elif messageHeader == "DELF":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            return messageHeader, sessionId, md5
        elif messageHeader == "FIND":
            sessionId = buffer[4:19]
            search_string = Messages.DeFill(buffer[19:39], '|')
            return messageHeader, sessionId, search_string
        elif messageHeader == "RREG":
            sessionId = buffer[4:19]
            md5 = buffer[19:51]
            ip_p2p = Messages.DeFillIP(buffer[51:66])
            port_p2p = Messages.DeFill(buffer[66:71], '0')
            return messageHeader, sessionId, md5, ip_p2p, int(port_p2p)
        elif messageHeader == "LOGO":
            sessionId = buffer[4:19]
            return messageHeader, sessionId
        elif messageHeader == "ERRO":
            raise Exception("Il destinatario ha risposto con un messaggio di errore")
        else:
            Messages.SendError(s)
            log.AddLog("Pacchetto non riconosciuto. Invio risposta: messaggio di errore (ERRO)")


class Messages:
    @staticmethod
    def SendError(s):
        packet = "ERRO"
        s.send(packet.encode())

    @staticmethod
    def ReadBuffer(s):
        buffer = ""
        while True:
            part = s.recv(4096).decode()
            if not part:
                break
            buffer += part
        return buffer

    @staticmethod
    def Fill(string, dim, pad):
        if (len(string) < dim):
            for i in range(dim - len(string)):
                string = pad + string
        return string

    @staticmethod
    def DeFill(string, pad):
        for char in string:
            if char == pad:
                string = string[1:]
            else:
                break
        return string

    @staticmethod
    def FillIP(ip):
        fullIP = ''
        fields = ip.split('.')
        for f in fields:
            f = Messages.Fill(f, 3, '0')
            fullIP += "%s." %f
        fullIP = fullIP[:-1]
        return fullIP

    @staticmethod
    def DeFillIP(fullIp):
        ip = ''
        fields = fullIp.split('.')
        for f in fields:
            f = Messages.DeFill(f, '0')
            ip += "%s." %f
        ip = ip[:-1]
        return ip

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