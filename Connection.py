class MessagesP2P:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionId = "0000000000000000"

    @staticmethod
    def Fill(string, dim):
        while len(string) < dim:
            string = string + '|'
        return string

    def LoginRequest(self, s):
        ip = self.ip
        port = self.port
        self.Fill(ip, 15)
        self.Fill(port, 5)
        packet = "LOGI%e%e" %ip %port
        s.send(packet.encode())

    @staticmethod
    def AddFileRequest():
        print "f"

    @staticmethod
    def RemoveFileRequest():
        print "f"

    @staticmethod
    def FindFileRequest():
        print "f"

    @staticmethod
    def RetriveFileRequest():
        print "f"

    @staticmethod
    def LogoutRequest():
        print "f"

    def Read(self, s):
        messageHeader = s.recv(4).decode()
        if messageHeader == "ALGI":
            self.sessionId = s.recv(16).decode()
        elif messageHeader == "AADD"
        elif messageHeader == "ADEL"
        elif messageHeader == "AFIN"
        elif messageHeader == "ARET"
        elif messageHeader == "ALGO"

class MessagesServer:
    @staticmethod
    def Send():
        print "f"