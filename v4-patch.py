from pathlib import Path
import sys

src_path = Path(sys.argv[1] if len(sys.argv) > 1 else "disneyworld-v3.html")
out_path = Path(sys.argv[2] if len(sys.argv) > 2 else "site/index.html")
src = src_path.read_text()

css_add = r'''
/* v4 photo treatment */
.hero.photoHero{min-height:300px;padding:24px 23px 22px;background-image:
linear-gradient(90deg,rgba(8,24,38,.92) 0%,rgba(8,24,38,.76) 48%,rgba(8,24,38,.26) 100%),
linear-gradient(180deg,rgba(8,24,38,.08),rgba(8,24,38,.78)),var(--heroPhoto);background-size:cover;background-position:center;box-shadow:0 24px 52px rgba(15,33,48,.28)}
.hero.photoHero:before{background:linear-gradient(180deg,rgba(255,255,255,.08),transparent 28%,rgba(5,18,30,.16));opacity:1}
.hero.photoHero:after{display:none}.hero.photoHero .heroTop{min-height:168px}.hero.photoHero .heroTop>div:first-child{align-self:flex-end;max-width:680px;text-shadow:0 2px 14px rgba(0,0,0,.35)}
.hero.photoHero .heroIcon{background:rgba(14,28,40,.28);border-color:rgba(255,255,255,.24)}
.hero.photoHero .heroArt{height:1px;background:rgba(255,255,255,.28);opacity:1}
.photoCredit{margin-top:9px;font-size:9px;color:rgba(255,255,255,.62);letter-spacing:.02em}
.dayCard.hasPhoto{min-height:160px;padding-top:72px;background-image:linear-gradient(180deg,rgba(255,255,255,.02) 0%,rgba(255,255,255,.94) 56%,#fff 100%),var(--dayPhoto);background-size:100% 92px,100% 92px;background-position:top center;background-repeat:no-repeat}
.dayCard.hasPhoto:after{display:none}.dayCard.hasPhoto:before{z-index:2}.dayCard.hasPhoto .dayIcon{z-index:3;background:rgba(255,255,255,.88);backdrop-filter:blur(8px)}
.dayCard.hasPhoto .dayDate{position:relative;z-index:3;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.88);box-shadow:0 4px 12px rgba(20,35,48,.10);display:inline-block}
.parkThumb{width:62px;height:62px;flex:0 0 62px;border-radius:17px;background-size:cover;background-position:center;box-shadow:0 8px 18px rgba(27,48,65,.12);border:1px solid rgba(255,255,255,.72)}
.featureBand{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;margin-top:14px}.featureTile{position:relative;overflow:hidden;min-height:126px;border-radius:22px;background-size:cover;background-position:center;border:1px solid rgba(255,255,255,.5);box-shadow:var(--shadow)}
.featureTile:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 28%,rgba(11,27,40,.82) 100%)}.featureTile span{position:absolute;left:14px;right:14px;bottom:12px;z-index:1;color:#fff;font-size:12px;font-weight:850;text-shadow:0 2px 8px rgba(0,0,0,.4)}
@media(max-width:430px){.hero.photoHero{min-height:282px}.hero.photoHero .heroTop{min-height:154px}.featureBand{grid-template-columns:1fr 1fr}.featureTile{min-height:112px}}
'''
src = src.replace('</style>', css_add + '\n</style>', 1)

photos = """const parkPhotos={
arrival:'https://images.squarespace-cdn.com/content/v1/6057e99eb4e03d64f1f9153d/0bffdfa3-0013-4019-a291-ddf74f902d9e/Art-of-Animation-Resort-Walt-Disney-World-1-1024x624.jpg?format=1000w',
animal:'https://uploads.grupodicas.com/2024/04/parque-animal-kingdom-disney-orlando.jpg',
studios:'https://images.squarespace-cdn.com/content/v1/65aacd0e6c445a6a3808299a/f3059134-6bfa-425e-a238-0e3c9fcf4909/Hollywood-Studios-Entrance',
magic:'https://pimg.mk.co.kr/news/cms/202310/27/news-p.v1.20231027.a49dd9d67c274caa8d1cbce903ea2f58.png',
epcot:'https://allears.net/wp-content/uploads/2023/05/2023-wdw-epcot-park-entrance-spaceship-earth-atmos.jpg',
water:'https://images.squarespace-cdn.com/content/v1/62d1fe4bab8d965a2eae197f/1668008469473-XV6HBIASNFZNTVT3IS08/blizzard-entrance.jpg'
};
const photoCredit={arrival:'Art of Animation',animal:'Tree of Life',studios:'Hollywood Studios',magic:'Cinderella Castle',epcot:'Spaceship Earth',water:'Blizzard Beach'};
"""
src = src.replace("const parkTheme={", photos + "const parkTheme={", 1)

