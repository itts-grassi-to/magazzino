import tkinter as tk
import globali as g
import mnProdotto as mnp

class Menu:
    def __on_click_prodotto_nuovo(self):
        mnp.ProdottoNuovo()
    def __on_click_prodotto_cerca(self):
        #print("cerca prodotto")
        mnp.ProdottoModifica()
    def __init__(self,parent,ruolo):
        self.__root = parent
        menubar = tk.Menu(self.__root)
        self.__root.config(menu=menubar)
        self.__menubar = menubar
        if ruolo==g.ruoli['AMMINISTRATORE']:
            self.__menuAmministratore()
    def __menuAmministratore(self):
        file_menu = tk.Menu(self.__menubar, tearoff=0) # tearoff=0 rimuove la linea tratteggiata iniziale

        self.__menubar.add_cascade(label="File", menu=file_menu) # Aggiunge "File" alla barra dei menu

        # Aggiunta di voci al menu "File"
        file_menu.add_command(label="Esci", command=self.__chiudi_file)
        #file_menu.add_command(label="Salva", command=salva_file)
        #file_menu.add_separator() # Separatore
        #file_menu.add_command(label="Esci", command=esci_applicazione)

        # 3. Creazione del menu "Prodotto"
        help_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__menubar.add_cascade(label="Prodotto", menu=help_menu)
        help_menu.add_command(label="Nuovo", command=self.__on_click_prodotto_nuovo)
        help_menu.add_command(label="Cerca", command=self.__on_click_prodotto_cerca)
        help_menu.add_command(label="Cancella", command="")
        # 3. Creazione del menu "Aiuto"
        help_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__menubar.add_cascade(label="Aiuto", menu=help_menu)

        # Aggiunta di voci al menu "Aiuto"
        help_menu.add_command(label="Informazioni", command=self.__mostra_info)

        # Aggiunta di un checkbutton di esempio
        #opzione_attiva = tk.BooleanVar()
        #opzione_attiva.set(True) # Imposta lo stato iniziale a True

    def __chiudi_file(self):
        #messagebox.showinfo("Menu", "Hai cliccato su 'Apri'")   
        #print("Apri file")
        #self.__root.focus()
        self.__root.destroy()
    def __mostra_info(self):
        #messagebox.showinfo("Menu", "Hai cliccato su 'Informazioni'")   
        print("Mostra informazioni")
    def getMenu(self, ruolo):
        return self.__menu.getMenu(ruolo)

