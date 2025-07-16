import globali as gb
import utility as db
class DB_asset(db.DB):
    def __init__(self):
        super().__init__(gb.gdbms)
        self.__nomeTB = "tbAsset"
        self.__nomeCampi = ["idAsset", "sigla","descrizione"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"varchar(50) NOT NULL UNIQUE",
            self.__nomeCampi[2]:"varchar(200) not NULL",
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def getCampo(self,i):
        return self.__nomeCampi[i]
    def inserisciAsset(self, sigla,descrizione,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: sigla,
                self.__nomeCampi[2]: descrizione
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._executeDDL(q)
    
    def _creaTabellaAsset(self):
        
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._executeDDL(q)
