import utility as db

class Installa:
    def __init__(self):
        self.db = db.DB()
        pass

    def installa(self):
        print("Starting installation...")
        self.db.executeDDL("CREATE TABLE IF NOT EXISTS example_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        print("Installation completed successfully.")