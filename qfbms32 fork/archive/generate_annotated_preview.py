import os
import shutil
from PIL import Image, ImageDraw, ImageFont
def generate_annotated_preview():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(project_dir, "qfbms32_layout_top_hi_raw.png")
    output_path = os.path.join(project_dir, "qfbms32_layout_labeled.png")
    brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\93328da4-de19-448d-baee-62cf3ea51873"
    brain_output_path = os.path.join(brain_dir, "qfbms32_layout_labeled.png")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw image {raw_path} not found. Please run build_qfbms32_layout.py first.")

    src_img = Image.open(raw_path).convert("RGBA")
    sw, sh = src_img.size

    # Canvas padding
    pad_left = 160
    pad_right = 160
    pad_top = 85
    pad_bottom = 160

    cw = sw + pad_left + pad_right
    ch = sh + pad_top + pad_bottom

    # Dark slate background for clean contrast
    canvas = Image.new("RGBA", (cw, ch), (22, 27, 34, 255))

    # Paste board render
    canvas.paste(src_img, (pad_left, pad_top), src_img)
    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_bold = "C:/Windows/Fonts/segoeuib.ttf"
    font_regular = "C:/Windows/Fonts/segoeui.ttf"
    if not os.path.exists(font_bold):
        font_bold = "C:/Windows/Fonts/arialbd.ttf"
        font_regular = "C:/Windows/Fonts/arial.ttf"

    font_corner = ImageFont.truetype(font_bold, 20)
    font_corner_sub = ImageFont.truetype(font_regular, 13)
    font_edge = ImageFont.truetype(font_bold, 18)
    font_edge_sub = ImageFont.truetype(font_regular, 13)
    font_res = ImageFont.truetype(font_bold, 15)
    font_res_sub = ImageFont.truetype(font_bold, 12)

    # Board corners (within raw image, board is at x: 30..1188, y: 30..315)
    # The rendered board is 130mm x 32mm
    scale_x = (sw - 60) / 130.0
    scale_y = (sh - 60) / 32.0

    bx0 = 30 + pad_left
    by0 = 30 + pad_top
    bx1 = sw - 30 + pad_left
    by1 = sh - 30 + pad_top

    # Helper for rounded badge
    def draw_badge(x, y, text, subtext="", bg_color=(30, 41, 59), border_color=(56, 189, 248), text_color=(255, 255, 255)):
        bbox_main = draw.textbbox((0, 0), text, font=font_corner if "Corner" in text else font_edge)
        tw = bbox_main[2] - bbox_main[0]
        th = bbox_main[3] - bbox_main[1]

        sw_w, sw_h = 0, 0
        if subtext:
            bbox_sub = draw.textbbox((0, 0), subtext, font=font_corner_sub)
            sw_w = bbox_sub[2] - bbox_sub[0]
            sw_h = bbox_sub[3] - bbox_sub[1]

        bw = max(tw, sw_w) + 24
        bh = th + (sw_h + 4 if subtext else 0) + 14

        rx0 = int(x - bw / 2)
        ry0 = int(y - bh / 2)
        rx1 = int(x + bw / 2)
        ry1 = int(y + bh / 2)

        draw.rounded_rectangle((rx0, ry0, rx1, ry1), radius=8, fill=bg_color, outline=border_color, width=2)
        
        main_y = ry0 + 6 if subtext else int(y - th / 2) - 2
        draw.text((x, main_y), text, font=font_corner if "Corner" in text else font_edge, fill=text_color, anchor="mt" if subtext else "mm")
        if subtext:
            draw.text((x, ry0 + th + 10), subtext, font=font_corner_sub, fill=(203, 213, 225), anchor="mt")
        return (rx0, ry0, rx1, ry1)

    # Corner targets & lines
    def mark_corner(corner_pt, badge_pt, label, subtext, color):
        cx, cy = corner_pt
        draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=color, width=3)
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=color)

        draw.line([badge_pt, corner_pt], fill=color, width=2)
        draw_badge(badge_pt[0], badge_pt[1], label, subtext, bg_color=(15, 23, 42), border_color=color, text_color=color)

    # 1. Four Corners: A, B, C, D
    # A (top-left)
    mark_corner((bx0, by0), (bx0 - 75, by0 - 40), "A", "Top-Left", (56, 189, 248))  # Cyan
    # B (top-right)
    mark_corner((bx1, by0), (bx1 + 75, by0 - 40), "B", "Top-Right", (56, 189, 248))
    # C (bottom-right)
    mark_corner((bx1, by1), (bx1 + 75, by1 + 45), "C", "Bottom-Right", (56, 189, 248))
    # D (bottom-left)
    mark_corner((bx0, by1), (bx0 - 75, by1 + 45), "D", "Bottom-Left", (56, 189, 248))

    # 2. Long Edges
    top_mid_x = (bx0 + bx1) // 2
    draw.line([(bx0 + 20, by0 - 15), (bx1 - 20, by0 - 15)], fill=(245, 158, 11), width=2)
    draw.polygon([(bx0 + 20, by0 - 15), (bx0 + 28, by0 - 19), (bx0 + 28, by0 - 11)], fill=(245, 158, 11))
    draw.polygon([(bx1 - 20, by0 - 15), (bx1 - 28, by0 - 19), (bx1 - 28, by0 - 11)], fill=(245, 158, 11))
    draw_badge(top_mid_x, by0 - 40, "▲ TOP EDGE (Long Edge) ▲", "130 mm", bg_color=(30, 27, 22), border_color=(245, 158, 11), text_color=(251, 191, 36))

    bot_mid_x = (bx0 + bx1) // 2
    draw_badge(bot_mid_x, by1 + 105, "▼ BOTTOM EDGE (Long Edge) ▼", "130 mm", bg_color=(30, 27, 22), border_color=(245, 158, 11), text_color=(251, 191, 36))
    draw.line([(bx0 + 20, by1 + 75), (bx1 - 20, by1 + 75)], fill=(245, 158, 11), width=2)
    draw.polygon([(bx0 + 20, by1 + 75), (bx0 + 28, by1 + 71), (bx0 + 28, by1 + 79)], fill=(245, 158, 11))
    draw.polygon([(bx1 - 20, by1 + 75), (bx1 - 28, by1 + 71), (bx1 - 28, by1 + 79)], fill=(245, 158, 11))

    # 3. Short Edges
    left_mid_y = (by0 + by1) // 2
    draw_badge(bx0 - 80, left_mid_y, "LEFT SIDE", "Short Edge (32 mm)", bg_color=(20, 30, 45), border_color=(129, 140, 248), text_color=(165, 180, 252))
    draw.line([(bx0 - 14, by0 + 20), (bx0 - 14, by1 - 20)], fill=(129, 140, 248), width=2)
    draw.polygon([(bx0 - 14, by0 + 20), (bx0 - 18, by0 + 28), (bx0 - 10, by0 + 28)], fill=(129, 140, 248))
    draw.polygon([(bx0 - 14, by1 - 20), (bx0 - 18, by1 - 28), (bx0 - 10, by1 - 28)], fill=(129, 140, 248))

    right_mid_y = (by0 + by1) // 2
    draw_badge(bx1 + 80, right_mid_y, "RIGHT SIDE", "Short Edge (32 mm)", bg_color=(20, 30, 45), border_color=(129, 140, 248), text_color=(165, 180, 252))
    draw.line([(bx1 + 14, by0 + 20), (bx1 + 14, by1 - 20)], fill=(129, 140, 248), width=2)
    draw.polygon([(bx1 + 14, by0 + 20), (bx1 + 10, by0 + 28), (bx1 + 18, by0 + 28)], fill=(129, 140, 248))
    draw.polygon([(bx1 + 14, by1 - 20), (bx1 + 10, by1 - 28), (bx1 + 18, by1 - 28)], fill=(129, 140, 248))



    # Save to project folder
    canvas.save(output_path)
    print("Saved annotated preview to:", output_path)

    # Save copy to brain directory for UI embedding
    os.makedirs(brain_dir, exist_ok=True)
    canvas.save(brain_output_path)
    print("Saved brain copy to:", brain_output_path)

if __name__ == "__main__":
    generate_annotated_preview()
