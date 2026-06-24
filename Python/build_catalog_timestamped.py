import re
import os
import requests
import textwrap
import time



# CONFIG
OUTPUT_DIR = "SD_CARD"
LCD_COLS   = 16
DELAY      = 1   # seconds between API calls (be polite to free API)
FAILED_LOG = "failed_downloads.txt"
# ─────────────────────────────────────────────────────────────────────────────



albums = [
    {"id": "001", "artist": "Ariana Grande",       "title": "Dangerous Woman"},
    {"id": "002", "artist": "Ariana Grande",       "title": "Thank U, Next"},
    {"id": "003", "artist": "Bad Bunny",           "title": "Debí Tirar Más Fotos"},
    {"id": "004", "artist": "Beyonce",             "title": "Lemonade"},
    {"id": "005", "artist": "Beyonce",             "title": "Renaissance"},
    {"id": "006", "artist": "Beyonce",             "title": "Cowboy Carter"},
    {"id": "007", "artist": "Billie Eilish",       "title": "Don't Smile at Me"},
    {"id": "008", "artist": "Billie Eilish",       "title": "When We All Fall Asleep, Where Do We Go?"},
    {"id": "009", "artist": "Billie Eilish",       "title": "Happier Than Ever"},
    {"id": "010", "artist": "Chappell Roan",       "title": "The Rise and Fall of a Midwest Princess"},
    {"id": "011", "artist": "Charli XCX",          "title": "Number 1 Angel"},
    {"id": "012", "artist": "Conan Gray",          "title": "Superache"},
    {"id": "013", "artist": "Fall Out Boy",        "title": "Mania"},
    {"id": "014", "artist": "Hayley Williams",     "title": "Petals for Armor"},
    {"id": "015", "artist": "Hayley Williams",     "title": "Flowers for Vases"},
    {"id": "016", "artist": "Hayley Williams",     "title": "Ego Death at a Bachelorette Party"},
    {"id": "017", "artist": "Josh Conway",         "title": "Plum"},
    {"id": "018", "artist": "Khalid",              "title": "American Teen"},
    {"id": "019", "artist": "Khalid",              "title": "Free Spirit"},
    {"id": "020", "artist": "Laufey",              "title": "Bewitched: The Goddess Edition"},
    {"id": "021", "artist": "Laufey",              "title": "A Night at the Symphony: Hollywood Bowl"},
    {"id": "022", "artist": "Lorde",               "title": "Pure Heroine"},
    {"id": "023", "artist": "Lorde",               "title": "Melodrama"},
    {"id": "024", "artist": "The Marias",          "title": "Superclean Vol. I"},
    {"id": "025", "artist": "The Marias",          "title": "Superclean Vol. II"},
    {"id": "026", "artist": "The Marias",          "title": "Cinema"},
    {"id": "027", "artist": "The Marias",          "title": "Submarine"},
    {"id": "028", "artist": "The Marias",          "title": "Nobody New"},
    {"id": "029", "artist": "The Marias",          "title": "Back to Me"},
    {"id": "030", "artist": "Michael Jackson",     "title": "Thriller"},
    {"id": "031", "artist": "My Chemical Romance", "title": "Three Cheers for Sweet Revenge"},
    {"id": "032", "artist": "My Chemical Romance", "title": "The Black Parade"},
    {"id": "033", "artist": "My Chemical Romance", "title": "The Black Parade Is Dead!"},
    {"id": "034", "artist": "Not For Radio",       "title": "Melt"},
    {"id": "035", "artist": "Not For Radio",       "title": "Bloom"},
    {"id": "036", "artist": "Olivia Rodrigo",      "title": "you seem pretty sad for a girl so in love"},
    {"id": "037", "artist": "Panic! at the Disco", "title": "A Fever You Can't Sweat Out"},
    {"id": "038", "artist": "Paramore",            "title": "All We Know Is Falling"},
    {"id": "039", "artist": "Paramore",            "title": "Riot!"},
    {"id": "040", "artist": "Paramore",            "title": "Decode"},
    {"id": "041", "artist": "Paramore",            "title": "I Caught Myself"},
    {"id": "042", "artist": "Paramore",            "title": "Brand New Eyes"},
    {"id": "043", "artist": "Paramore",            "title": "Paramore"},
    {"id": "044", "artist": "Paramore",            "title": "After Laughter"},
    {"id": "045", "artist": "Paramore",            "title": "This Is Why"},
    {"id": "046", "artist": "Pierce the Veil",     "title": "A Flair for the Dramatic"},
    {"id": "047", "artist": "Pierce the Veil",     "title": "Selfish Machines"},
    {"id": "048", "artist": "Pierce the Veil",     "title": "Collide with the Sky"},
    {"id": "049", "artist": "Pierce the Veil",     "title": "Misadventures"},
    {"id": "050", "artist": "Pierce the Veil",     "title": "The Jaws of Life"},
    {"id": "051", "artist": "Sabrina Carpenter",   "title": "Short n' Sweet (Deluxe)"},
    {"id": "052", "artist": "System of a Down",    "title": "System of a Down"},
    {"id": "053", "artist": "System of a Down",    "title": "Toxicity"},
    {"id": "054", "artist": "System of a Down",    "title": "Hypnotize"},
    {"id": "055", "artist": "Tyler, the Creator",  "title": "Igor"},
    {"id": "056", "artist": "Tyler, the Creator",  "title": "Call Me If You Get Lost"},
    {"id": "057", "artist": "Tyler, the Creator",  "title": "Chromakopia"},
    {"id": "058", "artist": "Wallows",             "title": "More"},
]

