# mainInstallazione.py
# creato by Daniele Ortu
# daniele.ortu@itisgrassi.edu.it

import sys
import os


# Ottieni il percorso della directory corrente di main_script.py ('avvio')
current_dir = os.path.dirname(os.path.abspath(__file__))

# Risali di un livello per arrivare alla directory 'tuo_progetto'
# Da 'avvio', vogliamo andare su per arrivare a 'tuo_progetto'
# e poi scendere in 'un_altra_cartella'
project_root = os.path.dirname(current_dir)

# Costruisci il percorso completo della cartella che contiene 'nome_modulo.py'
target_module_dir = os.path.join(project_root, 'utilita')
# Aggiungi questa directory al sys.path
sys.path.append(target_module_dir)


#import installazione as inst
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter import scrolledtext 
from tkinter import filedialog
import datetime


import utility as db
import dbRuoli as dbr
import dbUtenti as dbu
import dbCategorie as dbc
import dbSpecifiche as dbs
import dbProdotti as dbp
import dbAsset as dba
import dbAssegnare as dbasg
import globali as gb
import pickle

import hashlib

class Main():
    def on_click_seldir(self,event):
        directory_selezionata = filedialog.askdirectory()
        if directory_selezionata:
            self.__valSelDir.set(directory_selezionata)
    def __avviaInstallazione(self):
        try:
            #print("Starting installation...")
            self.__msgTxt("Avvio installazione ...")
            self.__incPB=self.__progressbar['maximum']/8
            if not self.__creaConfigurazione():
                return
            
            #************************************************************************************** tabella ruoli
            self.__msgTxt("Creo tabella ruoli")
            obj=dbr.DB_ruoli()
            e,msg = obj._creaTabellaRuoli()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            self.__msgTxt("Inserisco i ruoli di base")
            e,msg=obj._inserisciRuoliBase()
            if e:
                self.__msgTxt(msg)
                return            
            #************************************************************************************** tabella utenti
            self.__msgTxt("Creo tabella utenti")
            obj=dbu.DB_utenti()
            e,msg = obj._creaTabellaUtenti()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            self.__msgTxt("Inserisco utente admin")
            e,msg=obj._inserisciUtente("Amministratore", "Sistema", "admin", hashlib.md5("ortu".encode()).hexdigest(), 1,1)
            if e:
                self.__msgTxt(msg)
                return
            #************************************************************************************** tabella categorie
            self.__msgTxt("Creo tabella categorie")
            obj=dbc.DB_categorie()
            e,msg = obj._creaTabellaCategorie()
            if e:
                self.__msgTxt(msg)
                return
            e,msg=obj._inserisciCategorieBase()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            #************************************************************************************** tabella prodotti
            self.__msgTxt("Creo tabella prodotti")
            obj=dbp.DB_prodotti()
            e,msg = obj._creaTabellaProdotti()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            #***************************************************************************** tabella specifiche
            self.__msgTxt("Creo tabella specifiche")
            obj=dbs.DB_specifiche()
            e,msg = obj._creaTabellaSpecifiche()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            #***************************************************************************** tabella asset_older
            self.__msgTxt("Creo tabella degli asset older")
            obj=dba.DB_asset()
            e,msg = obj._creaTabellaAsset()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            #***************************************************************************** tabella tbAssegnare
            self.__msgTxt("Creo tabella assegnare")
            obj=dbasg.DB_assegnare()
            e,msg = obj._creaTabellaAssegnare()
            if e:
                self.__msgTxt(msg)
                return
            self.__progressbar['value']+= self.__incPB
            #************************************************************************************** fine
            self.__progressbar['value'] = 100
            self.__msgTxt("Installazione completata con successo.")
            self.__msgTxt("**************************************\n\n")
            #self.__txtLog.see(tk.END)
            messagebox.showinfo("Installazione completata", "L'installazione del database è stata completata con successo.")
        except Exception as e:
            self.__txtLog.insert(tk.END, f"Errore durante l'installazione: {e}\n\n")
            messagebox.showerror("Errore", f"Si è verificato un errore durante l'installazione: {e}")
        finally:
            self.__progressbar.stop()
            #self.__root.quit()
    def on_click_crea_configurazione(self):
        self.__creaConfigurazione()
    def __init__(self):
        super().__init__()
        w=750
        h=450
        self.__root=root=tk.Tk()
        root.geometry(str(w)+"x"+str(h))
        root.title("Installazione database Magazzino")
        root.resizable(False, True) 
        #root.iconbitmap(os.path.join(project_root, 'img', 'favicon-16x16.png'))
        root.grid()
        #*************************************************************************** DATA BASE
        frDB =tk.Frame(root,width=int(w),height=int(h)/3)
        frDB.grid(column=0,row=0,padx=5,pady=5,sticky="NSEW")
        #************************************************** indirizzo server
        lbIndirizzo=tk.Label(frDB,text="Indirizzo DBMS")
        lbIndirizzo.grid(column=0,row=0,padx=2,pady=5,sticky="E")
        self.valIndirizzo=tk.StringVar()
        self.valIndirizzo.set( "192.168.1.117" if gb.SVILUPPO  else "")
        txtIndirizzo=tk.Entry(frDB,textvariable=self.valIndirizzo,justify="center",width=20)
        txtIndirizzo.grid(column=1,row=0,pady=5,sticky="W")
        #************************************************** separatore
        #lbs=tk.Label(frDB,text="                            ",bg="black",font=("Arial", 2, "bold"))
        #lbs.grid(column=2,row=0,padx=10)
        #************************************************** user
        lbUser=tk.Label(frDB,text="    User")
        lbUser.grid(column=3,row=0,padx=2,pady=5,sticky="E")
        self.valUser=tk.StringVar()
        self.valUser.set( "dortu" if gb.SVILUPPO  else "")
        txtUser=tk.Entry(frDB,textvariable=self.valUser,justify="center",width=20)
        txtUser.grid(column=4,row=0,pady=5,sticky="W")
        #************************************************** Password
        lbPassword=tk.Label(frDB,text="    Password")
        lbPassword.grid(column=6,row=0,padx=1,pady=5,sticky="E")
        self.valPassword=tk.StringVar()
        self.valPassword.set( "ortu" if gb.SVILUPPO  else "")
        txtPassword=tk.Entry(frDB,textvariable=self.valPassword,justify="center",width=20,show='*')
        txtPassword.grid(column=7,row=0,pady=5,sticky="W")
        #************************************************** seleziona directory
        self.txtDir="Clicca qua per selezionare la directory d'installazione"
        self.__valSelDir=tk.StringVar()
        self.__valSelDir.set(self.txtDir)
        txtSelDir=tk.Entry(frDB,textvariable=self.__valSelDir, state="readonly")
        txtSelDir.grid(column=0,row=1,columnspan=8,pady=10,padx=20,sticky="WE")
        txtSelDir.bind("<Button-1>", self.on_click_seldir)
        #************************************************** progress bar
        # Creazione del widget Progressbar in modalità 'indeterminate'
        self.__progressbar = ttk.Progressbar(
            root, 
            orient='horizontal', 
            length=w-10, 
            mode='determinate'
        )
        self.__progressbar['value'] = 0 # Imposta il progresso al 50%
        self.__progressbar['maximum'] = 100 # Imposta il massimo a 100
        self.__progressbar.grid(row=2,column=0,padx=5,pady=10,sticky='EW')

        self.__ps=tk.Frame(root,padx=5,pady=5)
        self.__ps.grid(row=1,column=0)
        self.__ps.grid_columnconfigure(0, weight=1)
        self.__ps.grid_rowconfigure(0, weight=1)   
        btEsci=tk.Button(self.__ps,text="Esci",command=root.quit)
        btEsci.grid(row=0,column=0,sticky='EW',padx=5,pady=5)
        btAvvia=tk.Button(self.__ps,text="Avvia",command=self.__avviaInstallazione)
        btAvvia.grid(row=0,column=1,sticky='EW',padx=5,pady=5)  
        btConf=tk.Button(self.__ps,text="Crea file di configurazione",command=self.on_click_crea_configurazione)
        btConf.grid(row=0,column=2,sticky='EW',padx=5,pady=5)  

        self.__txtLog = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15,
                                      font=("Arial", 10), bd=2, relief=tk.GROOVE)
        self.__txtLog.grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')
    def __msgTxt(self,msg):
        self.__txtLog.insert(tk.END, datetime.datetime.now().strftime("%H:%M:%S")+": "+msg+"\n")
        self.__txtLog.see(tk.END)
    def __creaConfigurazione(self):
        if not self.__possoProseguire():
            return False
        file_name= gb.gdbms["dir"]+"/"+gb.gdbms["nome_FC"]
        try:
            with open(file_name, 'wb') as f:
                pickle.dump(gb.gdbms, f)
            print(f"Dizionario salvato con successo in '{file_name}'")
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")    
            return False
    def run(self):
        self.__root.mainloop()    
    def __possoProseguire(self):

        gb.gdbms={
            "host": self.valIndirizzo.get(),
            "nome_schema": "inventario",
            "user": self.valUser.get(),
            "password": self.valPassword.get(),
            "dir": self.__valSelDir.get(),
            "nome_FC":"config"
        }

        obj = db.DB(gb.gdbms)
        r =obj.connect()
        if obj.connection==None:
            messagebox.showerror("WEEE",r)
            return False
        if obj.connection.is_connected():
            obj.connection.close()
        if self.__valSelDir.get()==self.txtDir:
            messagebox.showerror("WEEE","Inserisci la directori di installazione")
            return False
        return True 
if __name__=="__main__":
    #print("Starting mainInstallazione.py...")
    #inst.Installa().installa()
    m=Main()
    m.run()
