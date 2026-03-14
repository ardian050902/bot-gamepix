import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
"Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991B) AppleWebKit/537.36 Chrome/124.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 Chrome/124.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 Version/16.0 Safari/605.1.15",
"Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 Version/16.4 Mobile Safari/604.1",
]

def klik_tombol_pertama(page):
    try:
        iframe1 = page.frame_locator("iframe").first
        iframe1.locator("button.gpxLoader-button").click()
        return True
    except:
        return False


def cari_dan_klik_learn_more(page):

    teks_tombol_list = [
        "mehr","mehr info","weitere infos","jetzt buchen",
        "sign up","website","anmelden","zum shop",
        "abonnieren","geschaft besuchen","learn more","try today"
    ]

    for percobaan in range(5):
        for frame in page.frames:

            if "gamepix.com" in frame.url:
                continue

            for teks in teks_tombol_list:
                try:

                    tombol = frame.locator(f"text=/{teks}/i")

                    if tombol.count() == 0:
                        continue

                    tombol_pertama = tombol.first

                    try:
                        tombol_pertama.scroll_into_view_if_needed(timeout=1000)
                    except:
                        pass

                    try:
                        tombol_pertama.click(timeout=1500)
                        return True
                    except:
                        pass

                except:
                    continue

        time.sleep(2)

    return False


def run_simulasi(sesi_ke):

    print(f"\n🌐 Memulai sesi ke-{sesi_ke}...")

    user_agent = random.choice(USER_AGENTS)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            viewport={"width":400,"height":650},
            user_agent=user_agent,
            timezone_id="Europe/Berlin",
            locale="de-DE"
        )

        context.add_init_script("""
        Object.defineProperty(navigator,'webdriver',{get:()=>undefined});
        """)

        url = "https://gamesfreeonlinehub.blogspot.com/2026/02/kobadoo-numbers-free-brain-game-online.html"

        page = context.new_page()

        print(f"🌐 Membuka halaman {url}")

        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        tunggu = random.randint(5,8)
        time.sleep(tunggu)

        if not klik_tombol_pertama(page):

            context.close()
            browser.close()

            print(f"⚠️ Sesi ke-{sesi_ke} gagal klik tombol pertama.")
            return


        tunggu_iklan = random.randint(10,16)

        print(f"⏳ Menunggu sebelum deteksi iklan ({tunggu_iklan} detik)...")

        time.sleep(tunggu_iklan)

        learn_more_diklik = cari_dan_klik_learn_more(page)

        if learn_more_diklik:

            waktu_tunggu = random.randint(8,11)

            print(f"🕒 Tombol iklan berhasil diklik. Menunggu {waktu_tunggu} detik...")

        else:

            waktu_tunggu = random.randint(0,2)

            print(f"⚠️ Tidak ada tombol iklan.")

        time.sleep(waktu_tunggu)

        context.close()
        browser.close()

        print(f"✅ Sesi ke-{sesi_ke} selesai")


if __name__ == "__main__":

    sesi_ke = 1

    while True:

        try:

            run_simulasi(sesi_ke)

            sesi_ke += 1

        except KeyboardInterrupt:

            print("🛑 Dihentikan oleh pengguna.")
            break

        except Exception as e:

            print(f"❌ Terjadi kesalahan pada sesi ke-{sesi_ke}: {e}")

            sesi_ke += 1

            time.sleep(random.randint(8,15))
