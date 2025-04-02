from pynput import keyboard
from audio_controller import set_spotify_volume, skip_spotify_track
from ui_manager import SpotifyPopupUI
from utils import log_error

def on_press(key, ui):
    try:
        if not ui.enable_keys:
            return
        if key == keyboard.Key.up:
            set_spotify_volume("volume_up")
        elif key == keyboard.Key.down:
            set_spotify_volume("volume_down")
        elif key == keyboard.Key.right:
            skip_spotify_track("next")
        elif key == keyboard.Key.left:
            skip_spotify_track("previous")
    except Exception as e:
        log_error(f"Erreur Listener : {e}")

def main():
    ui = SpotifyPopupUI()
    listener = keyboard.Listener(on_press=lambda key: on_press(key, ui))
    listener.start()
    try:
        ui.run()
    finally:
        listener.stop()

if __name__ == "__main__":
    main()
