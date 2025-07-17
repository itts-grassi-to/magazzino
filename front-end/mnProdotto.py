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
        if self.__valSigla.get()=="":
            msg.showerror("Controllo campo","Non hai inserito la sigla del prodotto",parent=self._root)
            return
        if self.__valCategoria.get()==self.__dummy:
            self.__showerror("Controllo campo","Non hai inserito il tipo del prodotto",parent=self._root)
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
            msg.showerror("Errore DBMS",txt)
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
        pass


if gfr.SVILUPPO:
    p=ProdottoNuovo()
    p._root.mainloop()
