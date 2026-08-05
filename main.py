import os
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PAGES = [
    {
        "name": "صفحه اصلی",
        "url": "https://www.sanjesh.org/fa-IR/sanjesh/1/page/%D8%B5%D9%81%D8%AD%D9%87-%D8%A7%D8%B5%D9%84%DB%8C"
    },
    {
        "name": "سراسری",
        "url": "https://www.sanjesh.org/fa-IR/sanjesh/4924/page/%D8%B3%D8%B1%D8%A7%D8%B3%D8%B1%DB%8C"
    },
    {
        "name": "دکتری تخصصی",
        "url": "https://www.sanjesh.org/fa-IR/sanjesh/4929/page/%D8%AF%DA%A9%D8%AA%D8%B1%D8%A7%DB%8C-%D8%AA%D8%AE%D8%B5%D8%B5%DB%8C"
    }
]


def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def get_page_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text("\n", strip=True)


def load_old():
    if os.path.exists("old_data.json"):
        with open("old_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_new(data):
    with open("old_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def main():

    old_data = load_old()
    new_data = {}

    changes = []

    for page in PAGES:
        text = get_page_text(page["url"])
        new_data[page["name"]] = text

        if page["name"] in old_data:
            if text != old_data[page["name"]]:
                changes.append(page["name"])

    if changes:
        message = "🔔 تغییر جدید در سایت سازمان سنجش\n\n"
        message += "\n".join(
            ["📌 " + x for x in changes]
        )

        send_message(message)

    save_new(new_data)


if __name__ == "__main__":
    main()
