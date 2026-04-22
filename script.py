import time
import random
from playwright.sync_api import sync_playwright

# Gunakan USER_AGENTS yang sudah Anda miliki (tetap sama)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

def klik_tombol_pertama(page):
    try:
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click(timeout=5000)
        return True
    except:
        return False

def cari_dan_klik_learn_more(page):
    # Logika cari dan klik tombol (tetap sama seperti milik Anda)
    found = False
    teks_tombol_list = ["mehr", "learn more", "sign up", "try today"]
    for frame in page.frames:
        if "gamepix.com" in frame.url: continue
        for teks in teks_tombol_list:
            tombol = frame.locator(f"text=/{teks}/i").first
            if tombol.count() > 0:
                try:
                    tombol.click(timeout=2000)
                    found = True
                    return True
                except: continue
    return found

def run_simulasi():
    print("Memulai sesi simulasi...")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 400, "height": 650},
            user_agent=random.choice(USER_AGENTS)
        )
        page = context.new_page()
        page.goto("https://gamesfreeonlinehub.blogspot.com/2026/04/epic-duck.html")
        
        time.sleep(5)
        if klik_tombol_pertama(page):
            time.sleep(10)
            cari_dan_klik_learn_more(page)
        
        context.close()
        browser.close()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_simulasi()
