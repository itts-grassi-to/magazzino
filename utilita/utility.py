import mysql.connector
from mysql.connector import Error


class DB:
    def __init__(self,p):
        self.__host = p["host"] #"192.168.1.117"
        self.db_name = p["nome_schema"] #"magazzino"
        self.__user = p["user"] #"dortu"
        self.__psw = p["password"] #"ortu"
        self.data = {}
    
    def connect(self):
        return self.__connect()
    def __connect(self):
        # da valorizzare i parametri
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
    '''
    def __connecto(self):
        #print(f"Connecting to database: {self.db_name}")
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
    '''
    def __disconnect(self):
        #print(f"Disconnecting from database: {self.db_name}")
        if self.connection.is_connected():
            self.connection.close()
            #print("Disconnected successfully")
        else:
            #print("No active connection to disconnect")
            pass
    def _executeDDL(self, query):
        #print(f"Executing query: {query}")
        r=self.__connect()
        if not self.connection or not self.connection.is_connected():
            #print("No active connection to execute query")
            #return "No active connection to execute query"
            return True, r
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            #print("Query executed successfully")
            return False,"Query eseguita con successo"
        except Error as e:
            #print(f"Error executing query: {e}")
            print(query)
            return True,f"Error executing query: {e}"
        finally:
            self.__disconnect() 
    def _executeDML(self, query):
        #print(f"Executing query: {query}")
        dict_cursor = None
        records={}
        r=self.__connect()
        if not self.connection or not self.connection.is_connected():
            #print("No active connection to execute query")
            #return "No active connection to execute query"
            return True,r
        
        try:
            dict_cursor = self.connection.cursor(dictionary=True)
            dict_cursor.execute(query)
            records=dict_cursor.fetchall()
            #print("Query executed successfully")
            return False,records
        except Error as e:
            #print(f"Error executing query: {e}")
            print(query)
            return True, f"Error executing query: {e}"
        finally:
            if dict_cursor:
                dict_cursor.close()
            self.__disconnect() 
    def _creaCampi(self, campi):
        r=""
        for ch in campi:
            r+= f"`{ch}` {campi[ch]}, "
        r = r[:-2]  # Remove the last comma and space
        return r
    def __formataValore(self, v):
        if isinstance(v, str):
            return f"'{v}'"
        elif isinstance(v, int) or isinstance(v, float):
            return str(v)
        elif v is None:
            return "NULL"
        else:
            raise ValueError(f"Unsupported value type: {type(v)}")
    def _creaInsertInto(self, nomeTB, dati):
        ins_to = f"INSERT INTO `{nomeTB}` ("
        valori = f"VALUES ("
        on_dup = f"ON DUPLICATE KEY UPDATE "
        for ch in dati:
            if dati[ch] is not None:
                ins_to += f"`{ch}`, "
                valori += self.__formataValore(dati[ch]) + ", "
                on_dup += f"`{ch}`={self.__formataValore(dati[ch])}, "
        ins_to = ins_to[:-2] + ")  "
        valori = valori[:-2] + ")"
        on_dup = on_dup[:-2] + ";"
        return ins_to + valori + " " + on_dup
    def _creaFK(self, i,nomeTB, nomeFK, nomeTB_FK,nomePK_FK):
        return f" \
            CONSTRAINT `fk_{nomeTB}_{i}` \
                FOREIGN KEY (`{nomeFK}`) \
                    REFERENCES `{nomeTB_FK}` (`{nomePK_FK}`) ON DELETE NO ACTION ON UPDATE NO ACTION"
    def getSchemi(self):
        return self.__connect()
        if r==none:
            print("Connection failed")
        else:
            print("Connection successful")
            self.__.disconnect()         
    
#***********************************DB_ruoli

#DB().test()


