import utility as db

class Installa:
    def __init__(self,pb):
        self.__pb = pb
        self.db = db.DB()
        pass
    def __creaTabellaUtenti(self):
        return  \
            "CREATE TABLE IF NOT EXISTS `tbUtenti` ( \
            `idtbUtenti` int(11) NOT NULL AUTO_INCREMENT,\
            `nome` varchar(100) NOT NULL, \
            `cognome` varchar(100) NOT NULL, \
            `budge` varchar(45) DEFAULT NULL, \
            `user` varchar(45) NOT NULL, \
            `password` char(32) NOT NULL, \
            PRIMARY KEY (`idtbUtenti`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "
            
    def installa(self):
        print("Starting installation...")
        print("Creo tabella utenti")
        #self.db.executeDDL("CREATE TABLE IF NOT EXISTS example_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        self.db.executeDDL(self.__creaTabellaUtenti())
        self.__pb['value'] = 50
        print("Tabella utenti creata con successo.")
        print("Installation completed successfully.")