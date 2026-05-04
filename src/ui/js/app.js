// ── State ──────────────────────────────────────────────
const state = {
  players: [],
  rounds: [],       // array of arrays of game dicts
  currentRound: 0,
  totalGames: 0,
};

// ── PyWebView bridge ───────────────────────────────────
async function api(fn, ...args) {
  if (window.pywebview && window.pywebview.api) {
    return await window.pywebview.api[fn](...args);
  }
  // Dev fallback: mock responses
  return mockApi(fn, args);
}

// ── UI helpers ─────────────────────────────────────────
function showPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  document.getElementById('nav-' + name).classList.add('active');
  if (name === 'standings') refreshStandings();
}

function toast(msg, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show' + (isError ? ' error' : '');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.className = '', 3000);
}

function setStatus(text, active = false) {
  document.getElementById('statusText').textContent = text;
  const bar = document.getElementById('statusBar');
  bar.className = 'status-bar' + (active ? ' active' : '');
}

function updateExportButton() {
  const exportBtn = document.getElementById('btnExportRound');
  exportBtn.disabled = state.rounds.length === 0 || state.currentRound < 0;
}

function outcomeLabel(outcome) {
  if (!outcome || outcome === 'None' || outcome === 'null') return '<span class="badge pending">Pending</span>';
  const map = {
    'WHITE_WIN': '<span class="badge white-win">White Wins</span>',
    'BLACK_WIN': '<span class="badge black-win">Black Wins</span>',
    'DRAW':      '<span class="badge draw">Draw</span>',
  };
  return map[outcome] || `<span class="badge pending">${outcome}</span>`;
}

// ── Load Players ───────────────────────────────────────
async function browseFile() {
  const result = await api('pick_file');
  if (result && result.path) {
    document.getElementById('csvPath').value = result.path;
    document.getElementById('btnLoad').disabled = false;
  }
}

async function loadPlayers() {
  const path = document.getElementById('csvPath').value.trim();
  if (!path) { toast('No file selected.', true); return; }

  try {
    const result = await api('load_players', path);
    if (result.error) { toast(result.error, true); return; }

    state.players = result.players;
    renderPlayersTable();
    updateStats();
    setStatus(`${state.players.length} players loaded`, true);
    toast(`Loaded ${state.players.length} players`);
    document.getElementById('playersCard').style.display = '';
  } catch(e) {
    toast('Failed to load players: ' + e, true);
  }
}

function renderPlayersTable() {
  const tb = document.getElementById('playersTable');
  tb.innerHTML = state.players.map((p, i) =>
    `<tr>
      <td style="color:var(--muted)">${i + 1}</td>
      <td>${p.firstName} ${p.lastName}</td>
      <td style="color:var(--gold)">${p.rating ?? '—'}</td>
    </tr>`
  ).join('');
}

// ── Generate Round ─────────────────────────────────────
async function generateRound() {
  if (!state.players.length) { toast('Load players first.', true); return; }
  try {
    const result = await api('generate_round');
    if (result.error) { toast(result.error, true); return; }

    state.rounds.push(result.games);
    state.currentRound = state.rounds.length - 1;
    state.totalGames += result.games.length;
    updateStats();
    renderRoundTabs();
    renderGames(state.currentRound);
    updateExportButton();
    document.getElementById('gamesCard').style.display = '';
    toast(`Round ${state.rounds.length} generated — ${result.games.length} games`);
  } catch(e) {
    toast('Error generating round: ' + e, true);
  }
}

function renderRoundTabs() {
  const tabs = document.getElementById('roundTabs');
  tabs.innerHTML = state.rounds.map((_, i) =>
    `<button class="round-tab ${i === state.currentRound ? 'active' : ''}"
       onclick="selectRound(${i})">Round ${i + 1}</button>`
  ).join('');
}

function selectRound(idx) {
  state.currentRound = idx;
  renderRoundTabs();
  renderGames(idx);
  updateExportButton();
}

function renderGames(roundIdx) {
  const games = state.rounds[roundIdx];
  const tb = document.getElementById('gamesTable');
  tb.innerHTML = games.map(g => {
    const wName = `${g.white.firstName} ${g.white.lastName}`;
    const bName = `${g.black.firstName} ${g.black.lastName}`;
    return `<tr id="game-row-${g.id}">
      <td style="color:var(--muted);font-size:0.7rem">#${g.id}</td>
      <td>${wName}<br><span style="color:var(--muted);font-size:0.65rem">ID: ${g.white.id ?? '—'}</span></td>
      <td>${bName}<br><span style="color:var(--muted);font-size:0.65rem">ID: ${g.black.id ?? '—'}</span></td>
      <td>
        <div class="result-toggle" id="result-${g.id}">
          <button class="result-btn ${g.outcome === 'WHITE_WIN' ? 'active win' : ''}" onclick="recordResult(${g.id}, 1)" title="White Wins">W</button>
          <button class="result-btn ${g.outcome === 'DRAW' ? 'active draw' : ''}" onclick="recordResult(${g.id}, 3)" title="Draw">D</button>
          <button class="result-btn ${g.outcome === 'BLACK_WIN' ? 'active loss' : ''}" onclick="recordResult(${g.id}, 2)" title="Black Wins">B</button>
        </div>
      </td>
      <td>
        <button class="btn btn-sm danger" onclick="swapPlayers(${g.id})">Swap</button>
      </td>
    </tr>`;
  }).join('');
}

