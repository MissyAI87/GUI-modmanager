

# curseforge_api.py
import os
import requests

# You can replace this with your actual API key or use an environment variable
CURSEFORGE_API_KEY = os.getenv("CURSEFORGE_API_KEY") or "$2a$10$KAucp617yW3CyHUnkfnYY.CvWqLeWK20GtBDvFks/W7L1uKHxn7gm"
BASE_URL = "https://api.curseforge.com/v1"
GAME_ID_SIMS4 = 118

HEADERS = {
    "Accept": "application/json",
    "x-api-key": CURSEFORGE_API_KEY
}

def search_mods(keywords):
    mods = []
    for keyword in keywords:
        print(f"\n🔎 Searching CurseForge for: {keyword}")
        url = f"{BASE_URL}/mods/search"
        params = {
            "gameId": GAME_ID_SIMS4,
            "searchFilter": keyword,
            "pageSize": 20
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            found = data.get("data", [])
            print(f"→ Found {len(found)} results.")
            for mod in found:
                name = mod.get("name")
                site = mod.get("links", {}).get("websiteUrl")
                dl = mod.get("latestFiles", [{}])[0].get("downloadUrl")
                print(f"🧩 {name}\n   🔗 {site}")
                if dl:
                    print(f"   ⬇️ {dl}")
                mods.append({
                    "name": name,
                    "summary": mod.get("summary"),
                    "url": site,
                    "download": dl
                })
        except Exception as e:
            print(f"❌ Error searching CurseForge: {e}")
    return mods

if __name__ == "__main__":
    import sys
    keywords = sys.argv[1:]
    results = search_mods(keywords)
    for mod in results:
        print(f"{mod['name']}: {mod['url']}")