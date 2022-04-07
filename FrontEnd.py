class Menu:
    @staticmethod
    def ShortMenu():
        print("MENU'")
        print("1 - Scarica file")
        print("2 - Carica file")
        print("3 - Logout")
        while True:
            scelta = input("\nInserire il numero dell'operazione desiderata: ")
            if scelta == "1":
                return 1
            elif scelta == "2":
                return 2
            elif scelta == "3":
                return 3
            else: 
                print ("Operazione non riconosciuta, riprovare")

    @staticmethod
    def LongMenu():
        print("MENU'")
        print("1 - Scarica file")
        print("2 - Carica file")
        print("3 - Rimuovi file")
        print("4 - Logout")
        print("")
        while True:
            scelta = input("\nInserire il numero dell'operazione desiderata: ")
            if scelta == "1":
                return 1
            elif scelta == "2":
                return 2
            elif scelta == "3":
                return 3
            elif scelta == "4":
                return 3
            else:
                print("Operazione non riconosciuta, riprovare")

    @staticmethod
    def SearchString():
        while True:
            stringa = input("Inserire la stringa di ricerca (max 20 caratteri): ")
            stringa = stringa.lower()
            if len(stringa) <= 20:
                if stringa.isalnum():
                    return stringa
                else: 
                    print("Errore, la stringa contiene caratteri invalidi")
            else: 
                print("Errore, la stringa supera i 20 caratteri")
    
    @staticmethod
    def SearchResult(files):
        fileIndex = ''
        peerIndex = ''
        i  =1
        print("Risultati: ")
        for f in files:
            print("%i) %s %s" %(i, f.md5, f.nome))
            i += 1
            k = 1
            for p in f.peers:
                print("\t%i) %s %s" %(k, p.ip, p.porta))
                k += 1
        while True:
            fileIndex = input("Selezionare il file da scaricare: ")
            try:
                fileIndex = int(fileIndex)
                if fileIndex <= 0 or fileIndex > len(files):
                    print("File non riconosciuto, riprovare")
                else:
                    fileIndex -= 1
                    break
            except:
                print("Selezione invalida, riprovare")
        file = files[fileIndex]
        while True:
            peerIndex = input("Selezionare il peer da cui scaricare: ")
            try:
                peerIndex = int(peerIndex)
                if peerIndex <= 0 or peerIndex > len(file.peers):
                    print("Peer non riconosciuto, riprovare")
                else:
                    peerIndex -= 1
                    break
            except:
                print("Selezione invalida, riprovare")
        return file, file.peers[peerIndex].ip, file.peers[peerIndex].port

    @staticmethod
    def SelectFile(files):
        i = 1
        for f in files:
            print("%i) %s %s" %(i, f.md5, f.nome))
            i += 1
        while True:
            fileIndex = input("Selezionare il file da rimuovere dalla rete: ")
            try:
                fileIndex = int(fileIndex)
                if fileIndex <= 0 or fileIndex > len(files):
                    print("File non riconosciuto, riprovare")
                else:
                    fileIndex -= 1
                    break
            except:
                print("Selezione invalida, riprovare")
        return files[fileIndex].md5

    @staticmethod
    def CheckIp(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        i = 1
        for p in parts:
            if len(p) != 3:
                return False
            try:
                firstP = 0
                p = int(p)
                if p < 0 or p > 255:
                    return False
                elif p == 127 or p == 0 and i == 1:
                    return False
                elif p == 255 and i == 4:
                    return False
                elif p == 254 and firstP == 169:
                    return False
                elif i == 1:
                    firstP = p
            except:
                return False
            i += 1
        return True