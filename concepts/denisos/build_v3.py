"""Build the DenisOS concept site from denis.zone content.

Reads parts extracted from ~/denis-build (roles, notes, games, simulation,
case studies) and writes a self-contained static site to OUT.
"""
import json, os, shutil, html

HOME = os.path.expanduser('~')
T = f'{HOME}/.cache/denis-site-tools/denisos/'
REPO = f'{HOME}/denis-build'
OUT = f'{T}site'

P = json.load(open(T + 'v3parts.json'))
P['simjs'] = P['simjs'].replace('b.className="badge "+st.k;', 'b.className="badge "+(st.k==="note"?"step":st.k);').replace('.dot{', '.sdot{').replace('d.className="dot "', 'd.className="sdot "')
ROLES = json.load(open(T + 'roles.json'))

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/assets/photos')
shutil.copytree(f'{REPO}/assets/fonts/story', OUT + '/assets/fonts/story')
for f in ['arsenal-dressing-room-480', 'volcanic-rocks-480', 'restaurant-table-480', 'gym-training-480',
          'volcanic-rocks-800', 'street-portrait-800', 'street-portrait-480']:
    shutil.copy(f'{REPO}/assets/photos/{f}.webp', OUT + '/assets/photos/')
for f in ['favicon.svg', 'favicon-32.png', 'apple-touch-icon.png']:
    shutil.copy(f'{REPO}/{f}', OUT + '/')

CHAPTERS = [(0, 1, 'The foundations', '2009–2013'), (2, 6, 'Building products', '2013–2019'),
            (7, 10, 'Engineering at scale', '2019–2024'), (11, 11, 'Designing systems', '2024–2026')]
journey = ''
for a, b, name, yrs in CHAPTERS:
    journey += f'<section class="j-chapter"><h3><span>{yrs}</span>{name}</h3><ol>'
    for r in ROLES[a:b + 1]:
        journey += (f'<li><div class="j-when">{html.escape(r["period"])}</div><div><strong>{html.escape(r["company"])}</strong>'
                    f'<span class="j-role">{html.escape(r["role"])}</span><p>{html.escape(r["story"])}</p></div></li>')
    journey += '</ol></section>'
journey += ('<section class="j-chapter j-next"><h3><span>2026 →</span>Up next</h3><ol><li><div class="j-when">Nov 2026</div>'
            '<div><strong>Transact</strong><span class="j-role">Integrations · Financial services</span>'
            '<p>New domain, same instincts.</p></div></li></ol></section>')

notes_list = ''.join(
    f'<button type="button" class="n-item" data-note="{i}" aria-pressed="{"true" if i == 0 else "false"}"><strong>{n["title"]}</strong><span>{n["date"]}</span></button>'
    for i, n in enumerate(P['notes']))
notes_bodies = ''.join(
    f'<article class="n-body" data-note="{i}"{"" if i == 0 else " hidden"}><p class="n-date">{n["date"]}</p><h2>{n["title"]}</h2><p class="n-sub">{n["sub"]}</p>{n["body"]}</article>'
    for i, n in enumerate(P['notes']))

APPS = [  # id, label, icon colour, glyph
    ('about', 'About', '#f36e45', '☺'), ('journey', 'Journey', '#3d7be0', '▤'), ('work', 'Work', '#202b30', '◆'),
    ('terminal', 'Terminal', '#111', '>_'), ('sim', 'Simulator', '#6b4bd8', '⇄'), ('notes', 'Notes', '#f2c94c', '✎'),
    ('duel', 'Word Duel', '#1f6f58', 'A→B'), ('timer', 'Timer', '#c8102e', '5.00'), ('mail', 'Mail', '#2f80ed', '✉'),
]
ICONS = {
 'about': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
 'journey': '<path d="M4 6h16M4 12h10M4 18h13"/><circle cx="19" cy="12" r="1.6"/>',
 'work': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
 'terminal': '<path d="m5 8 4 4-4 4M12 17h7"/>',
 'sim': '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10M6 8l5 8.3M18 8l-5 8.3"/>',
 'notes': '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h5"/>',
 'duel': '<rect x="3" y="7" width="7" height="10" rx="1.5"/><rect x="14" y="7" width="7" height="10" rx="1.5"/><path d="M10 12h4"/>',
 'timer': '<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4l2.5 2M10 2h4"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
}
dock = ''.join(
    f'<button type="button" class="app-icon" data-open="{a}" aria-label="Open {l}"><span class="glyph" style="background:{c}"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[a]}</svg></span><span class="app-label">{l}</span><i class="run-dot" aria-hidden="true"></i></button>'
    for a, l, c, g in APPS)


