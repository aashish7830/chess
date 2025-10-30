from flask import Flask, Response, make_response

app = Flask(__name__)


@app.get("/")
def index() -> Response:
    html = (
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#111827" />
    <link rel="manifest" href="/manifest.webmanifest" />
    <link rel="icon" href="/icon.svg" type="image/svg+xml" />
    <title>Offline Chess</title>
    <style>
      :root { --bg:#0b1020; --panel:#111827; --text:#f9fafb; --muted:#9ca3af; --accent:#10b981; --warn:#f59e0b; --sqLight:#ffffff; --sqDark:#000000; }
      html, body { height:100%; margin:0; }
      body { background: radial-gradient(1200px 800px at 30% 20%, #151a2e, var(--bg)); color:var(--text); font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial, sans-serif; display:flex; align-items:flex-start; justify-content:center; padding-top:24px; padding-bottom:24px; }
      .app { width:min(100vw, 1100px); padding:16px; display:grid; grid-template-columns: 1fr 320px; gap:16px; }
      body.view-horiz .app { grid-template-columns: 1fr; }
      @media (max-width: 900px) { .app { grid-template-columns: 1fr; } }
      .card { background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.08); border-radius:14px; box-shadow: 0 10px 30px rgba(0,0,0,0.35); backdrop-filter: blur(6px); }
      .board-wrap { aspect-ratio: 1 / 1; position:relative; }
      .board { width:100%; height:100%; display:grid; grid-template-columns: repeat(8, 1fr); grid-template-rows: repeat(8, 1fr); overflow:hidden; border-radius:14px; border:1px solid rgba(255,255,255,0.12); box-shadow: 0 20px 40px rgba(0,0,0,0.45); }
      .sq { position:relative; display:flex; align-items:center; justify-content:center; font-size: clamp(24px, 5.2vw, 40px); transition: transform .08s ease; }
      .sq:hover { transform: scale(1.02); }
      .l { background: var(--sqDark); } .d { background: var(--sqLight); }
      .pc { line-height:1; filter: drop-shadow(0 2px 1px rgba(0,0,0,.35)); }
      .pc.w { color:#ffffff; text-shadow: 0 0 1px #000, 0 0 2px #000; }
      .pc.b { color:#000000; text-shadow: 0 0 1px #fff, 0 0 2px #fff; }
      .hl { outline: 3px solid rgba(16,185,129,0.9); z-index:2; }
      .mv { box-shadow: inset 0 0 0 4px rgba(16,185,129,0.8); }
      .t { position:absolute; left:6px; bottom:6px; font-size:11px; }
      .l .t { color: rgba(255,255,255,0.7); }
      .d .t { color: rgba(0,0,0,0.55); }
      .side { padding:14px; display:flex; flex-direction:column; gap:12px; }
      .header { display:flex; align-items:center; justify-content:space-between; gap:12px; }
      .title { font-weight:700; letter-spacing:.3px; }
      .sub { color:var(--muted); font-size:13px; }
      .btns { display:flex; gap:8px; flex-wrap:wrap; }
      button { background: #1f2937; color:var(--text); border:1px solid rgba(255,255,255,0.08); padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:600; }
      button:hover { background:#263142; }
      .status { padding:10px 12px; background:#0f172a; border:1px dashed rgba(255,255,255,0.15); border-radius:10px; }
      .moves { max-height: 300px; overflow:auto; padding:8px; background:#0f172a; border-radius:10px; border:1px solid rgba(255,255,255,0.08); }
      .row { display:flex; gap:8px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size:13px; }
      .pill { display:inline-flex; align-items:center; gap:6px; padding:6px 10px; background:#0f172a; border-radius:999px; border:1px solid rgba(255,255,255,0.08); }
      .dot { width:10px; height:10px; border-radius:50%; background:var(--accent); box-shadow: 0 0 12px var(--accent); transition: background .2s ease; }

      /* Settings modal */
      .modal { position: fixed; inset: 0; display:none; align-items:flex-start; justify-content:center; padding:24px; background: rgba(0,0,0,0.45); }
      .modal.open { display:flex; }
      .panel { width:min(100%, 760px); background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:16px; }
      .panel h2 { margin:6px 0 12px; font-size:26px; letter-spacing:.5px; }
      .rows { display:flex; flex-direction:column; gap:12px; }
      .rowset { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:10px 12px; background:#0f172a; border-radius:12px; border:1px solid rgba(255,255,255,0.08); }
      .rowset .label { color:var(--muted); min-width:120px; }
      .opts { display:flex; gap:8px; flex-wrap:wrap; }
      .opt { background:#1f2937; border:1px solid rgba(255,255,255,0.12); padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:600; }
      .opt.active { background:#065f46; border-color:#10b981; }
      .opt[disabled] { opacity:.5; cursor:not-allowed; }
      @media (max-width: 560px) { .btns button { flex:1 1 calc(50% - 8px); } }
      .footer { display:flex; justify-content:flex-end; gap:8px; margin-top:10px; }
    </style>
  </head>
  <body>
    <div class="app">
      <div class="card board-wrap">
        <div id="board" class="board"></div>
      </div>
      <div class="card side">
        <div class="header">
          <div>
            <div class="title">Offline Chess</div>
            <div class="sub">2 players • same device • works offline</div>
          </div>
          <div class="pill"><span class="dot"></span><span id="statusDot">Ready</span></div>
        </div>
        <div class="btns">
          <button id="newGame">New Game</button>
          <button id="flipBoard">Flip Board</button>
          <button id="undo">Undo Move</button>
          <button id="openSettings">Settings</button>
          <button id="installBtn" hidden>Install App</button>
        </div>
        <div class="status" id="status"></div>
        <div class="moves" id="moves"></div>
      </div>
    </div>
    <!-- Settings Modal -->
    <div class="modal" id="settingsModal" aria-hidden="true">
      <div class="panel">
        <h2>Settings</h2>
        <div class="rows">
          <div class="rowset">
            <div class="label">View</div>
            <div class="opts">
              <button class="opt" data-setting="view" data-value="vert" id="optViewVert">VERT.</button>
              <button class="opt" data-setting="view" data-value="horiz" id="optViewHoriz">HORIZ.</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">Theme</div>
            <div class="opts">
              <button class="opt" data-setting="theme" data-value="classic" id="optThemeClassic">CLASSIC</button>
              <button class="opt" data-setting="theme" data-value="green" id="optThemeGreen">GREEN</button>
              <button class="opt" data-setting="theme" data-value="wood" id="optThemeWood">WOOD</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">Sounds</div>
            <div class="opts">
              <button class="opt" data-setting="sound" data-value="on" id="optSoundOn">ON</button>
              <button class="opt" data-setting="sound" data-value="off" id="optSoundOff">OFF</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">Mode</div>
            <div class="opts">
              <button class="opt" data-setting="mode" data-value="2p" id="optMode2p">2 PLAYERS</button>
              <button class="opt" data-setting="mode" data-value="ai" id="optModeAi">VS AI</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">AI Plays As</div>
            <div class="opts">
              <button class="opt" data-setting="aiAs" data-value="white" id="optAiWhite">WHITE</button>
              <button class="opt" data-setting="aiAs" data-value="black" id="optAiBlack">BLACK</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">Play As</div>
            <div class="opts">
              <button class="opt" data-setting="playAs" data-value="white" id="optPlayWhite">WHITE</button>
              <button class="opt" data-setting="playAs" data-value="black" id="optPlayBlack">BLACK</button>
            </div>
          </div>
          <div class="rowset">
            <div class="label">Helper</div>
            <div class="opts">
              <button class="opt" data-setting="helper" data-value="on" id="optHelpOn">ON</button>
              <button class="opt" data-setting="helper" data-value="off" id="optHelpOff">OFF</button>
            </div>
          </div>
        </div>
        <div class="footer">
          <button id="closeSettings">Close</button>
        </div>
      </div>
    </div>
    <script src="/app.js"></script>
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('/sw.js');
        });
      }
    </script>
  </body>
</html>
        """
    )
    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/app.js")
def app_js() -> Response:
    js = (
        """
"use strict";

// Chess logic and UI in one file to keep app portable
(function() {
  const boardEl = document.getElementById('board');
  const statusEl = document.getElementById('status');
  const movesEl = document.getElementById('moves');
  const installBtn = document.getElementById('installBtn');
  const settingsBtn = document.getElementById('openSettings');
  const settingsModal = document.getElementById('settingsModal');
  const closeSettings = document.getElementById('closeSettings');

  let deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.hidden = false;
  });
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice; // result ignored
    deferredPrompt = null;
    installBtn.hidden = true;
  });

  const filesToCache = ['/', '/app.js', '/manifest.webmanifest', '/icon.svg'];
  // Status
  statusEl.textContent = 'White to move';

  // Settings (persisted)
  const defaultSettings = { view: 'vert', sound: 'on', playAs: 'white', helper: 'on', theme: 'classic', mode: '2p', aiAs: 'black' };
  let settings = loadSettings();

  function loadSettings() {
    try { return { ...defaultSettings, ...(JSON.parse(localStorage.getItem('chess.settings')||'{}')) }; } catch { return { ...defaultSettings }; }
  }
  function saveSettings() { localStorage.setItem('chess.settings', JSON.stringify(settings)); }
  function applySettings() {
    document.body.classList.toggle('view-horiz', settings.view === 'horiz');
    // helper affects highlighting; applied in code paths
    applyTheme();
    // enable/disable AI side options
    const disableAiSide = settings.mode !== 'ai';
    document.getElementById('optAiWhite').disabled = disableAiSide;
    document.getElementById('optAiBlack').disabled = disableAiSide;
  }
  function syncSettingsUI() {
    const map = {
      view: { vert: document.getElementById('optViewVert'), horiz: document.getElementById('optViewHoriz') },
      theme: { classic: document.getElementById('optThemeClassic'), green: document.getElementById('optThemeGreen'), wood: document.getElementById('optThemeWood') },
      sound: { on: document.getElementById('optSoundOn'), off: document.getElementById('optSoundOff') },
      playAs: { white: document.getElementById('optPlayWhite'), black: document.getElementById('optPlayBlack') },
      helper: { on: document.getElementById('optHelpOn'), off: document.getElementById('optHelpOff') },
      mode: { '2p': document.getElementById('optMode2p'), ai: document.getElementById('optModeAi') },
      aiAs: { white: document.getElementById('optAiWhite'), black: document.getElementById('optAiBlack') },
    };
    Object.keys(map).forEach(key => {
      Object.keys(map[key]).forEach(val => { map[key][val].classList.toggle('active', settings[key] === val); });
    });
  }

  settingsBtn.addEventListener('click', () => { settingsModal.classList.add('open'); syncSettingsUI(); });
  closeSettings.addEventListener('click', () => { settingsModal.classList.remove('open'); });
  settingsModal.addEventListener('click', (e) => { if (e.target === settingsModal) settingsModal.classList.remove('open'); });
  settingsModal.querySelectorAll('.opt').forEach(btn => btn.addEventListener('click', (e) => {
    const key = e.currentTarget.dataset.setting; const value = e.currentTarget.dataset.value;
    settings[key] = value; saveSettings(); applySettings(); syncSettingsUI();
  }));

  function applyTheme() {
    const root = document.documentElement.style;
    if (settings.theme === 'classic') { root.setProperty('--sqLight', '#ffffff'); root.setProperty('--sqDark', '#000000'); }
    else if (settings.theme === 'green') { root.setProperty('--sqLight', '#e6ffed'); root.setProperty('--sqDark', '#116149'); }
    else if (settings.theme === 'wood') { root.setProperty('--sqLight', '#d7b899'); root.setProperty('--sqDark', '#8b5a2b'); }
  }

  // Board representation
  // Pieces encoded: 'P','N','B','R','Q','K' for white, lowercase for black
  const startFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  let position = null;
  let history = [];
  let flipped = false;

  function parseFEN(fen) {
    const [piecePlacement, activeColor, castling, enPassant, halfmove, fullmove] = fen.split(' ');
    const rows = piecePlacement.split('/');
    const board = [];
    for (let r = 0; r < 8; r++) {
      const row = [];
      for (const ch of rows[r]) {
        if (/\d/.test(ch)) {
          const n = parseInt(ch, 10);
          for (let i = 0; i < n; i++) row.push(null);
        } else {
          row.push(ch);
        }
      }
      board.push(row);
    }
    return { board, turn: activeColor, castling, enPassant: enPassant === '-' ? null : enPassant, halfmove: Number(halfmove), fullmove: Number(fullmove) };
  }

  function clonePosition(pos) {
    return {
      board: pos.board.map(row => row.slice()),
      turn: pos.turn,
      castling: pos.castling,
      enPassant: pos.enPassant,
      halfmove: pos.halfmove,
      fullmove: pos.fullmove,
    };
  }

  function sqToCoords(sq) { // 'e4' -> [r,c]
    const file = sq.charCodeAt(0) - 97;
    const rank = 8 - parseInt(sq[1], 10);
    return [rank, file];
  }

  function coordsToSq(r, c) { // [r,c] -> 'e4'
    return String.fromCharCode(97 + c) + (8 - r);
  }

  function inside(r, c) { return r >= 0 && r < 8 && c >= 0 && c < 8; }
  function colorOf(p) { return !p ? null : (p === p.toUpperCase() ? 'w' : 'b'); }

  // Generate pseudo-legal moves (then filter by king safety)
  function generateMoves(pos) {
    const moves = [];
    const us = pos.turn;
    const them = us === 'w' ? 'b' : 'w';
    const dir = us === 'w' ? -1 : 1; // white pawns move up (r-1)

    function addMove(fromR, fromC, toR, toC, flags) {
      const from = coordsToSq(fromR, fromC);
      const to = coordsToSq(toR, toC);
      moves.push({ from, to, flags: flags || {} });
    }

    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
      const p = pos.board[r][c];
      if (!p || colorOf(p) !== us) continue;
      const up = p.toUpperCase();
      if (up === 'P') {
        const nr = r + dir;
        if (inside(nr, c) && !pos.board[nr][c]) {
          if (nr === (us === 'w' ? 0 : 7)) {
            ['Q','R','B','N'].forEach(prom => addMove(r, c, nr, c, { promo: us === 'w' ? prom : prom.toLowerCase() }));
          } else addMove(r, c, nr, c);
          const startRank = us === 'w' ? 6 : 1;
          const nr2 = r + 2*dir;
          if (r === startRank && !pos.board[nr2][c]) addMove(r, c, nr2, c, { dbl: true });
        }
        // captures
        for (const dc of [-1, 1]) {
          const nc = c + dc;
          if (!inside(nr, nc)) continue;
          const target = pos.board[nr][nc];
          if (target && colorOf(target) === them) {
            if (nr === (us === 'w' ? 0 : 7)) {
              ['Q','R','B','N'].forEach(prom => addMove(r, c, nr, nc, { promo: us === 'w' ? prom : prom.toLowerCase() }));
            } else addMove(r, c, nr, nc);
          }
        }
        // en passant
        if (pos.enPassant) {
          const [er, ec] = sqToCoords(pos.enPassant);
          if (er === nr && Math.abs(ec - c) === 1) addMove(r, c, er, ec, { ep: true });
        }
      } else if (up === 'N') {
        const steps = [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]];
        for (const [dr, dc] of steps) {
          const nr = r + dr, nc = c + dc;
          if (!inside(nr, nc)) continue;
          const t = pos.board[nr][nc];
          if (!t || colorOf(t) === them) addMove(r, c, nr, nc);
        }
      } else if (up === 'B' || up === 'R' || up === 'Q') {
        const rays = [];
        if (up !== 'B') rays.push([1,0],[-1,0],[0,1],[0,-1]);
        if (up !== 'R') rays.push([1,1],[1,-1],[-1,1],[-1,-1]);
        for (const [dr, dc] of rays) {
          let nr = r + dr, nc = c + dc;
          while (inside(nr, nc)) {
            const t = pos.board[nr][nc];
            if (!t) { addMove(r, c, nr, nc); }
            else { if (colorOf(t) === them) addMove(r, c, nr, nc); break; }
            nr += dr; nc += dc;
          }
        }
      } else if (up === 'K') {
        for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
          if (!dr && !dc) continue;
          const nr = r + dr, nc = c + dc;
          if (!inside(nr, nc)) continue;
          const t = pos.board[nr][nc];
          if (!t || colorOf(t) === them) addMove(r, c, nr, nc);
        }
        // Castling
        const rights = pos.castling;
        const homeRank = us === 'w' ? 7 : 0;
        if (r === homeRank && c === 4) {
          if ((us === 'w' && rights.includes('K')) || (us === 'b' && rights.includes('k'))) {
            if (!pos.board[homeRank][5] && !pos.board[homeRank][6]) addMove(r, c, homeRank, 6, { castle: 'K' });
          }
          if ((us === 'w' && rights.includes('Q')) || (us === 'b' && rights.includes('q'))) {
            if (!pos.board[homeRank][1] && !pos.board[homeRank][2] && !pos.board[homeRank][3]) addMove(r, c, homeRank, 2, { castle: 'Q' });
          }
        }
      }
    }

    // Filter by king safety
    return moves.filter(mv => {
      const pos2 = applyMove(clonePosition(pos), mv, true);
      return !isKingInCheck(pos2, us);
    });
  }

  function isKingInCheck(pos, color) {
    // find king
    let kr = -1, kc = -1, king = color === 'w' ? 'K' : 'k';
    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) if (pos.board[r][c] === king) { kr = r; kc = c; }
    const them = color === 'w' ? 'b' : 'w';
    // Attacks by pawns
    const dir = color === 'w' ? -1 : 1; // direction of our pawns, but we want enemy attacks
    const pdir = color === 'w' ? 1 : -1; // enemy pawns move towards king
    for (const dc of [-1, 1]) {
      const r = kr + pdir, c = kc + dc;
      if (inside(r, c) && pos.board[r][c] && pos.board[r][c].toLowerCase() === 'p' && colorOf(pos.board[r][c]) === them) return true;
    }
    // Knights
    const ns = [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]];
    for (const [dr, dc] of ns) {
      const r = kr + dr, c = kc + dc;
      if (inside(r, c) && pos.board[r][c] && pos.board[r][c].toLowerCase() === 'n' && colorOf(pos.board[r][c]) === them) return true;
    }
    // Sliders
    const rays = {
      rook: [[1,0],[-1,0],[0,1],[0,-1]],
      bishop: [[1,1],[1,-1],[-1,1],[-1,-1]]
    };
    for (const [dr, dc] of rays.rook) {
      let r = kr + dr, c = kc + dc;
      while (inside(r, c)) {
        const t = pos.board[r][c];
        if (t) { const up = t.toUpperCase(); if (colorOf(t) === them && (up === 'R' || up === 'Q')) return true; break; }
        r += dr; c += dc;
      }
    }
    for (const [dr, dc] of rays.bishop) {
      let r = kr + dr, c = kc + dc;
      while (inside(r, c)) {
        const t = pos.board[r][c];
        if (t) { const up = t.toUpperCase(); if (colorOf(t) === them && (up === 'B' || up === 'Q')) return true; break; }
        r += dr; c += dc;
      }
    }
    // King
    for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
      if (!dr && !dc) continue;
      const r = kr + dr, c = kc + dc;
      if (inside(r, c) && pos.board[r][c] && pos.board[r][c].toLowerCase() === 'k' && colorOf(pos.board[r][c]) === them) return true;
    }
    return false;
  }

  function applyMove(pos, mv, skipTurnToggle) {
    const [fr, fc] = sqToCoords(mv.from);
    const [tr, tc] = sqToCoords(mv.to);
    const piece = pos.board[fr][fc];
    const us = colorOf(piece);
    const them = us === 'w' ? 'b' : 'w';

    // Reset enPassant by default
    pos.enPassant = null;

    // Halfmove clock
    if (piece.toLowerCase() === 'p' || pos.board[tr][tc]) pos.halfmove = 0; else pos.halfmove += 1;

    // Castling rights update when king/rook moves or rook captured
    function removeRight(ch) { if (pos.castling.includes(ch)) pos.castling = pos.castling.replace(ch, ''); }
    if (piece.toLowerCase() === 'k') {
      if (us === 'w') { removeRight('K'); removeRight('Q'); } else { removeRight('k'); removeRight('q'); }
    }
    if (piece.toLowerCase() === 'r') {
      if (us === 'w' && fr === 7 && fc === 0) removeRight('Q');
      if (us === 'w' && fr === 7 && fc === 7) removeRight('K');
      if (us === 'b' && fr === 0 && fc === 0) removeRight('q');
      if (us === 'b' && fr === 0 && fc === 7) removeRight('k');
    }
    const captured = pos.board[tr][tc];
    if (captured && captured.toLowerCase() === 'r') {
      if (them === 'w' && tr === 7 && tc === 0) removeRight('Q');
      if (them === 'w' && tr === 7 && tc === 7) removeRight('K');
      if (them === 'b' && tr === 0 && tc === 0) removeRight('q');
      if (them === 'b' && tr === 0 && tc === 7) removeRight('k');
    }

    // En passant capture
    if (mv.flags && mv.flags.ep) {
      const capR = us === 'w' ? tr + 1 : tr - 1;
      pos.board[capR][tc] = null;
    }

    // Move piece
    pos.board[tr][tc] = piece;
    pos.board[fr][fc] = null;

    // Promotion
    if (mv.flags && mv.flags.promo) pos.board[tr][tc] = mv.flags.promo;

    // Double pawn push -> set enPassant square
    if (mv.flags && mv.flags.dbl) {
      const epR = us === 'w' ? tr + 1 : tr - 1;
      pos.enPassant = coordsToSq(epR, tc);
    }

    // Castling rook move
    if (mv.flags && mv.flags.castle) {
      const homeRank = us === 'w' ? 7 : 0;
      if (mv.flags.castle === 'K') {
        // rook h -> f
        pos.board[homeRank][5] = pos.board[homeRank][7];
        pos.board[homeRank][7] = null;
      } else {
        // rook a -> d
        pos.board[homeRank][3] = pos.board[homeRank][0];
        pos.board[homeRank][0] = null;
      }
      if (us === 'w') { pos.castling = pos.castling.replace('K','').replace('Q',''); }
      else { pos.castling = pos.castling.replace('k','').replace('q',''); }
    }

    // Turn toggle and fullmove
    if (!skipTurnToggle) {
      pos.turn = pos.turn === 'w' ? 'b' : 'w';
      if (pos.turn === 'w') pos.fullmove += 1;
    }
    return pos;
  }

  function setup() {
    position = parseFEN(startFEN);
    // Respect Play As: flip board if user wants to play black
    flipped = settings.playAs === 'black';
    render();
    updateStatus();
    history = [];
    movesEl.innerHTML = '';
    // If vs AI and AI is white, let AI move first
    maybeAIMove();
  }

  function render() {
    boardEl.innerHTML = '';
    const files = ['a','b','c','d','e','f','g','h'];
    const ranks = [8,7,6,5,4,3,2,1];
    const filesV = flipped ? files.slice().reverse() : files;
    const ranksV = flipped ? ranks.slice().reverse() : ranks;
    for (let rIdx = 0; rIdx < 8; rIdx++) {
      for (let cIdx = 0; cIdx < 8; cIdx++) {
        const r = 8 - ranksV[rIdx], c = filesV[cIdx].charCodeAt(0) - 97;
        const sq = coordsToSq(r, c);
        const p = position.board[r][c];
        const el = document.createElement('div');
        el.className = 'sq ' + (((r + c) % 2 === 0) ? 'd' : 'l');
        el.dataset.sq = sq;
        if ((rIdx === 7) && (cIdx === 0)) {
          // no-op to satisfy linter-like style
        }
        const t = document.createElement('div');
        t.className = 't';
        t.textContent = (cIdx === 0 ? ranksV[rIdx] : '') + '';
        const ft = document.createElement('div');
        ft.className = 't';
        ft.style.right = '6px';
        ft.style.left = 'auto';
        ft.style.bottom = 'auto';
        ft.style.top = '6px';
        ft.textContent = (rIdx === 7 ? filesV[cIdx] : '');
        el.appendChild(t);
        el.appendChild(ft);
        if (p) {
          const span = document.createElement('span');
          span.className = 'pc ' + (p === p.toUpperCase() ? 'w' : 'b');
          span.textContent = pieceToGlyph(p);
          el.appendChild(span);
        }
        boardEl.appendChild(el);
      }
    }
  }

  function pieceToGlyph(p) {
    const map = {
      'K':'♔','Q':'♕','R':'♖','B':'♗','N':'♘','P':'♙',
      'k':'♚','q':'♛','r':'♜','b':'♝','n':'♞','p':'♟'
    };
    return map[p];
  }

  let selected = null;
  let legalForSelected = [];

  boardEl.addEventListener('click', (e) => {
    if (settings.mode === 'ai' && ((settings.aiAs === 'white' && position.turn === 'w') || (settings.aiAs === 'black' && position.turn === 'b'))) {
      return; // ignore clicks during AI turn
    }
    const sqEl = e.target.closest('.sq');
    if (!sqEl) return;
    const sq = sqEl.dataset.sq;
    const [r, c] = sqToCoords(sq);
    const p = position.board[r][c];
    if (selected) {
      // try move
      const mv = legalForSelected.find(m => m.to === sq);
      if (mv) {
        // detect capture before state mutates
        const [tr, tc] = sqToCoords(mv.to);
        const preTarget = position.board[tr][tc];
        const wasCapture = !!preTarget || (mv.flags && mv.flags.ep);
        history.push(JSON.stringify(position));
        applyMove(position, mv);
        render();
        selected = null;
        legalForSelected = [];
        updateStatus(mv);
        playMoveSound(wasCapture ? 'capture' : 'move');
        // If vs AI, trigger AI reply
        maybeAIMove();
        return;
      }
    }
    if (p && colorOf(p)[0] === position.turn) {
      selected = sq;
      legalForSelected = generateMoves(position).filter(m => m.from === sq);
      highlightSquares([sq].concat(legalForSelected.map(m => m.to)));
    } else {
      selected = null;
      legalForSelected = [];
      clearHighlights();
    }
  });

  function clearHighlights() { document.querySelectorAll('.sq').forEach(e => { e.classList.remove('hl'); e.classList.remove('mv'); }); }
  function highlightSquares(sqs) {
    clearHighlights();
    if (settings.helper !== 'on') return;
    sqs.forEach(s => { const el = document.querySelector(`.sq[data-sq="${s}"]`); if (el) el.classList.add('hl'); });
    if (sqs.length > 1) sqs.slice(1).forEach(s => { const el = document.querySelector(`.sq[data-sq="${s}"]`); if (el) el.classList.add('mv'); });
  }

  function updateStatus(lastMv) {
    const us = position.turn; const them = us === 'w' ? 'b' : 'w';
    const moves = generateMoves(position);
    const inCheck = isKingInCheck(position, us);
    let text = (us === 'w' ? 'White' : 'Black') + ' to move';
    if (inCheck && moves.length === 0) text = 'Checkmate! ' + (us === 'w' ? 'Black' : 'White') + ' wins';
    else if (!inCheck && moves.length === 0) text = 'Stalemate!';
    else if (inCheck) text += ' — Check!';
    statusEl.textContent = text;
    const dot = document.querySelector('.dot');
    if (text.startsWith('Checkmate')) { dot.style.background = '#ef4444'; }
    else if (inCheck) { dot.style.background = '#f59e0b'; }
    else { dot.style.background = 'var(--accent)'; }
    if (lastMv) appendMove(lastMv);
  }

  function appendMove(mv) {
    const row = document.createElement('div');
    row.className = 'row';
    const ply = document.createElement('div');
    ply.textContent = (position.turn === 'w') ? (position.fullmove - 1) + '.' : position.fullmove + '...';
    const san = document.createElement('div');
    san.textContent = mvToAlgebraic(mv);
    row.appendChild(ply);
    row.appendChild(san);
    movesEl.appendChild(row);
    movesEl.scrollTop = movesEl.scrollHeight;
  }

  function mvToAlgebraic(mv) {
    const [fr, fc] = sqToCoords(mv.from); const [tr, tc] = sqToCoords(mv.to);
    const p = position.board[tr][tc]; // after the move applied already
    const piece = (p || '').toUpperCase();
    const capture = mv.flags && (mv.flags.ep || false);
    const pieceChar = piece === 'P' ? '' : piece;
    const promo = mv.flags && mv.flags.promo ? ('=' + mv.flags.promo.toUpperCase()) : '';
    const check = (() => { const pos2 = clonePosition(position); const us = pos2.turn; pos2.turn = us === 'w' ? 'b' : 'w'; return isKingInCheck(pos2, pos2.turn); })();
    const suffix = check ? '+' : '';
    const sameFile = fc !== tc;
    const takes = sameFile && piece === 'P';
    return (takes ? (String.fromCharCode(97 + fc) + 'x') : '') + mv.to + promo + suffix;
  }

  // Sounds (WebAudio tiny tones)
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;
  function playMoveSound(kind) {
    if (settings.sound !== 'on') return;
    if (!AudioCtx) return;
    if (!audioCtx) audioCtx = new AudioCtx();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    const now = audioCtx.currentTime;
    const freq = kind === 'capture' ? 360 : 520;
    osc.frequency.setValueAtTime(freq, now);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.16, now + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.18);
    osc.connect(gain).connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.2);
  }

  // --- Simple AI (minimax depth 2 with alpha-beta) ---
  const pieceValue = { p:100, n:320, b:330, r:500, q:900, k:0 };
  function evaluate(pos) {
    let score = 0;
    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
      const p = pos.board[r][c]; if (!p) continue;
      const val = pieceValue[p.toLowerCase()] || 0;
      score += (p === p.toUpperCase()) ? val : -val;
    }
    return score; // positive = white better
  }
  function isTerminal(pos) {
    const moves = generateMoves(pos);
    if (moves.length > 0) return false;
    return true; // checkmate or stalemate handled by consumers
  }
  function minimax(pos, depth, alpha, beta, maximizingFor) {
    if (depth === 0 || isTerminal(pos)) {
      const evalScore = evaluate(pos);
      return maximizingFor === 'w' ? evalScore : -evalScore;
    }
    const moves = generateMoves(pos);
    if (pos.turn === maximizingFor) {
      let best = -Infinity;
      for (const mv of moves) {
        const child = applyMove(clonePosition(pos), mv);
        const val = minimax(child, depth - 1, alpha, beta, maximizingFor);
        if (val > best) best = val;
        if (val > alpha) alpha = val;
        if (beta <= alpha) break;
      }
      return best;
    } else {
      let best = Infinity;
      for (const mv of moves) {
        const child = applyMove(clonePosition(pos), mv);
        const val = minimax(child, depth - 1, alpha, beta, maximizingFor);
        if (val < best) best = val;
        if (val < beta) beta = val;
        if (beta <= alpha) break;
      }
      return best;
    }
  }
  function chooseAIMove(pos, aiColor) {
    const moves = generateMoves(pos);
    if (moves.length === 0) return null;
    // prefer captures slightly first for ordering
    moves.sort((a,b) => ((pos.board[sqToCoords(b.to)[0]][sqToCoords(b.to)[1]]?1:0) - (pos.board[sqToCoords(a.to)[0]][sqToCoords(a.to)[1]]?1:0)));
    let bestVal = -Infinity, best = moves[0];
    for (const mv of moves) {
      const child = applyMove(clonePosition(pos), mv);
      const val = minimax(child, 2 - 1, -Infinity, Infinity, aiColor); // depth 2 total
      const jitter = (Math.random() - 0.5) * 5; // tiny randomness
      if (val + jitter > bestVal) { bestVal = val + jitter; best = mv; }
    }
    return best;
  }
  function isAITurn() {
    if (settings.mode !== 'ai') return false;
    return (settings.aiAs === 'white' && position.turn === 'w') || (settings.aiAs === 'black' && position.turn === 'b');
  }
  function maybeAIMove() {
    if (!isAITurn()) return;
    setTimeout(() => {
      const mv = chooseAIMove(position, settings.aiAs === 'white' ? 'w' : 'b');
      if (!mv) return;
      const [tr, tc] = sqToCoords(mv.to); const pre = position.board[tr][tc];
      const wasCapture = !!pre || (mv.flags && mv.flags.ep);
      applyMove(position, mv);
      render(); clearHighlights(); updateStatus(mv);
      playMoveSound(wasCapture ? 'capture' : 'move');
    }, 180);
  }

  document.getElementById('newGame').addEventListener('click', () => setup());
  document.getElementById('flipBoard').addEventListener('click', () => { flipped = !flipped; render(); clearHighlights(); });
  document.getElementById('undo').addEventListener('click', () => {
    if (history.length === 0) return;
    position = JSON.parse(history.pop());
    render();
    clearHighlights();
    updateStatus();
  });

  // Init
  applySettings();
  setup();
})();
        """
    )
    resp = make_response(js)
    resp.headers["Content-Type"] = "application/javascript; charset=utf-8"
    return resp


@app.get("/manifest.webmanifest")
def manifest() -> Response:
    manifest_json = (
        """
{
  "name": "Offline Chess",
  "short_name": "Chess",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0b1020",
  "theme_color": "#111827",
  "icons": [
    { "src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable" }
  ]
}
        """
    ).strip()
    resp = make_response(manifest_json)
    resp.headers["Content-Type"] = "application/manifest+json; charset=utf-8"
    return resp


@app.get("/icon.svg")
def icon_svg() -> Response:
    svg = (
        """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="256" height="256" rx="48" fill="#0b1020"/>
  <g transform="translate(28,16)">
    <path d="M80 56c0-17.673 14.327-32 32-32s32 14.327 32 32v8h8c8.837 0 16 7.163 16 16v16c0 8.837-7.163 16-16 16h-8v56c0 8.837-7.163 16-16 16H96c-8.837 0-16-7.163-16-16v-56h-8c-8.837 0-16-7.163-16-16V80c0-8.837 7.163-16 16-16h8v-8z" fill="url(#g)"/>
    <circle cx="112" cy="24" r="8" fill="#f9fafb"/>
  </g>
</svg>
        """
    ).strip()
    resp = make_response(svg)
    resp.headers["Content-Type"] = "image/svg+xml; charset=utf-8"
    return resp


@app.get("/sw.js")
def service_worker() -> Response:
    sw = (
        """
const CACHE_NAME = 'offline-chess-v1';
const ASSETS = ['/', '/app.js', '/manifest.webmanifest', '/icon.svg'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => k === CACHE_NAME ? null : caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(req, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match('/')))
  );
});
        """
    ).strip()
    resp = make_response(sw)
    resp.headers["Content-Type"] = "application/javascript; charset=utf-8"
    return resp


if __name__ == "__main__":
    # Run the app: python app.py, then open http://localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)


