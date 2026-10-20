// Antigravity PCB Part Annotator & Calibrator
// Ultra-fast HTML5 Canvas + Board mm Math

(function () {
  'use strict';

  // --- APPLICATION STATE ---
  const state = {
    currentImage: null,
    imageSrc: '',
    imagePath: '',
    imageWidth: 813,
    imageHeight: 200,

    // Calibration
    boardWidthMm: 130.0,
    boardHeightMm: 32.0,
    scaleMmPerPx: 0.1600,
    originX_px: 0,
    originY_px: 0,
    calibMode: 'crop', // 'crop' (image bounds = board bounds) or '2point'
    calibPoints: [],

    // Viewport Transform (Pan & Zoom)
    zoom: 1.0,
    panX: 50,
    panY: 50,
    isPanning: false,
    panStartX: 0,
    panStartY: 0,

    // Active Tool
    activeTool: 'pan', // 'pan', 'box', 'point', 'ruler', 'calib'
    showGrid: false,
    showOutline: true,

    // Components list
    components: [],
    selectedCompIndex: -1,

    // In-progress drawing
    isDrawing: false,
    dragStart: { x: 0, y: 0 },
    dragCurrent: { x: 0, y: 0 },
    rulerDistMm: 0,

    // History for Undo/Redo
    history: [],
    historyIndex: -1,

    // Prefixes counter for auto-increment
    counters: { R: 1, C: 1, U: 1, J: 1, Q: 1, D: 1, TP: 1, L: 1 }
  };

  // --- DOM ELEMENTS ---
  const canvas = document.getElementById('mainCanvas');
  const ctx = canvas.getContext('2d');
  const viewport = document.getElementById('canvasViewport');

  // HUD
  const hudX = document.getElementById('hudX');
  const hudY = document.getElementById('hudY');
  const hudPx = document.getElementById('hudPx');
  const zoomPercent = document.getElementById('zoomPercent');
  const calibText = document.getElementById('calibText');
  const calibPill = document.getElementById('calibPill');

  // Controls
  const imageSelect = document.getElementById('imageSelect');
  const fileInput = document.getElementById('fileInput');
  const btnUploadImage = document.getElementById('btnUploadImage');
  const boardPreset = document.getElementById('boardPreset');
  const boardWidthMmInput = document.getElementById('boardWidthMm');
  const boardHeightMmInput = document.getElementById('boardHeightMm');
  const boardScaleInput = document.getElementById('boardScaleMmPerPx');
  const originModeSelect = document.getElementById('originMode');
  const btnApplyCalib = document.getElementById('btnApplyCalib');

  // Component Props Form
  const propRef = document.getElementById('propRef');
  const propVal = document.getElementById('propVal');
  const propFp = document.getElementById('propFp');
  const propX = document.getElementById('propX');
  const propY = document.getElementById('propY');
  const propW = document.getElementById('propW');
  const propH = document.getElementById('propH');
  const propAutoInc = document.getElementById('propAutoInc');
  const selIndexBadge = document.getElementById('selIndexBadge');
  const btnDeletePart = document.getElementById('btnDeletePart');
  const btnDuplicatePart = document.getElementById('btnDuplicatePart');
  const btnSideTop = document.getElementById('btnSideTop');
  const btnSideBot = document.getElementById('btnSideBot');
  const rotBtns = document.querySelectorAll('.rot-btn[data-rot]');
  const chipBtns = document.querySelectorAll('.chip-btn');

  // Drawer & Table
  const bottomDrawer = document.getElementById('bottomDrawer');
  const drawerHeader = document.getElementById('drawerHeader');
  const drawerToggleIcon = document.getElementById('drawerToggleIcon');
  const partsCount = document.getElementById('partsCount');
  const partsTableBody = document.getElementById('partsTableBody');
  const btnClearAll = document.getElementById('btnClearAll');

  // Modals
  const modalAgent = document.getElementById('modalAgent');
  const modalTitle = document.getElementById('modalTitle');
  const modalDesc = document.getElementById('modalDesc');
  const modalCodePreview = document.getElementById('modalCodePreview');
  const btnCopyModal = document.getElementById('btnCopyModal');
  const modalClose = document.getElementById('modalClose');

  // Header Actions
  const btnAgentModal = document.getElementById('btnAgentModal');
  const btnSaveWorkspace = document.getElementById('btnSaveWorkspace');
  const btnKiCadScript = document.getElementById('btnKiCadScript');

  // Toolbar Buttons
  const toolBtns = {
    pan: document.getElementById('toolPan'),
    box: document.getElementById('toolBox'),
    point: document.getElementById('toolPoint'),
    ruler: document.getElementById('toolRuler'),
    calib: document.getElementById('toolCalib')
  };
  const btnToggleGrid = document.getElementById('btnToggleGrid');
  const btnToggleOutline = document.getElementById('btnToggleOutline');
  const btnZoomFit = document.getElementById('btnZoomFit');
  const btnZoomIn = document.getElementById('btnZoomIn');
  const btnZoomOut = document.getElementById('btnZoomOut');
  const btnUndo = document.getElementById('btnUndo');
  const btnRedo = document.getElementById('btnRedo');

  // --- INITIALIZATION ---
  function init() {
    setupCanvas();
    setupEventListeners();
    setupHotkeys();
    loadWorkspaceImages();

    // Default image
    const defaultImg = "Q VFBMS32 AI PCB/_reference/vfbms32_cad_top_reference_rotated.png";
    loadImageFromPath(defaultImg);
  }

  // --- CANVAS RESIZE & SETUP ---
  function setupCanvas() {
    function resize() {
      const rect = viewport.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      render();
    }
    window.addEventListener('resize', resize);
    resize();
  }

  // --- IMAGE LOADING ---
  function loadImageFromPath(relPath) {
    state.imagePath = relPath;
    const url = `/api/image?path=${encodeURIComponent(relPath)}`;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      state.currentImage = img;
      state.imageSrc = url;
      state.imageWidth = img.naturalWidth || img.width;
      state.imageHeight = img.naturalHeight || img.height;
      recalculateScale();
      zoomToFit();
      render();
      loadProjectAnnotations();
    };
    img.src = url;
  }

  function recalculateScale() {
    if (state.calibMode === 'crop') {
      state.scaleMmPerPx = state.boardWidthMm / state.imageWidth;
      state.originX_px = 0;
      state.originY_px = 0;
    }
    boardScaleInput.value = state.scaleMmPerPx.toFixed(4);
    calibText.textContent = `${state.boardWidthMm.toFixed(1)} × ${state.boardHeightMm.toFixed(1)} mm (${state.scaleMmPerPx.toFixed(4)} mm/px)`;
    calibPill.classList.remove('warning');
  }

  function zoomToFit() {
    if (!state.currentImage) return;
    const rect = viewport.getBoundingClientRect();
    const pad = 60;
    const scaleX = (rect.width - pad * 2) / state.imageWidth;
    const scaleY = (rect.height - pad * 2) / state.imageHeight;
    state.zoom = Math.min(scaleX, scaleY, 4.0);
    state.panX = (rect.width - state.imageWidth * state.zoom) / 2;
    state.panY = (rect.height - state.imageHeight * state.zoom) / 2;
    updateZoomHUD();
    render();
  }

  function updateZoomHUD() {
    zoomPercent.textContent = `${Math.round(state.zoom * 100)}%`;
  }

  // --- COORDINATE CONVERSIONS ---
  function clientToImage(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const canvasX = clientX - rect.left;
    const canvasY = clientY - rect.top;
    const imgX = (canvasX - state.panX) / state.zoom;
    const imgY = (canvasY - state.panY) / state.zoom;
    return { x: imgX, y: imgY };
  }

  function imageToMm(imgX, imgY) {
    const mmX = (imgX - state.originX_px) * state.scaleMmPerPx;
    const mmY = (imgY - state.originY_px) * state.scaleMmPerPx;
    return { x: mmX, y: mmY };
  }

  function mmToImage(mmX, mmY) {
    const imgX = (mmX / state.scaleMmPerPx) + state.originX_px;
    const imgY = (mmY / state.scaleMmPerPx) + state.originY_px;
    return { x: imgX, y: imgY };
  }

  function imageToCanvas(imgX, imgY) {
    return {
      x: imgX * state.zoom + state.panX,
      y: imgY * state.zoom + state.panY
    };
  }

  // --- FOOTPRINT AUTO-DETECTION ---
  function suggestFootprint(w_mm, h_mm) {
    const maxDim = Math.max(w_mm, h_mm);
    const minDim = Math.min(w_mm, h_mm);

    // Passives
    if (Math.abs(maxDim - 1.0) < 0.35 && Math.abs(minDim - 0.5) < 0.3) return { fp: "R_0402_1005Metric", prefix: "R" };
    if (Math.abs(maxDim - 1.6) < 0.35 && Math.abs(minDim - 0.8) < 0.3) return { fp: "R_0603_1608Metric", prefix: "R" };
    if (Math.abs(maxDim - 2.0) < 0.45 && Math.abs(minDim - 1.25) < 0.4) return { fp: "R_0805_2012Metric", prefix: "R" };
    if (Math.abs(maxDim - 3.2) < 0.5 && Math.abs(minDim - 1.6) < 0.4) return { fp: "R_1206_3216Metric", prefix: "R" };

    // SOT-23
    if (Math.abs(maxDim - 2.9) < 0.6 && Math.abs(minDim - 2.4) < 0.6) return { fp: "SOT-23", prefix: "Q" };

    // SOIC-8
    if (Math.abs(maxDim - 5.0) < 0.8 && Math.abs(minDim - 4.0) < 0.8) return { fp: "SOIC-8_3.9x4.9mm_P1.27mm", prefix: "U" };

    // QFN-32 (5x5mm)
    if (Math.abs(maxDim - 5.0) < 0.7 && Math.abs(minDim - 5.0) < 0.7) return { fp: "QFN-32-1EP_5x5mm_P0.5mm", prefix: "U" };

    // TQFP-48 / BQ76952 (7x7mm)
    if (Math.abs(maxDim - 7.0) < 1.0 && Math.abs(minDim - 7.0) < 1.0) return { fp: "TQFP-48_7x7mm_P0.5mm", prefix: "U" };

    // ESP32-C3-MINI-1 (13.2 x 16.6 mm)
    if (Math.abs(maxDim - 16.6) < 2.5 && Math.abs(minDim - 13.2) < 2.5) return { fp: "ESP32-C3-MINI-1", prefix: "U" };

    // XT30
    if (maxDim > 8.0 && minDim > 4.5 && maxDim < 13.0) return { fp: "XT30PW-M", prefix: "J" };

    return null;
  }

  function getNextRef(prefix = "U") {
    if (!state.counters[prefix]) state.counters[prefix] = 1;
    // Find next unused
    let num = state.counters[prefix];
    while (state.components.some(c => c.ref === `${prefix}${num}`)) {
      num++;
    }
    state.counters[prefix] = num + 1;
    return `${prefix}${num}`;
  }

  // --- RENDER PIPELINE ---
  function render() {
    const rect = viewport.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);

    if (!state.currentImage) {
      ctx.fillStyle = '#64748b';
      ctx.font = '14px Space Grotesk';
      ctx.textAlign = 'center';
      ctx.fillText('Select or drop a reference image to begin', rect.width / 2, rect.height / 2);
      return;
    }

    ctx.save();
    ctx.translate(state.panX, state.panY);
    ctx.scale(state.zoom, state.zoom);

    // 1. Draw Reference Image
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(state.currentImage, 0, 0, state.imageWidth, state.imageHeight);

    // 2. Draw Board Outline (Green edge)
    if (state.showOutline) {
      ctx.strokeStyle = '#00f5d4';
      ctx.lineWidth = 1.5 / state.zoom;
      ctx.strokeRect(0, 0, state.imageWidth, state.imageHeight);

      // Corner radius indicator (1mm corner arcs)
      const r_px = 1.0 / state.scaleMmPerPx;
      ctx.strokeStyle = 'rgba(0, 245, 212, 0.4)';
      ctx.strokeRect(r_px, r_px, state.imageWidth - 2 * r_px, state.imageHeight - 2 * r_px);
    }

    // 3. Millimeter Grid
    if (state.showGrid) {
      drawMmGrid();
    }

    // 4. Draw Existing Components
    state.components.forEach((comp, idx) => {
      drawComponent(comp, idx === state.selectedCompIndex);
    });

    // 5. Draw Active In-Progress Dragging
    if (state.isDrawing) {
      if (state.activeTool === 'box') {
        const x1 = Math.min(state.dragStart.x, state.dragCurrent.x);
        const y1 = Math.min(state.dragStart.y, state.dragCurrent.y);
        const w = Math.abs(state.dragCurrent.x - state.dragStart.x);
        const h = Math.abs(state.dragCurrent.y - state.dragStart.y);

        ctx.fillStyle = 'rgba(0, 245, 212, 0.2)';
        ctx.fillRect(x1, y1, w, h);
        ctx.strokeStyle = '#00f5d4';
        ctx.lineWidth = 1.5 / state.zoom;
        ctx.setLineDash([4 / state.zoom, 2 / state.zoom]);
        ctx.strokeRect(x1, y1, w, h);
        ctx.setLineDash([]);

        // Live Dimension badge
        const mmW = (w * state.scaleMmPerPx).toFixed(2);
        const mmH = (h * state.scaleMmPerPx).toFixed(2);
        drawFloatingBadge(x1 + w / 2, y1 - 8 / state.zoom, `${mmW} × ${mmH} mm`, '#00f5d4');
      } else if (state.activeTool === 'ruler') {
        ctx.beginPath();
        ctx.moveTo(state.dragStart.x, state.dragStart.y);
        ctx.lineTo(state.dragCurrent.x, state.dragCurrent.y);
        ctx.strokeStyle = '#ffd166';
        ctx.lineWidth = 2 / state.zoom;
        ctx.stroke();

        const dx = (state.dragCurrent.x - state.dragStart.x) * state.scaleMmPerPx;
        const dy = (state.dragCurrent.y - state.dragStart.y) * state.scaleMmPerPx;
        const distMm = Math.hypot(dx, dy).toFixed(2);
        const midX = (state.dragStart.x + state.dragCurrent.x) / 2;
        const midY = (state.dragStart.y + state.dragCurrent.y) / 2;
        drawFloatingBadge(midX, midY, `${distMm} mm (${(distMm * 39.37).toFixed(1)} mil)`, '#ffd166');
      }
    }

    ctx.restore();
  }

  function drawMmGrid() {
    const stepMm = 5.0; // 5mm grid
    const stepPx = stepMm / state.scaleMmPerPx;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 0.5 / state.zoom;

    for (let x = 0; x <= state.imageWidth; x += stepPx) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, state.imageHeight);
      ctx.stroke();
    }
    for (let y = 0; y <= state.imageHeight; y += stepPx) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(state.imageWidth, y);
      ctx.stroke();
    }
  }

  function drawComponent(comp, isSelected) {
    const p1 = mmToImage(comp.x_mm - comp.w_mm / 2, comp.y_mm - comp.h_mm / 2);
    const w_px = comp.w_mm / state.scaleMmPerPx;
    const h_px = comp.h_mm / state.scaleMmPerPx;
    const center_px = mmToImage(comp.x_mm, comp.y_mm);

    ctx.save();
    ctx.translate(center_px.x, center_px.y);
    ctx.rotate((comp.rot || 0) * Math.PI / 180);

    // Box style
    const isIC = comp.ref.startsWith('U') || comp.ref.startsWith('IC');
    const isConn = comp.ref.startsWith('J') || comp.ref.startsWith('XT');
    const isPassive = comp.ref.startsWith('R') || comp.ref.startsWith('C');

    let baseColor = isIC ? '#9d4edd' : isConn ? '#ffd166' : isPassive ? '#00f5d4' : '#38bdf8';
    if (isSelected) baseColor = '#ffffff';

    ctx.fillStyle = isSelected ? 'rgba(255, 255, 255, 0.25)' : (isIC ? 'rgba(157, 78, 221, 0.25)' : 'rgba(0, 245, 212, 0.15)');
    ctx.fillRect(-w_px / 2, -h_px / 2, w_px, h_px);

    ctx.strokeStyle = baseColor;
    ctx.lineWidth = (isSelected ? 2.5 : 1.5) / state.zoom;
    ctx.strokeRect(-w_px / 2, -h_px / 2, w_px, h_px);

    // Center Crosshair
    const ch = 4 / state.zoom;
    ctx.beginPath();
    ctx.moveTo(-ch, 0); ctx.lineTo(ch, 0);
    ctx.moveTo(0, -ch); ctx.lineTo(0, ch);
    ctx.strokeStyle = baseColor;
    ctx.lineWidth = 1 / state.zoom;
    ctx.stroke();

    // Orientation Indicator (Pin 1 dot / arrow on top-left of footprint)
    const pinRadius = Math.max(1.5, Math.min(w_px, h_px) * 0.12);
    ctx.beginPath();
    ctx.arc(-w_px / 2 + pinRadius * 1.5, -h_px / 2 + pinRadius * 1.5, pinRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#ff0055';
    ctx.fill();

    ctx.restore();

    // RefDes label badge (always horizontal for readability)
    drawFloatingBadge(center_px.x, center_px.y - (h_px / 2) - (8 / state.zoom), comp.ref, baseColor);
  }

  function drawFloatingBadge(x, y, text, color) {
    ctx.font = `${Math.max(10, 11 / state.zoom)}px JetBrains Mono`;
    const padding = 3 / state.zoom;
    const metrics = ctx.measureText(text);
    const w = metrics.width + padding * 2;
    const h = 13 / state.zoom;

    ctx.fillStyle = '#11151f';
    ctx.fillRect(x - w / 2, y - h / 2, w, h);
    ctx.strokeStyle = color;
    ctx.lineWidth = 1 / state.zoom;
    ctx.strokeRect(x - w / 2, y - h / 2, w, h);

    ctx.fillStyle = color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
  }

  // --- EVENT LISTENERS ---
  function setupEventListeners() {
    // Canvas Navigation & Dragging
    viewport.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    viewport.addEventListener('wheel', onWheel, { passive: false });

    // Toolbar Tool Toggles
    Object.keys(toolBtns).forEach(toolName => {
      toolBtns[toolName].addEventListener('click', () => setTool(toolName));
    });

    // View Toggles
    btnToggleGrid.addEventListener('click', () => {
      state.showGrid = !state.showGrid;
      btnToggleGrid.classList.toggle('active', state.showGrid);
      render();
    });
    btnToggleOutline.addEventListener('click', () => {
      state.showOutline = !state.showOutline;
      btnToggleOutline.classList.toggle('active', state.showOutline);
      render();
    });
    btnZoomFit.addEventListener('click', zoomToFit);
    btnZoomIn.addEventListener('click', () => zoomAtCenter(1.25));
    btnZoomOut.addEventListener('click', () => zoomAtCenter(0.8));

    // History Buttons
    btnUndo.addEventListener('click', undo);
    btnRedo.addEventListener('click', redo);

    // Inspector Updates
    propRef.addEventListener('input', updateSelectedCompFromForm);
    propVal.addEventListener('input', updateSelectedCompFromForm);
    propFp.addEventListener('input', updateSelectedCompFromForm);
    propX.addEventListener('input', updateSelectedCompFromForm);
    propY.addEventListener('input', updateSelectedCompFromForm);
    propW.addEventListener('input', updateSelectedCompFromForm);
    propH.addEventListener('input', updateSelectedCompFromForm);

    btnSideTop.addEventListener('click', () => {
      btnSideTop.classList.add('active');
      btnSideBot.classList.remove('active');
      updateSelectedCompFromForm();
    });
    btnSideBot.addEventListener('click', () => {
      btnSideBot.classList.add('active');
      btnSideTop.classList.remove('active');
      updateSelectedCompFromForm();
    });

    rotBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        rotBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        updateSelectedCompFromForm();
      });
    });

    // Quick Footprint Chips
    chipBtns.forEach(chip => {
      chip.addEventListener('click', () => {
        const fp = chip.getAttribute('data-fp');
        propFp.value = fp;
        if (state.selectedCompIndex >= 0) {
          updateSelectedCompFromForm();
        }
      });
    });

    // Delete & Duplicate
    btnDeletePart.addEventListener('click', deleteSelectedComponent);
    btnDuplicatePart.addEventListener('click', duplicateSelectedComponent);

    // Calibration panel
    btnApplyCalib.addEventListener('click', () => {
      state.boardWidthMm = parseFloat(boardWidthMmInput.value) || 130.0;
      state.boardHeightMm = parseFloat(boardHeightMmInput.value) || 32.0;
      recalculateScale();
      render();
      updateComponentsTable();
    });

    boardPreset.addEventListener('change', () => {
      if (boardPreset.value === 'vfbms32') {
        boardWidthMmInput.value = '130.0';
        boardHeightMmInput.value = '32.0';
      } else if (boardPreset.value === 'sfhall') {
        boardWidthMmInput.value = '42.0';
        boardHeightMmInput.value = '42.0';
      }
      btnApplyCalib.click();
    });

    // Drawer collapse / expand
    drawerHeader.addEventListener('click', (e) => {
      if (e.target === btnClearAll) return;
      const isExpanded = bottomDrawer.classList.contains('expanded');
      bottomDrawer.classList.toggle('expanded', !isExpanded);
      bottomDrawer.classList.toggle('collapsed', isExpanded);
      drawerToggleIcon.textContent = isExpanded ? '▲ Expand' : '▼ Collapse';
    });

    btnClearAll.addEventListener('click', () => {
      if (confirm('Clear all marked components?')) {
        saveHistory();
        state.components = [];
        selectComponent(-1);
        updateComponentsTable();
        render();
      }
    });

    // Image Picker
    imageSelect.addEventListener('change', () => {
      if (imageSelect.value) {
        loadImageFromPath(imageSelect.value);
      }
    });

    btnUploadImage.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (evt) => {
          const img = new Image();
          img.onload = () => {
            state.currentImage = img;
            state.imageWidth = img.naturalWidth;
            state.imageHeight = img.naturalHeight;
            recalculateScale();
            zoomToFit();
            render();
          };
          img.src = evt.target.result;
        };
        reader.readAsDataURL(file);
      }
    });

    // Modals
    btnAgentModal.addEventListener('click', openAgentModal);
    btnKiCadScript.addEventListener('click', openKiCadScriptModal);
    modalClose.addEventListener('click', () => modalAgent.classList.remove('open'));
    btnCopyModal.addEventListener('click', () => {
      navigator.clipboard.writeText(modalCodePreview.textContent).then(() => {
        btnCopyModal.textContent = 'Copied!';
        setTimeout(() => { btnCopyModal.textContent = 'Copy to Clipboard'; }, 1800);
      });
    });

    btnSaveWorkspace.addEventListener('click', saveAnnotationsToWorkspace);
  }

  // --- MOUSE & PAN/ZOOM HANDLING ---
  function onMouseDown(e) {
    if (e.button === 1 || e.spaceKey || state.activeTool === 'pan') {
      state.isPanning = true;
      state.panStartX = e.clientX - state.panX;
      state.panStartY = e.clientY - state.panY;
      viewport.style.cursor = 'grabbing';
      return;
    }

    if (e.button === 0) { // Left click
      const imgPos = clientToImage(e.clientX, e.clientY);

      if (state.activeTool === 'box' || state.activeTool === 'ruler') {
        state.isDrawing = true;
        state.dragStart = imgPos;
        state.dragCurrent = imgPos;
      } else if (state.activeTool === 'point') {
        // Drop Pin 1 / point marker
        saveHistory();
        const mm = imageToMm(imgPos.x, imgPos.y);
        const ref = getNextRef('TP');
        state.components.push({
          ref: ref,
          val: 'TestPoint',
          footprint: 'TestPoint_Pad_D1.0mm',
          x_mm: parseFloat(mm.x.toFixed(2)),
          y_mm: parseFloat(mm.y.toFixed(2)),
          w_mm: 1.0,
          h_mm: 1.0,
          rot: 0,
          side: 'top'
        });
        selectComponent(state.components.length - 1);
        updateComponentsTable();
        render();
      } else {
        // Selection hit test
        const clickedIndex = findComponentAt(imgPos.x, imgPos.y);
        selectComponent(clickedIndex);
        render();
      }
    }
  }

  function onMouseMove(e) {
    const imgPos = clientToImage(e.clientX, e.clientY);
    const mmPos = imageToMm(imgPos.x, imgPos.y);

    hudX.textContent = `${mmPos.x.toFixed(2)} mm`;
    hudY.textContent = `${mmPos.y.toFixed(2)} mm`;
    hudPx.textContent = `${Math.round(imgPos.x)}, ${Math.round(imgPos.y)}`;

    if (state.isPanning) {
      state.panX = e.clientX - state.panStartX;
      state.panY = e.clientY - state.panStartY;
      render();
      return;
    }

    if (state.isDrawing) {
      state.dragCurrent = imgPos;
      render();
    }
  }

  function onMouseUp(e) {
    if (state.isPanning) {
      state.isPanning = false;
      viewport.style.cursor = state.activeTool === 'pan' ? 'grab' : 'crosshair';
      return;
    }

    if (state.isDrawing) {
      state.isDrawing = false;
      const x1 = Math.min(state.dragStart.x, state.dragCurrent.x);
      const y1 = Math.min(state.dragStart.y, state.dragCurrent.y);
      const w = Math.abs(state.dragCurrent.x - state.dragStart.x);
      const h = Math.abs(state.dragCurrent.y - state.dragStart.y);

      // Minimum size threshold to avoid accidental micro-clicks
      if (w > 3 && h > 3 && state.activeTool === 'box') {
        saveHistory();
        const centerImgX = x1 + w / 2;
        const centerImgY = y1 + h / 2;
        const centerMm = imageToMm(centerImgX, centerImgY);
        const wMm = parseFloat((w * state.scaleMmPerPx).toFixed(2));
        const hMm = parseFloat((h * state.scaleMmPerPx).toFixed(2));

        // Auto-suggest footprint
        const suggestion = suggestFootprint(wMm, hMm);
        const prefix = suggestion ? suggestion.prefix : 'U';
        const fp = suggestion ? suggestion.fp : (propFp.value || 'Package_QFN');
        const ref = getNextRef(prefix);

        const newComp = {
          ref: ref,
          val: propVal.value || (fp.split('_')[0]),
          footprint: fp,
          x_mm: parseFloat(centerMm.x.toFixed(2)),
          y_mm: parseFloat(centerMm.y.toFixed(2)),
          w_mm: wMm,
          h_mm: hMm,
          rot: wMm < hMm && (fp.includes('0805') || fp.includes('0402')) ? 90 : 0,
          side: btnSideTop.classList.contains('active') ? 'top' : 'bottom'
        };

        state.components.push(newComp);
        selectComponent(state.components.length - 1);
        updateComponentsTable();
      }
      render();
    }
  }

  function onWheel(e) {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const newZoom = Math.max(0.1, Math.min(50.0, state.zoom * zoomFactor));

    state.panX = mouseX - (mouseX - state.panX) * (newZoom / state.zoom);
    state.panY = mouseY - (mouseY - state.panY) * (newZoom / state.zoom);
    state.zoom = newZoom;

    updateZoomHUD();
    render();
  }

  function zoomAtCenter(factor) {
    const rect = viewport.getBoundingClientRect();
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    const newZoom = Math.max(0.1, Math.min(50.0, state.zoom * factor));
    state.panX = cx - (cx - state.panX) * (newZoom / state.zoom);
    state.panY = cy - (cy - state.panY) * (newZoom / state.zoom);
    state.zoom = newZoom;
    updateZoomHUD();
    render();
  }

  function setTool(toolName) {
    state.activeTool = toolName;
    Object.keys(toolBtns).forEach(name => {
      toolBtns[name].classList.toggle('active', name === toolName);
    });
    viewport.style.cursor = toolName === 'pan' ? 'grab' : 'crosshair';
  }

  // --- SELECTION & INSPECTOR ---
  function findComponentAt(imgX, imgY) {
    for (let i = state.components.length - 1; i >= 0; i--) {
      const c = state.components[i];
      const p1 = mmToImage(c.x_mm - c.w_mm / 2, c.y_mm - c.h_mm / 2);
      const w_px = c.w_mm / state.scaleMmPerPx;
      const h_px = c.h_mm / state.scaleMmPerPx;
      if (imgX >= p1.x && imgX <= p1.x + w_px && imgY >= p1.y && imgY <= p1.y + h_px) {
        return i;
      }
    }
    return -1;
  }

  function selectComponent(index) {
    state.selectedCompIndex = index;
    if (index >= 0 && index < state.components.length) {
      const c = state.components[index];
      selIndexBadge.textContent = `${c.ref} (#${index + 1})`;
      propRef.value = c.ref;
      propVal.value = c.val || '';
      propFp.value = c.footprint || '';
      propX.value = c.x_mm;
      propY.value = c.y_mm;
      propW.value = c.w_mm;
      propH.value = c.h_mm;

      rotBtns.forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.getAttribute('data-rot')) === (c.rot || 0));
      });

      btnSideTop.classList.toggle('active', c.side !== 'bottom');
      btnSideBot.classList.toggle('active', c.side === 'bottom');

      highlightTableRow(index);
    } else {
      selIndexBadge.textContent = 'None Selected';
      highlightTableRow(-1);
    }
  }

  function updateSelectedCompFromForm() {
    if (state.selectedCompIndex < 0 || state.selectedCompIndex >= state.components.length) return;
    saveHistory();
    const c = state.components[state.selectedCompIndex];
    c.ref = propRef.value.trim();
    c.val = propVal.value.trim();
    c.footprint = propFp.value.trim();
    c.x_mm = parseFloat(propX.value) || c.x_mm;
    c.y_mm = parseFloat(propY.value) || c.y_mm;
    c.w_mm = parseFloat(propW.value) || c.w_mm;
    c.h_mm = parseFloat(propH.value) || c.h_mm;

    const activeRot = document.querySelector('.rot-btn.active[data-rot]');
    c.rot = activeRot ? parseInt(activeRot.getAttribute('data-rot')) : 0;
    c.side = btnSideBot.classList.contains('active') ? 'bottom' : 'top';

    updateComponentsTable();
    render();
  }

  function deleteSelectedComponent() {
    if (state.selectedCompIndex >= 0 && state.selectedCompIndex < state.components.length) {
      saveHistory();
      state.components.splice(state.selectedCompIndex, 1);
      selectComponent(-1);
      updateComponentsTable();
      render();
    }
  }

  function duplicateSelectedComponent() {
    if (state.selectedCompIndex >= 0 && state.selectedCompIndex < state.components.length) {
      saveHistory();
      const orig = state.components[state.selectedCompIndex];
      const prefix = orig.ref.replace(/[0-9]/g, '') || 'U';
      const copy = { ...orig, ref: getNextRef(prefix), x_mm: orig.x_mm + 2.0 };
      state.components.push(copy);
      selectComponent(state.components.length - 1);
      updateComponentsTable();
      render();
    }
  }

  // --- TABLE UPDATES ---
  function updateComponentsTable() {
    partsCount.textContent = state.components.length;
    partsTableBody.innerHTML = '';

    state.components.forEach((c, idx) => {
      const tr = document.createElement('tr');
      if (idx === state.selectedCompIndex) tr.classList.add('selected');

      tr.innerHTML = `
        <td><b>${c.ref}</b></td>
        <td>${c.val || '-'}</td>
        <td style="color:var(--text-dim)">${c.footprint}</td>
        <td>${c.x_mm.toFixed(2)}</td>
        <td>${c.y_mm.toFixed(2)}</td>
        <td>${c.w_mm.toFixed(2)}</td>
        <td>${c.h_mm.toFixed(2)}</td>
        <td>${c.rot || 0}°</td>
        <td>${c.side || 'top'}</td>
        <td><button class="btn" style="padding:1px 6px; font-size:0.7rem; color:var(--accent-red);" data-del="${idx}">✕</button></td>
      `;

      tr.addEventListener('click', (e) => {
        if (e.target.hasAttribute('data-del')) {
          saveHistory();
          state.components.splice(idx, 1);
          selectComponent(-1);
          updateComponentsTable();
          render();
          return;
        }
        selectComponent(idx);
        // Pan & Center view on this component
        const center = mmToImage(c.x_mm, c.y_mm);
        const rect = viewport.getBoundingClientRect();
        state.panX = rect.width / 2 - center.x * state.zoom;
        state.panY = rect.height / 2 - center.y * state.zoom;
        render();
      });

      partsTableBody.appendChild(tr);
    });
  }

  function highlightTableRow(index) {
    const rows = partsTableBody.querySelectorAll('tr');
    rows.forEach((r, i) => r.classList.toggle('selected', i === index));
  }

  // --- HISTORY (UNDO/REDO) ---
  function saveHistory() {
    state.history = state.history.slice(0, state.historyIndex + 1);
    state.history.push(JSON.stringify(state.components));
    if (state.history.length > 50) state.history.shift();
    state.historyIndex = state.history.length - 1;
  }

  function undo() {
    if (state.historyIndex > 0) {
      state.historyIndex--;
      state.components = JSON.parse(state.history[state.historyIndex]);
      selectComponent(-1);
      updateComponentsTable();
      render();
    }
  }

  function redo() {
    if (state.historyIndex < state.history.length - 1) {
      state.historyIndex++;
      state.components = JSON.parse(state.history[state.historyIndex]);
      selectComponent(-1);
      updateComponentsTable();
      render();
    }
  }

  // --- KEYBOARD SHORTCUTS ---
  function setupHotkeys() {
    window.addEventListener('keydown', (e) => {
      // Don't trigger when typing in input
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

      if (e.key === 'v' || e.key === 'V') setTool('pan');
      if (e.key === 'b' || e.key === 'B') setTool('box');
      if (e.key === 'p' || e.key === 'P') setTool('point');
      if (e.key === 'm' || e.key === 'M') setTool('ruler');
      if (e.key === 'c' || e.key === 'C') setTool('calib');
      if (e.key === 'g' || e.key === 'G') btnToggleGrid.click();
      if (e.key === 'o' || e.key === 'O') btnToggleOutline.click();
      if (e.key === 'z' || e.key === 'Z') zoomToFit();
      if (e.key === '+' || e.key === '=') zoomAtCenter(1.25);
      if (e.key === '-' || e.key === '_') zoomAtCenter(0.8);
      if (e.key === 'Delete' || e.key === 'Backspace') deleteSelectedComponent();

      // Rotation shortcut 'R'
      if (e.key === 'r' || e.key === 'R') {
        if (state.selectedCompIndex >= 0) {
          const c = state.components[state.selectedCompIndex];
          c.rot = ((c.rot || 0) + 90) % 360;
          selectComponent(state.selectedCompIndex);
          render();
        }
      }

      // Ctrl+Z / Ctrl+Y
      if (e.ctrlKey && e.key === 'z') { e.preventDefault(); undo(); }
      if (e.ctrlKey && e.key === 'y') { e.preventDefault(); redo(); }

      // Ctrl+S
      if (e.ctrlKey && e.key === 's') { e.preventDefault(); saveAnnotationsToWorkspace(); }
    });

    // Clipboard Paste (Ctrl+V) image support
    window.addEventListener('paste', (e) => {
      const items = e.clipboardData.items;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          const reader = new FileReader();
          reader.onload = (evt) => {
            const img = new Image();
            img.onload = () => {
              state.currentImage = img;
              state.imageWidth = img.naturalWidth;
              state.imageHeight = img.naturalHeight;
              recalculateScale();
              zoomToFit();
              render();
            };
            img.src = evt.target.result;
          };
          reader.readAsDataURL(blob);
          break;
        }
      }
    });
  }

  // --- WORKSPACE API INTEGRATION ---
  function loadWorkspaceImages() {
    fetch('/api/scan-images')
      .then(res => res.json())
      .then(images => {
        imageSelect.innerHTML = '';
        images.forEach(img => {
          const opt = document.createElement('option');
          opt.value = img.rel_path;
          opt.textContent = `${img.name} (${img.folder}) [${img.width}x${img.height}px]`;
          if (img.name === 'vfbms32_cad_top_reference_rotated.png') {
            opt.selected = true;
          }
          imageSelect.appendChild(opt);
        });
      })
      .catch(err => {
        console.warn('API /api/scan-images not available:', err);
      });
  }

  function loadProjectAnnotations() {
    const annotFile = "Q VFBMS32 AI PCB/pcb_annotations.json";
    fetch(`/api/load-annotations?file=${encodeURIComponent(annotFile)}`)
      .then(res => res.json())
      .then(res => {
        if (res.exists && res.data) {
          state.components = res.data.components || [];
          if (res.data.calibration) {
            state.boardWidthMm = res.data.calibration.board_width_mm || 130.0;
            state.boardHeightMm = res.data.calibration.board_height_mm || 32.0;
            recalculateScale();
          }
          updateComponentsTable();
          saveHistory();
          render();
        }
      })
      .catch(err => console.log('No prior annotations loaded:', err));
  }

  function saveAnnotationsToWorkspace() {
    const payload = {
      target_path: "Q VFBMS32 AI PCB/pcb_annotations.json",
      data: {
        reference_image: state.imagePath,
        calibration: {
          board_width_mm: state.boardWidthMm,
          board_height_mm: state.boardHeightMm,
          scale_x_mm_per_px: state.scaleMmPerPx,
          image_width_px: state.imageWidth,
          image_height_px: state.imageHeight
        },
        components: state.components
      }
    };

    fetch('/api/save-annotations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      btnSaveWorkspace.textContent = 'Saved ✓';
      setTimeout(() => {
        btnSaveWorkspace.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          Save to Project
        `;
      }, 1800);
    })
    .catch(err => {
      alert('Error saving to workspace: ' + err);
    });
  }

  // --- MODALS ---
  function openAgentModal() {
    modalTitle.textContent = "Copy Prompt for Antigravity AI Agent";
    modalDesc.textContent = "Copy and paste this structured prompt into chat to generate/align footprints:";

    const mdLines = [
      `### Component Placement Coordinates (${state.components.length} parts)`,
      `**Board Dimensions:** ${state.boardWidthMm} mm × ${state.boardHeightMm} mm (Scale: ${state.scaleMmPerPx.toFixed(4)} mm/px)`,
      '',
      '| Ref | Value | Footprint | X (mm) | Y (mm) | Rot | Side |',
      '| :--- | :--- | :--- | :--- | :--- | :--- | :--- |'
    ];

    state.components.forEach(c => {
      mdLines.push(`| ${c.ref} | ${c.val || '-'} | ${c.footprint} | ${c.x_mm.toFixed(2)} | ${c.y_mm.toFixed(2)} | ${c.rot || 0}° | ${c.side || 'top'} |`);
    });

    mdLines.push('', '```json');
    mdLines.push(JSON.stringify({
      calibration: {
        board_width_mm: state.boardWidthMm,
        board_height_mm: state.boardHeightMm,
        scale_mm_per_px: state.scaleMmPerPx
      },
      components: state.components
    }, null, 2));
    mdLines.push('```');

    modalCodePreview.textContent = mdLines.join('\n');
    modalAgent.classList.add('open');
  }

  function openKiCadScriptModal() {
    modalTitle.textContent = "Generated KiCad pcbnew Python Script";
    modalDesc.textContent = "Save or copy this script to place all footprints automatically in KiCad:";

    const code = [
      '# KiCad pcbnew Placement Script',
      'import pcbnew',
      '',
      `BOARD_WIDTH_MM = ${state.boardWidthMm}`,
      `BOARD_HEIGHT_MM = ${state.boardHeightMm}`,
      '',
      'COMPONENTS = ' + JSON.stringify(state.components, null, 2),
      '',
      'def place_all(board_path="VFBMS32.kicad_pcb"):',
      '    board = pcbnew.LoadBoard(board_path)',
      '    for item in COMPONENTS:',
      '        fp = board.FindFootprintByReference(item["ref"])',
      '        if fp:',
      '            pos = pcbnew.VECTOR2I(pcbnew.FromMM(item["x_mm"]), pcbnew.FromMM(item["y_mm"]))',
      '            fp.SetPosition(pos)',
      '            fp.SetOrientation(pcbnew.EDA_ANGLE(item["rot"], pcbnew.DEGREES_T))',
      '            print(f"Placed {item[\'ref\']} at ({item[\'x_mm\']}, {item[\'y_mm\']}) mm")',
      '    pcbnew.SaveBoard(board_path, board)',
      '    print("All parts placed successfully!")',
      '',
      'if __name__ == "__main__":',
      '    place_all()'
    ].join('\n');

    modalCodePreview.textContent = code;
    modalAgent.classList.add('open');
  }

  // Launch
  init();
})();
