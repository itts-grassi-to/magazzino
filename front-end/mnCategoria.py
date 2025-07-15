import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import tkinter.font as tkfont
import dbCategorie as dbc


class Categoria:
    def __init__(self,ini):
        self.root = tk.Toplevel()
        self.root.title(ini["titolo"])
        self.root.geometry(ini["dimensioni"])
        self.root.resizable(False, False)
        self.root.grid()
        self.root.attributes("-topmost",1) 
class VisuCategoria(Categoria):
    def __on_click_cerca(self):
        print("Cliccato cerca")
    def __on_click_seleziona(self):
        selected_items_ids = self.__treeCategorie.selection()
        if not selected_items_ids:
            msg.showerror("Seleziona","Nessun elemento selezionato!",parent=self.root)
            return
        item_details = self.__treeCategorie.item(selected_items_ids[0])   
        # print(item_details) 
        self.__r=item_details["values"]
        self.root.destroy()
        
    def __on_click_esci(self):
        print("Cliccato esci")
    def __init__(self):
        w="400"
        h="350"
        ini = {"id":"Visualizza","titolo":"Visualizza categoria","dimensioni":w+"x"+h}
        super().__init__(ini)
        self.__obyCategorie= dbc.DB_categorie()
        self.__r=[]
        #******************************************************* cerca
        self.__valCerca=tk.StringVar()
        txtCerca=tk.Entry(self.root,textvariable=self.__valCerca)
        txtCerca.grid(column=0,row=0,padx=5,pady=5,sticky="EW")
        btCerca=tk.Button(self.root,text="cerca",command=self.__on_click_cerca)
        btCerca.grid(column=1,row=0,padx=5,pady=5,sticky="W")
        #******************************************************* Treeview categorie
        style = ttk.Style(self.root)
        style.configure("rosso.Treeview", 
                        background="red", foreground="white")
        self.__treeCategorie = ttk.Treeview(
            self.root, 
            columns=("col1", "col2"), 
            show="headings",
            height=10,
            selectmode="browse"
        )
        self.__treeCategorie.heading("col1", text="ID")
        self.__treeCategorie.heading("col2", text="DESCRIZIONE")
        self.__treeCategorie.column("col1", width=40)
        self.__treeCategorie.column("col2", width=300)
        self.__valCategorie=self.__obyCategorie.getCategorie()
        i=0
        while i<len(self.__valCategorie):
            self.__treeCategorie.insert("","end",
                values=(
                    self.__valCategorie[i][self.__obyCategorie.getCampo(0)],
                    self.__valCategorie[i][self.__obyCategorie.getCampo(1)]
                )
            )
            i+=1
        scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.__treeCategorie.yview)
        self.__treeCategorie.configure(yscrollcommand=scrollbar_y.set)
        self.__treeCategorie.grid(column=0,row=1,columnspan=2,padx=5,pady=5)
        scrollbar_y.grid(column=2,row=1,padx=0,pady=5,sticky="NS")
        #******************************************************************************* pulsantiera
        btSeleziona = tk.Button(self.root,text="Seleziona",command=self.__on_click_seleziona)
        btSeleziona.grid(column=0,row=2,padx=5,pady=5,sticky="E")
        btEsci = tk.Button(self.root,text="Esci",command=self.__on_click_esci)
        btEsci.grid(column=1,row=2,padx=5,pady=5,sticky="W")

    def getSelezionato(self):
        return self.__r[0],self.__r[1]