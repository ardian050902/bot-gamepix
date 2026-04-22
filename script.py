import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
]

def klik_tombol_pertama(page):
    try:
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click(timeout=10000)
        return True
    except:
        return False

def cari_dan_klik_learn_more(page):
    teks_tombol_list = ["mehr", "learn more", "sign up", "try today", "zum shop"]
    # Tunggu agar halaman benar-benar dimuat
    page.wait_for_load_state("networkidle")
    
    for frame in page.frames:
        try:
            if "gamepix.com" in frame.url or frame.is_detached:
                continue
            
            for teks in teks_tombol_list:
                tombol = frame.locator(f"text=/{teks}/i").first
                if tombol.count() > 0:
                    tombol.click(timeout=3000)
                    print(f"Berhasil klik: {teks}")
                    return True
        except:
            continue
    return False

def run_simulasi():
    print("Memulai sesi...")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 400, "height": 650},
            user_agent=random.choice(USER_AGENTS)
        )
        page = context.new_page()
        
        try:
            page.goto("https://gamesfreeonlinehub.blogspot.com/2026/04/epic-duck.html")
            
            if klik_tombol_pertama(page):
                time.sleep(15) # Waktu tunggu iklan muncul
                if not cari_dan_klik_learn_more(page):
                    print("Iklan tidak ditemukan.")
            else:
                print("Gagal klik tombol pertama.")
        except Exception as e:
            print(f"Error: {e}")
        
        context.close()
        browser.close()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_simulasi()
