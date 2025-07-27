SVILUPPO = False
if SVILUPPO:
    
    import pickle
    try:
        with open('config', 'rb') as f:
            gdbms=loaded_dictionary = pickle.load(f)
    except FileNotFoundError:
       print("Apertura file di configurazione Configurazione fallita in sviluppo")
    
    logato={
        "ID": 1,
        "NOME": "Sviluppo",
        "COGNOME":"",
        "RUOLO" : 100
    }
else:
    logato={}

gdbms = {}
stato={
    "DISPONIBILE":1,
    "NON DISPONIBILE":2,
    "EVASO":3
}
ruoli = {
            "AMMINISTRATORE": 1,
            "OPERATORE": 100,
            "VISUALIZZATORE": 1000
        }
def is_number(s):
    s=s.replace(",",".")
    try:
        float(s)  # Tenta di convertire in float
        return True
    except ValueError:
        return False
#is_number("7,5")
