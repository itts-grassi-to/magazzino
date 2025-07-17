
import tkinter as tk
import globali as gb

class Main_front():
    def __init__(self):
        self.__whidtBunner = 87
        self.__root = tk.Tk()
        self.__root.title("Magazzino")
        self.__root.geometry("800x300")
        self.__root.resizable(False, False)
        self.__root.grid()
        import menu as mn        
        mn.Menu(self.__root,gb.logato['RUOLO'])
        
        self.__wBunner = tk.Frame(self.__root, padx=1, pady=0)
        self.__wBunner.grid(row=0, column=0)
        self.__lblBunner = tk.Label(
            self.__wBunner, text=f"Sei logato come {gb.logato['NOME'][:self.__whidtBunner]}", font=("Arial", 12,'bold'), bg="#6A0DAD",fg='white',width=self.__whidtBunner,height=1)
        self.__lblBunner.grid(row=0, column=0, padx=5, pady=10, sticky='NSWE' )


