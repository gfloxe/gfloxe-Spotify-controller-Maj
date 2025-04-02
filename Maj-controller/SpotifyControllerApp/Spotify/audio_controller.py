from comtypes import CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pyautogui
from utils import log_error

def get_spotify_volume():
    try:
        CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                return int(volume.GetMasterVolume() * 100)
        return None
    except Exception as e:
        log_error(f"Erreur lors de la récupération du volume : {e}")
        return None
    finally:
        CoUninitialize()

def set_spotify_volume(action):
    try:
        CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                current_volume = volume.GetMasterVolume()
                if action == "volume_up":
                    volume.SetMasterVolume(min(current_volume + 0.025, 1.0), None)
                elif action == "volume_down":
                    volume.SetMasterVolume(max(current_volume - 0.025, 0.0), None)
                return
    except Exception as e:
        log_error(f"Erreur lors de l'ajustement du volume : {e}")
    finally:
        CoUninitialize()

def skip_spotify_track(action):
    try:
        if action == "next":
            pyautogui.press("nexttrack")
        elif action == "previous":
            pyautogui.press("prevtrack")
    except Exception as e:
        log_error(f"Erreur lors du changement de piste : {e}")
