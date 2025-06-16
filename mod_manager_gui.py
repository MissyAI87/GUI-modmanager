"""
mod_manager_gui.py – Mod Manager 2.0 (Streamlit GUI)

Version: 2025-06-15
Author: Mary (MissyAI)

Overview:
• Streamlit-based GUI to search and manage Sims 4 mods.
• Scrapes mods from CurseForge, ModTheSims, and (placeholder) SimsDom.
• Displays clickable mod links with source labels.
• Highlights outdated mods using KnownModVersions.json.
• Optionally runs mod fixer script (sims4_mod_fixer.py).

How to Run:
1. In Terminal, navigate to the script folder.
2. Run: streamlit run mod_manager_gui.py

Requirements:
- streamlit
- beautifulsoup4
- requests
- KnownModVersions.json (optional, for version checking)
"""

# ──────────────────────────────
# 🔍 CURSEFORGE SCRAPER
# ──────────────────────────────
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_curseforge(keywords: List[str], seen_urls: set, start_index: int, limit: int) -> Tuple[List[Dict], int]:
    results = []
    index = start_index
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    curse_url = "https://www.curseforge.com/sims4/mods?search="
    for kw in keywords:
        try:
            search_page = requests.get(curse_url + kw, headers=headers, timeout=15)
            st.write(f"CurseForge URL fetched: {search_page.url}")
            soup = BeautifulSoup(search_page.text, "html.parser")
            st.write(f"CurseForge HTML title: {soup.title.string if soup.title else 'No title'}")
            st.write(f"CurseForge - Total <a> tags: {len(soup.find_all('a'))}")
            with open("curseforge_raw.html", "w", encoding="utf-8") as f:
                f.write(search_page.text)
            search_page.raise_for_status()
        except Exception as e:
            st.warning(f"CurseForge search failed for '{kw}': {e}")
            continue
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            if href.startswith("/sims4/mods/") and href.count("/") >= 3:
                mod_name = anchor.get_text(strip=True)
                full_url = "https://www.curseforge.com" + href
                if full_url not in seen_urls:
                    results.append({
                        "index": index,
                        "name": mod_name or f"CurseForge Mod {index}",
                        "url": full_url,
                        "source": "CurseForge"
                    })
                    seen_urls.add(full_url)
                    index += 1
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break
    return results, index

# ──────────────────────────────
# 🔍 MODTHESIMS SCRAPER
# ──────────────────────────────
# scraper_modthesims.py
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_modthesims(keywords: List[str], seen_urls: set, start_index: int, limit: int) -> Tuple[List[Dict], int]:
    results = []
    index = start_index
    base_url = "https://modthesims.info"
    search_url = base_url + "/search.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    for kw in keywords:
        params = {"search": kw, "go": "Go"}
        try:
            resp = requests.get(search_url, params=params, headers=headers, timeout=15)
            st.write(f"ModTheSims URL fetched: {resp.url}")
            soup = BeautifulSoup(resp.text, "html.parser")
            st.write(f"ModTheSims HTML title: {soup.title.string if soup.title else 'No title'}")
            st.write(f"ModTheSims - Total <a> tags: {len(soup.find_all('a'))}")
            with open("modthesims_raw.html", "w", encoding="utf-8") as f:
                f.write(resp.text)
            resp.raise_for_status()
        except Exception as e:
            st.warning(f"Failed to fetch search results for '{kw}': {e}")
            continue
        for a in soup.find_all("a", href=True):
            href = a["href"]
            name = a.get_text(strip=True)
            if "/downloads/" in href and name and not name.startswith(("Downloads Home", "Newest", "Popular", "Updated", "Featured", "Picked")):
                url = base_url + href
                if url not in seen_urls:
                    download_url = url + ".zip"
                    results.append({
                        "index": index,
                        "name": name,
                        "url": download_url,
                        "source": "ModTheSims"
                    })
                    seen_urls.add(url)
                    index += 1
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break
    return results, index

