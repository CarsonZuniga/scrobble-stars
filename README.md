# Scrobble Stars

Rates your Navidrome library using Last.fm global playcounts.  
Each track in an album gets 1–5 ★ based on its relative popularity, and ratings are synced back to Navidrome through the Subsonic API.  

## Configuration

Create a `.env` file in the project root with your settings:

```env
NAVIDROME_URL=http://localhost:4533/rest
NAVIDROME_USERNAME=your_username
NAVIDROME_PASSWORD=your_password
SUBSONIC_API_VERSION=1.16.1
CLIENT=scrobble-stars
LASTFM_API_KEY=your_lastfm_api_key
```

- **NAVIDROME_URL** – Navidrome server API URL (usually ends with `/rest`)  
- **NAVIDROME_USERNAME** / **NAVIDROME_PASSWORD** – Navidrome login  
- **SUBSONIC_API_VERSION** – API version (e.g. `1.16.1`)  
- **CLIENT** – client name that shows up in Subsonic logs  
- **LASTFM_API_KEY** – API key from [Last.fm](https://www.last.fm/api/account/create)  

## Run with Docker

Build and start the service:

```bash
docker compose up -d --build
```

Logs can be tailed with:

```bash
docker compose logs -f
```

The app will fetch albums from Navidrome, look up track playcounts on Last.fm, calculate ratings, and push them back.  
