import time
import random
from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 Version/16.4 Mobile Safari/604.1"
]

def klik_tombol_pertama(page):
    try:
        iframe = page.frame_locator("iframe").first
        btn = iframe.locator("button.gpxLoader-button")
        btn.scroll_into_view_if_needed(timeout=2000)
        btn.click(timeout=5000)
        return True
    except:
        return False


def scan_cepat(page):
    keywords = ["learn more", "visit site", "open", "sign up", "mehr info"]

    for frame in page.frames:
        if "gamepix.com" in frame.url:
            continue

        for teks in keywords:
            try:
                tombol = frame.locator(f"text=/{teks}/i")
                if tombol.count() == 0:
                    continue

                tombol = tombol.first

                try:
                    tombol.click(timeout=2000)
                    print(f"⚡ FAST KLIK: {teks}")
                    return True
                except:
                    box = tombol.bounding_box()
                    if box:
                        page.mouse.click(
                            box["x"] + box["width"]/2,
                            box["y"] + box["height"]/2
                        )
                        print(f"⚡ FAST KLIK (mouse): {teks}")
                        return True
            except:
                continue

    return False


def cari_dan_klik(page):
    keywords = [
        "learn more", "visit site", "open", "sign up",
        "mehr", "anmelden", "weitere infos", "website",
        "install", "download", "play", "open app"
    ]

    for _ in range(3):
        for frame in page.frames:
            if "gamepix.com" in frame.url:
                continue

            for teks in keywords:
                try:
                    tombol = frame.locator(f"text=/{teks}/i")
                    if tombol.count() == 0:
                        continue

                    tombol = tombol.first

                    try:
                        tombol.scroll_into_view_if_needed(timeout=2000)
                    except:
                        pass

                    try:
                        tombol.click(timeout=2000)
                        print(f"💰 KLIK: {teks}")
                        return True
                    except:
                        box = tombol.bounding_box()
                        if box:
                            page.mouse.click(
                                box["x"] + box["width"]/2,
                                box["y"] + box["height"]/2
                            )
                            print(f"💰 KLIK (mouse): {teks}")
                            return True

                except:
                    continue

        time.sleep(1)  # lebih cepat dari sebelumnya

    return False


def run_simulasi(sesi_ke):
    print(f"\n🚀 Sesi ke-{sesi_ke}")
    ua = random.choice(USER_AGENTS)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent=ua,
            viewport={"width": 400, "height": 700},
            locale="de-DE",
            timezone_id="Europe/Berlin"
        )

        page = context.new_page()

        try:
            url = "https://gamesfreeonlinehub.blogspot.com/2026/01/turbo-dismounting-play-free-online.html?m=1"
            page.goto(url, timeout=60000)
            print("🌐 Halaman terbuka")

            time.sleep(5)

            if not klik_tombol_pertama(page):
                print("⚠️ Gagal klik tombol game")
                return

            tunggu = random.randint(20, 30)
            print(f"⏳ Tunggu iklan muncul {tunggu} detik")
            time.sleep(tunggu)

            berhasil = False

            if scan_cepat(page):
                berhasil = True
            elif cari_dan_klik(page):
                berhasil = True

            if berhasil:
                stay = random.randint(35, 45)
                print(f"🕒 Stay di halaman iklan {stay} detik")
                time.sleep(stay)
            else:
                print("⚠️ Iklan tidak ditemukan")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            browser.close()
            print(f"✅ Selesai sesi {sesi_ke}")


if __name__ == "__main__":
    for sesi in range(1, 5):
        try:
            run_simulasi(sesi)

            if sesi < 4:
                jeda = random.randint(30, 60)
                print(f"😴 Jeda {jeda} detik...")
                time.sleep(jeda)

        except Exception as e:
            print(f"Error loop: {e}")
