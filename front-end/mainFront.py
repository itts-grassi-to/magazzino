import tkinter as tk
import tkinter.messagebox as messagebox
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
target_module_dir = os.path.join(project_root, 'utilita')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)
target_module_dir = os.path.join(project_root, 'img')
if target_module_dir not in os.sys.path:
    os.sys.path.append(target_module_dir)

import globali as g
import menu as mn
import dbUtenti as dbu


class Main_front_pre():
    def __init__(self):
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
        self.__varUser.set("admin")  # Imposta l'utente inizialmente vuoto
        self.__txtUser = tk.Entry(self.__root, textvariable=self.__varUser)
        self.__txtUser.grid(row=0, column=1, padx=5, pady=10, sticky='W' )
        self.__txtUser.focus()
        #****************************************************************************************   Password
        self.__lblPsw = tk.Label(self.__root, text="Password")
        self.__lblPsw.grid(row=1, column=0, padx=5, pady=10, sticky='E' )
        self.__varPsw = tk.StringVar()
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
    def __cmdLogin(self):
        if self.__varUser.get() == "" or self.__varPsw.get() == "":
            messagebox.showerror("Errore", "Inserire user e/o password.")
            return
        obj = dbu.DB_utenti()
        if obj.isAutorizzato(self.__varUser.get(), self.__varPsw.get())==True:
            #print(g.logato)
            self.__root.destroy()
            # Avvia la finestra principale dell'applicazione
            main_window = Main_front()
            main_window.run()
            #messagebox.showinfo("Login eseguito","Login eseguito con successo.")
        else:
            messagebox.showerror("Errore", "User e/o password errati.")
            return
    def __cmdRegistrazione(self):
        messagebox.showinfo("Lavori in corso.")

    def run(self):
        self.__root.mainloop()

class Main_front():
    def __init__(self):
        self.__whidtBunner = 87
        self.__root = tk.Tk()
        self.__root.title("Magazzino")
        self.__root.geometry("800x300")
        self.__root.resizable(False, False)
        self.__root.grid()
        
        mn.Menu(self.__root,g.logato['RUOLO'])
        
        self.__wBunner = tk.Frame(self.__root, padx=1, pady=0)
        self.__wBunner.grid(row=0, column=0)
        self.__lblBunner = tk.Label(
            self.__wBunner, text=f"Sei logato come {g.logato['NOME'][:self.__whidtBunner]}", font=("Arial", 12,'bold'), bg="#6A0DAD",fg='white',width=self.__whidtBunner,height=1)
        self.__lblBunner.grid(row=0, column=0, padx=5, pady=10, sticky='NSWE' )
    def run(self):
        self.__root.mainloop()



if __name__=="__main__":
    #print("Starting mainInstallazione.py...")
    #inst.Installa().installa()
    m=Main_front_pre()
    m.run()