old = """function dayStrip(){return \`<div class="dayStrip">\${DAYS.map(d=>{const t=parkTheme[d.type];return \`<button class="dayCard \${d.date===state.day?'active':''}" data-day="\${d.date}" style="--dayAccent:\${t.accent};--dayGlow:\${t.glow}"><span class="dayDate">\${fmtDate(d.date)}</span><span class="dayIcon">\${icon(t.icon)}</span><strong>\${d.name}</strong><small>\${d.subtitle}</small></button>\`}).join('')}</div>\`}"""
new = """function dayStrip(){return \`<div class="dayStrip">\${DAYS.map(d=>{const t=parkTheme[d.type],ph=parkPhotos[d.type];return \`<button class="dayCard hasPhoto \${d.date===state.day?'active':''}" data-day="\${d.date}" style="--dayAccent:\${t.accent};--dayGlow:\${t.glow};--dayPhoto:url('\${ph}')"><span class="dayDate">\${fmtDate(d.date)}</span><span class="dayIcon">\${icon(t.icon)}</span><strong>\${d.name}</strong><small>\${d.subtitle}</small></button>\`}).join('')}</div>\`}"""
assert old in src
src = src.replace(old, new, 1)

old = """function hero(d,overview=false){const t=parkTheme[d.type],p=progress(d);return \`<section class="hero" style="--park:\${t.accent};--heroGlow:\${t.glow}"><div class="heroTop"><div><div class="eyebrow">\${overview?'Aakash · Preeti · Vihaan':fmtDate(d.date)+' · '+d.hours}</div><h2>\${overview?'Your Disney trip, ready to go.':d.name}</h2><p>\${overview?'Your booked Lightning Lanes are locked in. Everything else is arranged around location, major attractions and Vihaan’s 92 cm height.':d.subtitle}</p></div><div class="heroIcon">\${icon(t.icon)}</div></div><div class="chips"><span class="chip blue">\${d.ll.length?d.ll.length+' booked LL':'No booked LL'}</span><span class="chip good">\${p.done}/\${p.total} complete</span>\${syncBadge()}</div>\${nowCard(d)}<div class="heroArt"></div></section>\`}"""
new = """function hero(d,overview=false){const t=parkTheme[d.type],p=progress(d),ph=parkPhotos[d.type];return \`<section class="hero photoHero" style="--park:\${t.accent};--heroGlow:\${t.glow};--heroPhoto:url('\${ph}')"><div class="heroTop"><div><div class="eyebrow">\${overview?'Aakash · Preeti · Vihaan':fmtDate(d.date)+' · '+d.hours}</div><h2>\${overview?'Your Disney trip, ready to go.':d.name}</h2><p>\${overview?'Your booked Lightning Lanes are locked in. Everything else is arranged around location, major attractions and Vihaan’s 92 cm height.':d.subtitle}</p></div><div class="heroIcon">\${icon(t.icon)}</div></div><div class="chips"><span class="chip blue">\${d.ll.length?d.ll.length+' booked LL':'No booked LL'}</span><span class="chip good">\${p.done}/\${p.total} complete</span>\${syncBadge()}</div>\${nowCard(d)}<div class="photoCredit">\${photoCredit[d.type]}</div></section>\`}"""
assert old in src
src = src.replace(old, new, 1)

old = """function home(){const d=DAYS.find(x=>x.date===today())||day();pageTitle.textContent='Trip Overview';app.innerHTML=\`\${hero(d,true)}<section class="section"><div class="sectionHead"><h3>Six-day plan</h3><span>Tap any day</span></div>\${dayStrip()}</section>"""
new = """function home(){const d=DAYS.find(x=>x.date===today())||day();pageTitle.textContent='Trip Overview';app.innerHTML=\`\${hero(d,true)}<div class="featureBand"><div class="featureTile" style="background-image:url('\${parkPhotos.magic}')"><span>Magic Kingdom · Sep 21</span></div><div class="featureTile" style="background-image:url('\${parkPhotos.epcot}')"><span>EPCOT · Sep 22</span></div></div><section class="section"><div class="sectionHead"><h3>Six-day plan</h3><span>Tap any day</span></div>\${dayStrip()}</section>"""
assert old in src
src = src.replace(old, new, 1)

old = """function daysView(){pageTitle.textContent='All Days';app.innerHTML=\`<section class="section">\${dayStrip()}</section><section class="section"><div class="list">\${DAYS.map(d=>{const t=parkTheme[d.type],p=progress(d);return \`<button class="listItem" data-day="\${d.date}" style="width:100%;text-align:left;color:inherit"><span style="color:\${t.accent}">\${icon(t.icon)}</span><div><strong>\${fmtDate(d.date)} · \${d.name}</strong><p>\${d.subtitle} · \${p.done}/\${p.total} complete</p></div></button>\`}).join('')}</div></section>\`;bind()}"""
new = """function daysView(){pageTitle.textContent='All Days';app.innerHTML=\`<section class="section">\${dayStrip()}</section><section class="section"><div class="list">\${DAYS.map(d=>{const t=parkTheme[d.type],p=progress(d);return \`<button class="listItem" data-day="\${d.date}" style="width:100%;text-align:left;color:inherit"><span class="parkThumb" style="background-image:url('\${parkPhotos[d.type]}')"></span><div><strong>\${fmtDate(d.date)} · \${d.name}</strong><p>\${d.subtitle} · \${p.done}/\${p.total} complete</p></div></button>\`}).join('')}</div></section>\`;bind()}"""
assert old in src
src = src.replace(old, new, 1)

src = src.replace('<title>DisneyWorld 2026</title>', '<title>DisneyWorld 2026</title>\\n  <meta name="app-version" content="v4-photo" />', 1)
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(src)
print(f"Prepared v4: {len(src)} bytes")
