(() => {
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const boot = $('#boot'), lock = $('#lock'), desktop = $('#desktop');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const phone = () => matchMedia('(max-width: 760px)').matches;
const params = new URLSearchParams(location.search);

/* ---------- clock ---------- */
const tick = () => {
  const d = new Date();
  $('#lock-date').textContent = d.toLocaleDateString('en-GB', {weekday: 'long', day: 'numeric', month: 'long'});
  $('#lock-time').textContent = d.toLocaleTimeString('en-GB', {hour: '2-digit', minute: '2-digit'});
  $('#bar-time').textContent = d.toLocaleDateString('en-GB', {weekday: 'short', day: 'numeric', month: 'short'}) + '  ' + d.toLocaleTimeString('en-GB', {hour: '2-digit', minute: '2-digit'});
};
tick(); setInterval(tick, 10000);

/* ---------- boot ---------- */
const ua = navigator.userAgent;
const os = /Android/.test(ua) ? 'Android' : /iPhone|iPad/.test(ua) ? 'iOS' : /Mac/.test(ua) ? 'macOS' : /Win/.test(ua) ? 'Windows' : /Linux/.test(ua) ? 'Linux' : 'a computer';
const br = /Edg\//.test(ua) ? 'Edge' : /Firefox\//.test(ua) ? 'Firefox' : /Chrome\//.test(ua) ? 'Chrome' : /Safari\//.test(ua) ? 'Safari' : 'a browser';
const lines = ['<b>DenisOS 17.0</b>  (build 2009 → 2026)', '', `Hello. Your browser says: <b>${os} · ${br}</b>`,
  'mounting /work ............ <i>ok</i>', 'mounting /journey ......... <i>ok</i>', 'connecting integrations ... <i>ok</i>',
  'starting event bus ........ <i>ok</i>', 'loading /life (arsenal, travel, food, gym) <i>ok</i>', '', 'ready.'];
let booted = false, bootTimer = 0;
const endBoot = () => {
  if (booted) return; booted = true; clearTimeout(bootTimer);
  boot.classList.add('gone'); setTimeout(() => boot.remove(), 500);
  removeEventListener('keydown', endBoot); boot.removeEventListener('click', endBoot);
};
const seen = (() => { try { return sessionStorage.getItem('dz-booted') } catch { return null } })();
if (reduced || seen || params.has('app')) { boot.remove(); booted = true; }
else {
  try { sessionStorage.setItem('dz-booted', '1') } catch {}
  addEventListener('keydown', endBoot); boot.addEventListener('click', endBoot);
  let i = 0; const log = $('#boot-log');
  const step = () => { if (booted) return; if (i < lines.length) { log.innerHTML += lines[i++] + '\n'; bootTimer = setTimeout(step, i < 3 ? 380 : 220); } else bootTimer = setTimeout(endBoot, 700); };
  step();
}

/* ---------- lock ---------- */
let unlocked = false;
const unlock = () => {
  if (unlocked) return; unlocked = true; endBoot();
  lock.classList.add('gone'); lock.setAttribute('aria-hidden', 'true'); lock.inert = true;
  desktop.inert = false; desktop.removeAttribute('aria-hidden'); desktop.focus({preventScroll: true});
};
desktop.inert = true; desktop.setAttribute('aria-hidden', 'true');
$('#unlock').addEventListener('click', unlock);
addEventListener('keydown', e => { if (!unlocked && booted && ['Enter', ' ', 'ArrowUp'].includes(e.key) && e.target === document.body) { e.preventDefault(); unlock(); } });
lock.addEventListener('wheel', e => { if (e.deltaY > 20) unlock(); }, {passive: true});
let y0 = null;
lock.addEventListener('pointerdown', e => { y0 = e.clientY; });
lock.addEventListener('pointerup', e => { if (y0 !== null && y0 - e.clientY > 60) unlock(); y0 = null; });
lock.addEventListener('touchstart', e => { y0 = e.touches[0].clientY; }, {passive: true});
lock.addEventListener('touchend', e => { if (y0 !== null && y0 - e.changedTouches[0].clientY > 60) unlock(); y0 = null; });
$('.skip-link').addEventListener('click', e => { e.preventDefault(); unlock(); });

/* ---------- windows ---------- */
let z = 100, opened = 0;
const setRunning = (app, on) => $$(`.app-icon[data-open="${app}"]`).forEach(b => b.classList.toggle('running', on));
const front = w => { $$('.window.front').forEach(x => x.classList.remove('front')); w.classList.add('front'); w.style.zIndex = ++z; };
const open = app => {
  const w = $('#win-' + app); if (!w) return;
  if (w.hidden) {
    w.hidden = false;
    if (!w.dataset.placed && !phone()) {
      const W = w.offsetWidth, H = w.offsetHeight, n = opened++ % 6;
      w.style.left = Math.max(12, Math.min(innerWidth - W - 12, innerWidth / 2 - W / 2 + (n - 2) * 34)) + 'px';
      w.style.top = Math.max(42, Math.min(innerHeight - H - 96, 70 + n * 26)) + 'px';
      w.dataset.placed = '1';
    }
    w.dataset.opener = document.activeElement?.dataset?.open ? app : '';
  }
  front(w); setRunning(app, true);
  (w.querySelector('#term-in') || w.querySelector('.light.close') || w).focus({preventScroll: true});
  if (phone()) document.body.style.overflow = 'hidden';
};
const close = (w, keepRunning) => {
  w.hidden = true; if (!keepRunning) setRunning(w.dataset.app, false);
  if (phone()) document.body.style.overflow = '';
  const icon = $(`.${phone() ? 'home-grid' : 'dock'} .app-icon[data-open="${w.dataset.app}"]`); icon && icon.focus({preventScroll: true});
};
$$('[data-open]').forEach(b => b.addEventListener('click', () => { if (!unlocked) unlock(); open(b.dataset.open); }));
$$('.window').forEach(w => {
  w.tabIndex = -1;
  w.addEventListener('pointerdown', () => front(w));
  $('.close', w).addEventListener('click', () => close(w));
  $('.min', w).addEventListener('click', () => close(w, true));
  $('.back', w).addEventListener('click', () => close(w));
  const bar = $('.titlebar', w); let drag = null;
  bar.addEventListener('pointerdown', e => {
    if (phone() || e.target.closest('button')) return;
    drag = {x: e.clientX - w.offsetLeft, y: e.clientY - w.offsetTop}; bar.setPointerCapture(e.pointerId);
  });
  bar.addEventListener('pointermove', e => {
    if (!drag) return;
    w.style.left = Math.max(-w.offsetWidth + 120, Math.min(innerWidth - 120, e.clientX - drag.x)) + 'px';
    w.style.top = Math.max(30, Math.min(innerHeight - 60, e.clientY - drag.y)) + 'px';
  });
  bar.addEventListener('pointerup', () => { drag = null; });
});
addEventListener('keydown', e => {
  if (e.key !== 'Escape' || !unlocked) return;
  const top = $$('.window:not([hidden])').sort((a, b) => (+b.style.zIndex || 0) - (+a.style.zIndex || 0))[0];
  if (top) close(top);
});

/* ---------- notes ---------- */
$$('.n-item').forEach(b => b.addEventListener('click', () => {
  $$('.n-item').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  $$('.n-body').forEach(x => { x.hidden = x.dataset.note !== b.dataset.note; });
  $('.n-view').scrollTop = 0;
}));

/* ---------- terminal ---------- */
const log = $('#term-log'), form = $('#term-form'), input = $('#term-in'), hist = []; let cur = 0;
const apps = {about: 'About', journey: 'Journey', work: 'Work', sim: 'Simulator', notes: 'Notes', duel: 'Word Duel', timer: 'Timer', mail: 'Mail'};
const C = {
  help: () => 'Commands:\n  whoami        a little about me\n  ls            list the apps\n  open <app>    open one (e.g. open work)\n  experience    17 years in one paragraph\n  stack         what I work with\n  next          what\'s next\n  arsenal | travel | gym | food\n  contact       say hello\n  clear         clear the screen',
  whoami: () => 'Denis Martins. Senior software engineer, 17 years in.\nI design integration platforms, own them in production and mentor the people who build them.',
  ls: () => Object.keys(apps).map(a => a.padEnd(10)).join('') ,
  experience: () => 'Twelve roles since 2009: reporting, products, lending and payments, clinical research,\nwealth management, telecoms and energy. Type "open journey" for the timeline.',
  stack: () => 'API design · integrations · event-driven systems · domain modelling\nAzure · AWS · Service Bus/SQS · Terraform · Docker · Datadog\nPHP/Laravel · Java · Go · TypeScript. Tools, not the headline.',
  next: () => 'Transact. Integrations in financial services.',
  arsenal: () => 'North London is red. COYG.', travel: () => 'Unfamiliar streets, good food, ideally a sunny coast.',
  gym: () => 'One more rep.', food: () => 'Have you eaten?', contact: () => 'hello@denis.zone, or "open mail".',
  sudo: () => 'Nice try.', exit: () => { setTimeout(() => close($('#win-terminal')), 250); return 'logout'; }
};
const print = (cmd, out) => {
  const p = document.createElement('div');
  p.innerHTML = '<span class="p">denis@os</span>:<span class="d">~</span>$ ';
  p.append(cmd); if (out) p.append('\n' + out); log.append(p);
  const body = log.closest('.wbody'); body.scrollTop = body.scrollHeight;
};
form.addEventListener('submit', e => {
  e.preventDefault(); const q = input.value.trim(); input.value = ''; if (!q) return;
  hist.push(q); cur = hist.length; const [k, arg] = q.toLowerCase().split(/\s+/);
  if (k === 'clear') { log.textContent = ''; return; }
  if (k === 'open') { const a = Object.keys(apps).find(x => x === arg || apps[x].toLowerCase() === arg); print(q, a ? 'opening ' + apps[a] + '…' : 'open: no such app. Try "ls".'); if (a) setTimeout(() => open(a), 200); return; }
  print(q, C[k] ? C[k]() : `zsh: command not found: ${k}. Try "help".`);
});
input.addEventListener('keydown', e => {
  if (e.key === 'ArrowUp' && hist.length) { e.preventDefault(); cur = Math.max(0, cur - 1); input.value = hist[cur]; }
  if (e.key === 'ArrowDown' && hist.length) { e.preventDefault(); cur = Math.min(hist.length, cur + 1); input.value = hist[cur] || ''; }
});
$('#win-terminal .wbody').addEventListener('click', () => input.focus());

/* ---------- deep link: ?app=work ---------- */
if (params.has('app')) { unlock(); open(params.get('app')); }
})();