# ──────────────────────────────
# 🚧 SIMSDOM SCRAPER (PLACEHOLDER)
# ──────────────────────────────
# scraper_simsdom.py
# Placeholder for future SimsDom scraper module
from typing import List, Dict, Tuple

def scrape_simsdom(keywords: List[str], seen_urls: set, start_index: int, limit: int) -> Tuple[List[Dict], int]:
    """
    Placeholder function for SimsDom scraping.
    """
    st.write("SimsDom scraper called.")
    st.write("This is a placeholder scraper. Returning no results.")
    # Future implementation goes here
    return [], start_index

import streamlit as st
import sys
import os
import glob
import re
import json
import shutil
from typing import List, Dict, Tuple

st.title("Mod Manager 2.0")

# --- Keyword search UI and feedback ---
keywords_input = st.text_input("Enter keywords (comma-separated):", key="keyword_input")
result_limit = st.slider("Max results per site:", 5, 50, 10)

 # ──────────────────────────────
 # 🧠 SCRAPER COORDINATOR
 # ──────────────────────────────
 # Runs all scraper functions, aggregates results, and ensures no duplicates.
def run_mod_finder(keywords: List[str], limit: int) -> List[Dict]:
    results = []
    seen_urls = set()
    index = 1

    st.write(f"🔍 Using keywords: {keywords}")

    scrapers = [
        ("CurseForge", scrape_curseforge),
        ("ModTheSims", scrape_modthesims),
        ("SimsDom", scrape_simsdom),  # Placeholder
    ]

    for name, scraper_func in scrapers:
        try:
            st.write(f"🔍 Running scraper: {name}")
            new_results, index = scraper_func(keywords, seen_urls, index, limit)
            results.extend(new_results)
            st.write(f"🔍 {name} found {len(new_results)} results.")
            st.success(f"✅ {name} scrape complete.")
        except Exception as e:
            st.warning(f"⚠️ {name} scraper failed: {e}")

    st.write(f"Total mods found: {len(results)}")
    if not results:
        st.warning("❌ No mods found for the provided keywords.")
    return results

# ──────────────────────────────
# 🖱 USER INPUT HANDLER
# ──────────────────────────────
if keywords_input:
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    st.write(f"Parsed keywords: {keywords}")
    st.write("🧼 Clearing previous search data...")
    st.write(f"Searching for: {keywords}")
    with st.spinner("Searching mods..."):
        results = run_mod_finder(keywords, result_limit)
    st.write(f"Results received: {results}")
    if not results:
        st.warning("No results found for those keywords.")
    else:
        for mod in results:
            name = mod['name'].lower()
            if any(bad in name for bad in ["downloads home", "newest", "popular", "updated", "featured", "picked"]):
                continue
            st.markdown(f"[{mod['name']} – {mod['source']}]({mod['url']})")
    # ──────────────────────────────
    # 📦 MOD VERSION CHECK
    # ──────────────────────────────
    if os.path.exists("KnownModVersions.json"):
        with open("KnownModVersions.json") as f:
            known_versions = json.load(f)
        outdated = []
        for mod in results:
            name = mod["name"]
            if name in known_versions:
                outdated.append((name, known_versions[name]["latest"], known_versions[name]["url"]))
        if outdated:
            st.warning("🧭 Outdated mods found:")
            for name, latest, url in outdated:
                st.markdown(f"- **{name}** (Latest: {latest}) → [Update Link]({url})")
        else:
            st.success("✅ All found mods are current (based on version file).")
else:
    st.info("Please enter keywords to begin your search.")

st.markdown("---")

# ──────────────────────────────
# 🛠 EXTERNAL SCRIPT TRIGGER
# ──────────────────────────────
# Runs the mod fixer cleanup tool when button is clicked.
if st.button("Apply Mod Fixes"):
    try:
        os.system("python3 sims4_mod_fixer.py")
        st.success("✅ Mod fixes applied.")
    except Exception as e:
        st.error(f"❌ Failed to apply mod fixes: {e}")

# ... rest of mod_manager_gui.py unchanged ...