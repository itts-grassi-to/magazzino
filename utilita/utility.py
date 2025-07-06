import mysql.connector
from mysql.connector import Error

class DB:
    def __init__(self):
        self.__host="192.168.1.117"
        self.db_name = "magazzino"
        self.__user = "dortu"
        self.__psw="ortu"
        self.data = {}
    def _connect(self):
        self.__connect()
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
                print("Connection successful")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None
    def disconnect(self):
        print(f"Disconnecting from database: {self.db_name}")
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected successfully")
        else:
            print("No active connection to disconnect")

    def executeDDL(self, query):
        #print(f"Executing query: {query}")
        self.__connect()
        if not self.connection or not self.connection.is_connected():
            print("No active connection to execute query")
            return None
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")
            return None 
    def test(self):
        return self.__connect()
        if r==none:
            print("Connection failed")
        else:
            print("Connection successful")
            self.__.disconnect()    

DB().test()


