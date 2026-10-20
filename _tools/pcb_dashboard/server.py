#!/usr/bin/env python3
"""
PCB Dashboard server.
Serves the UI and talks to KiCad through kicad_bridge.py (run with KiCad's own Python).

  python server.py            -> http://localhost:5180
"""
import datetime
import http.server
import json
import mimetypes
import os
import socketserver
import subprocess
import urllib.parse
from PIL import Image

PORT = 5180
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", ".."))
KICAD_PYTHON = r"C:\Program Files\KiCad\10.0\bin\python.exe"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
BRIDGE = os.path.join(TOOL_DIR, "kicad_bridge.py")
SKIP_DIRS = {".git", ".history", "node_modules", ".dashboard_backups", "__pycache__"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

_board_cache = {}  # abs_path -> (mtime, data)


def render_3d_file(board_full):
    return os.path.splitext(board_full)[0] + "_3d_top.png"


def render_board_3d(board_full):
    if not os.path.isfile(board_full):
        raise FileNotFoundError(f"Board file not found: {board_full}")
    out_png = render_3d_file(board_full)
    cmd = [
        KICAD_CLI, "pcb", "render",
        "--side", "top",
        "--width", "4000",
        "--height", "2000",
        "--background", "transparent",
        "-o", out_png,
        board_full
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if res.returncode != 0 or not os.path.isfile(out_png):
        raise RuntimeError(f"kicad-cli render failed: {res.stderr or res.stdout}")

    try:
        im = Image.open(out_png)
        bbox = im.getbbox()
        if bbox:
            im.crop(bbox).save(out_png)
    except Exception as e:
        print(f"PIL crop warning: {e}")

    mtime = os.path.getmtime(out_png)
    dt = datetime.datetime.fromtimestamp(mtime)
    timestamp_str = dt.strftime("%b %d, %I:%M:%S %p")
    return {
        "status": "ok",
        "image": rel(out_png),
        "timestamp": timestamp_str,
        "mtime": mtime
    }


def get_render_3d_status(board_full):
    out_png = render_3d_file(board_full)
    if not os.path.isfile(out_png):
        return {"exists": False}
    mtime = os.path.getmtime(out_png)
    dt = datetime.datetime.fromtimestamp(mtime)
    timestamp_str = dt.strftime("%b %d, %I:%M:%S %p")
    return {
        "exists": True,
        "image": rel(out_png),
        "timestamp": timestamp_str,
        "mtime": mtime
    }


def safe_path(rel):
    rel = urllib.parse.unquote(rel or "").lstrip("/\\")
    full = os.path.normpath(os.path.join(REPO_ROOT, rel))
    if not full.startswith(REPO_ROOT):
        raise PermissionError("path outside repo")
    return full


def rel(full):
    return os.path.relpath(full, REPO_ROOT).replace("\\", "/")


def walk_files(exts):
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                yield os.path.join(root, f)


def run_bridge(*args):
    proc = subprocess.run(
        [KICAD_PYTHON, BRIDGE, *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    out = proc.stdout
    idx = out.find("@@JSON@@")
    if idx < 0:
        raise RuntimeError((proc.stderr or out or "bridge failed")[-2000:])
    return json.loads(out[idx + len("@@JSON@@"):])


def boxes_file(board_full):
    return os.path.splitext(board_full)[0] + ".boxes.json"


def read_board(full):
    mtime = os.path.getmtime(full)
    cached = _board_cache.get(full)
    if cached and cached[0] == mtime:
        return cached[1]
    data = run_bridge("read", full)
    data["path"] = rel(full)
    _board_cache[full] = (mtime, data)
    return data


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=TOOL_DIR, **kw)

    def log_message(self, fmt, *args):
        try:
            msg = fmt % args
        except Exception:
            msg = str(fmt)
        if "/api/" in msg:
            super().log_message(fmt, *args)

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        try:
            if u.path == "/api/boards":
                boards = sorted(rel(p) for p in walk_files({".kicad_pcb"}))
                return self.send_json(boards)

            if u.path == "/api/images":
                imgs = []
                for p in walk_files(IMAGE_EXTS):
                    norm = rel(p).lower()
                    if "_3d_top" in norm or "_3d_bottom" in norm or "/scratch/" in norm or norm.startswith("scratch/") or "test_" in norm or ".tempmediastorage" in norm:
                        continue
                    imgs.append({"path": rel(p), "name": os.path.basename(p),
                                 "kb": round(os.path.getsize(p) / 1024)})
                imgs.sort(key=lambda i: ("_reference" not in i["path"], i["path"]))
                return self.send_json(imgs)

            if u.path == "/api/board":
                full = safe_path(q.get("path", [""])[0])
                return self.send_json(read_board(full))

            if u.path == "/api/boxes":
                bf = boxes_file(safe_path(q.get("path", [""])[0]))
                if not os.path.isfile(bf):
                    return self.send_json({"exists": False})
                with open(bf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["exists"] = True
                return self.send_json(data)

            if u.path == "/api/render_status":
                full = safe_path(q.get("path", [""])[0])
                return self.send_json(get_render_3d_status(full))

            if u.path == "/api/render_3d":
                full = safe_path(q.get("path", [""])[0])
                return self.send_json(render_board_3d(full))

            if u.path == "/api/image":
                full = safe_path(q.get("path", [""])[0])
                if not os.path.isfile(full):
                    return self.send_error(404)
                mime = mimetypes.guess_type(full)[0] or "application/octet-stream"
                with open(full, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
        except Exception as e:  # noqa: BLE001
            return self.send_json({"error": str(e)}, 500)

        if u.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        try:
            if u.path == "/api/render_3d":
                full = safe_path(q.get("path", [""])[0])
                return self.send_json(render_board_3d(full))

            if u.path == "/api/boxes":
                full = safe_path(q.get("path", [""])[0])
                if not full.lower().endswith(".kicad_pcb"):
                    raise ValueError("path must be a .kicad_pcb")
                bf = boxes_file(full)
                payload.pop("exists", None)
                payload["board"] = rel(full)
                tmp = bf + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=1)
                os.replace(tmp, bf)
                return self.send_json({"status": "ok", "file": rel(bf)})
        except Exception as e:  # noqa: BLE001
            return self.send_json({"error": str(e)}, 500)
        self.send_error(404)


def main():
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"PCB Dashboard -> http://localhost:{PORT}   (repo: {REPO_ROOT})")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
