import asyncio
from playwright.async_api import async_playwright
import random

async def gas_nonstop():
    target_link = "https://data527.click/c51ee7c319bffb52a9c0/947fa142e8/?placementName=default"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Pakai Profile iPhone 15 Pro Max biar CPM Advertica Meledak
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            viewport={'width': 390, 'height': 844}
        )
        
        counter = 1
        while True:
            page = await context.new_page()
            try:
                print(f"🔥 Sesi Ke-{counter} | OTW Cuan $100...")
                await page.goto(target_link, wait_until="networkidle", timeout=60000)
                
                # Simulasi Manusia: Scroll & Klik Random
                for _ in range(random.randint(2, 5)):
                    await page.mouse.wheel(0, random.randint(400, 800))
                    await asyncio.sleep(random.randint(3, 6))
                
                # Cari & Klik Tombol (Download/Daftar/Next)
                elements = await page.query_selector_all('a, button, [role="button"]')
                if elements:
                    target = random.choice(elements)
                    await target.click(timeout=5000)
                    print(f"🖱️ Interaksi Klik Selesai")

                # Ngetem lama biar dianggap REAL HUMAN
                ngetem = random.randint(40, 70)
                print(f"⏱️ Sesi {counter} Selesai, ngetem {ngetem}s...")
                await asyncio.sleep(ngetem)
                
            except Exception as e:
                print(f"⚠️ Sesi {counter} Error, lanjut sesi berikutnya...")
            
            await page.close()
            counter += 1
            if counter > 350: break # Safety break setelah 5-6 jam

        await browser.close()

if __name__ == "__main__":
    asyncio.run(gas_nonstop())
