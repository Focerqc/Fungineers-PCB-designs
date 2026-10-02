import numpy as np

# In KiCad 3D rotation, when rotate=(0,0,90), does X' = -Y or +Y?
# In KiCad 3d_matrix.cpp:
# rotation angles are yaw (Z), pitch (Y), roll (X).
# For positive angle around Z in standard KiCad:
# x_new = x*cos - y*sin
# y_new = x*sin + y*cos
# For 90 deg: cos=0, sin=1 => x_new = -y, y_new = x.
# But in KiCad 3D viewer, board has Y pointing downwards in 2D (KiCad 5/6/7) or Y pointing upwards in 3D?
# In KiCad 3D viewer, KiCad converts 2D (where Y is down) to 3D (where Y is up or down).

# Let's inspect the actual rendered image pixels!
# In the 3D render VFBMS32_render_3d.png:
# The yellow XT30 body has the mating port facing left (towards X < 0).
# The gold pins extend from the body towards the right (towards X > 0).

# Let's verify by rendering a board with just 1 pad and 1 step model at known coordinates!
