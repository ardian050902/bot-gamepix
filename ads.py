import asyncio
from playwright.async_api import async_playwright
import random

async def gas_dollar():
    # LINK IKLAN LU
    target_link = "https://data527.click/c51ee7c319bffb52a9c0/947fa142e8/?placementName=default"
    
    async with async_playwright() as p:
        # Pake User Agent Chrome asli biar gak dikira bot GitHub
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        counter = 1
        while True:
            page = await context.new_page()
            try:
                print(f"🚀 Sesi {counter} | Mencari Cuan...")
                await page.goto(target_link, wait_until="domcontentloaded", timeout=60000)
                
                # 1. Tunggu iklan beneran muncul (15 detik)
                await asyncio.sleep(15)
                
                # 2. KLIK PAKSA DI TENGAH LAYAR (Iklan biasanya di sini)
                # Kita klik di koordinat x:200, y:300 (area tengah HP/Browser)
                await page.mouse.click(200, 300)
                print("🖱️ KLIK PAKSA BERHASIL!")
                
                # 3. Ngetem setelah klik (PENTING!)
                # Jangan langsung tutup, diem dulu 30-40 detik biar kliknya Valid
                await asyncio.sleep(random.randint(30, 45))
                
                print(f"✅ Sesi {counter} Berhasil di-convert jadi Dollar!")
                
            except Exception as e:
                print(f"⚠️ Error: {e}")
            
            await page.close()
            counter += 1
            if counter > 50: break # Biar gak kena banned, 50 sesi per jalan dulu

        await browser.close()

if __name__ == "__main__":
    asyncio.run(gas_dollar())
  