def win(app, title, body, w=760, h=560, cls=''):
    return (f'<section class="window {cls}" id="win-{app}" data-app="{app}" role="dialog" aria-label="{title}" hidden style="--w:{w}px;--h:{h}px">'
            f'<header class="titlebar"><div class="lights"><button type="button" class="light close" aria-label="Close {title}"></button>'
            f'<button type="button" class="light min" aria-label="Minimise {title}"></button><span class="light zoom" aria-hidden="true"></span></div>'
            f'<span class="wtitle">{title}</span><button type="button" class="back" aria-label="Back to home screen">‹ Home</button></header>'
            f'<div class="wbody">{body}</div></section>')


about = ('<div class="about"><div class="about-head"><img src="/assets/photos/street-portrait-480.webp" alt="Denis on a sunny street" width="480" height="640">'
         '<div><p class="kicker">ABOUT THIS COMPUTER</p><h2>Denis Martins</h2><dl class="spec">'
         '<dt>Model</dt><dd>Senior software engineer</dd><dt>Build</dt><dd>2009 → 17 years</dd>'
         '<dt>Specialty</dt><dd>Integrations · APIs · event-driven systems</dd><dt>Next</dt><dd>Transact, financial services</dd>'
         '<dt>Runs on</dt><dd>Arsenal, travel, good food, one more rep</dd></dl></div></div>'
         '<p class="lead">I build software for a living, but I\'d rather not spend every conversation talking about it.</p>'
         '<div class="tiles">'
         '<figure><img src="/assets/photos/arsenal-dressing-room-480.webp" alt="Denis in the Arsenal dressing room" loading="lazy" width="480" height="640"><figcaption><b>North London is red.</b> A long-term relationship with no refunds.</figcaption></figure>'
         '<figure><img src="/assets/photos/volcanic-rocks-480.webp" alt="Denis on volcanic rocks in Tenerife" loading="lazy" width="480" height="640"><figcaption><b>I\'d rather go somewhere.</b> Back to Tenerife more than once.</figcaption></figure>'
         '<figure><img src="/assets/photos/restaurant-table-480.webp" alt="Steak and vegetables at a restaurant" loading="lazy" width="480" height="853"><figcaption><b>Have you eaten?</b> Sometimes the best memory is lunch.</figcaption></figure>'
         '<figure><img src="/assets/photos/gym-training-480.webp" alt="Denis taking a mirror photo at the gym" loading="lazy" width="480" height="945"><figcaption><b>One more rep.</b> Some problems can\'t be solved by restarting the server.</figcaption></figure>'
         '</div></div>')

work = ('<div class="work"><p class="kicker">SELECTED WORK</p><h2>Three problems worth solving.</h2>'
        '<p class="muted">Kept generic on purpose: the problem, the decision, the trade-off and what changed.</p>'
        + ''.join(P['cases']) + '<h2 class="mt">The kind of platform I build</h2>' + P['diagram']
        + '<h2 class="mt">Five things I hold to</h2>' + P['principles'] + '</div>')

terminal = ('<div class="term" id="term"><div class="term-log" id="term-log">'
            '<span class="p">denis@os</span>:<span class="d">~</span>$ whoami\nDenis Martins. Senior software engineer, 17 years in.\n'
            'Type <b>help</b> to see what you can ask.\n</div>'
            '<form id="term-form" autocomplete="off"><label for="term-in"><span class="p">denis@os</span>:<span class="d">~</span>$</label>'
            '<input id="term-in" spellcheck="false" autocapitalize="off" aria-label="Terminal command"></form></div>')

sim = ('<div class="simwrap"><p class="muted">An order moving through a system built the way I\'d build one: bounded contexts, an aggregate, '
       'an event store, a payment saga and a separate read model. Break something, then place the order.</p>'
       '<button class="run" id="run-demo" type="button">PLACE AN ORDER ↗</button>' + P['sim'] + '</div>')

notes = f'<div class="notesapp"><nav class="n-list" aria-label="Notes">{notes_list}</nav><div class="n-view">{notes_bodies}</div></div>'

duel = ('<div class="gamewrap"><p class="muted">Change one letter at a time to make a new word. Every valid word resets the 60-second clock.</p>'
        + P['word'] + '<a class="ext" href="https://duel.denis.zone/" target="_blank" rel="noopener">Play the full game: duel.denis.zone ↗</a></div>')
