# Superflux Hall Sensor PCB

High-precision hall sensor PCB designed for the Fungineers Superflux motor.

---

## 1. Design Overview

- **Layer Stackup**: 2-Layer FR4, 1.6 mm thickness
- **Solder Mask**: Purple (`#43135C` / `#591271`), matching Superflux motor branding
- **Surface Finish**: ENIG (Electroless Nickel Immersion Gold)
- **Stator Alignment**: Derived from original stator drawing `sf hall locations.DXF` (27-slot stator, $13.\overline{3}^\circ$ pitch)

### Hall Sensor Centers (at $R = 56.15\,\text{mm}$):
- **U1**: $23^\circ 20'$ ($23.3333^\circ$)
- **U2**: $63^\circ 20'$ ($63.3333^\circ$)
- **U3**: $103^\circ 20'$ ($103.3333^\circ$)
- **Sensor Pitch**: Exactly $40.000^\circ$ (3 stator teeth) between sensors.
- **Pin Spread**: $\pm 2.45^\circ$ ($2.40\,\text{mm}$ pitch) between outer pins and centered middle pin.

---

## 2. TODO / Future Work: Hall Slot 3D Edge Plating

> [!WARNING]
> **CAD Modeling Note — Hall Slot Edge Plating**
>
> The hall sensor slots currently have:
> - $1.25\,\text{mm}$ wide clean U-slots on `Edge.Cuts` with semicircular rounded bottoms ($R = 0.625\,\text{mm}$).
> - U-shaped copper solder lands on `F.Cu` and `B.Cu` framing each slot with zero protrusion into the slot or past the outer board edge.
>
> **Known CAD Limitation**:
> In physical manufacturing (e.g., JLCPCB castellated holes / edge plating), the internal vertical walls of these slots are plated with copper and immersion gold. However, the standard KiCad STEP export pipeline (`kicad-cli pcb export step`) does not generate 3D vertical copper plating along internal `Edge.Cuts` slot profiles—it only exports planar surface copper pads and cylindrical through-hole barrels.
>
> **Action Required**:
> The pads are close and functional for component clearance and leg passage, but need work later to accurately model the vertical edge plating in the CAD/STEP assembly (either via custom 3D STEP body injection or an updated KiCad castellated modeling workflow).
