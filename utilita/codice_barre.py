import barcode
from barcode.writer import ImageWriter

DIR_IMG_CB = "/home/daniele//Scrivania/tmp/"
#DIR_IMG_CB = ""

class CB:
    def __init__(self,cb=None):
        self.__cb=cb
        self.__opzioni = {
                'module_width': 0.15,   # Larghezza di base di una barra in mm
                'module_height': 5,   # Altezza delle barre in mm
                'font_size': 4,        # Dimensione del font per il testo sotto il barcode in mm
                'text_distance': 2,    # Distanza tra barcode e testo in mm
                'quiet_zone': 6,       # Moltiplicatore per la quiet zone (spazio bianco ai lati)
                'dpi': 300             # Risoluzione dell'immagine in DPI
            }    
    def set(self,cb):
        self.__cb = cb
    def incrementa_esadecimale_ricorsivo(self):
        """
        Incrementa di uno una cifra esadecimale rappresentata come lista di caratteri.

        Args:
            cifre_esadecimali: Una stringa da trasformare lista di stringhe, 
            dove ogni stringa è una cifra esadecimale
                            (es. ['0', '1', 'A', 'F']).

        Returns:
            Una nuova lista di stringhe rappresentante la cifra esadecimale incrementata.
        """
        self.__list_cifre_modificabile = list(self.__cb)
        # Dizionari per la conversione tra cifra esadecimale e intero
        self.__valori_esadecimali = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15
        }
        self.__cifre_da_valori = {v: k for k, v in self.__valori_esadecimali.items()}
        # Creiamo una copia della lista per evitare di modificare l'originale in place
        #list_cifre_modificabile = list(cifre_esadecimali)

        # Iniziamo la ricorsione dall'ultima cifra (la meno significativa)
        # aggiungendo il risultato del riporto iniziale (se c'è)
        risultato_riporto = self.__incrementa_ric(len(self.__list_cifre_modificabile) - 1)

        return ''.join(self.__list_cifre_modificabile)   
    def __incrementa_ric(self, index):
        '''
        # Caso base: se siamo fuori dall'inizio della lista, significa che abbiamo un riporto
        # che deve essere aggiunto come nuova cifra all'inizio (es. FFF + 1 = 1000)        
        if index < 0:
            return ['1'] + self.__list_cifre_modificabile # Aggiunge '1' all'inizio
        '''
        #cifra_corrente = self.__cifre_da_valori[(self.__list_cifre_modificabile[index])]
        #valore_cifra = self.__valori_esadecimali[cifra_corrente]
        valore_cifra = self.__valori_esadecimali[self.__list_cifre_modificabile[index]]
        # Incrementa la cifra corrente
        valore_incrementato = valore_cifra + 1

        # Se non c'è riporto (la cifra non supera F/15)
        if valore_incrementato < 16:
            self.__list_cifre_modificabile[index] = self.__cifre_da_valori[valore_incrementato]
            return []  # Nessun riporto, la ricorsione si ferma qui
        else:
            # C'è riporto (la cifra è diventata 16 o più)
            self.__list_cifre_modificabile[index] = '0'  # Resetta la cifra corrente a 0
            # Chiama ricorsivamente per gestire il riporto sulla cifra precedente
            return self.__incrementa_ric(index - 1)

    def genera_code128(self):
        """
        Genera un'immagine di un codice a barre Code 128 da una stringa data.

        Args:
            testo_da_codificare (str): La stringa alfanumerica da codificare (max 15 caratteri).
            nome_file_output (str): Il nome del file immagine di output (senza estensione).
        """

        nome_file_output=DIR_IMG_CB+f"cb{self.__cb}"
        testo_da_codificare = self.__cb
        if not isinstance(testo_da_codificare, str):
            print("Errore: Il testo da codificare deve essere una stringa.")
            return

        if len(testo_da_codificare) > 15:
            print(f"Avviso: Il testo fornito è più lungo di 15 caratteri ({len(testo_da_codificare)}).")
            print("Il Code 128 può gestire testi più lunghi, ma la richiesta specificava 15 caratteri.")
            # Non blocchiamo, ma avvisiamo l'utente. Il Code 128 gestirà comunque la lunghezza maggiore.

        # Rimuovi spazi iniziali/finali per evitare problemi imprevisti
        testo_da_codificare = testo_da_codificare.strip()

        # Verifica se il testo è vuoto dopo il trim
        if not testo_da_codificare:
            print("Errore: La stringa da codificare è vuota o contiene solo spazi.")
            return

        try:
            # Crea l'oggetto Code128
            # writer=ImageWriter() specifica che vogliamo un'immagine (PNG per default)
            codice_128 = barcode.Code128(testo_da_codificare, writer=ImageWriter())

            # Salva il codice a barre su un file
            # Il metodo save() aggiunge automaticamente l'estensione .png
            percorso_file = codice_128.save(nome_file_output,options=self.__opzioni)
            print(f"Codice a barre Code 128 generato e salvato come: {percorso_file}")
            

        except Exception as e:
            print(f"Si è verificato un errore durante la generazione del codice a barre: {e}")



#CB("000000000000001").genera_code128()

# --- Esempio di utilizzo ---

# Esempio 1: Stringa di 15 caratteri alfanumerici
#mia_stringa = "ABC123DEF456GHI"
#genera_code128(mia_stringa, "mio_codice_15_caratteri")

# Esempio 2: Stringa più corta
#altra_stringa = "TEST12345"
#genera_code128(altra_stringa, "mio_codice_corto")

# Esempio 3: Stringa con caratteri speciali (Code 128 li supporta)
#stringa_speciale = "A1_B2/C3*D4!"
#genera_code128(stringa_speciale, "mio_codice_speciale")

# Esempio 4: Stringa più lunga (verrà stampato un avviso)
#stringa_lunga = "QUESTA_E_UNA_STRINGA_MOLTO_LUNGA_CHE_SUPER_I_15_CARATTERI_MA_CODE128_LA_GESTISCE_LO_STESSO"
#genera_code128(stringa_lunga, "mio_codice_lungo")

# Esempio 5: Stringa vuota o non stringa (verrà gestito l'errore)
# genera_code128("", "codice_vuoto")
# genera_code128(12345, "codice_non_stringa")

