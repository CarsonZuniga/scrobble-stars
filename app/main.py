import time
from app.config import SLEEP_TIME_SECONDS
from app.subsonic import get_all_albums, get_songs, set_rating
from app.last_fm import get_track_listens
import statistics
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def get_stars(plays, counts):
    mean = statistics.mean(counts)
    stdev = statistics.pstdev(counts) or 1  # avoid div0
    z = (plays - mean) / stdev

    # map z-score into 1–5
    if z <= -1.0:
        return 1
    elif z <= -0.5:
        return 2
    elif z < 0.5:
        return 3
    elif z < 1.0:
        return 4
    else:
        return 5

def main():
    while True:
        try:
            albums = get_all_albums()
            for album in albums:
                try:
                    logger.info(f"Album: {album['name']}")
                    songs = get_songs(album['id'])
                    track_titles = [song['title'] for song in songs]
                    playcounts = get_track_listens(album['artist'], album['name'], track_titles)
                    max_count = max(playcounts.values() or [0])
                    if max_count == 0:
                        continue
                    for song in songs:
                        title = song["title"]
                        track_id = song["id"]
                        plays = playcounts.get(title, 0)

                        # Relative rating (most popular track = 5★)
                        stars = get_stars(plays, playcounts.values())
                        logger.info(f". {title} -> plays={plays}, rating={stars}★")
                        try:
                            set_rating(track_id, stars)
                        except Exception as e:
                            logger.warning(f"  Failed to set rating: {e}")
                except Exception as e:
                    logger.error(f"Error processing album {album['name']}: {e}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")

        time.sleep(SLEEP_TIME_SECONDS)

if __name__ == "__main__":
    main()
