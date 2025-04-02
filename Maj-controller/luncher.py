import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

# Vérifier si le script est lancé en mode administrateur
if not is_admin():
    print("Relance du script en mode administrateur...")
    # Relancer le script en mode administrateur
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Définir le chemin du bureau
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Construire le chemin complet de l'exécutable à partir du bureau
exe_path = os.path.join(
    desktop_path,
    "Maj-controller",
    "SpotifyControllerApp",
    "Spotify",
    "__pycache__",
    "build-Maj",
    "Spotify-controller-Maj.exe"
)

# Vérifier si le fichier existe
if os.path.isfile(exe_path):
    print("Lancement de l'exécutable en mode administrateur...")
    # Lancer l'exécutable avec élévation
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    if result <= 32:
        print("Erreur lors du lancement de l'exécutable.")
else:
    print("Fichier non trouvé sur le bureau :", exe_path)
