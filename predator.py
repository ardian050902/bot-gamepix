import time
import random
from playwright.sync_api import sync_playwright

LIST_URL = [
    "https://gamesfreeonlinehub.blogspot.com/2026/02/canjump-free-platform-game-online.html?m=1",
    "https://gamesfreeonlinehub.blogspot.com/2026/02/going-right-free-arcade-game-online.html?m=1",
    "https://gamesfreeonlinehub.blogspot.com/2026/02/sokoballs-free-puzzle-game-online.html?m=1",
    "https://gamesfreeonlinehub.blogspot.com/2026/02/hoop-world-free-basketball-game-online.html?m=1"
]

def run_session(id_sesi):
    url = random.choice(LIST_URL)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
            viewport={"width": 390, "height": 844}
        )
        page = context.new_page()
        try:
            print(f"🚀 {id_sesi} | Loading: {url[-20:]}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(20) # Simulasi baca/main
            
            # Cari elemen iklan
            ad = page.query_selector("ins.adsbygoogle, iframe[id^='aswift'], div[id^='google_ads']")
            if ad:
                ad.scroll_into_view_if_needed()
                time.sleep(2)
                ad.click()
                print(f"🔥 {id_sesi} | [CLICKED] Iklan dipatuk!")
                time.sleep(20) # Stay di halaman iklan biar valid
            
            print(f"✅ {id_sesi} Sukses.")
        except:
            print(f"⚠️ {id_sesi} Skip/Timeout.")
        finally:
            browser.close()

if __name__ == "__main__":
    # Kita batasi 5 sesi aja per run biar gak dicurigai GitHub
    for i in range(5):
        run_session(f"SESI-{i}")
        time.sleep(5)
      
