# mainInstallazione.py
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
import datetime

import utility as db
import globali as gb
import hashlib

class Main():
    def __avviaInstallazione(self):
        try:
            print("Starting installation...")
            self.__incPB=self.__progressbar['maximum']/5

            self.__msgTxt("Creo tabella ruoli")
            obj=db.DB_ruoli()
            obj._creaTabellaRuoli()
            self.__progressbar['value']+= self.__incPB
            self.__msgTxt("Inserisco i ruoli di base")
            t=obj._inserisciRuolo(1,"AMMINISTRATORE")
            if t!="":
                self.__msgTxt("Errore durante l'inserimento del ruolo AMMINISTRATORE: "+t)
                return
            self.__msgTxt("Creo tabella utenti")
            #self._creaTabella(0,"utenti",self.__creaTabellaUtenti() )
            self.__msgTxt("Inserisco utente admin")
            #self._creaTabella(1,"utenti",self.__inserisciUtenteAdmin())
            
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
    def __init__(self):
        super().__init__()
        wl=500
        self.__root=root=tk.Tk()
        root.geometry(str(wl)+"x500")
        root.title("Installazione database Magazzino")
        root.resizable(False, False) 
        #root.iconbitmap(os.path.join(project_root, 'img', 'favicon-16x16.png'))
        root.grid()
        
        # Creazione del widget Progressbar in modalità 'indeterminate'
        self.__progressbar = ttk.Progressbar(
            root, 
            orient='horizontal', 
            length=wl-10, 
            mode='determinate'
        )
        self.__progressbar['value'] = 0 # Imposta il progresso al 50%
        self.__progressbar['maximum'] = 100 # Imposta il massimo a 100
        self.__progressbar.grid(row=0,column=0,padx=5,pady=50,sticky='EW')

        self.__ps=tk.Frame(root,padx=5,pady=5)
        self.__ps.grid(row=1,column=0)
        self.__ps.grid_columnconfigure(0, weight=1)
        self.__ps.grid_rowconfigure(0, weight=1)   
        btEsci=tk.Button(self.__ps,text="Esci",command=root.quit)
        btEsci.grid(row=0,column=0,sticky='EW',padx=5,pady=5)
        btAvvia=tk.Button(self.__ps,text="Avvia",command=self.__avviaInstallazione)
        btAvvia.grid(row=0,column=1,sticky='EW',padx=5,pady=5)  

        self.__txtLog = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15,
                                      font=("Arial", 10), bd=2, relief=tk.GROOVE)
        self.__txtLog.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')
    def __inserisciRuoliBase(self):
        r = "INSERT INTO `tbRuolo` (`idRuolo`, `descrizione`) VALUES "
        for rl in gb.ruoli:
            r += f"({gb.ruoli[rl]}, '{rl}'), "
        r = r[:-2] + ";"
        return r
    def __creaTabellaUtenti(self):
        return " \
                    CREATE TABLE IF NOT EXISTS `tbUtenti` ( \
                    `idtbUtenti` int(11) NOT NULL AUTO_INCREMENT,\
                    `nome` varchar(100) NOT NULL,\
                    `cognome` varchar(100) NOT NULL,\
                    `budge` varchar(45) DEFAULT NULL,\
                    `user` varchar(45) NOT NULL,\
                    `password` char(32) NOT NULL,\
                    `fkRuolo` int(11) NOT NULL,\
                    PRIMARY KEY (`idtbUtenti`),\
                    KEY `fk_tbUtenti_1_idx` (`fkRuolo`),\
                    CONSTRAINT `fk_tbUtenti_1` FOREIGN KEY (`fkRuolo`) REFERENCES `tbRuolo` (`idRuolo`) ON DELETE NO ACTION ON UPDATE NO ACTION\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\
                "
    def __inserisciUtenteAdmin(self):
        r = "INSERT INTO `tbUtenti` ( `nome`, `cognome`, `user`, `password`, `fkRuolo`) VALUES  \
            ('Amministratore', 'Sistema','admin', '"+hashlib.md5("ortu".encode()).hexdigest()+"', 1);"
        print(r)
        return r
    def __msgTxt(self,msg):
        self.__txtLog.insert(tk.END, datetime.datetime.now().strftime("%H:%M:%S")+": "+msg+"\n")
        self.__txtLog.see(tk.END)
    def run(self):
        self.__root.mainloop()    
            
if __name__=="__main__":
    #print("Starting mainInstallazione.py...")
    #inst.Installa().installa()
    m=Main()
    m.run()
