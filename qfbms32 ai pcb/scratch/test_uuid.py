import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")
template_fp = board.FindFootprintByReference("R_B1")
clone = pcbnew.FOOTPRINT(template_fp)
print("Template UUID:", template_fp.m_Uuid.AsString())
print("Clone UUID before:", clone.m_Uuid.AsString())
clone.SetPosition(pcbnew.VECTOR2I(0, 0))
# Generate new KIID
new_kiid = pcbnew.KIID()
print("New KIID:", new_kiid.AsString())
clone.SetUuid(new_kiid)
for pad in clone.Pads():
    pad.SetUuid(pcbnew.KIID())
print("Clone UUID after:", clone.m_Uuid.AsString())
