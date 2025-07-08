import utility as db
import dbRuoli

class DB_utenti(db.DB):
    def __init__(self):
        super().__init__()
        self.__nomeTB = "tbUtenti"
        self.__nomeCampi = ["idtbUtenti", "nome", "cognome", "budge", "user", "password", "fkRuolo"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
                    self.__nomeCampi[1]: "varchar(100) NOT NULL",\
                    self.__nomeCampi[2]: "varchar(100) NOT NULL",\
                    self.__nomeCampi[3]: "varchar(45) DEFAULT NULL",\
                    self.__nomeCampi[4]: "varchar(45) NOT NULL",\
                    self.__nomeCampi[5]: "char(32) NOT NULL",\
                    self.__nomeCampi[6]: "int(11) NOT NULL",\
       }
    def getPK(self):
        return self.__nomeCampi[0]
    def getFK(self):
        return self.__nomeCampi[6]
    def _inserisciUtente(self, nome, cognome, user, password, fkRuolo, PK=None, budge=None):
        dati = {
            self.__nomeCampi[0]: PK, 
            self.__nomeCampi[1]: nome,
            self.__nomeCampi[2]: cognome,
            self.__nomeCampi[3]: budge,
            self.__nomeCampi[4]: user,
            self.__nomeCampi[5]: password,
            self.getFK(): fkRuolo
        }

        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._execute(q)
    
    def _creaTabellaUtenti(self):
        dbr = dbRuoli.DB_ruoli()
        q = f"\
                CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
                {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.getPK()}`), \
            {self._creaFK(1,self.__nomeTB, self.getFK(), dbr.getNomeTB(), dbr.getPK())} \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "
        #print(q)
        return self._execute(q)
