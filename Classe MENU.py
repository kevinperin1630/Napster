class menu:

    @staticmethod
    def ShortMenu():
        # Menù ridotto, nel caso all'inserimento venisse inserito un carattere differente da 1, 2 o 3, il valore di ritorno sarà 0,
        #    altrimenti sarà l'equivalente in intero del numero inserito
        print("MENU'")
        print("1 - Scarica file")
        print("2 - Carica file")
        print("3 - Logout")
        print("")
        scelta = input("Inserire il numero relativo all'operazione desiderata: ")
        if scelta == "1":
            return 1
        elif scelta == "2":
            return 2
        elif scelta == "3":
            return 3
        else:
            return 0
    
    @staticmethod
    def LongMenu():
        # Menù ridotto, nel caso all'inserimento venisse inserito un carattere differente da 1, 2 o 3, il valore di ritorno sarà 0,
        #    altrimenti sarà l'equivalente in intero del numero inserito
        print("MENU'")
        print("1 - Scarica file")
        print("2 - Carica file")
        print("3 - Rimuovi file")
        print("4 - Logout")
        print("")
        scelta = input("Inserire il numero relativo all'operazione desiderata: ")
        if scelta == "1":
            return 1
        elif scelta == "2":
            return 2
        elif scelta == "3":
            return 3
        elif scelta == "4":
            return 3
        else:
            return 0
    
    @staticmethod
    def SearchString():
        #Metodo che valuta la validità di una stringa di ricerca e la ritorna come valore, in caso non sia valida il valore di ritorno sarà '-'
        stringa = input("Inserire la stringa di ricerca (max 20 caratteri): ")
        if len(stringa)>=20:
            charValidi=true
            for i in stringa:
                if i!='a' or i!='b' or i!='c' or i!='d' or i!='e' or i!='f' 
                or i!='g' or i!='h' or i!='i' or i!='j' or i!='k' or i!='l' 
                or i!='m' or i!='n' or i!='o' or i!='p' or i!='q' or i!='r' 
                or i!='s' or i!='t' or i!='u' or i!='v' or i!='w' or i!='x' 
                or i!='y' or i!='z' or i!='1' or i!='2' or i!='3' or i!='4'
                or i!='5' or i!='6' or i!='7' or i!='8' or i!='9':
                charValidi= false
            if charValidi:
                return stringa
            else:return '-'
        else:return '-'
    
    @staticmethod
    def ShowFiles(*file):
        i=1
        print("Lista dei file: ")
        for f in file:
            print(i," - ", file.md5, " ", file.nome)
            i = i+1
        
        fileSelezionato = input("Inserire il numero corrispondente al file da selezionare: ")

        charValidi=true
        for i in stringa:
            if i!='1' or i!='2' or i!='3' or i!='4'
            or i!='5' or i!='6' or i!='7' or i!='8' or i!='9':
            charValidi= false

        if charValidi:
            return file[fileSelezionato]
        else return "NO" #mettere un valore di ritorno migliore nel caso in cui il tizio inserisca un carattere non valido