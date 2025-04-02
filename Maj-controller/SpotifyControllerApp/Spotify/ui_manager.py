import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import time
import subprocess
import sys
import os
from infi.systray import SysTrayIcon
from utils import log_error, scroll_text_if_needed
from audio_controller import get_spotify_volume
from spotify_manager import SpotifyAPI
from PIL import Image  # pour la redimension d'image

class SpotifyPopupUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spotify Info")
        self.enable_keys = True
        self.spotify_api = SpotifyAPI()
        self.setup_ui()
        self.setup_systray()
    
    def setup_ui(self):
        self.apply_rounded_corners()
        
        self.album_label = tk.Label(self.root, bg="#2b2b2b")
        self.album_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        
        self.title_label = tk.Label(self.root, text="", font=("Helvetica", 10, "bold"), fg="white", bg="#2b2b2b")
        self.title_label.grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))
        
        self.artist_label = tk.Label(self.root, text="", font=("Helvetica", 8), fg="gray", bg="#2b2b2b")
        self.artist_label.grid(row=1, column=1, sticky="w", padx=5)
        
        self.volume_label = tk.Label(self.root, text="", font=("Helvetica", 8), fg="white", bg="#2b2b2b")
        self.volume_label.grid(row=2, column=1, sticky="w", padx=5)
        
        self.time_label = tk.Label(self.root, text="", font=("Helvetica", 8), fg="white", bg="#2b2b2b")
        self.time_label.grid(row=3, column=1, sticky="w", padx=5, pady=(5, 0))
        
        self.progress_canvas = tk.Canvas(self.root, width=200, height=6, bg="#2b2b2b", highlightthickness=0)
        self.progress_canvas.grid(row=4, column=1, sticky="w", padx=5, pady=(0, 5))
        
        self.reset_button = tk.Button(
            self.root,
            text="Reinitialiser la popup",
            font=("Helvetica", 9),
            bg="#292929",
            fg="white",
            command=self.reset_popup
        )
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
    
    def apply_rounded_corners(self):
        try:
            self.root.geometry("300x100+1325+20")
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            self.root.attributes('-transparentcolor', '#1e1e1e')
            canvas_bg = tk.Canvas(self.root, width=300, height=100, bg="#1e1e1e", highlightthickness=0)
            canvas_bg.place(x=0, y=0)
            self.draw_rounded_rectangle(canvas_bg, 0, 0, 300, 100, radius=30, fill="#2b2b2b")
            canvas_bg.lower()
        except Exception as e:
            log_error(f"Erreur dans apply_rounded_corners : {e}")
    
    def draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def adjust_popup_size(self):
        try:
            self.root.update_idletasks()
            title_width = self.title_label.winfo_reqwidth()
            artist_width = self.artist_label.winfo_reqwidth()
            max_width = max(title_width, artist_width, 200)
            new_width = min(max_width + 500, 300)
            self.root.geometry(f"{new_width}x100+1335+20")
        except Exception as e:
            log_error(f"Erreur lors de l'ajustement de la taille de la popup : {e}")
    
    def update_popup_background(self, album_image_url):
        try:
            bg_color = "#000000"
            self.root.configure(bg=bg_color)
            self.album_label.configure(bg=bg_color)
            self.title_label.configure(bg=bg_color, fg="white")
            self.artist_label.configure(bg=bg_color)
            self.volume_label.configure(bg=bg_color)
            self.time_label.configure(bg=bg_color)
            self.progress_canvas.configure(bg=bg_color)
        except Exception as e:
            log_error(f"Erreur lors de la mise à jour du fond : {e}")
    
    def reset_popup(self):
        # Construction du chemin complet vers l'exécutable
        executable_path = os.path.join(os.path.expanduser("~"), "Documents", "SpotifyControllerApp", "Spotify", "main.py")
        print("Chemin de l'exécutable :", executable_path)
        
        # Vérifier que le fichier existe
        if os.path.exists(executable_path):
            try:
                # Utilisation de shell=True pour Windows, si nécessaire
                subprocess.Popen([executable_path], shell=True)
                print("Lancement réussi.")
                os._exit(0)
            except Exception as e:
                log_error(f"Erreur lors du lancement de '{executable_path}' : {e}")
        else:
            log_error(f"Fichier introuvable : {executable_path}")

    def update_popup(self):
        try:
            song_title, artist_name, progress_ms, duration_ms, album_image_url = self.spotify_api.get_current_song()
            spotify_volume = get_spotify_volume()
            
            scroll_text_if_needed(self.title_label, song_title if song_title else "Aucun titre")
            self.artist_label.config(text=artist_name if artist_name else "En attente d'un Artiste")
            self.volume_label.config(text=f"Volume : {spotify_volume}%" if spotify_volume is not None else "Volume")
            
            current_time = time.strftime("%M:%S", time.gmtime(progress_ms // 1000))
            total_time = time.strftime("%M:%S", time.gmtime(duration_ms // 1000))
            self.time_label.config(text=f"{current_time} / {total_time}")
            
            if duration_ms > 0:
                progress = (progress_ms / duration_ms) * 200
                self.progress_canvas.delete("progress")
                self.progress_canvas.create_rectangle(0, 0, progress, 6, fill="white", outline="", tags="progress")
            
            if album_image_url:
                response = requests.get(album_image_url, timeout=1)
                album_image = Image.open(BytesIO(response.content))
                album_image = album_image.resize((50, 50), Image.Resampling.LANCZOS)
                album_photo = ImageTk.PhotoImage(album_image)
                self.album_label.config(image=album_photo)
                self.album_label.image = album_photo
            
            self.adjust_popup_size()
            self.root.after(500, self.update_popup)
        except Exception as e:
            log_error(f"Erreur lors de la mise à jour de la popup : {e}")
    
    def setup_systray(self):
        menu_options = (
            ("Afficher", None, lambda systray: self.root.deiconify()),
            ("Masquer", None, lambda systray: self.root.withdraw()),
            ("Reinitialiser la popup", None, lambda systray: self.reset_popup()),
            ("Activer/Désactiver les touches", None, self.toggle_keys),
        )
        self.systray = SysTrayIcon("icon.ico", "Spotify Manager", menu_options, on_quit=lambda systray: self.root.quit())
        self.systray.start()
    
    def toggle_keys(self, systray=None):
        self.enable_keys = not self.enable_keys
        menu_options = (
            ("Afficher", None, lambda systray: self.root.deiconify()),
            ("Masquer", None, lambda systray: self.root.withdraw()),
            ("Reinitialiser la popup", None, lambda systray: self.reset_popup()),
            ("Activer les touches" if not self.enable_keys else "Désactiver les touches", None, self.toggle_keys),
        )
        self.systray.update(menu_options)
    
    def run(self):
        self.update_popup()
        self.root.mainloop()

if __name__ == "__main__":
    app = SpotifyPopupUI()
    app.run()
