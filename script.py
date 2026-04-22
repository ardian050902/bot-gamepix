import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
]

def klik_tombol_pertama(page):
    try:
        # Gunakan locator yang lebih spesifik
        iframe = page.frame_locator("iframe").first
        iframe.locator("button.gpxLoader-button").click(timeout=10000)
        return True
    except:
        return False

def cari_dan_klik_learn_more(page):
    teks_tombol_list = ["mehr", "learn more", "sign up", "try today", "zum shop"]
    
    # Coba cari di semua frame yang tersedia
    for frame in page.frames:
        try:
            if "gamepix.com" in frame.url or frame.is_detached:
                continue
            
            for teks in teks_tombol_list:
                tombol = frame.locator(f"text=/{teks}/i").first
                if tombol.count() > 0:
                    tombol.click(timeout=5000)
                    print(f"Berhasil klik: {teks}")
                    return True
        except:
            continue
    return False

def run_simulasi():
    print("Memulai sesi simulasi...")
    with sync_playwright() as p:
        # Menggunakan firefox dan memperpanjang timeout global
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 400, "height": 650},
            user_agent=random.choice(USER_AGENTS)
        )
        page = context.new_page()
        page.set_default_timeout(60000) # Perpanjang timeout ke 60 detik
        
        try:
            # Menggunakan domcontentloaded agar lebih cepat
            page.goto("https://gamesfreeonlinehub.blogspot.com/2026/04/epic-duck.html", 
                      wait_until="domcontentloaded")
            
            time.sleep(10) # Jeda agar elemen utama siap
            
            if klik_tombol_pertama(page):
                print("Tombol pertama berhasil diklik, menunggu iklan...")
                time.sleep(20) # Waktu tunggu iklan muncul di server lambat
                if not cari_dan_klik_learn_more(page):
                    print("Iklan tidak ditemukan atau halaman tidak memuat iklan.")
            else:
                print("Gagal menemukan/klik tombol pertama.")
                
        except Exception as e:
            print(f"Error saat eksekusi: {e}")
        
        context.close()
        browser.close()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_simulasi()
