import globali as gb
import utility as db
class DB_categorie(db.DB):
    def __init__(self):
        super().__init__(gb.gdbms)
        self.__nomeTB = "tbCategorie"
        self.__nomeCampi = ["idCategoria", "descrizione"]
        self.__campi = {
            self.__nomeCampi[0]:"int(11) NOT NULL AUTO_INCREMENT", 
            self.__nomeCampi[1]:"varchar(40) not NULL"
        }
    def getNomeTB(self):
        return self.__nomeTB
    def getPK(self):
        return self.__nomeCampi[0]
    def getCampo(self,i):
        return self.__nomeCampi[i]
    def _inserisciCategorieBase(self):
        e,r=self.inserisciCategoria("COMPUTER",1)
        if e:
            #print(f"Error inserting role: {r}")
            return e,r
        e,r= self.inserisciCategoria("FERRAMENTA",2)
        if e:
            #print(f"Error inserting role: {r}")
            return e,r
        e,r=self.inserisciCategoria("PANNELLINI SOLARI",3)
        if e:
            #print(f"Error inserting role: {r}")
            return e,r
        return False,""
    def inserisciCategoria(self, descrizione,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: descrizione
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._executeDDL(q)
    
    def getCategorie(self):
        q = f"SELECT * FROM {self.__nomeTB} "
        q+= f" ORDER BY {self.__nomeCampi[1]}"
        return self._executeDML(q)
    def _creaTabellaCategorie(self):
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._executeDDL(q)
