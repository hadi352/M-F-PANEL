import os
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("KATABUMP_EMAIL")
PASSWORD = os.environ.get("KATABUMP_PASSWORD")
SERVER_ID = os.environ.get("SERVER_ID")

def main():
    if not (EMAIL and PASSWORD and SERVER_ID):
        raise SystemExit("Secrets تعریف نشده‌اند")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1280, "height": 720}).new_page()
        try:
            page.goto("https://control.katabump.com/auth/login", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)
            page.locator('input[name="username"], input[name="email"], input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            page.locator('button[type="submit"], input[type="submit"]').first.click()
            page.wait_for_timeout(8000)
            page.goto(f"https://control.katabump.com/server/{SERVER_ID}", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)
            btn = page.locator('button:has-text("Renew"), a:has-text("Renew")')
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                print("Renew کلیک شد")
                page.wait_for_timeout(3000)
            else:
                print("دکمه Renew فعال نیست")
        except Exception:
            page.screenshot(path="error_screenshot.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    main()
