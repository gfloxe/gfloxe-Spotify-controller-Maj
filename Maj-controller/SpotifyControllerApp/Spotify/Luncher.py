import subprocess
import sys
import os

if __name__ == '__main__':
    # Construction du chemin absolu vers main.py dans le dossier Documents de l'utilisateur
    script_path = os.path.join(os.path.expanduser("~"), "Documents", "SpotifyControllerApp", "Spotify", "main.py")
    
    # Lancement du script sans ouvrir de fenêtre de terminal (spécifique à Windows)
    subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NO_WINDOW)
