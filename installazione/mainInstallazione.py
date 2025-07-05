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

import installazione as inst

if __name__=="__main__":
    print("Starting mainInstallazione.py...")
    inst.Installa().installa()
