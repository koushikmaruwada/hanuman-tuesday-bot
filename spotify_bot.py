import os
import datetime
import time
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# === Load values from .env file ===
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

HANUMAN_PLAYLIST_URI = os.getenv("HANUMAN_PLAYLIST_URI")
OTHER_PLAYLIST_URIS = os.getenv("OTHER_PLAYLIST_URIS", "").split(",")

# === Setup authentication ===
scope = "user-read-playback-state user-modify-playback-state"

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    ))
except Exception as e:
    print(f"❌ Spotify auth failed: {e}")
    exit()

# === Function: Get active device ID ===
def get_active_device():
    try:
        devices = sp.devices()
        if devices['devices']:
            return devices['devices'][0]['id']
        print("⚠️ No active Spotify device found. Open Spotify on your phone or PC.")
        return None
    except Exception as e:
        print(f"❌ Failed to fetch devices: {e}")
        return None

# === Function: Start playback ===
def play_playlist(uri):
    device_id = get_active_device()
    if not device_id:
        print("⏳ Waiting for Spotify device to appear...")
        for _ in range(6):
            time.sleep(5)
            device_id = get_active_device()
            if device_id:
                break
        if not device_id:
            print("❌ Still no device. Exiting.")
            return
    try:
        sp.start_playback(device_id=device_id, context_uri=uri)
        print(f"🎶 Playing: {uri}")
    except Exception as e:
        print(f"⚠️ Failed to start playback: {e}")

# === Main logic based on day ===
today = datetime.datetime.today().strftime('%A')
print(f"📅 Today is {today}")

if today == "Tuesday":
    print("🙏 Playing Hanuman playlist.")
    play_playlist(HANUMAN_PLAYLIST_URI)
else:
    print("🎵 Playing regular playlists.")
    for uri in OTHER_PLAYLIST_URIS:
        if uri.strip():
            play_playlist(uri.strip())
            time.sleep(5)
