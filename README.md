# Japan Visa Tracker for Embassy of Japan in Egypt

This Python script monitors the [Embassy of Japan in Egypt visa status page](https://www.eg.emb-japan.go.jp/itpr_en/11_000001_pick.html) and notifies you via **Pushover** when your visa application number appears, or when the list of results changes.

## 🚀 Features
- Scrapes the embassy website every 30 minutes (configurable).
- Detects if your **8-digit visa application number** is published.
- Alerts when new numbers are added or removed from the list.
- Sends push notifications via **Pushover API**.
- Console logging for real-time updates.
- Uses **Playwright** for reliable page rendering.

## 📦 Requirements
- Python 3.9+
- [Playwright](https://playwright.dev/python/)
- `requests` library
- Pushover account (for API token & user key)

Install dependencies:
```bash
pip install playwright requests
playwright install
````

## ⚙️ Configuration

Edit the script and set your Pushover credentials:

```python
PUSHOVER_USER_KEY = "your_user_key_here"
PUSHOVER_API_TOKEN = "your_api_token_here"
```

You can also adjust the check interval (default: 30 minutes):

```python
CHECK_INTERVAL = 30 * 60
```

## ▶️ Usage

Run the script:

```bash
python japan-visa-tracker-for-egyptians.py
```

Enter your 8-digit visa application number when prompted.
The script will then keep monitoring and notify you when:

* ✅ Your visa is ready.
* 🔔 The list changes (new or removed numbers).

## 📜 License

MIT License – feel free to use and improve this script.
