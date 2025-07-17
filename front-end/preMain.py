import tkinter as tk
import tkinter.messagebox as messagebox
import os
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
target_module_dir = os.path.join(project_root, 'utilita')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)
target_module_dir = os.path.join(project_root, 'img')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)

import sviluppo as g
import globali as gb
import dbUtenti as dbu
import mainFront as mnf

class Main_front_pre():
    def __init__(self):
    #def run(self):
        self.__root = tk.Tk()
        self.__root.title("Magazzino")
        self.__root.geometry("400x300")
        self.__root.resizable(False, False)
        self.__root.grid()

        #icon_path =project_root+"/img/favicon.ico"
        #icon_path = current_dir+"/favicon.ico"
        #self.__root.iconbitmap(icon_path)

        #****************************************************************************************   User
        self.__lblUser = tk.Label(self.__root, text="User")
        self.__lblUser.grid(row=0, column=0, padx=5, pady=10, sticky='E' )
        self.__varUser = tk.StringVar()
        if g.SVILUPPO:
            self.__varUser.set("admin")  # Imposta l'utente inizialmente vuoto
        self.__txtUser = tk.Entry(self.__root, textvariable=self.__varUser)
        self.__txtUser.grid(row=0, column=1, padx=5, pady=10, sticky='W' )
        self.__txtUser.focus()
        #****************************************************************************************   Password
        self.__lblPsw = tk.Label(self.__root, text="Password")
        self.__lblPsw.grid(row=1, column=0, padx=5, pady=10, sticky='E' )
        self.__varPsw = tk.StringVar()
        if g.SVILUPPO:
            self.__varPsw.set("ortu")  # Imposta la password inizialmente vuota
        self.__txtPsw = tk.Entry(self.__root, textvariable=self.__varPsw, show='*')
        self.__txtPsw.grid(row=1, column=1, padx=5, pady=10, sticky='W' )

        #**************************************************************************************** Pulsanti
        self.__f1= tk.Frame(self.__root, padx=1, pady=5,width=400, height=200)
        self.__f1.grid(row=2, column=0, columnspan=2, sticky='EW')
        self.__f1.grid_columnconfigure(0, weight=1)
        self.__f1.grid_rowconfigure(0, weight=1)
        #******************************************************************** Pulsante Login
        self.__btnLogin = tk.Button(self.__f1, text="Login", command=self.__cmdLogin)
        self.__btnLogin.grid(row=3, column=0, padx=5, pady=10)
        #******************************************************************** Pulsante registrazione
        self.__btnRegistrazione = tk.Button(self.__f1, text="Registrazione", command=self.__cmdRegistrazione)
        self.__btnRegistrazione.grid(row=3, column=1, padx=10, pady=10,sticky='E')
        #******************************************************************** Pulsante Esci
        self.__btnEsci = tk.Button(self.__f1, text="Esci", command=self.__root.quit)
        self.__btnEsci.grid(row=3, column=2,padx=1, pady=10)
        self.__root.mainloop()
    def __cmdLogin(self):
        if self.__varUser.get() == "" or self.__varPsw.get() == "":
            messagebox.showerror("Errore", "Inserire user e/o password.")
            return
        obj = dbu.DB_utenti()
        autorizzato,dati=obj.isAutorizzato(self.__varUser.get(), self.__varPsw.get())
        if autorizzato:
            #print(dati)
            self.__root.destroy()
            gb.logato["ID"] = dati[obj.getCampo(0)]
            gb.logato['NOME'] = dati[obj.getCampo(1)]+" "+dati[obj.getCampo(2)]
            gb.logato['RUOLO'] = dati[obj.getCampo(6)]
            #self.__root.destroy()      
            # Avvia la finestra principale dell'applicazione
            main_window = mnf.Main_front()
            #main_window.run()
            #messagebox.showinfo("Login eseguito","Login eseguito con successo.")
        else:
            messagebox.showerror("Errore", dati)
            return
    def __cmdRegistrazione(self):
        messagebox.showinfo("Lavori in corso.")
    def run(self):
        self.__root.mainloop()



if __name__=="__main__":
    try:
        with open('config', 'rb') as f:
            gb.gdbms=loaded_dictionary = pickle.load(f)
        m=Main_front_pre()
        m.run()
    except FileNotFoundError:
       messagebox.showerror("File configurazione","Il file di configurazione non è stato installato.\nRivolgersi all'amministratore")
    except Exception as e:
        messagebox.showerror("File configurazione","Il file di configurazione non è stato installato.\nRivolgersi all'amministratore")
    
    
