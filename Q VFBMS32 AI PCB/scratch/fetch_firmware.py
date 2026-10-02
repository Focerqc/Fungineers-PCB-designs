import os
import urllib.request
import json

scratch_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch"
fw_dump_dir = os.path.join(scratch_dir, "firmware_dump")
os.makedirs(fw_dump_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_url(url, dest_path=None):
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            if dest_path:
                with open(dest_path, "wb") as f:
                    f.write(content)
            return content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# 1. Fetch hw.h and hw.c from vesc_express
hw_h_url = "https://raw.githubusercontent.com/vedderb/vesc_express/c085911d8f74a6d1f52f69c17bc035e00e060201/main/hwconf/vesc/vbms32/hw.h"
hw_h_path = os.path.join(fw_dump_dir, "hw.h")
hw_h_text = fetch_url(hw_h_url, hw_h_path)

hw_c_url = "https://raw.githubusercontent.com/vedderb/vesc_express/c085911d8f74a6d1f52f69c17bc035e00e060201/main/hwconf/vesc/vbms32/hw.c"
hw_c_path = os.path.join(fw_dump_dir, "hw.c")
hw_c_text = fetch_url(hw_c_url, hw_c_path)

# Also check folder contents of vesc_express vbms32
express_api_url = "https://api.github.com/repos/vedderb/vesc_express/contents/main/hwconf/vesc/vbms32"
express_json_str = fetch_url(express_api_url)
if express_json_str:
    try:
        items = json.loads(express_json_str)
        print("vesc_express vbms32 directory items:")
        for item in items:
            print(f"  {item.get('name')} -> {item.get('download_url')}")
            if item.get("name") not in ["hw.h", "hw.c"] and item.get("download_url"):
                fetch_url(item.get("download_url"), os.path.join(fw_dump_dir, item.get("name")))
    except Exception as e:
        print("Error parsing express items:", e)

# 2. Fetch vesc_pkg vbms32_micro contents
pkg_api_url = "https://api.github.com/repos/vedderb/vesc_pkg/contents/vbms32_micro"
pkg_json_str = fetch_url(pkg_api_url)
if pkg_json_str:
    try:
        items = json.loads(pkg_json_str)
        print("\nvesc_pkg vbms32_micro directory items:")
        for item in items:
            name = item.get("name")
            dl_url = item.get("download_url")
            print(f"  {name} -> {dl_url}")
            if dl_url:
                fetch_url(dl_url, os.path.join(fw_dump_dir, name))
    except Exception as e:
        print("Error parsing pkg items:", e)

print("\n--- Download complete ---")
