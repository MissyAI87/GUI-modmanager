# === ModTheSims Scraper ===
# Description:
#   - Searches ModTheSims for Sims 4 mods using keyword tags
#   - Returns a list of mod titles and URLs
#   - Intended to be used as a module in a larger mod-finding system

# --- Imports ---
import requests
from bs4 import BeautifulSoup

# --- Constants ---
BASE_URL = "https://modthesims.info"

# --- Main Search Function ---
def search_modthesims(keywords):
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for keyword in keywords:
        print(f"\n🔍 Searching ModTheSims for: {keyword}")
        # Search URL uses the general site search form
        search_url = f"{BASE_URL}/search.php?query={keyword}&go=Go&gs=1&f=38"

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            if "Access Denied" in response.text or "blocked" in response.text.lower():
                print("🚫 Request may have been blocked by ModTheSims.")
                continue
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Mod listings are anchor tags whose href starts with '/download.php?t='
            mod_blocks = soup.select("a[href^='/download.php?t=']")

            if not mod_blocks:
                print(f"→ Search completed for '{keyword}' but returned 0 results.")
                continue

            for link in mod_blocks[:10]:  # Limit to first 10 results
                title = link.text.strip()
                url = BASE_URL + link.get("href")
                results.append({
                    "keyword": keyword,
                    "title": title,
                    "url": url
                })
                print(f"🧩 {title}\n   🔗 {url}")
            print(f"✅ Done searching '{keyword}' – {len(mod_blocks)} results.")

        except Exception as e:
            print(f"❌ Error searching MTS for '{keyword}': {e}")
    return results

# --- CLI Entrypoint ---
if __name__ == "__main__":
    import sys
    search_modthesims(sys.argv[1:])