timer = ('<div class="gamewrap"><p class="muted">Start the timer and stop it at exactly 5.00 seconds.</p>' + P['timer']
         + '<a class="ext" href="https://play.denis.zone/" target="_blank" rel="noopener">Play Last One Standing: play.denis.zone ↗</a></div>')

mail = ('<div class="mail"><div class="m-head"><span>To:</span> hello@denis.zone</div><div class="m-head"><span>Subject:</span> Hello</div>'
        '<p>The best conversations usually start with a good question. If you\'ve got one, I\'d love to hear it.</p>'
        '<div class="m-actions"><a class="btn" href="mailto:hello@denis.zone">Send an email ↗</a>'
        '<a class="btn ghost" href="https://www.linkedin.com/in/martinsdenis/" target="_blank" rel="noopener">LinkedIn ↗</a>'
        '<a class="btn ghost" href="https://github.com/bornonthe12th" target="_blank" rel="noopener">GitHub ↗</a></div></div>')

windows = (win('about', 'About Denis', about, 720, 620) + win('journey', 'Journey — 12 roles since 2009', f'<div class="journey">{journey}</div>', 640, 600)
           + win('work', 'Work', work, 900, 640) + win('terminal', 'denis@os — zsh', terminal, 640, 400, 'dark')
           + win('sim', 'Simulator — POST /orders', sim, 760, 640, 'dark') + win('notes', 'Notes', notes, 820, 560)
           + win('duel', 'Word Duel', duel, 560, 640) + win('timer', 'Timer', timer, 460, 360) + win('mail', 'New message', mail, 520, 360))

CSS = open(os.path.join(os.path.dirname(__file__), 'v3.css')).read()
JS = open(os.path.join(os.path.dirname(__file__), 'v3.js')).read()
PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>DenisOS — Denis Martins</title><meta name="description" content="Denis Martins, senior software engineer, as an operating system. Unlock it and open the apps.">
<meta name="robots" content="noindex"><meta name="theme-color" content="#0b0f14">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/story/DMSans-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}{P['css']}</style></head><body>
<a class="skip-link" href="#desktop">Skip the intro</a>
<div class="boot" id="boot" aria-hidden="true"><pre id="boot-log"></pre><p class="boot-hint">Click or press any key to skip</p></div>
<div class="lock" id="lock" role="region" aria-label="Lock screen">
  <div class="lock-bg" aria-hidden="true"></div>
  <div class="lock-clock"><p id="lock-date"></p><p id="lock-time" class="big"></p></div>
  <div class="lock-notes">
    <div class="notif"><span class="n-icon" style="background:#202b30">dz</span><div><b>denis.zone</b><span class="n-now">now</span><p>New chapter: Transact. Integrations in financial services.</p></div></div>
    <div class="notif"><span class="n-icon" style="background:#c8102e">5.00</span><div><b>Last One Standing</b><span class="n-now">2m ago</span><p>Can you feel five seconds?</p></div></div>
  </div>
  <button type="button" class="unlock" id="unlock"><span class="chev" aria-hidden="true">⌃</span>Click or swipe up to unlock</button>
</div>
<main class="desktop" id="desktop" tabindex="-1" aria-label="DenisOS desktop">
  <header class="menubar"><span class="logo">dz</span><b>DenisOS</b>
    <nav class="menus" aria-label="Apps"><button type="button" data-open="about">About</button><button type="button" data-open="work">Work</button>
    <button type="button" data-open="journey">Journey</button><button type="button" data-open="notes">Notes</button><button type="button" data-open="mail">Contact</button></nav>
    <span class="status"><a href="https://denis.zone/" class="real">denis.zone ↗</a><span id="bar-time"></span></span></header>
  <div class="desk-hello"><p class="kicker">DENIS MARTINS<br>SENIOR SOFTWARE ENGINEER</p><h1>I make things<br>work together.</h1>
    <p>Integrations, APIs and event-driven systems. 17 years in, next stop Transact. Open an app to look around.</p></div>
  <div class="home-grid" aria-label="Apps">{dock}</div>
  {windows}
  <nav class="dock" aria-label="Dock">{dock}</nav>
</main>
<script>{JS}</script>
<script>(()=>{{{P['gamesjs']}}})();</script>
<script>(()=>{{{P['simjs']}}})();</script>
</body></html>'''
open(OUT + '/index.html', 'w').write(PAGE)
open(OUT + '/robots.txt', 'w').write('User-agent: *\nDisallow: /\n')
print('wrote', OUT, len(PAGE) // 1024, 'KB')
