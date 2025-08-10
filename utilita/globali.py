SVILUPPO = True
if SVILUPPO:
    import tkinter as tk
    import pickle
    try:
        with open('config', 'rb') as f:
            gdbms=loaded_dictionary = pickle.load(f)
    except FileNotFoundError:
       print("Apertura file di configurazione Configurazione fallita in sviluppo")
    
    logato={
        "ID": 1,
        "NOME": "Sviluppo",
        "COGNOME":"",
        "RUOLO" : 100
    }
else:
    logato={}
    gdbms = {}
stato={
    "DISPONIBILE":1,
    "NON DISPONIBILE":2,
    "EVASO":3
}
ruoli = {
            "AMMINISTRATORE": 1,
            "OPERATORE": 100,
            "VISUALIZZATORE": 1000
        }
def getStato( valore):
    if not is_number(valore):
        return "None"
    valore = int(valore)
    for chiave, v in stato.items():
        if v == valore:
            return chiave
    return None 
def is_number(s):
    s=s.replace(",",".")
    try:
        float(s)  # Tenta di convertire in float
        return True
    except ValueError:
        return False
class Filtro:
    def __on_click_ck(self):
        if self.__ck.selection_get():
            self.__txt.config(state="disabled")
        else:
            self.__txt.config(state="normal")
    def __init__(self, root,col=0,riga=0):
        self._root = root
        self._frFiltro = tk.Frame(self._root)
        self._frFiltro.grid(column=col, row=riga, padx=10, pady=10, sticky="NSEW")
        self._frFiltro.columnconfigure(0, weight=1)
        self._frFiltro.rowconfigure(0, weight=1)
        self._frFiltro.rowconfigure(1, weight=1)
        self._frFiltro.rowconfigure(2, weight=1)
        self.__vTxt = tk.StringVar()
        
        self.__txt= tk.Entry(self._frFiltro, textvariable=self.__vTxt, font=("Arial", 10), width=10)
        self.__txt.grid(column=0, row=0, padx=10, pady=10, sticky="NSEW")
        #txt.bind("<Return>", self._on_enter)
        self.__vTxt.set("")

        self.__ck=tk.Checkbutton(self._frFiltro, text="CB" , onvalue="1", offvalue="0",
                               command=self.__on_click_ck, font=("Arial", 10), width=10)
        self.__ck.grid(column=1, row=0, padx=10, pady=10, sticky="NSEW")
        self.__ck.selection_clear()  
        self._frFiltro.columnconfigure(1, weight=1)
        self._frFiltro.rowconfigure(0, weight=1)
        self._frFiltro.rowconfigure(1, weight=1)
        self._frFiltro.rowconfigure(2, weight=1)  
        
