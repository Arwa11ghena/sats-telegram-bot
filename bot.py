import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        },
        timeout=20
    )


@app.route("/")
def home():
    return "SATS Telegram Bot is running successfully 🚀"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)

    if isinstance(data, dict):
        message = "\n".join(
            [f"<b>{k}</b>: {v}" for k, v in data.items()]
        )
    else:
        message = str(data)

    send_telegram("📈 <b>TradingView Alert</b>\n\n" + message)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
