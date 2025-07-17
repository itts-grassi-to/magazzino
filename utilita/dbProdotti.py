import globali as gb
import utility as db
import dbCategorie as dbc
import dbUtenti as dbu
class DB_prodotti(db.DB):
    def __init__(self):
        super().__init__(gb.gdbms)
        self.__nomeTB = "tbProdotti"
        self.__nomeCampi = ["idProdotto", "cb","sigla","timestamp","fkCategoria","fkUtente","quantita","um"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"char(15) unique default '000000000000000'",
            self.__nomeCampi[2]:"varchar(40) not NULL",
            self.__nomeCampi[3]:"timestamp NULL DEFAULT current_timestamp()",
            self.__nomeCampi[4]:"int(11) not null",
            self.__nomeCampi[5]:"int(11) not null",
            self.__nomeCampi[6]:"float not null",
            self.__nomeCampi[7]:"varchar(5)  not null",
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def getCampo(self,i):
        return self.__nomeCampi[i]
    def getMaxCB(self):
        try:
            q=F"SELECT max({self.__nomeCampi[1]}) as cbmax FROM {self.__nomeTB}"
            e,r = self._executeDML(q)
            return False,'00000000000000' if r[0]['cbmax']==None else r[0]['cbmax']
            #print(f"risultato cb={r}")
        except:
            return True,r
    def inserisciCategoria(self, descrizione,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: descrizione
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._executeDDL(q)
    def _creaTabellaProdotti(self):
        ut=dbu.DB_utenti()
        cat=dbc.DB_categorie()
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`), \
                CONSTRAINT `fk_{self.__nomeTB}_1` \
                FOREIGN KEY (`{self.__nomeCampi[4]}`) \
                REFERENCES `{cat.getNomeTB()}` (`{cat.getPK()}`) ON DELETE NO ACTION ON UPDATE NO ACTION, \
                CONSTRAINT `fk_{self.__nomeTB}_2` \
                FOREIGN KEY (`{self.__nomeCampi[5]}`) \
                REFERENCES `{ut.getNomeTB()}` (`{ut.getPK()}`) ON DELETE NO ACTION ON UPDATE NO ACTION \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._executeDDL(q)
