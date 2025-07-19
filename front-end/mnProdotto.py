import sviluppo as gfr
import tkinter as tk
from tkinter import ttk 
import tkinter.messagebox as msg

import dbProdotti as dbp
import codice_barre as ucb
import mnCategoria as mnc
import globali as gb
class Prodotto:
    def __init__(self,ini):
        if gb.logato["RUOLO"]>gb.ruoli["OPERATORE"]:
            msg.showinfo("Nuovo prodotto","Per aggiungere prodotti devi essere almeno OPERATORE")
            return
        self._root = tk.Toplevel()
        self._root.title(ini["titolo"])
        self._root.geometry(ini["dimensioni"])
        self._root.resizable(False, False)
        self._root.grid()
        self._root.attributes("-topmost",1)

class ProdottoNuovo(Prodotto):
    def __on_click_stampa(self):
        self.__objCB.set(self.__valCB.get())
        self.__objCB.genera_code128()
    def __on_click_salva(self):
        tsigla=self.__valSigla.get()
        if tsigla=="":
            msg.showerror("Controllo campo","Non hai inserito la sigla del prodotto",parent=self._root)
            return
        if self.__valCategoria["sval"].get()==self.__dummy:
            msg.showerror("Controllo campo","Non hai inserito il tipo del prodotto",parent=self._root)
            return
        tquantita=self.__valQuantita.get()
        if tquantita=="":
            msg.showerror("Controllo campo","Non hai inserito la quantità",parent=self._root)
            return
        if not gb.is_number(tquantita):
            msg.showerror("Controllo campo","Non hai inserito la quantità",parent=self._root)
            return        
        tum=self.__valUM.get()
        if tum==self.__dummyUM or tum=="":
            msg.showerror("Controllo campo","Non hai inserito l'unità di misura",parent=self._root)
            return
        obj=dbp.DB_prodotti()
        e,mess=obj.inserisciProdotto(
                        self.__valCB.get(), tsigla, 
                        self.__valCategoria["ival"].get(),
                        gb.logato["ID"],tquantita,
                        tum,gb.stato[self.__cmbStato.get()],
                        PK=None,timestamp=None)
        if e:
            msg.showerror("Errore inserimento",mess,parent=self._root)
            return
        msg.showinfo("Inserimento riuscito",f"Il prodotto {tsigla} è stato inserito con successo",parent=self._root)
        self._root.destroy()
    def __on_click_esci(self):
        pass
    def __on_click_categoria(self,event):
        self.__objCategoria = mnc.VisuCategoria()
        #self.__objCategoria.root.grab_set()
        self.__objCategoria.root.transient(self._root)
        self._root.wait_window(self.__objCategoria.root)
        ival,sval= self.__objCategoria.getSelezionato()
        self.__valCategoria["ival"].set(ival)
        if ival==-1:
            self.__valCategoria["sval"].set(self.__dummy)
        else:
            self.__valCategoria["sval"].set(sval)
    def __on_click_UM(self,event):
        if self.__valUM.get() == self.__dummyUM:
            self.__valUM.set("")
    def __init__(self):
    #def run(self):
        w="400"
        h="300"
        ini = {"id":"NUOVO","titolo":f"Nuovo prodotto. ","dimensioni":w+"x"+h}
        super().__init__(ini)
        self.__wBunner = tk.Frame(self._root, padx=1, pady=0)
        self.__wBunner.grid(row=0, column=0)
        self.__fr1 =tk.Frame(self._root,width=int(w),height=int(h)/2)
        self.__fr1.grid(column=0,row=1,padx=5,pady=5,sticky="NSEW")
        #self.__frSpecifiche =tk.Frame(self._root,width=int(w),height=int(h)/2)
        #self.__frSpecifiche.grid(column=0,row=1,padx=5,pady=5,sticky="NSEW")
        self.__fr2 =tk.Frame(self._root,width=int(w),height=int(h)/2)
        self.__fr2.grid(column=0,row=2,padx=5,pady=5,sticky="NSEW")  
        self.__objCB=ucb.CB()
        self.__objDBP = dbp.DB_prodotti()
        self.__objCategoria = None
        self.__dummy="Clicca qui per inserire la categoria..."
        self.__dummyUM="Unita di misura"
        #*************************************************************************************** bunner
        self.__lblBunner = tk.Label(
            self.__wBunner, text=f"Sei logato come {gb.logato['NOME']}", 
            font=("Arial", 12,'bold'), bg="#6A0DAD",fg='white',width=int(int(w)/9.2),height=1)
        self.__lblBunner.grid(row=0, column=0, columnspan=3, padx=5, pady=10, sticky='NSWE' )
        #*************************************************************************************** codice a barre
        lblCBT = tk.Label(self.__fr1,text="Codice a barre")
        lblCBT.grid(column=0,row=1,padx=5,pady=5)
        #*********************************************
        errore,txt=self.__getNuovoCB()
        if errore:
            msg.showerror("Errore DBMS",txt,parent=self._root)
            self._root.destroy()
        self.__valCB = tk.StringVar()
        self.__valCB.set(txt)
        txtCB = tk.Entry(self.__fr1,width=16,textvariable=self.__valCB,
                         state=tk.DISABLED, justify=tk.CENTER)
        txtCB.grid(column=1,row=1,pady=5)
        #*********************************************
        btStampaCB = tk.Button(self.__fr1,text="Stampa",command=self.__on_click_stampa)
        btStampaCB.grid(column=2,row=1,padx=5,pady=5)        
        #************************************************************************************************ sigla
        lblSigla = tk.Label(self.__fr1,text="Sigla")
        lblSigla.grid(column=0,row=2,padx=5,pady=5,sticky="E")
        #***********
        self.__valSigla = tk.StringVar()
        txtCB = tk.Entry(self.__fr1,width=16,textvariable=self.__valSigla, justify=tk.LEFT)
        txtCB.grid(column=1,row=2,pady=5)
        #************************************************************************************************** categoria
        self.__valCategoria={"ival":tk.IntVar(),"sval":tk.StringVar()}
        self.__valCategoria["ival"].set(-1)
        self.__valCategoria["sval"].set(self.__dummy)
        txtCategoria = tk.Entry(self.__fr1,width=16,
                                textvariable=self.__valCategoria["sval"],
                                state="readonly",justify=tk.CENTER)
        txtCategoria.grid(column=0,row=3,pady=5,columnspan=2,sticky="EW")
        txtCategoria.bind("<Button-1>", self.__on_click_categoria)
        #************************************************************************************************ quantita
        lblQ = tk.Label(self.__fr1,text="Quantita")
        lblQ.grid(column=0,row=4,padx=5,pady=5,sticky="E")
        #***********
        self.__valQuantita = tk.StringVar()
        self.__valQuantita.set(1)
        txtCB = tk.Entry(self.__fr1,width=6,textvariable=self.__valQuantita, justify=tk.LEFT)
        txtCB.grid(column=1,row=4,columnspan=3,pady=5,sticky="W")
        #**************
        self.__valUM = tk.StringVar()
        self.__valUM.set(self.__dummyUM)
        txtUM = tk.Entry(self.__fr1,width=15,textvariable=self.__valUM, justify=tk.CENTER)
        txtUM.grid(column=1,row=4,columnspan=3,pady=5)
        txtUM.bind("<Button-1>", self.__on_click_UM)
        #************************************************************************************************ disponibilità
        lblStato = tk.Label(self.__fr1,text="Stato")
        lblStato.grid(column=0,row=5,padx=5,pady=5,sticky="E")
        #***********
        opt=[]
        for ch in gb.stato:
            opt.append(ch)
        self.__cmbStato = ttk.Combobox(self.__fr1, values=opt,state="readonly")
        self.__cmbStato.set("DISPONIBILE")
        self.__cmbStato.grid(column=1,row=5,padx=5,pady=5,sticky="W")
        #******************************************************************************* pulsantiera
        btSalva = tk.Button(self.__fr2,text="Salva",command=self.__on_click_salva)
        btSalva.grid(column=0,row=0,padx=5,pady=5)
        btEsci = tk.Button(self.__fr2,text="Esci",command=self.__on_click_esci)
        btEsci.grid(column=1,row=0,padx=5,pady=5)

    def __getNuovoCB(self):

        errore,self.__cb=self.__objDBP.getMaxCB()
        if errore:
            return True, self.__cb
        self.__objCB.set(self.__cb)
        self.__cb=self.__objCB.incrementa_esadecimale_ricorsivo()
        return False,self.__cb
       
class ProdottoModifica(Prodotto):
    def __init__(self):
        self.__frFiltro=tk.Frame(self._root)
        self._frVisualizza=tk.Frame(self._root)
        
    def visualizza(self,cb=None):
        #******************************************************* Treeview prodotti
        objProdotto=dbp.DB_prodotti()
        style = ttk.Style(self._root)
        style.configure("rosso.Treeview", 
                        background="red", foreground="white")


        self.__treeCategorie = ttk.Treeview(
            self._root, 
            columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), 
            show="headings",
            height=10,
            selectmode="browse"
        )
        self.__treeCategorie.heading("col1", text="ID")
        self.__treeCategorie.heading("col2", text="DESCRIZIONE")
        self.__treeCategorie.column("col1", width=40)
        self.__treeCategorie.column("col2", width=300)
        e,self.__valCategorie=self.__obyCategorie.getCategorie()
        if e:
            msg.showerror("Categorie","Errore nella lettura delle categorie.\nContattare l'amministratore")
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


if gfr.SVILUPPO:
    p=ProdottoModifica()
    p._root.mainloop()
