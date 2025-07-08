import tkinter as tk
import tkinter.messagebox as messagebox

class Main_front():
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Magazzino")
        self.__root.geometry("400x300")
        self.__root.resizable(False, False)
        self.__root.grid()

        # Label
        self.__label = tk.Label(self.__root, text="Benvenuto nel sistema di gestione del magazzino!")
        self.__label.pack(pady=20)

        # Button to start installation
        self.__btnInstall = tk.Button(self.__root, text="Avvia Installazione", command=self.avviaInstallazione)
        self.__btnInstall.pack(pady=10)

    def avviaInstallazione(self):
        messagebox.showinfo("Installazione", "L'installazione del database è stata avviata.")

    def run(self):
        self.__root.mainloop()
if __name__=="__main__":
    #print("Starting mainInstallazione.py...")
    #inst.Installa().installa()
    m=Main_front()
    m.run()
