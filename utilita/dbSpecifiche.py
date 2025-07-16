import globali as gb
import utility as db
import dbProdotti as dbp
class DB_specifiche(db.DB):
    def __init__(self):
        super().__init__(gb.gdbms)
        self.__nomeTB = "tbSpecifiche"
        self.__nomeCampi = ["idSpecifiche", "descrizione","tipo","visibileA","fkProdotto"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"varchar(100) NOT NULL",
            self.__nomeCampi[2]:"varchar(40) not NULL",
            self.__nomeCampi[3]:"int(11) not null",
            self.__nomeCampi[4]:"int(11) not null"
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def inserisciSpecifica(self, descrizione,tipo,visibileA,fkProdotto,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: descrizione,
                self.__nomeCampi[2]: tipo,
                self.__nomeCampi[3]: visibileA,
                self.__nomeCampi[4]: fkProdotto
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._executeDDL(q)
    
    def _creaTabellaSpecifiche(self):
        dp=dbp.DB_prodotti()
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`), \
                CONSTRAINT `fk_{self.__nomeTB}_1` \
                FOREIGN KEY (`{self.__nomeCampi[4]}`) \
                REFERENCES `{dp.getNomeTB()}` (`{dp.getPK()}`) ON DELETE NO ACTION ON UPDATE NO ACTION \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._executeDDL(q)
