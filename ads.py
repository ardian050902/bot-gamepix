import time
import random
from playwright.sync_api import sync_playwright

# List User Agent Lengkap buat variasi trafik
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 11; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 EdgA/124.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/124.0 Mobile/15E148 Safari/605.1.15"
]

def klik_tombol_pertama(page):
    """Klik tombol play awal GamePix agar sesi dianggap valid"""
    try:
        # Mencari iframe gamepix dan klik tombol loader
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click(timeout=5000)
        return True
    except:
        # Fallback klik tengah jika tombol spesifik tidak ketemu
        try:
            page.mouse.click(200, 350)
            return True
        except:
            return False

def cari_dan_klik_learn_more(page):
    """Mencari dan berinteraksi dengan iklan (Revenue Hunter)"""
    found = False
    # Daftar teks tombol iklan yang sering muncul
    teks_tombol_list = [
        "learn more", "open", "visit", "install", "try today",
        "sign up", "website", "anmelden", "zum shop",
        "mehr info", "selengkapnya", "daftar", "shop now"
    ]

    # Coba scan beberapa kali karena iklan sering muncul telat
    for percobaan in range(3):
        for frame in page.frames:
            # Lewati frame internal gamepix agar tidak salah klik
            if "gamepix.com" in frame.url:
                continue

            for teks in teks_tombol_list:
                try:
                    tombol = frame.locator(f"text=/{teks}/i")
                    if tombol.count() > 0:
                        tombol.first.scroll_into_view_if_needed(timeout=1000)
                        tombol.first.click(timeout=2000)
                        found = True
                        break
                except:
                    continue
            if found: break
        if found: break
        time.sleep(3)

    return found

def run_simulasi(sesi_ke):
    print(f"🌐 Memulai Sesi ke-{sesi_ke}...")
    user_agent = random.choice(USER_AGENTS)

    with sync_playwright() as p:
        # Pake Firefox sesuai rekomendasi biar trust score tinggi
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 400, "height": 700},
            user_agent=user_agent,
            locale="en-US"
        )

        # Script anti-bot agar tidak kedeteksi headless
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # URL target blog lu
        url = "https://gamesfreeonlinehub.blogspot.com/2026/01/merge-mine-idle-clicker-play-free-online.html?m=1"
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.randint(3, 5))

            # Klik Play Game (Traffic)
            if not klik_tombol_pertama(page):
                print(f"⚠️ Sesi {sesi_ke}: Tombol Play gak ketemu, lanjut scan iklan.")

            # Tunggu iklan interstitial/overlay muncul
            tunggu_iklan = random.randint(12, 18)
            print(f"⏳ Menunggu iklan muncul ({tunggu_iklan} detik)...")
            time.sleep(tunggu_iklan)

            # Cari dan Klik Iklan (Revenue)
            if cari_dan_klik_learn_more(page):
                # Ngetem lama biar Dollar cair (Sweet Spot 35-50 detik)
                waktu_tunggu = random.randint(35, 50)
                print(f"💰 Iklan diklik! Ngetem {waktu_tunggu} detik...")
            else:
                waktu_tunggu = random.randint(5, 10)
                print(f"⚠️ Iklan tidak ditemukan, ngetem bentar ({waktu_tunggu}s)...")

            time.sleep(waktu_tunggu)

        except Exception as e:
            print(f"❌ Terjadi kesalahan: {e}")

        context.close()
        browser.close()
        print(f"✅ Sesi ke-{sesi_ke} Selesai.\n")

if __name__ == "__main__":
    sesi_ke = 1
    while True:
        try:
            run_simulasi(sesi_ke)
            sesi_ke += 1
            # Delay antar sesi biar natural
            time.sleep(random.randint(2, 5))
        except KeyboardInterrupt:
            break
        except:
            time.sleep(5)
      
