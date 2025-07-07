import mysql.connector
from mysql.connector import Error

    

class DB:
    def __init__(self):
        self.__host="192.168.1.117"
        self.db_name = "magazzino"
        self.__user = "dortu"
        self.__psw="ortu"
        self.data = {}
    def __connect(self):
        print(f"Connecting to database: {self.db_name}")
        try:
            self.connection = mysql.connector.connect(
                host=self.__host,
                database=self.db_name,
                user=self.__user,
                password=self.__psw
            )
            if self.connection.is_connected():
                self.__cursor = self.connection.cursor()
                #print("Connection successful")
                return "Connection successful"
        except Error as e:
            #print(f"Error while connecting to MySQL: {e}")
            self.connection = None
            return f"Error while connecting to MySQL: {e}"
    def __disconnect(self):
        print(f"Disconnecting from database: {self.db_name}")
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected successfully")
        else:
            print("No active connection to disconnect")
    def _execute(self, query):
        #print(f"Executing query: {query}")
        r=self.__connect()
        if not self.connection or not self.connection.is_connected():
            #print("No active connection to execute query")
            #return "No active connection to execute query"
            return r
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            #print("Query executed successfully")
            return ""
        except Error as e:
            #print(f"Error executing query: {e}")
            print(query)
            return f"Error executing query: {e}"
        finally:
            self.__disconnect() 
    def _creaCampi(self, campi):
        r=""
        for ch in campi:
            r+= f"`{ch}` {campi[ch]}, "
        r = r[:-2]  # Remove the last comma and space
        return r
    def _creaInsertInto(self, nomeTB, campi):
        r = f"INSERT INTO `{nomeTB}` ("
        for ch in campi:
            r += f"`{ch}`, "
        r = r[:-2] + ")  "
        return r
    def test(self):
        return self.__connect()
        if r==none:
            print("Connection failed")
        else:
            print("Connection successful")
            self.__.disconnect()         
#***********************************DB_ruoli
class DB_ruoli(DB):
    def __init__(self):
        super().__init__()
        self.__nomeTB = "tbRuolo"
        self.__nomePK = "idRuolo"
        self.__campi = {
            self.__nomePK:"int(11) NOT NULL AUTO_INCREMENT", 
            "descrizione":"varchar(20) DEFAULT NULL"
        }
        self.__ruoliBase = {
            "AMMINISTRATORE": 1,
            "OPERATORE": 100,
            "VISUALIZZATORE": 100
        }
    def _inserisciRuolo(self, id,ruolo):
        q = f"{self._creaInsertInto(self.__nomeTB,self.__campi)} values({id}, '{ruolo}') \
        ON DUPLICATE KEY UPDATE `descrizione`='{ruolo}';"
        return self._execute(q)
    def __creaOrUpdateRuolo(self, id, ruolo):
        q = f"ON DUPLICATE KEY UPDATE `descrizione`='{ruolo}';"
        return q

    def _creaTabellaRuoli(self):
        q = \
            f"CREATE TABLE IF NOT EXISTS `tbRuolo` ( \
             {self._creaCampi(self.__campi)}, \
            PRIMARY KEY (`{self.__nomePK}`) \
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; \
            "  
        #print(q)
        return self._execute(q)

#DB().test()


