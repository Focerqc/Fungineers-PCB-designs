// Board Boxes: draw color-coded boxes over a reference image, pattern them, export a placement prompt.
// Coordinates are KiCad board millimetres. Boxes store their CENTER (x, y) and size (w, h).
(function () {
  'use strict';

  const PALETTE = ['#4ea1ff', '#ff6b6b', '#ffd166', '#06d6a0', '#c77dff', '#ff9f1c', '#f15bb5', '#9ef01a', '#00bbf9'];
  const DIRS = { right: [1, 0], down: [0, 1], left: [-1, 0], up: [0, -1] };
  const DIR_ARROW = { right: '→', down: '↓', left: '←', up: '↑' };

  // ---------- STATE ----------
  const S = {
    boardPath: '',
    board: null,             // from KiCad bridge: { bbox, edges, footprints }
    refImg: null,
    doc: emptyDoc(),
    view: { x: 0, y: 0, scale: 15 },
    showRef: true,
    show3D: false,
    showParts: true,
    showTopCu: false,
    showBotCu: false,
    showVias: false,
    selectMode: false,
    infoMode: false,
    hoverFp: null,
    infoFp: null,
    activePreset: null,
    mousePos: null,
    render3dImg: null,
    render3dPath: null,
    renderIsoPath: null,
    isoView: { x: 0, y: 0, scale: 1 },
    isoDrag: null,
    opacity: 0.75,
    snap: 0.05,
    activeColor: null,
    sel: null,               // { id, i }  (i = instance index inside the box's pattern)
    drag: null,
    pan: null,
    space: false,
    undo: [],
    redo: [],
  };

  function emptyDoc() {
    return { version: 1, ref: '', refFit: { ox: 0, oy: 0, sx: 100, sy: 100 }, colors: [], boxes: [] };
  }

  // ---------- DOM ----------
  const $ = id => document.getElementById(id);
  const canvas = $('canvas');
  const ctx = canvas.getContext('2d');
  const stage = $('stage');

  const uid = p => p + Math.random().toString(36).slice(2, 8) + Date.now().toString(36).slice(-3);
  const r2 = v => Math.round(v * 1000) / 1000;
  const fmt = v => (Math.round(v * 100) / 100).toFixed(2);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function toast(msg, type = 'info', ms = 3500) {
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.innerHTML = msg;
    $('toasts').appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateY(-6px)'; setTimeout(() => el.remove(), 300); }, ms);
  }

  // ---------- VIEW TRANSFORMS ----------
  function resize() {
    const r = stage.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = r.width * dpr;
    canvas.height = r.height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    render();
  }
  const toScreen = (x, y) => ({ x: (x - S.view.x) * S.view.scale, y: (y - S.view.y) * S.view.scale });
  const toBoard = (sx, sy) => ({ x: sx / S.view.scale + S.view.x, y: sy / S.view.scale + S.view.y });
  function mouseBoard(e) {
    const r = canvas.getBoundingClientRect();
    return toBoard(e.clientX - r.left, e.clientY - r.top);
  }
  const snap = v => (S.snap > 0 ? Math.round(v / S.snap) * S.snap : v);

  function fit() {
    const bb = S.board?.bbox;
    if (!bb) return;
    const r = stage.getBoundingClientRect();
    const pad = 70;
    S.view.scale = Math.min((r.width - pad * 2) / Math.max(bb.w, 1), (r.height - pad * 2) / Math.max(bb.h, 1), 80);
    S.view.x = bb.x - (r.width / S.view.scale - bb.w) / 2;
    S.view.y = bb.y - (r.height / S.view.scale - bb.h) / 2;
    render();
  }

  // ---------- DATA MODEL ----------
  const color = id => S.doc.colors.find(c => c.id === id);
  const box = id => S.doc.boxes.find(b => b.id === id);
  const colorIndex = id => S.doc.colors.findIndex(c => c.id === id);

  // All visible instances of a box (pattern copies are derived, so they stay linked to the box).
  function instances(b) {
    const p = b.pat;
    if (!p || p.n <= 1) return [{ id: b.id, i: 0, x: b.x, y: b.y, w: b.w, h: b.h, c: b.c }];
    const [dx, dy] = DIRS[p.dir] || DIRS.right;
    const out = [];
    for (let i = 0; i < p.n; i++) {
      if (p.skip && p.skip.includes(i)) continue;
      out.push({ id: b.id, i, x: b.x + dx * p.pitch * i, y: b.y + dy * p.pitch * i, w: b.w, h: b.h, c: b.c });
    }
    return out;
  }
  const allInstances = () => S.doc.boxes.flatMap(instances);
  function instanceOf(sel) {
    if (!sel) return null;
    const b = box(sel.id);
    if (!b) return null;
    return instances(b).find(it => it.i === sel.i) || instances(b)[0] || null;
  }
  function offsetOf(b, i) {
    if (!b.pat) return [0, 0];
    const [dx, dy] = DIRS[b.pat.dir] || DIRS.right;
    return [dx * b.pat.pitch * i, dy * b.pat.pitch * i];
  }
  const liveCount = b => instances(b).length;
  const totalCount = () => S.doc.boxes.reduce((n, b) => n + liveCount(b), 0);

  function ensureColor() {
    if (!S.doc.colors.length) addColor(false);
    if (!color(S.activeColor)) S.activeColor = S.doc.colors[0].id;
  }

  function addColor(commitIt = true) {
    const used = new Set(S.doc.colors.map(c => c.hex));
    const hex = PALETTE.find(p => !used.has(p)) || PALETTE[S.doc.colors.length % PALETTE.length];
    const c = { id: uid('c'), hex, note: '' };
    S.doc.colors.push(c);
    S.activeColor = c.id;
    S.sel = null;
    if (commitIt) commit();
    renderLegend();
    return c;
  }

  function breakOut(b, i) {
    // Detach instance i into its own standalone box; pattern keeps the rest in place.
    const it = instances(b).find(x => x.i === i);
    if (!it) return null;
    if (!b.pat || liveCount(b) <= 1) return b;
    b.pat.skip = [...(b.pat.skip || []), i];
    const nb = { id: uid('b'), c: b.c, x: it.x, y: it.y, w: b.w, h: b.h, pat: null };
    S.doc.boxes.push(nb);
    return nb;
  }

  function unlinkAll(b) {
    const its = instances(b);
    const idx = S.doc.boxes.indexOf(b);
    const fresh = its.map(it => ({ id: uid('b'), c: b.c, x: it.x, y: it.y, w: b.w, h: b.h, pat: null }));
    S.doc.boxes.splice(idx, 1, ...fresh);
    return fresh;
  }

  function removeInstance(b, i) {
    if (!b.pat || liveCount(b) <= 1) {
      S.doc.boxes = S.doc.boxes.filter(x => x !== b);
      return;
    }
    b.pat.skip = [...(b.pat.skip || []), i];
  }

  // ---------- HISTORY + PERSISTENCE ----------
  const snapshot = () => JSON.stringify({ colors: S.doc.colors, boxes: S.doc.boxes });
  let lastSnap = null;
  function commit() {
    const s = snapshot();
    if (s === lastSnap) return;
    if (lastSnap !== null) S.undo.push(lastSnap);
    if (S.undo.length > 100) S.undo.shift();
    S.redo = [];
    lastSnap = s;
    scheduleSave();
    refreshUI();
  }
  function restore(s) {
    const d = JSON.parse(s);
    S.doc.colors = d.colors;
    S.doc.boxes = d.boxes;
    lastSnap = s;
    if (S.sel && !instanceOf(S.sel)) S.sel = null;
    ensureColor();
    scheduleSave();
    refreshUI();
  }
  function undo() {
    if (!S.undo.length) return;
    S.redo.push(lastSnap);
    restore(S.undo.pop());
    toast('Undo');
  }
  function redo() {
    if (!S.redo.length) return;
    S.undo.push(lastSnap);
    restore(S.redo.pop());
    toast('Redo');
  }

  function clearAllBoxes() {
    const n = S.doc.boxes.length;
    if (!n) return toast('No boxes or selections to clear', 'info');
    if (!confirm(`Are you sure you want to clear all ${n} box(es) and component selection(s)?`)) return;
    S.doc.boxes = [];
    S.sel = null;
    commit();
    toast(`Cleared all ${n} box(es). Press Undo to restore.`);
  }

  function toggleSelectMode() {
    S.selectMode = !S.selectMode;
    if (S.selectMode) {
      if (S.infoMode) toggleInfoMode(false);
      if (!S.showParts) {
        S.showParts = true;
        if ($('tglParts')) $('tglParts').classList.add('active');
      }
      ensureColor();
      toast('Select mode: click footprint parts on PCB to group them. Press Esc to exit.');
    } else {
      S.hoverFp = null;
      toast('Select mode exited');
    }
    refreshUI();
  }

  function toggleInfoMode(forceState) {
    S.infoMode = forceState !== undefined ? forceState : !S.infoMode;
    if (S.infoMode) {
      if (S.selectMode) {
        S.selectMode = false;
        if ($('btnSelectMode')) $('btnSelectMode').classList.remove('active');
      }
      if (!S.showParts) {
        S.showParts = true;
        if ($('tglParts')) $('tglParts').classList.add('active');
      }
      const card = $('partInfoCard');
      if (card) {
        card.classList.remove('hidden');
        if (!S.infoFp) {
          $('infoEmptyHint')?.classList.remove('hidden');
          $('infoBody')?.classList.add('hidden');
          $('infoRef').textContent = 'Select part';
        }
      }
      toast('Info mode: click any component on PCB to view details. (Press Esc to exit)');
    } else {
      S.hoverFp = null;
      if ($('partInfoCard')) $('partInfoCard').classList.add('hidden');
      S.infoFp = null;
      toast('Info mode exited');
    }
    refreshUI();
  }

  function showPartInfo(fp) {
    if (!fp) return;
    S.infoFp = fp;
    const card = $('partInfoCard');
    if (!card) return;
    card.classList.remove('hidden');
    $('infoEmptyHint')?.classList.add('hidden');
    $('infoBody')?.classList.remove('hidden');

    $('infoRef').textContent = fp.ref || '–';
    $('infoVal').textContent = fp.value || '–';
    $('infoFp').textContent = fp.fpid || '–';
    $('infoFp').title = fp.fpid || '';
    $('infoPos').textContent = `(${fmt(fp.x)}, ${fmt(fp.y)})`;
    $('infoRot').textContent = `${fp.rot}°`;
    $('infoSide').textContent = fp.side === 'B' ? 'Bottom (B.Cu)' : 'Top (F.Cu)';

    const numPads = fp.pads?.length || 0;
    $('infoPads').textContent = `${numPads} pad${numPads === 1 ? '' : 's'}`;

    // Extract pad nets
    const nets = [];
    if (fp.pads && fp.pads.length) {
      fp.pads.forEach(p => {
        if (p.net && !nets.includes(p.net)) nets.push(p.net);
      });
    }
    const netStr = nets.length ? nets.join(', ') : 'None / NC';
    $('infoNets').textContent = netStr;
    $('infoNets').title = nets.length ? nets.map((n, i) => `${i + 1}: ${n}`).join('\n') : '';

    if (fp.lcsc) {
      $('infoLcscRow')?.classList.remove('hidden');
      $('infoLcsc').textContent = fp.lcsc;
    } else {
      $('infoLcscRow')?.classList.add('hidden');
    }

    if (fp.mpn) {
      $('infoMpnRow')?.classList.remove('hidden');
      $('infoMpn').textContent = fp.mpn;
    } else {
      $('infoMpnRow')?.classList.add('hidden');
    }

    render();
    toast(`Inspecting <b>${fp.ref}</b> (${fp.value || fp.fpid || ''})`);
  }

  function copyPartInfo() {
    if (!S.infoFp) return;
    const fp = S.infoFp;
    const nets = fp.pads ? [...new Set(fp.pads.map(p => p.net).filter(Boolean))].join(', ') : '';
    const text = [
      `Reference: ${fp.ref}`,
      `Value: ${fp.value || '–'}`,
      `Footprint: ${fp.fpid || '–'}`,
      `Position: (${fmt(fp.x)}, ${fmt(fp.y)}) mm`,
      `Rotation: ${fp.rot}°`,
      `Side: ${fp.side === 'B' ? 'Bottom' : 'Top'}`,
      `Pads: ${fp.pads?.length || 0}`,
      nets ? `Nets: ${nets}` : '',
      fp.lcsc ? `LCSC: ${fp.lcsc}` : '',
      fp.mpn ? `MPN: ${fp.mpn}` : ''
    ].filter(Boolean).join('\n');

    navigator.clipboard.writeText(text).then(() => {
      const btn = $('btnCopyInfo');
      if (btn) {
        const old = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = old; }, 1500);
      }
      toast(`Copied <b>${fp.ref}</b> info to clipboard`);
    });
  }

  function closePartInfo() {
    S.infoFp = null;
    if (S.infoMode) {
      $('infoEmptyHint')?.classList.remove('hidden');
      $('infoBody')?.classList.add('hidden');
      $('infoRef').textContent = 'Select part';
    } else {
      $('partInfoCard')?.classList.add('hidden');
    }
    render();
  }

  let saveTimer = null;
  function setSaveState(text, cls) { const el = $('saveState'); el.textContent = text; el.className = `save-state ${cls || ''}`; }
  function scheduleSave() {
    if (!S.boardPath) return;
    setSaveState('unsaved', 'busy');
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 500);
  }
  async function save() {
    try {
      const res = await fetch(`/api/boxes?path=${encodeURIComponent(S.boardPath)}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(S.doc),
      }).then(r => r.json());
      if (res.error) throw new Error(res.error);
      setSaveState(`saved · ${res.file.split('/').pop()}`, 'ok');
    } catch (err) {
      setSaveState('save failed', 'err');
      toast(`Save failed: ${esc(err.message)}`, 'err');
    }
  }

  // ---------- LOADING ----------
  async function init() {
    resize();
    hookEvents();
    loading('Finding boards…');
    try {
      const [boards, images] = await Promise.all([
        fetch('/api/boards').then(r => r.json()),
        fetch('/api/images').then(r => r.json()),
      ]);
      const bSel = $('boardSelect');
      bSel.innerHTML = boards.map(b => `<option value="${esc(b)}">${esc(b)}</option>`).join('');
      const saved = localStorage.getItem('pcb_dashboard_last_board');
      bSel.value = (saved && boards.includes(saved)) ? saved :
                   (boards.find(b => /qfbms32\.kicad_pcb$/i.test(b)) ||
                    boards.find(b => /qfbms/i.test(b)) ||
                    boards[0] || '');

      const iSel = $('imageSelect');
      iSel.innerHTML = '<option value="">(none)</option>' +
        images.map(i => `<option value="${esc(i.path)}">${esc(i.path)} (${i.kb} KB)</option>`).join('');

      bSel.addEventListener('change', () => {
        localStorage.setItem('pcb_dashboard_last_board', bSel.value);
        loadBoard(bSel.value);
      });
      iSel.addEventListener('change', () => { S.doc.ref = iSel.value; loadRef(iSel.value); scheduleSave(); });

      if (bSel.value) await loadBoard(bSel.value);
      else loading(null);
    } catch (err) {
      loading(`Can't reach the dashboard server (${esc(err.message)}). Start it with: python _tools/pcb_dashboard/server.py`);
    }
  }

  function loading(text) {
    if (text === null) { $('loading').classList.add('done'); return; }
    $('loading').classList.remove('done');
    $('loadingText').innerHTML = text;
  }

  async function loadBoard(path) {
    S.boardPath = path;
    S.sel = null;
    S.undo = []; S.redo = [];
    loading(`Reading <b>${esc(path.split('/').pop())}</b> with KiCad… (first load can take ~10 s)`);
    try {
      const [board, doc] = await Promise.all([
        fetch(`/api/board?path=${encodeURIComponent(path)}`).then(r => r.json()),
        fetch(`/api/boxes?path=${encodeURIComponent(path)}`).then(r => r.json()),
      ]);
      if (board.error) throw new Error(board.error);
      S.board = board;
      S.doc = Object.assign(emptyDoc(), doc && !doc.error ? doc : {});
      S.doc.refFit = Object.assign({ ox: 0, oy: 0, sx: 100, sy: 100 }, S.doc.refFit);
      ensureColor();
      lastSnap = snapshot();

      // reference image: saved one, else best guess in the board's _reference folder
      const iSel = $('imageSelect');
      const opts = [...iSel.options].map(o => o.value).filter(Boolean);
      const dir = path.split('/').slice(0, -1).join('/');
      let ref = S.doc.ref && !S.doc.ref.toLowerCase().includes('_3d_top') && opts.includes(S.doc.ref) ? S.doc.ref : '';
      if (!ref) ref = opts.find(o => o.startsWith(dir + '/_reference/') && /top_reference_rotated\.png$/i.test(o)) ||
                      opts.find(o => o.startsWith(dir + '/_reference/')) || opts[0] || '';
      iSel.value = ref;
      S.doc.ref = ref;
      await loadRef(ref);

      fillRefFit();
      setSaveState(doc && doc.exists ? 'loaded' : 'new file', 'ok');
      loading(null);
      await checkRenderStatus(path);
      fit();
      refreshUI();
    } catch (err) {
      S.board = null;
      loading(`Couldn't read the board: ${esc(err.message)}`);
    }
  }

  async function checkRenderStatus(boardPath) {
    const badgeTop = $('renderTimeBadge');
    const badgeIso = $('renderIsoTimeBadge');
    const btnViewIso = $('btnViewIso');
    const dockIso = $('tglIsoView');
    if (!boardPath) return;
    try {
      const res = await fetch(`/api/render_status?path=${encodeURIComponent(boardPath)}`).then(r => r.json());
      // Top status
      const topInfo = res.top || (res.kind === 'top' || !res.kind ? res : null);
      if (topInfo && topInfo.exists) {
        if (badgeTop) {
          badgeTop.textContent = `Top: ${topInfo.timestamp}`;
          badgeTop.classList.add('fresh');
        }
        S.render3dPath = topInfo.image;
        await load3DRender(topInfo.image);
        S.show3D = true;
        if ($('tgl3D')) $('tgl3D').classList.add('active');
      } else {
        if (badgeTop) {
          badgeTop.textContent = 'Top: –';
          badgeTop.classList.remove('fresh');
        }
        S.render3dPath = null;
        S.render3dImg = null;
        S.show3D = false;
        if ($('tgl3D')) $('tgl3D').classList.remove('active');
      }

      // Iso status
      const isoInfo = res.iso;
      if (isoInfo && isoInfo.exists) {
        if (badgeIso) {
          badgeIso.textContent = `Iso: ${isoInfo.timestamp}`;
          badgeIso.classList.remove('hidden');
          badgeIso.classList.add('fresh');
        }
        if ($('isoTimeBadge')) $('isoTimeBadge').textContent = `Render: ${isoInfo.timestamp}`;
        S.renderIsoPath = isoInfo.image;
        if (btnViewIso) btnViewIso.classList.remove('hidden');
        if (dockIso) dockIso.classList.add('active');
      } else {
        if (badgeIso) {
          badgeIso.textContent = 'Iso: –';
          badgeIso.classList.add('hidden');
          badgeIso.classList.remove('fresh');
        }
        S.renderIsoPath = null;
        if (btnViewIso) btnViewIso.classList.add('hidden');
        if (dockIso) dockIso.classList.remove('active');
      }
      render();
    } catch {
      if (badgeTop) badgeTop.textContent = 'Top: –';
      if (badgeIso) badgeIso.textContent = 'Iso: –';
    }
  }

  function load3DRender(path) {
    return new Promise(resolve => {
      if (!path) { S.render3dImg = null; render(); return resolve(); }
      const img = new Image();
      img.onload = () => { S.render3dImg = img; render(); resolve(); };
      img.onerror = () => { S.render3dImg = null; resolve(); };
      img.src = `/api/image?path=${encodeURIComponent(path)}&t=${Date.now()}`;
    });
  }

  async function triggerRender3D(kind = 'top') {
    if (!S.boardPath) return toast('No board selected', 'warn');
    const isIso = kind === 'iso';
    const btn = isIso ? $('btnIsoRender3D') : $('btnTopRender3D');
    const badge = isIso ? $('renderIsoTimeBadge') : $('renderTimeBadge');
    const oldHtml = btn ? btn.innerHTML : '';

    if (btn) {
      btn.disabled = true;
      btn.classList.add('btn-spinning');
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg> Rendering ${isIso ? 'Iso' : 'Top'}…`;
    }
    if (badge) {
      badge.textContent = 'Rendering…';
      badge.classList.remove('hidden');
    }

    try {
      const res = await fetch(`/api/render_3d?path=${encodeURIComponent(S.boardPath)}&kind=${kind}`, { method: 'POST' }).then(r => r.json());
      if (res.error) throw new Error(res.error);

      if (isIso) {
        S.renderIsoPath = res.image;
        if (badge) {
          badge.textContent = `Iso: ${res.timestamp}`;
          badge.classList.remove('hidden');
          badge.classList.add('fresh');
        }
        if ($('isoTimeBadge')) $('isoTimeBadge').textContent = `Render: ${res.timestamp}`;
        if ($('btnViewIso')) $('btnViewIso').classList.remove('hidden');
        if ($('tglIsoView')) $('tglIsoView').classList.add('active');
        toast(`⚡ Isometric 3D render generated! (${res.timestamp})`);
        openIsoViewer();
      } else {
        S.render3dPath = res.image;
        await load3DRender(res.image);
        S.show3D = true;
        if ($('tgl3D')) $('tgl3D').classList.add('active');
        if (badge) {
          badge.textContent = `Top: ${res.timestamp}`;
          badge.classList.add('fresh');
        }
        toast(`⚡ 3D Top-down render generated! (${res.timestamp})`);
        render();
      }
    } catch (err) {
      toast(`3D Render failed: ${esc(err.message)}`, 'err');
      if (badge) badge.textContent = `${isIso ? 'Iso' : 'Top'}: Failed`;
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.classList.remove('btn-spinning');
        btn.innerHTML = oldHtml;
      }
    }
  }

  // ---------- ISOMETRIC 3D VIEWER ----------
  function openIsoViewer() {
    if (!S.renderIsoPath) {
      toast('Generating Isometric 3D render…');
      triggerRender3D('iso');
      return;
    }
    const modal = $('isoModal');
    const img = $('isoImg');
    $('isoSubTitle').textContent = `Inspect component height, colors & 3D shapes on ${S.boardPath.split('/').pop()}`;
    modal.classList.add('open');
    const doFit = () => requestAnimationFrame(() => fitIso());
    img.onload = doFit;
    img.src = `/api/image?path=${encodeURIComponent(S.renderIsoPath)}&t=${Date.now()}`;
    if (img.complete && img.naturalWidth) {
      doFit();
    }
    setTimeout(doFit, 60);
  }

  function closeIsoViewer() {
    $('isoModal').classList.remove('open');
  }

  function fitIso() {
    const vp = $('isoViewport');
    const img = $('isoImg');
    if (!img.naturalWidth || !img.naturalHeight) return;
    const pad = 40;
    const vw = vp.clientWidth - pad * 2;
    const vh = vp.clientHeight - pad * 2;
    const sc = Math.min(vw / img.naturalWidth, vh / img.naturalHeight, 1.0);
    S.isoView.scale = Math.max(0.1, sc);
    S.isoView.x = (vp.clientWidth - img.naturalWidth * S.isoView.scale) / 2;
    S.isoView.y = (vp.clientHeight - img.naturalHeight * S.isoView.scale) / 2;
    applyIsoTransform();
  }

  function applyIsoTransform() {
    const wrap = $('isoCanvasWrap');
    wrap.style.transform = `translate(${S.isoView.x}px, ${S.isoView.y}px) scale(${S.isoView.scale})`;
    $('isoZoomLevel').textContent = `${Math.round(S.isoView.scale * 100)}%`;
  }

  function zoomIso(factor, cx, cy) {
    const vp = $('isoViewport');
    const img = $('isoImg');
    if (!img.naturalWidth) return;
    if (cx === undefined) cx = vp.clientWidth / 2;
    if (cy === undefined) cy = vp.clientHeight / 2;
    const oldScale = S.isoView.scale;
    const newScale = Math.min(6.0, Math.max(0.15, oldScale * factor));
    S.isoView.x = cx - (cx - S.isoView.x) * (newScale / oldScale);
    S.isoView.y = cy - (cy - S.isoView.y) * (newScale / oldScale);
    S.isoView.scale = newScale;
    applyIsoTransform();
  }

  function loadRef(path) {
    return new Promise(resolve => {
      if (!path) { S.refImg = null; render(); return resolve(); }
      const img = new Image();
      img.onload = () => { S.refImg = img; render(); resolve(); };
      img.onerror = () => { toast(`Couldn't load image <code>${esc(path)}</code>`, 'err'); resolve(); };
      img.src = `/api/image?path=${encodeURIComponent(path)}`;
    });
  }

  function fillRefFit() {
    const f = S.doc.refFit;
    $('refOx').value = f.ox; $('refOy').value = f.oy; $('refSx').value = f.sx; $('refSy').value = f.sy;
  }

  // ---------- RENDER ----------
  function render() {
    const r = stage.getBoundingClientRect();
    ctx.clearRect(0, 0, r.width, r.height);
    if (!S.board) return;
    const bb = S.board.bbox;
    const sc = S.view.scale;

    const hasRef = S.showRef && S.refImg;
    const has3D = S.show3D && S.render3dImg;

    // Layer 1: Reference image (photo)
    if (hasRef) {
      const f = S.doc.refFit;
      const p = toScreen(bb.x + f.ox, bb.y + f.oy);
      ctx.save();
      // When both are visible, ref is the solid base underlay (alpha 1.0) so 3D cross-fades over it.
      // When only ref is visible, ref obeys the opacity slider.
      ctx.globalAlpha = has3D ? 1.0 : S.opacity;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(S.refImg, p.x, p.y, bb.w * (f.sx / 100) * sc, bb.h * (f.sy / 100) * sc);
      ctx.restore();
    }

    // Layer 2: 3D CAD render (KiCad 3D model)
    if (has3D) {
      const p = toScreen(bb.x, bb.y);
      ctx.save();
      ctx.globalAlpha = S.opacity;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(S.render3dImg, p.x, p.y, bb.w * sc, bb.h * sc);
      ctx.restore();
    }

    // board outline
    ctx.save();
    ctx.strokeStyle = 'rgba(60, 240, 208, 0.85)';
    ctx.lineWidth = 1.5;
    for (const seg of S.board.edges || []) {
      if (seg.length < 2) continue;
      ctx.beginPath();
      seg.forEach((pt, k) => { const s = toScreen(pt[0], pt[1]); k ? ctx.lineTo(s.x, s.y) : ctx.moveTo(s.x, s.y); });
      ctx.stroke();
    }
    ctx.restore();

    // existing footprints (dimmed pads or color-highlighted if selected)
    if (S.showParts || S.selectMode || S.infoMode) {
      ctx.save();
      for (const fp of S.board.footprints) {
        if (fp.side === 'B') continue;
        const selB = S.doc.boxes.find(b => b.ref === fp.ref);
        const col = selB ? color(selB.c) : null;
        const hex = col ? col.hex : null;
        const isHover = (S.selectMode || S.infoMode) && S.hoverFp === fp;
        const isInfoSel = S.infoFp === fp;

        ctx.fillStyle = isInfoSel ? '#ffb347' : (hex ? hex + '88' : (isHover ? (S.infoMode ? 'rgba(255, 179, 71, 0.65)' : 'rgba(60, 240, 208, 0.55)') : 'rgba(255, 255, 255, 0.22)'));
        for (const pad of fp.pads) {
          const c = toScreen(pad.x, pad.y);
          ctx.save();
          ctx.translate(c.x, c.y);
          ctx.rotate((-pad.angle * Math.PI) / 180);
          const w = Math.max(1, pad.w * sc), h = Math.max(1, pad.h * sc);
          ctx.fillRect(-w / 2, -h / 2, w, h);
          ctx.restore();
        }
        if (sc > 14 || hex || isHover || isInfoSel) {
          const c = toScreen(fp.x, fp.y);
          ctx.font = `600 ${Math.min(12, Math.max(9, sc * 0.52))}px "JetBrains Mono"`;
          ctx.fillStyle = isInfoSel ? '#ffb347' : (hex ? '#ffffff' : (isHover ? (S.infoMode ? '#ffb347' : '#3cf0d0') : 'rgba(255, 255, 255, 0.45)'));
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(fp.ref, c.x, c.y);
        }
      }
      ctx.restore();
    }

    // Bottom copper traces (B.Cu)
    if (S.showBotCu && S.board.tracks) {
      ctx.save();
      ctx.strokeStyle = '#4488ff';
      ctx.lineCap = 'round';
      for (const tr of S.board.tracks) {
        if (tr.layer === 'B.Cu') {
          const p1 = toScreen(tr.x1, tr.y1), p2 = toScreen(tr.x2, tr.y2);
          ctx.lineWidth = Math.max(1, tr.w * sc);
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
      ctx.restore();
    }

    // Top copper traces (F.Cu)
    if (S.showTopCu && S.board.tracks) {
      ctx.save();
      ctx.strokeStyle = '#ff4444';
      ctx.lineCap = 'round';
      for (const tr of S.board.tracks) {
        if (tr.layer === 'F.Cu') {
          const p1 = toScreen(tr.x1, tr.y1), p2 = toScreen(tr.x2, tr.y2);
          ctx.lineWidth = Math.max(1, tr.w * sc);
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
      ctx.restore();
    }

    // Vias
    if (S.showVias && S.board.vias) {
      ctx.save();
      for (const v of S.board.vias) {
        const p = toScreen(v.x, v.y);
        const rOuter = Math.max(1.5, (v.width / 2) * sc);
        const rDrill = Math.max(0.75, (v.drill / 2) * sc);
        ctx.fillStyle = '#ffc857';
        ctx.beginPath();
        ctx.arc(p.x, p.y, rOuter, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#07090e';
        ctx.beginPath();
        ctx.arc(p.x, p.y, rDrill, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    // boxes
    const selBox = S.sel ? box(S.sel.id) : null;
    for (const b of S.doc.boxes) {
      const col = color(b.c);
      const hex = col ? col.hex : '#888';
      const its = instances(b);
      const groupSel = selBox === b;

      // link line through pattern
      if (its.length > 1) {
        ctx.save();
        ctx.strokeStyle = hex;
        ctx.globalAlpha = groupSel ? 0.9 : 0.35;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        its.forEach((it, k) => { const s = toScreen(it.x, it.y); k ? ctx.lineTo(s.x, s.y) : ctx.moveTo(s.x, s.y); });
        ctx.stroke();
        ctx.restore();
      }

      for (const it of its) {
        const p = toScreen(it.x - it.w / 2, it.y - it.h / 2);
        const w = it.w * sc, h = it.h * sc;
        const isSel = groupSel && S.sel.i === it.i;
        ctx.save();
        ctx.fillStyle = hex + (groupSel ? '55' : '38');
        ctx.fillRect(p.x, p.y, w, h);
        ctx.strokeStyle = isSel ? '#ffffff' : hex;
        ctx.lineWidth = isSel ? 2 : groupSel ? 1.6 : 1.2;
        ctx.strokeRect(p.x, p.y, w, h);
        if (it.i === firstLive(b) && its.length > 1) {   // mark the pattern anchor
          ctx.fillStyle = hex;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.min(8, w / 2), p.y); ctx.lineTo(p.x, p.y + Math.min(8, h / 2)); ctx.fill();
        }
        // color number & component ref
        const ci = colorIndex(b.c) + 1;
        const tagText = b.ref ? `${ci} · ${b.ref}` : String(ci);
        if (w > 12 && h > 10) {
          ctx.font = `700 ${Math.min(13, Math.max(9, h * 0.55, w * 0.35))}px "JetBrains Mono"`;
          ctx.fillStyle = '#fff';
          ctx.globalAlpha = 0.95;
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(tagText, p.x + w / 2, p.y + h / 2);
        }
        ctx.restore();
        if (isSel) drawHandles(p.x, p.y, w, h);
      }
    }

    // box being drawn
    if (S.drag?.mode === 'draw') {
      const d = S.drag;
      const p1 = toScreen(d.x0, d.y0), p2 = toScreen(d.x1, d.y1);
      const hex = color(S.activeColor)?.hex || '#fff';
      ctx.save();
      ctx.fillStyle = hex + '40';
      ctx.strokeStyle = hex;
      ctx.setLineDash([4, 3]);
      ctx.lineWidth = 1.5;
      const x = Math.min(p1.x, p2.x), y = Math.min(p1.y, p2.y);
      ctx.fillRect(x, y, Math.abs(p2.x - p1.x), Math.abs(p2.y - p1.y));
      ctx.strokeRect(x, y, Math.abs(p2.x - p1.x), Math.abs(p2.y - p1.y));
      ctx.font = '500 11px "JetBrains Mono"';
      ctx.fillStyle = '#fff';
      ctx.setLineDash([]);
      ctx.fillText(`${fmt(Math.abs(d.x1 - d.x0))} × ${fmt(Math.abs(d.y1 - d.y0))} mm`, x, y - 6);
      ctx.restore();
    }

    // Ghost preview for active package preset
    if (S.activePreset && S.mousePos && !S.drag && !S.pan && S.board) {
      const cx = snap(S.mousePos.x), cy = snap(S.mousePos.y);
      const pw = S.activePreset.w, ph = S.activePreset.h;
      const p1 = toScreen(cx - pw / 2, cy - ph / 2);
      const sw = pw * sc, sh = ph * sc;
      const hex = color(S.activeColor)?.hex || '#3cf0d0';
      ctx.save();
      ctx.fillStyle = hex + '25';
      ctx.strokeStyle = hex;
      ctx.setLineDash([3, 3]);
      ctx.lineWidth = 1.5;
      ctx.fillRect(p1.x, p1.y, sw, sh);
      ctx.strokeRect(p1.x, p1.y, sw, sh);
      ctx.font = '600 11px "JetBrains Mono"';
      ctx.fillStyle = hex;
      ctx.setLineDash([]);
      ctx.fillText(`${S.activePreset.name} (${fmt(pw)}×${fmt(ph)})`, p1.x, p1.y - 5);
      ctx.restore();
    }

    // Select mode hover indicator over unselected footprint
    if (S.selectMode && S.hoverFp && !S.doc.boxes.some(b => b.ref === S.hoverFp.ref)) {
      const bb = getFpBBox(S.hoverFp);
      const p = toScreen(bb.x - bb.w / 2, bb.y - bb.h / 2);
      ctx.save();
      ctx.strokeStyle = '#3cf0d0';
      ctx.setLineDash([3, 2]);
      ctx.lineWidth = 1.5;
      ctx.strokeRect(p.x, p.y, bb.w * sc, bb.h * sc);
      ctx.font = '600 11px "JetBrains Mono"';
      ctx.fillStyle = '#3cf0d0';
    // Info mode hover indicator
    if (S.infoMode && S.hoverFp && S.hoverFp !== S.infoFp) {
      const bb = getFpBBox(S.hoverFp);
      const p = toScreen(bb.x - bb.w / 2, bb.y - bb.h / 2);
      ctx.save();
      ctx.strokeStyle = '#ffb347';
      ctx.setLineDash([3, 2]);
      ctx.lineWidth = 1.5;
      ctx.strokeRect(p.x, p.y, bb.w * sc, bb.h * sc);
      ctx.font = '600 11px "JetBrains Mono"';
      ctx.fillStyle = '#ffb347';
      ctx.fillText(`Inspect ${S.hoverFp.ref}`, p.x, p.y - 5);
      ctx.restore();
    }

    // Info mode selected footprint persistent highlight & badge
    if (S.infoFp) {
      const bb = getFpBBox(S.infoFp);
      const p = toScreen(bb.x - bb.w / 2, bb.y - bb.h / 2);
      ctx.save();
      ctx.strokeStyle = '#ffb347';
      ctx.lineWidth = 2.5;
      ctx.setLineDash([]);
      ctx.shadowColor = 'rgba(255, 179, 71, 0.6)';
      ctx.shadowBlur = 10;
      ctx.strokeRect(p.x - 2, p.y - 2, bb.w * sc + 4, bb.h * sc + 4);

      // Corner bracket accents
      const cornerLen = Math.min(12, Math.max(5, bb.w * sc * 0.25));
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#ffffff';
      ctx.beginPath();
      // NW
      ctx.moveTo(p.x - 4, p.y - 4 + cornerLen);
      ctx.lineTo(p.x - 4, p.y - 4);
      ctx.lineTo(p.x - 4 + cornerLen, p.y - 4);
      // NE
      ctx.moveTo(p.x + bb.w * sc + 4 - cornerLen, p.y - 4);
      ctx.lineTo(p.x + bb.w * sc + 4, p.y - 4);
      ctx.lineTo(p.x + bb.w * sc + 4, p.y - 4 + cornerLen);
      // SW
      ctx.moveTo(p.x - 4, p.y + bb.h * sc + 4 - cornerLen);
      ctx.lineTo(p.x - 4, p.y + bb.h * sc + 4);
      ctx.lineTo(p.x - 4 + cornerLen, p.y + bb.h * sc + 4);
      // SE
      ctx.moveTo(p.x + bb.w * sc + 4 - cornerLen, p.y + bb.h * sc + 4);
      ctx.lineTo(p.x + bb.w * sc + 4, p.y + bb.h * sc + 4);
      ctx.lineTo(p.x + bb.w * sc + 4, p.y + bb.h * sc + 4 - cornerLen);
      ctx.stroke();

      // Tooltip badge above component
      const badgeText = `${S.infoFp.ref}: ${S.infoFp.value || S.infoFp.fpid || ''}`;
      ctx.font = '700 11px "JetBrains Mono", monospace';
      const tw = ctx.measureText(badgeText).width;
      const bx = p.x + (bb.w * sc) / 2 - tw / 2 - 8;
      const by = p.y - 24;
      ctx.fillStyle = 'rgba(15, 20, 30, 0.92)';
      ctx.strokeStyle = '#ffb347';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(bx, by, tw + 16, 20, 4);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#ffb347';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(badgeText, bx + 8, by + 10);
      ctx.restore();
    }
  }

  function firstLive(b) { return instances(b)[0]?.i ?? 0; }

  function drawHandles(x, y, w, h) {
    ctx.save();
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#07090e';
    for (const [hx, hy] of [[x, y], [x + w, y], [x, y + h], [x + w, y + h]]) {
      ctx.fillRect(hx - 4, hy - 4, 8, 8);
      ctx.strokeRect(hx - 4, hy - 4, 8, 8);
    }
    ctx.restore();
  }

  // ---------- HIT TESTING ----------
  function getFpBBox(fp) {
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    if (fp.pads && fp.pads.length) {
      for (const p of fp.pads) {
        const pw = (p.w || 0.6) / 2, ph = (p.h || 0.6) / 2;
        minX = Math.min(minX, p.x - pw);
        maxX = Math.max(maxX, p.x + pw);
        minY = Math.min(minY, p.y - ph);
        maxY = Math.max(maxY, p.y + ph);
      }
    }
    if (fp.outline && fp.outline.length) {
      for (const seg of fp.outline) {
        for (const pt of seg) {
          minX = Math.min(minX, pt[0]);
          maxX = Math.max(maxX, pt[0]);
          minY = Math.min(minY, pt[1]);
          maxY = Math.max(maxY, pt[1]);
        }
      }
    }
    minX = Math.min(minX, fp.x - 0.4);
    maxX = Math.max(maxX, fp.x + 0.4);
    minY = Math.min(minY, fp.y - 0.4);
    maxY = Math.max(maxY, fp.y + 0.4);

    const pad = 0.2;
    return {
      x: (minX + maxX) / 2,
      y: (minY + maxY) / 2,
      w: Math.max(0.5, (maxX - minX) + pad * 2),
      h: Math.max(0.5, (maxY - minY) + pad * 2),
      minX: minX - pad,
      maxX: maxX + pad,
      minY: minY - pad,
      maxY: maxY + pad
    };
  }

  function hitFootprint(m) {
    if (!S.board?.footprints) return null;
    const tol = Math.max(0.5, 8 / S.view.scale); // mm
    let best = null;
    let bestScore = Infinity;
    for (const fp of S.board.footprints) {
      if (fp.side === 'B') continue;
      const bb = getFpBBox(fp);
      const centerDist = Math.hypot(m.x - fp.x, m.y - fp.y);
      const inBBox = (m.x >= bb.minX - tol && m.x <= bb.maxX + tol && m.y >= bb.minY - tol && m.y <= bb.maxY + tol);
      const nearCenter = centerDist <= Math.max(1.2, 12 / S.view.scale);
      if (inBBox || nearCenter) {
        const dist = Math.hypot(m.x - bb.x, m.y - bb.y);
        const area = bb.w * bb.h;
        const score = area * 4 + dist;
        if (score < bestScore) {
          bestScore = score;
          best = fp;
        }
      }
    }
    return best;
  }

  function hitHandle(m) {
    const it = instanceOf(S.sel);
    if (!it) return null;
    const tol = 6 / S.view.scale;
    const corners = { nw: [it.x - it.w / 2, it.y - it.h / 2], ne: [it.x + it.w / 2, it.y - it.h / 2],
                      sw: [it.x - it.w / 2, it.y + it.h / 2], se: [it.x + it.w / 2, it.y + it.h / 2] };
    for (const [k, [cx, cy]] of Object.entries(corners)) {
      if (Math.abs(m.x - cx) <= tol && Math.abs(m.y - cy) <= tol) return k;
    }
    return null;
  }
  function hitBox(m) {
    const tol = 3 / S.view.scale;
    const its = allInstances();
    // prefer smallest box under cursor
    let best = null;
    for (const it of its) {
      if (Math.abs(m.x - it.x) <= it.w / 2 + tol && Math.abs(m.y - it.y) <= it.h / 2 + tol) {
        if (!best || it.w * it.h < best.w * best.h) best = it;
      }
    }
    return best;
  }

  // ---------- MOUSE ----------
  function onDown(e) {
    if (!S.board) return;
    const m = mouseBoard(e);
    if (e.button === 1 || e.button === 2 || S.space) {
      S.pan = { x: e.clientX, y: e.clientY };
      canvas.className = 'panning';
      e.preventDefault();
      return;
    }
    if (e.button !== 0) return;

    // Component info inspection mode: click any component to inspect details
    if (S.infoMode) {
      const hitFp = hitFootprint(m);
      if (hitFp) {
        showPartInfo(hitFp);
        return;
      }
    }

    // Component selection mode: click existing footprint to group it
    if (S.selectMode) {
      const hitFp = hitFootprint(m);
      if (hitFp) {
        ensureColor();
        const existing = S.doc.boxes.find(b => b.ref === hitFp.ref);
        if (existing) {
          if (existing.c === S.activeColor) {
            // Deselect / remove from group
            S.doc.boxes = S.doc.boxes.filter(b => b !== existing);
            if (S.sel?.id === existing.id) S.sel = null;
            commit();
            toast(`Deselected <b>${hitFp.ref}</b>`);
            return;
          } else {
            // Move into active color group
            existing.c = S.activeColor;
            S.sel = { id: existing.id, i: 0 };
            commit();
            toast(`Moved <b>${hitFp.ref}</b> to active group`);
            return;
          }
        } else {
          // Add footprint as a box in the active color group
          const bb = getFpBBox(hitFp);
          const nb = {
            id: uid('b'),
            c: S.activeColor,
            x: r2(bb.x),
            y: r2(bb.y),
            w: r2(bb.w),
            h: r2(bb.h),
            ref: hitFp.ref,
            val: hitFp.value || '',
            fpid: hitFp.fpid || '',
            pat: null
          };
          S.doc.boxes.push(nb);
          S.sel = { id: nb.id, i: 0 };
          commit();
          toast(`Selected <b>${hitFp.ref}</b> into group`);
          return;
        }
      }
      S.sel = null;
      refreshUI();
      return;
    }

    const handle = hitHandle(m);
    if (handle) {
      const it = instanceOf(S.sel);
      S.drag = { mode: 'resize', handle, b: box(S.sel.id), i: S.sel.i,
                 fx: handle.includes('w') ? it.x + it.w / 2 : it.x - it.w / 2,      // fixed opposite corner
                 fy: handle.includes('n') ? it.y + it.h / 2 : it.y - it.h / 2 };
      return;
    }

    const hit = hitBox(m);
    if (hit) {
      let b = box(hit.id), i = hit.i;
      if (e.altKey && b.pat && liveCount(b) > 1) {
        b = breakOut(b, i);
        i = 0;
        toast('Broke box out of pattern');
      }
      S.sel = { id: b.id, i };
      S.drag = { mode: 'move', b, m0: m, x0: b.x, y0: b.y, moved: false };
      refreshUI();
      return;
    }

    S.sel = null;
    const x = snap(m.x), y = snap(m.y);
    S.drag = { mode: 'draw', x0: x, y0: y, x1: x, y1: y };
    refreshUI();
  }

  function onMove(e) {
    const m = mouseBoard(e);
    $('hudX').textContent = fmt(m.x);
    $('hudY').textContent = fmt(m.y);
    S.mousePos = m;
    if (S.activePreset && !S.drag && !S.pan) {
      render();
    }

    if (S.pan) {
      S.view.x -= (e.clientX - S.pan.x) / S.view.scale;
      S.view.y -= (e.clientY - S.pan.y) / S.view.scale;
      S.pan = { x: e.clientX, y: e.clientY };
      render();
      return;
    }

    if ((S.selectMode || S.infoMode) && !S.drag) {
      const prevHover = S.hoverFp;
      S.hoverFp = hitFootprint(m);
      if (S.hoverFp !== prevHover) {
        canvas.className = S.hoverFp ? 'over-box' : '';
        render();
      }
      return;
    }

    const d = S.drag;
    if (d?.mode === 'draw') {
      d.x1 = snap(m.x); d.y1 = snap(m.y);
      render();
      return;
    }
    if (d?.mode === 'move') {
      d.b.x = r2(snap(d.x0 + (m.x - d.m0.x)));
      d.b.y = r2(snap(d.y0 + (m.y - d.m0.y)));
      d.moved = true;
      render(); fillSelbar();
      return;
    }
    if (d?.mode === 'resize') {
      const x = snap(m.x), y = snap(m.y);
      const w = Math.max(0.05, Math.abs(x - d.fx)), h = Math.max(0.05, Math.abs(y - d.fy));
      const cx = (x + d.fx) / 2, cy = (y + d.fy) / 2;
      const [ox, oy] = offsetOf(d.b, d.i);
      d.b.w = r2(w); d.b.h = r2(h);
      d.b.x = r2(cx - ox); d.b.y = r2(cy - oy);
      render(); fillSelbar();
      return;
    }

    if (!S.board) return;
    const hd = hitHandle(m);
    canvas.className = hd ? (hd === 'nw' || hd === 'se' ? 'resize-nwse' : 'resize-nesw') : hitBox(m) ? 'over-box' : '';
  }

  function onUp() {
    if (S.pan) { S.pan = null; canvas.className = ''; return; }
    const d = S.drag;
    S.drag = null;
    if (!d) return;
    if (d.mode === 'draw') {
      const w = Math.abs(d.x1 - d.x0), h = Math.abs(d.y1 - d.y0);
      if (w * S.view.scale < 4 || h * S.view.scale < 4) {
        if (S.activePreset) {
          ensureColor();
          const cx = snap(d.x0), cy = snap(d.y0);
          const b = {
            id: uid('b'),
            c: S.activeColor,
            x: r2(cx),
            y: r2(cy),
            w: r2(S.activePreset.w),
            h: r2(S.activePreset.h),
            pat: null
          };
          const col = color(S.activeColor);
          if (col && !col.note) {
            col.note = S.activePreset.name;
            renderLegend();
          }
          S.doc.boxes.push(b);
          S.sel = null;
          commit();
          refreshUI();
          toast(`Placed ${S.activePreset.name} at (${fmt(cx)}, ${fmt(cy)})`);
          return;
        }
        render();
        return;
      }
      ensureColor();
      const b = { id: uid('b'), c: S.activeColor, x: r2((d.x0 + d.x1) / 2), y: r2((d.y0 + d.y1) / 2), w: r2(w), h: r2(h), pat: null };
      S.doc.boxes.push(b);
      S.sel = { id: b.id, i: 0 };
      commit();
      return;
    }
    commit();
  }

  function onWheel(e) {
    e.preventDefault();
    const r = canvas.getBoundingClientRect();
    const sx = e.clientX - r.left, sy = e.clientY - r.top;
    const before = toBoard(sx, sy);
    S.view.scale = Math.max(1, Math.min(400, S.view.scale * (e.deltaY < 0 ? 1.15 : 1 / 1.15)));
    const after = toBoard(sx, sy);
    S.view.x += before.x - after.x;
    S.view.y += before.y - after.y;
    render();
  }

  // ---------- KEYBOARD ----------
  function onKey(e) {
    const typing = ['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName);
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); openPrompt(); return; }
    if (typing) { if (e.key === 'Escape') document.activeElement.blur(); return; }

    const k = e.key.toLowerCase();
    if (e.code === 'Space') { S.space = true; e.preventDefault(); return; }
    if ((e.ctrlKey || e.metaKey) && k === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
    if ((e.ctrlKey || e.metaKey) && k === 'y') { e.preventDefault(); redo(); return; }
    if ((e.ctrlKey || e.metaKey) && k === 'd') { e.preventDefault(); duplicate(); return; }
    if (/^[1-9]$/.test(e.key)) {
      const c = S.doc.colors[+e.key - 1];
      if (c) { S.activeColor = c.id; renderLegend(); }
      return;
    }
    if (k === 'f') return fit();
    if (k === 'h') { S.showRef = !S.showRef; $('tglRef').classList.toggle('active', S.showRef); return render(); }
    if (k === 'r' && !e.ctrlKey && !e.metaKey) { flipPreset(); return; }
    if (k === 's' && !e.ctrlKey && !e.metaKey) { toggleSelectMode(); return; }
    if (k === 'x' && !e.ctrlKey && !e.metaKey) { toggleInfoMode(); return; }
    if (k === 'i' && !e.ctrlKey && !e.metaKey) { openIsoViewer(); return; }
    if (k === 'escape') {
      if ($('isoModal')?.classList.contains('open')) {
        closeIsoViewer();
        return;
      }
      if ($('modal')?.classList.contains('open')) {
        $('modal').classList.remove('open');
        return;
      }
      if (S.infoMode || S.infoFp) {
        closePartInfo();
        if (S.infoMode) toggleInfoMode(false);
        return render();
      }
      if (S.selectMode) {
        S.selectMode = false;
        S.hoverFp = null;
        refreshUI();
        toast('Select mode exited');
        return;
      }
      if (S.activePreset) {
        S.activePreset = null;
        updatePresetChipsUI();
        toast('Preset deactivated');
        return render();
      }
      S.sel = null;
      return refreshUI();
    }

    const b = S.sel && box(S.sel.id);
    if (!b) return;
    if (k === 'delete' || k === 'backspace') {
      e.preventDefault();
      if (e.shiftKey) S.doc.boxes = S.doc.boxes.filter(x => x !== b);
      else removeInstance(b, S.sel.i);
      S.sel = null;
      commit();
    } else if (k === 'b') {
      breakSelected();
    } else if (k.startsWith('arrow')) {
      e.preventDefault();
      const step = (S.snap || 0.05) * (e.shiftKey ? 10 : 1);
      if (k === 'arrowleft') b.x = r2(b.x - step);
      if (k === 'arrowright') b.x = r2(b.x + step);
      if (k === 'arrowup') b.y = r2(b.y - step);
      if (k === 'arrowdown') b.y = r2(b.y + step);
      commit();
    }
  }

  function duplicate() {
    const b = S.sel && box(S.sel.id);
    if (!b) return;
    const nb = JSON.parse(JSON.stringify(b));
    nb.id = uid('b');
    nb.x = r2(b.x + 1); nb.y = r2(b.y + 1);
    S.doc.boxes.push(nb);
    S.sel = { id: nb.id, i: firstLive(nb) };
    commit();
  }

  function breakSelected() {
    const b = S.sel && box(S.sel.id);
    if (!b || !b.pat || liveCount(b) <= 1) return toast('Not part of a pattern', 'warn');
    const nb = breakOut(b, S.sel.i);
    S.sel = { id: nb.id, i: 0 };
    commit();
  }

  // ---------- SELECTION BAR ----------
  function fillSelbar() {
    const it = instanceOf(S.sel);
    const bar = $('selbar');
    if (!it) { bar.classList.add('hidden'); return; }
    bar.classList.remove('hidden');
    const b = box(S.sel.id);
    const p = b.pat || { n: 1, dir: 'right', pitch: 0 };
    const active = document.activeElement;
    const set = (id, v) => { if ($(id) !== active) $(id).value = v; };
    set('inX', fmt(it.x)); set('inY', fmt(it.y)); set('inW', fmt(b.w)); set('inH', fmt(b.h));
    set('inCount', p.n);
    const along = p.dir === 'left' || p.dir === 'right' ? b.w : b.h;
    set('inPitch', p.n > 1 ? fmt(p.pitch) : '');
    set('inGap', p.n > 1 ? fmt(p.pitch - along) : '');
    $('inPitch').disabled = $('inGap').disabled = p.n <= 1;
    document.querySelectorAll('#dirBtns button').forEach(btn => btn.classList.toggle('on', btn.dataset.dir === p.dir && p.n > 1));
    const linked = b.pat && liveCount(b) > 1;
    $('btnBreakOne').disabled = $('btnBreakAll').disabled = !linked;
    $('btnBreakOne').style.opacity = $('btnBreakAll').style.opacity = linked ? 1 : 0.4;
    $('selColors').innerHTML = S.doc.colors.map((c, k) =>
      `<button data-c="${c.id}" class="${c.id === b.c ? 'on' : ''}" style="background:${c.hex}" title="${k + 1}: ${esc(c.note || 'no note')}"></button>`).join('');
  }

  function selbarInput(id) {
    const b = S.sel && box(S.sel.id);
    if (!b) return;
    const v = parseFloat($(id).value);
    if (!isFinite(v)) return;
    const [ox, oy] = offsetOf(b, S.sel.i);
    switch (id) {
      case 'inX': b.x = r2(v - ox); break;
      case 'inY': b.y = r2(v - oy); break;
      case 'inW': b.w = r2(Math.max(0.05, v)); break;
      case 'inH': b.h = r2(Math.max(0.05, v)); break;
      case 'inCount': setCount(b, Math.max(1, Math.min(200, Math.round(v)))); break;
      case 'inPitch': if (b.pat) b.pat.pitch = r2(v); break;
      case 'inGap': if (b.pat) b.pat.pitch = r2(v + (b.pat.dir === 'left' || b.pat.dir === 'right' ? b.w : b.h)); break;
    }
    commit();
  }

  function setCount(b, n) {
    if (n <= 1) {
      if (b.pat) {
        // collapse to the selected instance's position
        const it = instanceOf(S.sel);
        b.x = it.x; b.y = it.y;
        b.pat = null;
        S.sel = { id: b.id, i: 0 };
      }
      return;
    }
    if (!b.pat) b.pat = { n, dir: 'right', pitch: r2(b.w + 0.5), skip: [] };
    b.pat.n = n;
    b.pat.skip = (b.pat.skip || []).filter(i => i < n);
  }

  function setDir(dir) {
    const b = S.sel && box(S.sel.id);
    if (!b) return;
    if (!b.pat) setCount(b, 2);
    const oldAlong = b.pat.dir === 'left' || b.pat.dir === 'right' ? b.w : b.h;
    const gap = b.pat.pitch - oldAlong;
    b.pat.dir = dir;
    b.pat.pitch = r2((dir === 'left' || dir === 'right' ? b.w : b.h) + gap);   // keep the same gap
    commit();
  }

  // ---------- LEGEND ----------
  function renderLegend() {
    const ul = $('colorList');
    const counts = {};
    S.doc.boxes.forEach(b => { counts[b.c] = (counts[b.c] || 0) + liveCount(b); });
    ul.innerHTML = S.doc.colors.map((c, k) => {
      const compBoxes = S.doc.boxes.filter(b => b.c === c.id && b.ref);
      const chips = compBoxes.map(b => `
        <span class="fp-tag ${S.sel?.id === b.id ? 'active' : ''}" data-id="${b.id}" title="${b.ref} (${b.val || b.fpid || ''})">
          ${b.ref}
          <span class="del-fp" data-del-fp="${b.id}" title="Remove ${b.ref}">×</span>
        </span>
      `).join('');

      return `
      <li class="color-item" data-c="${c.id}">
        <div class="color-row ${c.id === S.activeColor ? 'active' : ''}" data-c="${c.id}" style="--row-color:${c.hex}">
          <span class="key">${k < 9 ? k + 1 : ''}</span>
          <span class="swatch" style="background:${c.hex}" title="Change color"><input type="color" value="${c.hex}" data-c="${c.id}"></span>
          <input class="note" data-c="${c.id}" value="${esc(c.note)}" placeholder="${compBoxes.length ? compBoxes.map(b => b.ref).join(', ') : 'what part is this?'}">
          <span class="cnt">${counts[c.id] || 0}</span>
          <button class="del" data-c="${c.id}" title="Delete color and its boxes">×</button>
        </div>
        ${chips ? `<div class="color-fps">${chips}</div>` : ''}
      </li>`;
    }).join('');
  }

  function onLegendClick(e) {
    const delFp = e.target.closest('[data-del-fp]');
    if (delFp) {
      const bid = delFp.dataset.delFp;
      const b = box(bid);
      const refName = b?.ref || 'component';
      S.doc.boxes = S.doc.boxes.filter(x => x.id !== bid);
      if (S.sel?.id === bid) S.sel = null;
      commit();
      toast(`Removed <b>${refName}</b> from group`);
      return;
    }

    const fpTag = e.target.closest('.fp-tag');
    if (fpTag) {
      const bid = fpTag.dataset.id;
      const b = box(bid);
      if (b) {
        S.sel = { id: bid, i: 0 };
        S.activeColor = b.c;
        refreshUI();
      }
      return;
    }

    const del = e.target.closest('.del');
    const row = e.target.closest('.color-row');
    if (!row) return;
    const id = row.dataset.c;
    if (del) {
      const n = S.doc.boxes.filter(b => b.c === id).reduce((a, b) => a + liveCount(b), 0);
      // Regular X does NOT ask to confirm (user can use Undo button)
      S.doc.colors = S.doc.colors.filter(c => c.id !== id);
      S.doc.boxes = S.doc.boxes.filter(b => b.c !== id);
      if (S.sel && !instanceOf(S.sel)) S.sel = null;
      ensureColor();
      commit();
      toast(`Deleted color group (${n} item${n === 1 ? '' : 's'}). Undo available.`, 'info');
      return;
    }
    S.activeColor = id;
    S.sel = null;
    refreshUI();
  }

  // ---------- EXPORT ----------
  function buildPrompt() {
    const boxesFile = S.boardPath.replace(/\.kicad_pcb$/i, '.boxes.json');
    const lines = [];
    lines.push(`### Parts to place / update on \`${S.boardPath}\``);
    lines.push('');
    lines.push(`Reference image: \`${S.doc.ref || '(none)'}\``);
    if (S.render3dPath) {
      lines.push(`Top-Down 3D CAD render: \`${S.render3dPath}\``);
    }
    if (S.renderIsoPath) {
      lines.push(`Isometric 3D CAD render: \`${S.renderIsoPath}\``);
    }
    lines.push(`Box file (same data, machine-readable): \`${boxesFile}\``);
    lines.push('');
    lines.push('X/Y = center in KiCad board coordinates (mm). W×H = part/box size. ' +
               'Place/update footprints directly on the PCB and move/align footprint to center. ' +
               'Check color notes to add new parts or correct/align existing footprints. Ask me if a note is missing or unclear.');

    let patLetter = 0;
    const patName = new Map();
    S.doc.boxes.forEach(b => { if (b.pat && liveCount(b) > 1) patName.set(b.id, String.fromCharCode(65 + (patLetter++ % 26))); });

    S.doc.colors.forEach((c, k) => {
      const bs = S.doc.boxes.filter(b => b.c === c.id);
      const its = bs.flatMap(b => instances(b).map(it => ({ ...it, b })));
      if (!its.length) return;
      const compRefs = bs.filter(b => b.ref).map(b => b.ref);
      const titleExtra = compRefs.length ? ` · Selected: ${compRefs.join(', ')}` : '';
      lines.push('');
      lines.push(`#### Color ${k + 1} (${c.hex}): ${c.note ? c.note : '**(no note, ask me)**'} · ${its.length} item${its.length > 1 ? 's' : ''}${titleExtra}`);
      lines.push('');
      lines.push('| # | Ref / Item | Value / Footprint | X (mm) | Y (mm) | W×H (mm) | Details / Pattern |');
      lines.push('|---|---|---|---|---|---|---|');
      let n = 0;
      for (const b of bs) {
        const list = instances(b);
        const name = patName.get(b.id);
        list.forEach((it, j) => {
          n++;
          const pat = name ? `${name} ${j + 1}/${list.length} · ${fmt(b.pat.pitch)} mm ${DIR_ARROW[b.pat.dir]}` : (b.ref ? 'Component on PCB' : '–');
          const refStr = b.ref ? `**${b.ref}**` : `Box ${n}`;
          const valStr = b.ref ? `${b.val || '–'} / ${b.fpid || '–'}` : '–';
          lines.push(`| ${n} | ${refStr} | ${valStr} | ${fmt(it.x)} | ${fmt(it.y)} | ${fmt(it.w)}×${fmt(it.h)} | ${pat} |`);
        });
      }
    });
    return lines.join('\n');
  }

  function flashCopied(btn, text) {
    if (!btn) return;
    const oldHtml = btn.innerHTML;
    btn.innerHTML = text;
    btn.classList.add('btn-copied');
    setTimeout(() => {
      btn.innerHTML = oldHtml;
      btn.classList.remove('btn-copied');
    }, 1500);
  }

  function openPrompt() {
    if (!totalCount()) return toast('No boxes yet. Drag on the board to draw one.', 'warn');
    const text = buildPrompt();
    $('modalText').textContent = text;
    const notes = S.doc.colors.filter(c => !c.note && S.doc.boxes.some(b => b.c === c.id)).length;
    $('modalSub').textContent = `${totalCount()} boxes` + (notes ? ` · ⚠ ${notes} color(s) without a note` : '');
    $('modal').classList.add('open');
    copy(text);
  }
  function copy(text) {
    navigator.clipboard.writeText(text).then(() => {
      toast('Prompt copied to clipboard');
      flashCopied($('btnExport'), `Copied! ✓ <em id="boxCount">${totalCount()}</em>`);
      flashCopied($('btnCopy'), 'Copied! ✓');
    }, () => toast('Clipboard blocked: select and copy manually', 'warn'));
  }

  // ---------- OPACITY CYCLING ----------
  let cycleRaf = null;
  let cycleStartTime = null;

  function setOpacity(val) {
    S.opacity = Math.max(0, Math.min(1, val));
    const pct = Math.round(S.opacity * 100);
    const slider = $('opacity');
    if (slider && document.activeElement !== slider) slider.value = pct;
    const valEl = $('opacityVal');
    if (valEl) valEl.textContent = `${pct}%`;
    render();
  }

  function startOpacityCycle() {
    stopOpacityCycle();
    cycleStartTime = performance.now();
    function tick(now) {
      if (!$('cycleOpacity').checked) return;
      const sec = Math.max(0.2, parseFloat($('cycleSec').value) || 2.0);
      const elapsed = (now - cycleStartTime) / 1000;
      // Smooth sine wave ping-pong 0 to 1
      const progress = (Math.sin((elapsed / sec) * Math.PI * 2 - Math.PI / 2) + 1) / 2;
      setOpacity(progress);
      cycleRaf = requestAnimationFrame(tick);
    }
    cycleRaf = requestAnimationFrame(tick);
  }

  function stopOpacityCycle() {
    if (cycleRaf) {
      cancelAnimationFrame(cycleRaf);
      cycleRaf = null;
    }
  }

  // ---------- UI REFRESH ----------
  function refreshUI() {
    renderLegend();
    fillSelbar();
    $('boxCount').textContent = totalCount();
    if ($('btnUndo')) $('btnUndo').disabled = S.undo.length === 0;
    if ($('btnRedo')) $('btnRedo').disabled = S.redo.length === 0;
    if ($('btnSelectMode')) $('btnSelectMode').classList.toggle('active', !!S.selectMode);
    if ($('btnInfoMode')) $('btnInfoMode').classList.toggle('active', !!S.infoMode);
    render();
  }

  // ---------- PRESETS ----------
  function updatePresetChipsUI() {
    const pc = $('presetChips');
    if (!pc) return;
    pc.querySelectorAll('.chip').forEach(c => {
      const active = S.activePreset && c.dataset.name === S.activePreset.name;
      c.classList.toggle('active', !!active);
    });
  }

  function onPresetClick(chip) {
    const name = chip.dataset.name;
    const w = parseFloat(chip.dataset.w);
    const h = parseFloat(chip.dataset.h);

    if (S.activePreset && S.activePreset.name === name) {
      S.activePreset = null;
      updatePresetChipsUI();
      render();
      toast('Preset cleared');
      return;
    }

    // Preserve flipped orientation if user already flipped preset
    const keepFlipped = S.activePreset ? S.activePreset.flipped : false;
    S.activePreset = {
      name,
      w: keepFlipped ? h : w,
      h: keepFlipped ? w : h,
      flipped: keepFlipped
    };
    updatePresetChipsUI();

    // Deselect any box so quick sizes acts purely as a stamp tool to drop new parts
    // and never accidentally resizes or resets orientation of existing boxes!
    S.sel = null;
    refreshUI();
    toast(`Preset ${name} active (${fmt(S.activePreset.w)} × ${fmt(S.activePreset.h)} mm) — click board to drop`);
  }

  function flipPreset() {
    if (S.activePreset) {
      const tmp = S.activePreset.w;
      S.activePreset.w = S.activePreset.h;
      S.activePreset.h = tmp;
      S.activePreset.flipped = !S.activePreset.flipped;
      updatePresetChipsUI();
      toast(`Flipped preset: ${fmt(S.activePreset.w)} × ${fmt(S.activePreset.h)} mm`);
      render();
      return;
    }
    const b = S.sel && box(S.sel.id);
    if (b) {
      const tmp = b.w;
      b.w = b.h;
      b.h = tmp;
      commit();
      fillSelbar();
      toast(`Flipped box: ${fmt(b.w)} × ${fmt(b.h)} mm`);
    }
  }

  // ---------- EVENTS ----------
  function hookEvents() {
    window.addEventListener('resize', () => {
      resize();
      if ($('isoModal')?.classList.contains('open')) {
        fitIso();
      }
    });
    canvas.addEventListener('mousedown', onDown);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    canvas.addEventListener('mouseleave', () => {
      S.mousePos = null;
      if (S.activePreset) render();
    });
    canvas.addEventListener('wheel', onWheel, { passive: false });
    canvas.addEventListener('contextmenu', e => e.preventDefault());
    window.addEventListener('keydown', onKey);
    window.addEventListener('keyup', e => { if (e.code === 'Space') S.space = false; });

    $('tglRef').onclick = () => { S.showRef = !S.showRef; $('tglRef').classList.toggle('active', S.showRef); render(); };
    const tgl3D = $('tgl3D');
    if (tgl3D) {
      tgl3D.onclick = () => {
        if (!S.render3dImg) {
          toast('No 3D render yet. Click <b>Render 3D</b> in the top bar to generate one.', 'info');
          return;
        }
        S.show3D = !S.show3D;
        tgl3D.classList.toggle('active', S.show3D);
        render();
      };
    }
    $('tglParts').onclick = () => { S.showParts = !S.showParts; $('tglParts').classList.toggle('active', S.showParts); render(); };

    const tglTopCu = $('tglTopCu');
    if (tglTopCu) {
      tglTopCu.onclick = () => {
        S.showTopCu = !S.showTopCu;
        tglTopCu.classList.toggle('active', S.showTopCu);
        render();
      };
    }
    const tglBotCu = $('tglBotCu');
    if (tglBotCu) {
      tglBotCu.onclick = () => {
        S.showBotCu = !S.showBotCu;
        tglBotCu.classList.toggle('active', S.showBotCu);
        render();
      };
    }
    const tglVias = $('tglVias');
    if (tglVias) {
      tglVias.onclick = () => {
        S.showVias = !S.showVias;
        tglVias.classList.toggle('active', S.showVias);
        render();
      };
    }

    const pChips = $('presetChips');
    if (pChips) {
      pChips.addEventListener('click', e => {
        const chip = e.target.closest('.chip');
        if (chip) onPresetClick(chip);
      });
    }
    const btnFlipPreset = $('btnFlipPreset');
    if (btnFlipPreset) btnFlipPreset.onclick = flipPreset;
    $('opacity').oninput = e => {
      if ($('cycleOpacity').checked) $('cycleOpacity').checked = false;
      stopOpacityCycle();
      setOpacity(e.target.value / 100);
    };
    $('cycleOpacity').onchange = e => {
      if (e.target.checked) startOpacityCycle();
      else stopOpacityCycle();
    };
    $('snap').onchange = e => { S.snap = parseFloat(e.target.value); };
    $('btnFit').onclick = fit;

    const btnTop = $('btnTopRender3D');
    if (btnTop) btnTop.onclick = () => triggerRender3D('top');
    const btnIso = $('btnIsoRender3D');
    if (btnIso) btnIso.onclick = () => triggerRender3D('iso');
    const btnViewIso = $('btnViewIso');
    if (btnViewIso) btnViewIso.onclick = openIsoViewer;
    const tglIsoView = $('tglIsoView');
    if (tglIsoView) tglIsoView.onclick = openIsoViewer;

    const btnUndo = $('btnUndo');
    if (btnUndo) btnUndo.onclick = undo;
    const btnRedo = $('btnRedo');
    if (btnRedo) btnRedo.onclick = redo;

    const btnSelectMode = $('btnSelectMode');
    if (btnSelectMode) btnSelectMode.onclick = toggleSelectMode;
    const btnInfoMode = $('btnInfoMode');
    if (btnInfoMode) btnInfoMode.onclick = () => toggleInfoMode();
    const btnCopyInfo = $('btnCopyInfo');
    if (btnCopyInfo) btnCopyInfo.onclick = copyPartInfo;
    const btnCloseInfo = $('btnCloseInfo');
    if (btnCloseInfo) btnCloseInfo.onclick = closePartInfo;
    const btnClearAll = $('btnClearAll');
    if (btnClearAll) btnClearAll.onclick = clearAllBoxes;

    // Isometric Viewer modal controls
    const btnIsoZoomIn = $('btnIsoZoomIn');
    if (btnIsoZoomIn) btnIsoZoomIn.onclick = () => zoomIso(1.25);
    const btnIsoZoomOut = $('btnIsoZoomOut');
    if (btnIsoZoomOut) btnIsoZoomOut.onclick = () => zoomIso(0.8);
    const btnIsoFit = $('btnIsoFit');
    if (btnIsoFit) btnIsoFit.onclick = fitIso;
    const btnIso100 = $('btnIso100');
    if (btnIso100) btnIso100.onclick = () => {
      const vp = $('isoViewport');
      const img = $('isoImg');
      if (!img.naturalWidth) return;
      S.isoView.scale = 1.0;
      S.isoView.x = (vp.clientWidth - img.naturalWidth) / 2;
      S.isoView.y = (vp.clientHeight - img.naturalHeight) / 2;
      applyIsoTransform();
    };
    const btnIsoRerender = $('btnIsoRerender');
    if (btnIsoRerender) btnIsoRerender.onclick = () => triggerRender3D('iso');
    const btnIsoClose = $('btnIsoClose');
    if (btnIsoClose) btnIsoClose.onclick = closeIsoViewer;
    $('isoModal')?.addEventListener('click', e => { if (e.target === $('isoModal')) closeIsoViewer(); });

    const isoVp = $('isoViewport');
    if (isoVp) {
      isoVp.addEventListener('wheel', e => {
        e.preventDefault();
        const r = isoVp.getBoundingClientRect();
        zoomIso(e.deltaY < 0 ? 1.15 : 0.87, e.clientX - r.left, e.clientY - r.top);
      }, { passive: false });
      isoVp.addEventListener('mousedown', e => {
        if (e.button === 0) {
          S.isoDrag = { x: e.clientX, y: e.clientY, ox: S.isoView.x, oy: S.isoView.y };
          isoVp.classList.add('grabbing');
        }
      });
      isoVp.addEventListener('dblclick', () => {
        if (Math.abs(S.isoView.scale - 1.0) < 0.15) fitIso();
        else {
          const img = $('isoImg');
          if (!img.naturalWidth) return;
          S.isoView.scale = 1.0;
          S.isoView.x = (isoVp.clientWidth - img.naturalWidth) / 2;
          S.isoView.y = (isoVp.clientHeight - img.naturalHeight) / 2;
          applyIsoTransform();
        }
      });
    }
    window.addEventListener('mousemove', e => {
      if (S.isoDrag) {
        S.isoView.x = S.isoDrag.ox + (e.clientX - S.isoDrag.x);
        S.isoView.y = S.isoDrag.oy + (e.clientY - S.isoDrag.y);
        applyIsoTransform();
      }
    });
    window.addEventListener('mouseup', () => {
      if (S.isoDrag) {
        S.isoDrag = null;
        $('isoViewport')?.classList.remove('grabbing');
      }
    });

    $('btnAddColor').onclick = () => addColor();
    $('colorList').addEventListener('click', onLegendClick);
    $('colorList').addEventListener('input', e => {
      const id = e.target.dataset.c;
      const c = color(id);
      if (!c) return;
      if (e.target.classList.contains('note')) { c.note = e.target.value; scheduleSave(); fillSelbar(); }
      if (e.target.type === 'color') { c.hex = e.target.value; e.target.parentElement.style.background = c.hex; render(); }
    });
    $('colorList').addEventListener('change', e => { if (e.target.dataset.c) commit(); });

    ['inX', 'inY', 'inW', 'inH', 'inCount', 'inPitch', 'inGap'].forEach(id => $(id).addEventListener('change', () => selbarInput(id)));
    $('dirBtns').addEventListener('click', e => { const d = e.target.dataset.dir; if (d) setDir(d); });
    $('selColors').addEventListener('click', e => {
      const id = e.target.dataset.c;
      const b = S.sel && box(S.sel.id);
      if (id && b) { b.c = id; S.activeColor = id; commit(); }
    });
    $('btnBreakOne').onclick = breakSelected;
    $('btnBreakAll').onclick = () => {
      const b = S.sel && box(S.sel.id);
      if (!b || !b.pat) return;
      const fresh = unlinkAll(b);
      S.sel = { id: fresh[0].id, i: 0 };
      commit();
      toast(`Unlinked ${fresh.length} boxes`);
    };
    $('btnDelete').onclick = () => {
      const b = S.sel && box(S.sel.id);
      if (!b) return;
      removeInstance(b, S.sel.i);
      S.sel = null;
      commit();
    };

    ['refOx', 'refOy', 'refSx', 'refSy'].forEach(id => $(id).addEventListener('input', () => {
      S.doc.refFit = {
        ox: parseFloat($('refOx').value) || 0, oy: parseFloat($('refOy').value) || 0,
        sx: parseFloat($('refSx').value) || 100, sy: parseFloat($('refSy').value) || 100,
      };
      render(); scheduleSave();
    }));
    $('btnRefReset').onclick = () => { S.doc.refFit = { ox: 0, oy: 0, sx: 100, sy: 100 }; fillRefFit(); render(); scheduleSave(); };

    $('btnExport').onclick = openPrompt;
    $('btnCopy').onclick = () => copy($('modalText').textContent);
    $('btnClose').onclick = () => $('modal').classList.remove('open');
    $('modal').addEventListener('click', e => { if (e.target === $('modal')) $('modal').classList.remove('open'); });
  }

  init();
})();
