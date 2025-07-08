import utility as db
class DB_ruoli(db.DB):
    def __init__(self):
        super().__init__()
        self.__nomeTB = "tbRuolo"
        self.__nomeCampi = ["idRuolo", "descrizione"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"varchar(20) DEFAULT NULL"
        }
        self.__ruoliBase = {
            "AMMINISTRATORE": 1,
            "OPERATORE": 100,
            "VISUALIZZATORE": 1000
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def _inserisciRuoliBase(self):
        
        dati={self.__nomeCampi[0]:1, self.__nomeCampi[1]:"AMMINISTRATORE"}
        r=self._inserisciRuolo(dati)
        if r:
            print(f"Error inserting role: {r}")
            return r
        dati={self.__nomeCampi[0]:100, self.__nomeCampi[1]:"OPERATORE"}
        r= self._inserisciRuolo(dati)
        if r:
            print(f"Error inserting role: {r}")
            return r
        dati={self.__nomeCampi[0]:1000, self.__nomeCampi[1]:"VISUALIZZATORE"}
        r=self._inserisciRuolo(dati)
        if r:
            print(f"Error inserting role: {r}")
            return r
        
        return ""
    def _inserisciRuolo(self, dati):
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._execute(q)
    
    def _creaTabellaRuoli(self):
        q = \
            f"CREATE TABLE IF NOT EXISTS `tbRuolo` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._execute(q)
