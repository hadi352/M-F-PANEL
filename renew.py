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
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        page = context.new_page()
        try:
            page.goto("https://control.katabump.com/auth/login", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            page.locator('input[name="username"], input[name="email"], input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            page.locator('button[type="submit"], input[type="submit"]').first.click()
            page.wait_for_timeout(8000)

            page.goto(f"https://control.katabump.com/server/{SERVER_ID}", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            if "login" in page.url:
                page.screenshot(path="error_screenshot.png")
                raise Exception("لاگین انجام نشد")

            btn = page.locator('button:has-text("Restart"), a:has-text("Restart")').first
            if btn.count() == 0 or not btn.is_visible():
                page.screenshot(path="error_screenshot.png")
                raise Exception("دکمه Restart پیدا نشد")

            btn.click()
            page.wait_for_timeout(2000)

            # اگر پنجره تأیید باز شد، تأیید می‌کنیم
            confirm = page.locator(
                '.modal button:has-text("Restart"), .modal button:has-text("Yes"), '
                '.modal button:has-text("Confirm"), [role="dialog"] button:has-text("Restart"), '
                '[role="dialog"] button:has-text("Yes"), [role="dialog"] button:has-text("Confirm")'
            )
            if confirm.count() > 0 and confirm.first.is_visible():
                confirm.first.click()
                print("تأیید ریستارت زده شد")

            page.wait_for_timeout(5000)
            page.screenshot(path="error_screenshot.png")
            print("✅ ریستارت انجام شد")
        except Exception as e:
            print("خطا:", e)
            try:
                page.screenshot(path="error_screenshot.png")
            except Exception:
                pass
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    main()
