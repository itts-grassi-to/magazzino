import tkinter as tk
import tkinter.messagebox as msg
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
target_module_dir = os.path.join(project_root, 'utilita')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)
target_module_dir = os.path.join(project_root, 'img')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)

import dbProdotti as dbp
import codice_barre as ucb
class Prodotto:
    def __init__(self,ini):
        self._root = tk.Tk()
        self._root.title(ini["titolo"])
        self._root.geometry(ini["dimensioni"])
        self._root.resizable(False, False)
        self._root.grid()

class ProdottoNuovo(Prodotto):
    def __on_click_stampa(self):
        self.__objCB.set(self.__valCB.get())
        self.__objCB.genera_code128()
    def __on_click_nuovo(self):
        pass
    def __on_click_esci(self):
        pass
    def __init__(self):
        w="400"
        h="300"
        ini = {"id":"NUOVO","titolo":"Nuovo prodotto","dimensioni":w+"x"+h}
        super().__init__(ini)
        self.__fr1 =tk.Frame(self._root,width=int(w),height=int(h)/2)
        self.__fr1.grid(column=0,row=0,padx=5,pady=5,sticky="NSEW")
        self.__fr2 =tk.Frame(self._root,width=int(w),height=int(h)/2)
        self.__fr2.grid(column=0,row=1,padx=5,pady=5,sticky="NSEW")  
        self.__objCB=ucb.CB()
        self.__objDBP = dbp.DB_prodotti()
        #************************************************************************************************* codice a barre
        lblCBT = tk.Label(self.__fr1,text="Codice a barre")
        lblCBT.grid(column=0,row=0,padx=5,pady=5)
        #*********************************************
        errore,txt=self.__getNuovoCB()
        if errore:
            msg.showerror("Errore DBMS",txt)
            self._root.destroy()
        self.__valCB = tk.StringVar()
        self.__valCB.set(txt)
        txtCB = tk.Entry(self.__fr1,width=16,textvariable=self.__valCB,state=tk.DISABLED, justify=tk.CENTER)
        txtCB.grid(column=1,row=0,pady=5)
        #*********************************************
        btStampaCB = tk.Button(self.__fr1,text="Stampa",command=self.__on_click_stampa)
        btStampaCB.grid(column=2,row=0,padx=5,pady=5)        
        #************************************************************************************************** sigla
        lblSigla = tk.Label(self.__fr1,text="Sigla")
        lblSigla.grid(column=0,row=1,padx=5,pady=5,sticky="E")
        #***********
        self.__valSigla = tk.StringVar()
        txtCB = tk.Entry(self.__fr1,width=16,textvariable=self.__valSigla, justify=tk.LEFT)
        txtCB.grid(column=1,row=1,pady=5)
        #************************************************************************************************* pulsantiera
        btSalva = tk.Button(self.__fr2,text="Nuovo",command=self.__on_click_nuovo)
        btSalva.grid(column=0,row=0,padx=5,pady=5)
        btEsci = tk.Button(self.__fr2,text="Esci",command=self.__on_click_esci)
        btEsci.grid(column=1,row=0,padx=5,pady=5)

        self._root.mainloop()
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



p=ProdottoNuovo()
#c=CB("FFFFF")
#print(c.incrementa_esadecimale_ricorsivo())
