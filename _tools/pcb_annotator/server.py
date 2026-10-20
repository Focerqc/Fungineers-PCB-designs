#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import urllib.parse
import mimetypes
import webbrowser
from PIL import Image

PORT = 5180
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", ".."))

class AnnotatorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=TOOL_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/api/scan-images":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            images = []
            valid_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
            for root, dirs, files in os.walk(REPO_ROOT):
                # skip git, brain, node_modules
                if ".git" in root or ".gemini" in root or "node_modules" in root or ".history" in root:
                    continue
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in valid_exts:
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, REPO_ROOT).replace("\\", "/")
                        size_kb = round(os.path.getsize(full_path) / 1024, 1)
                        dim_w, dim_h = None, None
                        try:
                            with Image.open(full_path) as im:
                                dim_w, dim_h = im.size
                        except Exception:
                            pass
                        images.append({
                            "name": f,
                            "rel_path": rel_path,
                            "size_kb": size_kb,
                            "width": dim_w,
                            "height": dim_h,
                            "folder": os.path.basename(os.path.dirname(full_path))
                        })
            # Prioritize reference images and VFBMS32
            images.sort(key=lambda x: (
                0 if "vfbms32_cad_top_reference_rotated" in x["name"] else
                1 if "_reference" in x["rel_path"] else
                2 if "Q VFBMS32" in x["rel_path"] else 3,
                x["rel_path"]
            ))
            self.wfile.write(json.dumps(images).encode("utf-8"))
            return

        elif path == "/api/image":
            rel_path = params.get("path", [""])[0]
            clean_rel = urllib.parse.unquote(rel_path).lstrip("/\\")
            full_path = os.path.normpath(os.path.join(REPO_ROOT, clean_rel))
            if not full_path.startswith(REPO_ROOT) or not os.path.isfile(full_path):
                self.send_error(404, "File not found")
                return

            mime_type, _ = mimetypes.guess_type(full_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(os.path.getsize(full_path)))
            self.end_headers()
            with open(full_path, "rb") as f:
                self.wfile.write(f.read())
            return

        elif path == "/api/load-annotations":
            proj_file = params.get("file", [""])[0]
            clean_file = urllib.parse.unquote(proj_file).lstrip("/\\")
            full_path = os.path.normpath(os.path.join(REPO_ROOT, clean_file))
            if not full_path.startswith(REPO_ROOT) or not os.path.isfile(full_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"exists": False, "data": None}).encode("utf-8"))
                return

            with open(full_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"exists": True, "data": content}).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/save-annotations":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body)
            target_rel = payload.get("target_path", "Q VFBMS32 AI PCB/pcb_annotations.json").lstrip("/\\")
            target_full = os.path.normpath(os.path.join(REPO_ROOT, target_rel))

            if not target_full.startswith(REPO_ROOT):
                self.send_error(403, "Invalid path")
                return

            os.makedirs(os.path.dirname(target_full), exist_ok=True)
            with open(target_full, "w", encoding="utf-8") as f:
                json.dump(payload.get("data", {}), f, indent=2)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "saved_to": target_rel,
                "components_count": len(payload.get("data", {}).get("components", []))
            }).encode("utf-8"))
            return

        elif path == "/api/generate-kicad-script":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body)
            data = payload.get("data", {})
            target_rel = payload.get("target_path", "Q VFBMS32 AI PCB/place_annotated_parts.py").lstrip("/\\")
            target_full = os.path.normpath(os.path.join(REPO_ROOT, target_rel))

            components = data.get("components", [])
            calib = data.get("calibration", {})

            # Build runnable python script for KiCad / standalone
            code_lines = [
                '# Generated by Antigravity PCB Annotator',
                '# Automatic Footprint Placement Script for KiCad pcbnew',
                'import os',
                'import pcbnew',
                '',
                f'# Board calibration: {calib.get("scale_x_mm_per_px", 0.16):.4f} mm/px',
                'COMPONENTS = [',
            ]
            for c in components:
                code_lines.append(f"    {{'ref': '{c.get('ref')}', 'val': '{c.get('val', '')}', 'fp': '{c.get('footprint', '')}', 'x': {c.get('x_mm', 0):.2f}, 'y': {c.get('y_mm', 0):.2f}, 'rot': {c.get('rot', 0):.1f}, 'side': '{c.get('side', 'top')}'}},")
            code_lines.extend([
                ']',
                '',
                'def place_parts(pcb_path=None):',
                '    if pcb_path is None:',
                '        pcb_path = r"VFBMS32.kicad_pcb"',
                '    board = pcbnew.LoadBoard(pcb_path)',
                '    for item in COMPONENTS:',
                '        fp = board.FindFootprintByReference(item["ref"])',
                '        if fp:',
                '            pos = pcbnew.VECTOR2I(pcbnew.FromMM(item["x"]), pcbnew.FromMM(item["y"]))',
                '            fp.SetPosition(pos)',
                '            fp.SetOrientation(pcbnew.EDA_ANGLE(item["rot"], pcbnew.DEGREES_T))',
                '            print(f"Updated {item[\'ref\']} at ({item[\'x\']}, {item[\'y\']})")',
                '    pcbnew.SaveBoard(pcb_path, board)',
                '    print("Placement complete and saved!")',
                '',
                'if __name__ == "__main__":',
                '    place_parts()',
                ''
            ])
            script_code = "\n".join(code_lines)
            with open(target_full, "w", encoding="utf-8") as f:
                f.write(script_code)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "script_path": target_rel,
                "parts_count": len(components)
            }).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

def run(port=PORT):
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), AnnotatorHandler) as httpd:
        print(f"=======================================================")
        print(f"  Antigravity PCB Annotator & Calibrator running at:")
        print(f"  http://localhost:{port}")
        print(f"  Repo Root: {REPO_ROOT}")
        print(f"=======================================================")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