// ── Record Result ──────────────────────────────────────
async function recordResult(gameId, code) {
  if (!code) { toast('Invalid result code.', true); return; }

  try {
    const result = await api('record_result', gameId, code);
    if (result.error) { toast(result.error, true); return; }

    // Update local state
    for (const round of state.rounds) {
      const g = round.find(g => g.id === gameId);
      if (g) { g.outcome = result.outcome; break; }
    }
    renderGames(state.currentRound);
    toast(`Result recorded for game ${gameId}`);
  } catch(e) {
    toast('Error recording result: ' + e, true);
  }
}

// ── Swap Players ───────────────────────────────────────
async function swapPlayers(gameId) {
  try {
    const result = await api('swap_players', gameId);
    if (result.error) { toast(result.error, true); return; }

    // Update local state and re-render
    for (const round of state.rounds) {
      const g = round.find(g => g.id === gameId);
      if (g) { [g.white, g.black] = [g.black, g.white]; break; }
    }
    renderGames(state.currentRound);
    toast(`Swapped colors for game ${gameId}`);
  } catch(e) {
    toast('Error swapping players: ' + e, true);
  }
}

async function exportCurrentRoundPgn() {
  if (state.currentRound < 0 || !state.rounds.length) {
    toast('Generate a round first.', true);
    return;
  }

  try {
    const result = await api('export_round_pgn', state.currentRound);
    if (result.error) { toast(result.error, true); return; }
    if (result.cancelled) { return; }

    toast(`PGN exported for Round ${state.currentRound + 1}`);
  } catch (e) {
    toast('Error exporting PGN: ' + e, true);
  }
}

// ── Standings ──────────────────────────────────────────
function refreshStandings() {
  const scores = {};
  const record = {};

  state.players.forEach(p => {
    const key = `${p.firstName} ${p.lastName}`;
    scores[key] = 0;
    record[key] = { w: 0, d: 0, l: 0, rating: p.rating };
  });

  for (const round of state.rounds) {
    for (const g of round) {
      const w = `${g.white.firstName} ${g.white.lastName}`;
      const b = `${g.black.firstName} ${g.black.lastName}`;
      if (g.outcome === 'WHITE_WIN') {
        scores[w] = (scores[w] || 0) + 1; record[w].w++;
        record[b].l++;
      } else if (g.outcome === 'BLACK_WIN') {
        scores[b] = (scores[b] || 0) + 1; record[b].w++;
        record[w].l++;
      } else if (g.outcome === 'DRAW') {
        scores[w] = (scores[w] || 0) + 0.5; record[w].d++;
        scores[b] = (scores[b] || 0) + 0.5; record[b].d++;
      }
    }
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const tb = document.getElementById('standingsTable');

  if (!sorted.length) {
    tb.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:32px">No data yet</td></tr>';
    return;
  }

  tb.innerHTML = sorted.map(([name, pts], i) => {
    const r = record[name] || {};
    return `<tr>
      <td style="color:var(--gold);font-family:'Playfair Display',serif;font-size:1.1rem">${i+1}</td>
      <td>${name}</td>
      <td style="color:var(--muted)">${r.rating ?? '—'}</td>
      <td style="color:var(--gold);font-weight:500">${pts}</td>
      <td style="color:#4a7c59">${r.w ?? 0}</td>
      <td style="color:#4a5f7c">${r.d ?? 0}</td>
      <td style="color:#7c4a4a">${r.l ?? 0}</td>
    </tr>`;
  }).join('');
}

function updateStats() {
  document.getElementById('statPlayers').textContent = state.players.length || '—';
  document.getElementById('statRounds').textContent = state.rounds.length || '—';
  document.getElementById('statGames').textContent = state.totalGames || '—';
}

// ── Mock API (dev/testing without Python) ─────────────
let mockRoundCount = 0;
function mockApi(fn, args) {
  if (fn === 'pick_file') return { path: 'mock_players.csv' };
  if (fn === 'load_players') {
    return { players: [
      { firstName: 'Alice', lastName: 'Smith', rating: 1950 },
      { firstName: 'Bob',   lastName: 'Jones', rating: 1800 },
      { firstName: 'Carol', lastName: 'Lee',   rating: 1650 },
      { firstName: 'Dave',  lastName: 'Kim',   rating: 1500 },
    ]};
  }
  if (fn === 'generate_round') {
    mockRoundCount++;
    return { games: [
      { id: mockRoundCount * 10 + 1, white: { firstName:'Alice', lastName:'Smith' }, black: { firstName:'Bob',   lastName:'Jones' }, outcome: null },
      { id: mockRoundCount * 10 + 2, white: { firstName:'Carol', lastName:'Lee'   }, black: { firstName:'Dave',  lastName:'Kim'   }, outcome: null },
    ]};
  }
  if (fn === 'record_result') {
    const map = { 1: 'WHITE_WIN', 2: 'BLACK_WIN', 3: 'DRAW' };
    return { outcome: map[args[1]] };
  }
  if (fn === 'swap_players') return { success: true };
  if (fn === 'export_round_pgn') return { success: true, path: `round_${args[0] + 1}.pgn` };
  return { error: 'Unknown function' };
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Components are already in the HTML, no loading needed
  updateExportButton();
  console.log('App initialized');
});
