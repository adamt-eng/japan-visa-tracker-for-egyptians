import datetime
import time
import re
import requests
from playwright.sync_api import sync_playwright

# --- CONFIG ---
PUSHOVER_USER_KEY = input("Enter your PUSHOVER_USER_KEY: ").strip()
PUSHOVER_API_TOKEN = input("Enter your PUSHOVER_API_TOKEN: ").strip()
URL = "https://www.eg.emb-japan.go.jp/itpr_en/11_000001_pick.html"
CHECK_INTERVAL = 30 * 60 # 30 minutes

# --- NOTIFICATIONS ---
def send_notification(message: str):
    print(message) # Log to terminal
    try:
        requests.post("https://api.pushover.net/1/messages.json", data= { "token": PUSHOVER_API_TOKEN, "user": PUSHOVER_USER_KEY, "message": message }, timeout=10)
    except Exception as e:
        print(f"Failed to send pushover message: {e}")

# --- FETCHING ---
def fetch_codes():
    """Fetch 8-digit codes starting with 7 from the embassy page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Visible browser
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # Wait until at least one <td> appears in DOM
        try:
            page.wait_for_selector("td", timeout=15000)
        except Exception:
            print("⚠️ Timed out waiting for <td> elements")

        html = page.content()
        browser.close()

    return re.findall(r"\b7\d{7}\b", html)

# --- MAIN ---
if __name__ == "__main__":
    # Ask user which visa number to watch
    SEARCH_STRING = input("Enter your 8-digit visa application number: ").strip()

    last_codes = []
    last_count = 0

    while True:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for updates...")
        try:
            codes = fetch_codes()
            count = len(codes)
            
            # Check if your visa number appears
            if SEARCH_STRING in codes:
                send_notification(f"✅ Your visa '{SEARCH_STRING}' is ready!")

            # Check if list changed
            elif codes != last_codes and last_codes:  # skip alert on very first run
                added = set(codes) - set(last_codes)
                removed = set(last_codes) - set(codes)
                msg = f"🔔 Visa list changed! Total now {count} codes."
                if added:
                    msg += f"\nNew: {', '.join(sorted(added))}"
                if removed:
                    msg += f"\nRemoved: {', '.join(sorted(removed))}"
                send_notification(msg)

            last_codes = codes
            last_count = count

        except Exception as e:
            send_notification(f"⚠️ Error checking site: {e}")

        time.sleep(CHECK_INTERVAL)