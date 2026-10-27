import math

# JST GH BM10B
jst_y = 22.00
jst_pin_y_local = 1.95
jst_pin_pad_h = 1.4
jst_pin_bottom = jst_y + jst_pin_y_local + (jst_pin_pad_h / 2.0)
jst_top_body = jst_y - 2.50

# R_B (0805 vertical, rot=90)
rb_y = 28.00
rb_pad_offset = 0.9125
rb_pad_h = 1.025
rb_top = rb_y - rb_pad_offset - (rb_pad_h / 2.0)
rb_bottom = rb_y + rb_pad_offset + (rb_pad_h / 2.0)

# R_F (0402 horizontal, rot=0)
rf_y = 30.65
rf_pad_h = 0.60
rf_top = rf_y - (rf_pad_h / 2.0)
rf_bottom = rf_y + (rf_pad_h / 2.0)

board_bottom = 32.00

print(f"JST top body edge:        {jst_top_body:.2f} mm")
print(f"JST pin pad bottom edge:  {jst_pin_bottom:.2f} mm")
print(f"--- GAP (JST to R_B):     {rb_top - jst_pin_bottom:.2f} mm ---")
print(f"R_B top pad edge:         {rb_top:.2f} mm")
print(f"R_B bottom pad edge:      {rb_bottom:.2f} mm")
print(f"--- GAP (R_B to R_F):     {rf_top - rb_bottom:.2f} mm ---")
print(f"R_F top pad edge:         {rf_top:.2f} mm")
print(f"R_F bottom pad edge:      {rf_bottom:.2f} mm")
print(f"--- GAP to board edge:    {board_bottom - rf_bottom:.2f} mm ---")