def log_failure(msg):
    with open(FAILED_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def fetch_tracklist(artist, title):
    """Fetch tracklist from MusicBrainz (free, no key needed)."""
    search_url = "https://musicbrainz.org/ws/2/release"
    params = {
        "query": f'release:"{title}" AND artist:"{artist}"',
        "fmt": "json",
        "limit": 1
    }
    headers = {"User-Agent": "VinylCatalog/1.0 (personal project)"}
    for attempt in range(3):

        try:
            r = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=30
            )
            break
        except requests.exceptions.Timeout:
            print(f"    MusicBrainz timeout, retry {attempt+1}/3")
            time.sleep(5)

    else:
        log_failure(f"TRACKLIST TIMEOUT | {artist} - {title}")
        return []
        
    releases = r.json().get("releases", [])
    if not releases:
        log_failure(f"TRACKLIST NOT FOUND | {artist} - {title}")
        return []
        
    release_id = releases[0]["id"]

    time.sleep(1)

    detail_url = f"https://musicbrainz.org/ws/2/release/{release_id}"
        
    r2 = requests.get(detail_url, params={"fmt": "json", "inc": "recordings"}, headers=headers, timeout=30)
       
    data = r2.json()
        
    tracks = []
    for medium in data.get("media", []):
        for track in medium.get("tracks", []):
            tracks.append(track["title"])

    return tracks

def fetch_timed_lyrics(artist, track):
    """
    Fetch synced lyrics from LRCLIB API
    Returns LRC formatted lyrics
    """

    url = "https://lrclib.net/api/search"

    params = {"artist_name" : artist, "track_name": track}

    headers = {"User-Agent": "SpinSync/1.0 (Arduino Lyrics Project)"}

    try:

        r = requests.get(
            url, 
            params = params,
            headers = headers,
            timeout = 15
        )

        if r.status_code != 200:
            log_failure(
                f"LRCLIB ERROR {r.status_code} | {artist} - {track}"
            )
            return ""
        
        results = r.json()

        if not results:
            log_failure(
                f"NO LRC | {artist} - {track}"
            )
            return ""
        
        #Prefer synced lyrics
        for song in results:

            if song.get("syncedLyrics") and len(song["syncedLyrics"]) > 20:

                return song["syncedLyrics"]
            
        log_failure(
            f"ONLY UNSYNCED | {artist} - {track}"
        )

        return ""
    
    except Exception as e:
        log_failure(
            f"LRCLIB EXCEPTION | {artist} - {track} | {e}"
        )

    return ""

def format_for_lcd(lrc_text, cols=16):
    
    output = []

    for line in lrc_text.splitlines():

        match = re.match(
            r"\[(\d+):(\d+\.\d+)\](.*)",
            line
        )

        if not match:
            continue

        minutes = int(match.group(1))
        seconds = float(match.group(2))

        timestamp = f"{minutes:02d}:{int(seconds):02d}.{int((seconds % 1)*100):02d}"

        lyric = match.group(3).strip()

        wrapped = textwrap.wrap(
            lyric,
            width=cols
        )

        if not wrapped:
            continue

        # group into LCD Screen
        for i in range(0, len(wrapped), 2):

            row1 = wrapped[i].ljust(cols)

            if i + 1 < len(wrapped):
                row2 = wrapped[i+1].ljust(cols)
            else:
                row2=" " * cols

            output.append(
                f"{timestamp}|{row1}|{row2}"
            )


    return "\n".join(output)

def safe_folder_name(album_id):
    return f"ALB{album_id}"

# ── BUILD ─────────────────────────────────────────────────────────────────────

with open(
    FAILED_LOG,
    "w",
    encoding="utf-8"
) as f:
    f.write("Spinsync Failure Log\n")
    f.write("====================\n\n")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# catalog.txt
with open(f"{OUTPUT_DIR}/catalog.txt", "w", newline="\n",encoding="utf-8") as f:
    for a in albums:
        f.write(f"{a['id']}|{a['title']}|{a['artist']}\n")

print(f"✓ catalog.txt written ({len(albums)} albums)")

# Per-album folders
for a in albums:
    folder = f"{OUTPUT_DIR}/{safe_folder_name(a['id'])}"
    os.makedirs(folder, exist_ok=True)

    print(f"\n[{a['id']}] {a['title']} — {a['artist']}")

    # Fetch tracklist
    tracks = fetch_tracklist(a["artist"], a["title"])
    time.sleep(DELAY)

    if not tracks:
        print("    ! Skipping album, no tracklist")
        continue

    with open(f"{folder}/tracklist.txt", "w", newline="\n", encoding="utf-8") as f:
        for i, t in enumerate(tracks, 1):
            f.write(f"{i:02d}|{t}\n")
    print(f"    ✓ tracklst.txt ({len(tracks)} tracks)")

    # Fetch lyrics for each track
    for i, track in enumerate(tracks, 1):
        fname = f"T{i:02d}.TXT"

        lyrics = fetch_timed_lyrics(a["artist"], track)
        time.sleep(DELAY)

        if lyrics:
            content = format_for_lcd(lyrics)
            print(f"    ✓ {fname}  ({track})")
        else:
            log_failure(f"LYRICS FAILED | {a['artist']} - {track}")
            content = f"Lyrics not\nfound\n\n{track[:16].ljust(16)}\n{'by '+a['artist'][:13]}\n"
            

        with open(f"{folder}/{fname}", "w", newline="\n", encoding="utf-8") as f:
            f.write(content)

print("\n\nDone! Copy the SD_CARD/ folder contents to your SD card.")
print(
    f"\nCheck {FAILED_LOG} for missing lyrics."
)
