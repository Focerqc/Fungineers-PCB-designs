import numpy as np

# In Meh ASM vbms STEP FILE.STEP:
# PCB is #122:
pcb_origin = np.array([603.4621162448456744, 864.9834333725589204, 1298.564081872252700])
# XT30PW-F is #342:
f_origin = np.array([659.8121162448458108, 866.4834333725588067, 1307.114908866982205])
# XT30PW-M is #694:
m_origin = np.array([663.4621162448459017, 866.4834333725588067, 1290.022183876417785])

print("F relative to PCB origin:", f_origin - pcb_origin)
print("M relative to PCB origin:", m_origin - pcb_origin)
print("Difference between M and F origin:", m_origin - f_origin)
