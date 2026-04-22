import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

def klik_tombol_pertama(page):
    try:
        # Menunggu iframe muncul
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click(timeout=10000)
        return True
    except:
        return False

def cari_dan_klik_learn_more(page):
    teks_tombol_list = ["mehr", "learn more", "sign up", "try today", "zum shop"]
    time.sleep(3) # Jeda agar elemen stabil
    
    for frame in page.frames:
        try:
            # Lewati frame gamepix
            if "gamepix.com" in frame.url: 
                continue
            
            # Cek apakah frame masih ada
            if frame.is_detached:
                continue
                
            for teks in teks_tombol_list:
                tombol = frame.locator(f"text=/{teks}/i").first
                # Cek apakah elemen ada tanpa error frame detached
                if tombol.count() > 0:
                    tombol.click(timeout=3000)
                    print(f"Berhasil klik tombol: {teks}")
                    return True
        except:
            continue
    return False

def run_simulasi():
    print("Memulai sesi simulasi...")
    with sync_playwright() as p:
        # Menggunakan firefox sesuai workflow
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 400, "height": 650},
            user_agent=random.choice(USER_AGENTS)
        )
        page = context.new_page()
        
        try:
            page.goto("https://gamesfreeonlinehub.blogspot.com/2026/04/epic-duck.html", wait_until="networkidle")
            
            if klik_tombol_pertama(page):
                print("Tombol pertama diklik, mencari iklan...")
                time.sleep(10)
                if cari_dan_klik_learn_more(page):
                    print("Iklan berhasil diinteraksi.")
                else:
                    print("Tombol iklan tidak ditemukan.")
            else:
                print("Tombol pertama gagal diklik.")
        except Exception as e:
            print(f"Error saat navigasi: {e}")
        
        context.close()
        browser.close()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_simulasi()
