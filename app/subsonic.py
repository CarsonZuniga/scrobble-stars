import requests
from app.config import NAVIDROME_URL, USERNAME, PASSWORD, API_VERSION, CLIENT


def get_all_albums():
    albums = []
    offset = 0
    page_size = 200  # Navidrome supports up to 200 per request

    while True:
        params = {
            "u": USERNAME,
            "p": PASSWORD,
            "v": API_VERSION,
            "c": CLIENT,
            "type": "alphabeticalByName",
            "size": page_size,
            "offset": offset,
            "f": "json"
        }
        resp = requests.get(f"{NAVIDROME_URL}/getAlbumList", params=params)
        data = resp.json()["subsonic-response"]

        # Break if no albumList
        if "albumList" not in data or "album" not in data["albumList"]:
            break

        page_albums = data["albumList"]["album"]
        albums.extend(page_albums)

        # If fewer than page_size returned, we’ve reached the end
        if len(page_albums) < page_size:
            break

        offset += page_size

    return albums

def get_songs(album_id):
    params = {
        "u": USERNAME,
        "p": PASSWORD,
        "v": API_VERSION,
        "c": CLIENT,
        "id": album_id,
        "f": "json"
    }
    resp = requests.get(f"{NAVIDROME_URL}/getAlbum", params=params)
    return resp.json()["subsonic-response"]["album"]["song"]

def set_rating(item_id: str, rating: int) -> None:
    """
    Push a rating (1-5) to Navidrome/Subsonic for a song or album.
    """
    rating = max(1, min(5, int(rating)))
    params = {
        "u": USERNAME,
        "p": PASSWORD,
        "v": API_VERSION,
        "c": CLIENT,
        "id": item_id,
        "rating": rating,
        "f": "json",
    }
    resp = requests.get(f"{NAVIDROME_URL}/setRating", params=params, timeout=15)
    data = resp.json().get("subsonic-response", {})
    if data.get("status") != "ok":
        raise RuntimeError(f"setRating failed: {data}")
