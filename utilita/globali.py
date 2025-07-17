SVILUPPO = True
if SVILUPPO:
    import pickle
    try:
        with open('config', 'rb') as f:
            gdbms=loaded_dictionary = pickle.load(f)
        logato={
            "ID": 1,
            "NOME": "Sviluppo",
            "COGNOME":"",
            "RUOLO" : 100
        }
    except FileNotFoundError:
       print("Configurazione fallita in sviluppo")
else:
    gdbms = {}
    logato={}
ruoli = {
            "AMMINISTRATORE": 1,
            "OPERATORE": 100,
            "VISUALIZZATORE": 1000
        }

