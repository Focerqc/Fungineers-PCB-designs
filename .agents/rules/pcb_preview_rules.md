# PCB Preview Generation Rules

Whenever generating or updating 2D or 3D preview images (`<board>_2d_view.png`, `<board>_top.png`) for any KiCad board in this workspace:

1. **Never Use Fixed 4:3 Defaults**: The KiCad MCP tool `get_board_2d_view` defaults to 1600x1200 (4:3), which severely distorts/stretches boards of different aspect ratios (e.g. wide boards like 88x28mm or square boards like 20x20mm).
2. **Always Compute Physical Aspect Ratio**:
   - Determine the physical board extents ($W_{\text{mm}} \times H_{\text{mm}}$) from `Edge.Cuts`.
   - Calculate aspect ratio: $R = W_{\text{mm}} / H_{\text{mm}}$.
   - Scale pixel dimensions targeting 2000 px on the longer side:
     - If $W \ge H$: `width = 2000`, `height = round(2000 / R)`.
     - If $H > W$: `height = 2000`, `width = round(2000 * R)`.
3. **Pass Explicit Dimensions to `get_board_2d_view`**:
   - Always supply the calculated `width` and `height` in the tool call arguments.
   - Or use the workspace helper script: `python render_board_preview.py "<path_to_pcb>"`.
4. **Preserve Geometric Integrity**:
   - Circles (mounting holes, vias, test points) must remain circular.
   - Chamfer angles ($45^\circ$) and arc radii must remain geometrically true.
