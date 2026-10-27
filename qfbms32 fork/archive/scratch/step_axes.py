import numpy as np

# In Meh ASM vbms STEP FILE.STEP:
# XT30PW-F (#342):
# Origin: (659.8121162448458108, 866.4834333725588067, 1307.114908866982205)
# AXIS (Z of part in asm): (0, 1, 0)
# REF (X of part in asm): (-1, 0, 0)
# Therefore, Y of part in asm = Z x X = (0, 1, 0) x (-1, 0, 0) = (0, 0, 1) ?
# Wait! In right handed system:
# X_asm = (-1, 0, 0)
# Z_asm = (0, 1, 0)
# Y_asm = Z_asm x X_asm = (0, 1, 0) x (-1, 0, 0) = (0, 0, 1)
# So part Y axis points along assembly +Z!
# Wait, let's verify if the mating face of F in the assembly is along X or Z:
# Look at AXIS2_PLACEMENT_3D #342:
# AXIS: (0, 1, 0)
# REF: (-1, 0, 0)
# If part coordinate is (x, y, z):
# Point in asm = Origin + x * REF + y * (AXIS x REF) ? Or standard STEP convention:
# STEP convention:
# P = Origin + x * (REF) + y * (AXIS x REF) + z * AXIS ? No!
# In STEP ISO 10303-42:
# AXIS2_PLACEMENT_3D(location, axis, ref_direction):
# z_axis = axis / |axis|
# x_axis = (ref_direction - (ref_direction . z_axis)*z_axis) / |...|
# y_axis = z_axis x x_axis
# So:
# z_axis is AXIS
# x_axis is REF
# y_axis is AXIS x REF
# For #342:
# z_axis = (0, 1, 0)
# x_axis = (-1, 0, 0)
# y_axis = (0, 1, 0) x (-1, 0, 0) = (0, 0, 1)

# Wait, let's check:
# For XT30PW-F, mating face was at y = -6.0.
# So along part Y axis, it is -6.0 * y_axis = (0, 0, -6.0) ?
# Wait, let's check if part Y or part X is mating face!
# Let's check which axis of the XT30 is the connector mating direction!
