import os, sys, json, datetime as dt
from zoneinfo import ZoneInfo
import requests
from pywebpush import webpush

now = dt.datetime.now(ZoneInfo("Europe/Rome"))
if not os.environ.get("FORCE") and not (now.weekday() == 0 and now.hour == 21):
    print("Non è lunedì alle 21 a Roma: esco."); sys.exit(0)

KEY = os.environ["YOUTUBE_API_KEY"]
API = "https://www.googleapis.com/youtube/v3"
def get(path, **p):
    r = requests.get(f"{API}/{path}", params={**p, "key": KEY}, timeout=30)
    r.raise_for_status(); return r.json()

ch = get("channels", part="statistics,contentDetails", forHandle=os.environ.get("YT_HANDLE", "@Nino09"))["items"][0]
st = ch["statistics"]; uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
ids, tok = [], None
while True:
    d = get("playlistItems", part="contentDetails", playlistId=uploads, maxResults=50, **({"pageToken": tok} if tok else {}))
    ids += [i["contentDetails"]["videoId"] for i in d["items"]]
    tok = d.get("nextPageToken")
    if not tok: break
likes = 0
for i in range(0, len(ids), 50):
    v = get("videos", part="statistics", id=",".join(ids[i:i+50]))
    likes += sum(int(x["statistics"].get("likeCount", 0)) for x in v["items"])

today = now.date().isoformat()
entry = {"date": today, "subs": int(st.get("subscriberCount", 0)), "views": int(st["viewCount"]), "likes": likes}
path = "data/history.json"
hist = json.load(open(path)) if os.path.exists(path) else []
prev = next((h for h in reversed(hist) if h["date"] != today), None)
hist = [h for h in hist if h["date"] != today] + [entry]
json.dump(hist, open(path, "w"), indent=1)

f = lambda n: f"{n:,}".replace(",", ".")
def part(name, k):
    s = f"{name} {f(entry[k])}"
    if prev: s += f" ({entry[k]-prev[k]:+,})".replace(",", ".")
    return s
body = " · ".join([part("Iscritti", "subs"), part("Views", "views"), part("Like", "likes")]) + "\nAggiorna anche TikTok!"

webpush(
    subscription_info=json.loads(os.environ["PUSH_SUBSCRIPTION"]),
    data=json.dumps({"title": "Nino09: andamento settimanale", "body": body, "url": "./"}),
    vapid_private_key=os.environ["VAPID_PRIVATE_KEY"],
    vapid_claims={"sub": "mailto:" + os.environ["VAPID_EMAIL"]},
)
print("Notifica inviata:", body)
