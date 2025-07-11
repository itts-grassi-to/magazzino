import utility as db
class DB_categorie(db.DB):
    def __init__(self):
        super().__init__()
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
    def inserisciCategoria(self, descrizione,PK=None):
        dati={
                self.__nomeCampi[0]: PK, 
                self.__nomeCampi[1]: descrizione
            }
        q = self._creaInsertInto(self.__nomeTB,dati)
        return self._execute(q)
    
    def _creaTabellaCategorie(self):
        q = \
            f"CREATE TABLE IF NOT EXISTS `{self.__nomeTB}` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomeCampi[0]}`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._execute(q)
