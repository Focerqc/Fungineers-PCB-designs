from pathlib import Path

t = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym").read_text(
    encoding="utf-8"
)
i = t.find('(symbol "Conn_01x02"')
print("idx", i)
print(t[i : i + 500])
