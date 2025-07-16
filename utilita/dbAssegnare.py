import globali as gb
import utility as db
import dbProdotti as dbp
import dbAsset as dba
import dbUtenti as dbu
class DB_assegnare(db.DB):
    def __init__(self):
        super().__init__(gb.gdbms)
        self.__nomeTB = "tbAssegnare"
        self.__nomeCampi = ["idAssegnare", "dataAssegnazione","fkProdotto","fkAsset","fkUtente"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"timestamp NULL DEFAULT current_timestamp()",
            self.__nomeCampi[2]:"int(11) not null",
            self.__nomeCampi[3]:"int(11) not null",
            self.__nomeCampi[4]:"int(11) not null"
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def getCampo(self,i):
        return self.__nomeCampi[i]
    def inserisciAssegnare(self, data,fkProdotto,fkAsset,fkUtente,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: data,
                self.__nomeCampi[2]: fkProdotto,
                self.__nomeCampi[3]: fkAsset,
                self.__nomeCampi[4]: fkUtente
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._executeDDL(q)
    
    def _creaTabellaAssegnare(self):
        dp=dbp.DB_prodotti()
        da=dba.DB_asset()
        du=dbu.DB_utenti()
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`), \
                CONSTRAINT `fk_{self.__nomeTB}_1` \
                FOREIGN KEY (`{self.__nomeCampi[2]}`) \
                REFERENCES `{dp.getNomeTB()}` (`{dp.getCampo(0)}`) ON DELETE NO ACTION ON UPDATE NO ACTION, \
                CONSTRAINT `fk_{self.__nomeTB}_2` \
                FOREIGN KEY (`{self.__nomeCampi[3]}`) \
                REFERENCES `{da.getNomeTB()}` (`{da.getCampo(0)}`) ON DELETE NO ACTION ON UPDATE NO ACTION, \
                CONSTRAINT `fk_{self.__nomeTB}_3` \
                FOREIGN KEY (`{self.__nomeCampi[4]}`) \
                REFERENCES `{du.getNomeTB()}` (`{du.getCampo(0)}`) ON DELETE NO ACTION ON UPDATE NO ACTION \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._executeDDL(q)
