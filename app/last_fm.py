import requests
import threading
import time
from app.config import LASTFM_API_KEY

_rate_limit_lock = threading.Lock()
_request_timestamps = []

def _rate_limited_request():
    with _rate_limit_lock:
        now = time.time()
        # Remove timestamps older than 1 second
        global _request_timestamps
        _request_timestamps = [t for t in _request_timestamps if now - t < 1]
        if len(_request_timestamps) >= 5:
            # Wait until we can make a new request
            sleep_time = 1 - (now - _request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            now = time.time()
            _request_timestamps = [t for t in _request_timestamps if now - t < 1]
        _request_timestamps.append(time.time())


def get_track_listens(artist: str, album: str, track_titles: list[str]):
    """
    Fetches Last.fm playcounts for each track in an album.
    Returns a dict: {track_title: playcount}
    """
    base_url = "http://ws.audioscrobbler.com/2.0/"
    results = {}
    for track in track_titles:
        _rate_limited_request()
        params = {
            "method": "track.getInfo",
            "api_key": LASTFM_API_KEY,
            "artist": artist,
            "track": track,
            "format": "json"
        }
        resp = requests.get(base_url, params=params)
        data = resp.json()
        playcount = None
        if "track" in data and "playcount" in data["track"]:
            playcount = int(data["track"]["playcount"])
        results[track] = playcount
    return results
