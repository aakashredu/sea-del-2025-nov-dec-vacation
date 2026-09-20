from pathlib import Path
import sys

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])

css = r'''
/* v4 photo treatment */
.hero.photoHero{min-height:292px;background-size:cover!important;background-position:center!important;box-shadow:0 24px 52px rgba(15,33,48,.28)!important}
.hero.photoHero:after{display:none}.hero.photoHero .heroTop{min-height:160px}.hero.photoHero .heroTop>div:first-child{align-self:flex-end;max-width:680px;text-shadow:0 2px 14px rgba(0,0,0,.38)}
.hero.photoHero .heroIcon{background:rgba(14,28,40,.30);border-color:rgba(255,255,255,.24)}
.dayCard.hasPhoto{min-height:160px;padding-top:73px;background-size:100% 94px!important;background-position:top center!important;background-repeat:no-repeat!important}
.dayCard.hasPhoto:after{display:none}.dayCard.hasPhoto .dayIcon{z-index:3;background:rgba(255,255,255,.88);backdrop-filter:blur(8px)}
.dayCard.hasPhoto .dayDate{position:relative;z-index:3;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.90);box-shadow:0 4px 12px rgba(20,35,48,.10);display:inline-block}
.featureBand{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;margin-top:14px}.featureTile{position:relative;overflow:hidden;min-height:122px;border-radius:22px;background-size:cover;background-position:center;border:1px solid rgba(255,255,255,.5);box-shadow:var(--shadow)}
.featureTile:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 28%,rgba(11,27,40,.82) 100%)}.featureTile span{position:absolute;left:14px;right:14px;bottom:12px;z-index:1;color:#fff;font-size:12px;font-weight:850;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.parkThumb{width:62px;height:62px;flex:0 0 62px;border-radius:17px;background-size:cover;background-position:center;box-shadow:0 8px 18px rgba(27,48,65,.12);border:1px solid rgba(255,255,255,.72)}
@media(max-width:430px){.hero.photoHero{min-height:280px}.hero.photoHero .heroTop{min-height:150px}.featureBand{grid-template-columns:1fr 1fr}.featureTile{min-height:108px}}
'''
src = src.replace('</style>', css + '\n</style>', 1)

js = r'''<script>
(function(){
var photos={
'Arrival':'https://images.squarespace-cdn.com/content/v1/6057e99eb4e03d64f1f9153d/0bffdfa3-0013-4019-a291-ddf74f902d9e/Art-of-Animation-Resort-Walt-Disney-World-1-1024x624.jpg?format=1000w',
'Animal Kingdom':'https://uploads.grupodicas.com/2024/04/parque-animal-kingdom-disney-orlando.jpg',
'Hollywood Studios':'https://images.squarespace-cdn.com/content/v1/65aacd0e6c445a6a3808299a/f3059134-6bfa-425e-a238-0e3c9fcf4909/Hollywood-Studios-Entrance',
'Magic Kingdom':'https://pimg.mk.co.kr/news/cms/202310/27/news-p.v1.20231027.a49dd9d67c274caa8d1cbce903ea2f58.png',
'EPCOT':'https://allears.net/wp-content/uploads/2023/05/2023-wdw-epcot-park-entrance-spaceship-earth-atmos.jpg',
'Water Park + Flight':'https://images.squarespace-cdn.com/content/v1/62d1fe4bab8d965a2eae197f/1668008469473-XV6HBIASNFZNTVT3IS08/blizzard-entrance.jpg'
};
function photoFor(name){return photos[name]||photos['Magic Kingdom'];}
var busy=false;
function enhance(){
 if(busy)return; busy=true;
 requestAnimationFrame(function(){
  try{
   document.querySelectorAll('.dayCard').forEach(function(card){
    var n=card.querySelector('strong'); if(!n)return;
    var u=photoFor(n.textContent.trim()); card.classList.add('hasPhoto');
    card.style.backgroundImage='linear-gradient(180deg,rgba(255,255,255,.02) 0%,rgba(255,255,255,.95) 60%,#fff 100%),url("'+u+'")';
   });
   var hero=document.querySelector('.hero');
   if(hero){
    var title=(document.querySelector('#pageTitle')||{}).textContent||'';
    if(title==='Trip Overview'){
      var a=document.querySelector('.dayCard.active strong'); if(a) title=a.textContent.trim();
    }
    if(photos[title]){
      hero.classList.add('photoHero');
      hero.style.backgroundImage='linear-gradient(90deg,rgba(8,24,38,.92) 0%,rgba(8,24,38,.74) 50%,rgba(8,24,38,.26) 100%),linear-gradient(180deg,rgba(8,24,38,.05),rgba(8,24,38,.76)),url("'+photos[title]+'")';
    }
   }
   if((document.querySelector('#pageTitle')||{}).textContent==='Trip Overview' && !document.querySelector('.featureBand')){
    var h=document.querySelector('.hero');
    if(h){
      var band=document.createElement('div'); band.className='featureBand';
      band.innerHTML='<div class="featureTile" style="background-image:url(&quot;'+photos['Magic Kingdom']+'&quot;)"><span>Magic Kingdom - Sep 21</span></div><div class="featureTile" style="background-image:url(&quot;'+photos['EPCOT']+'&quot;)"><span>EPCOT - Sep 22</span></div>';
      h.insertAdjacentElement('afterend',band);
    }
   }
   if((document.querySelector('#pageTitle')||{}).textContent==='All Days'){
    document.querySelectorAll('.listItem').forEach(function(row){
      if(row.querySelector('.parkThumb'))return;
      var strong=row.querySelector('strong'); if(!strong)return;
      var txt=strong.textContent; var key=Object.keys(photos).find(function(k){return txt.indexOf(k)>=0;}); if(!key)return;
      var t=document.createElement('span'); t.className='parkThumb'; t.style.backgroundImage='url("'+photos[key]+'")';
      var first=row.firstElementChild; if(first && first.tagName==='SPAN') first.replaceWith(t); else row.prepend(t);
    });
   }
  }finally{busy=false;}
 });
}
var app=document.querySelector('#app'); if(app)new MutationObserver(enhance).observe(app,{childList:true,subtree:true});
enhance();
})();
</script>'''
src = src.replace('</body>', js + '\n</body>', 1)
src = src.replace('<title>DisneyWorld 2026</title>', '<title>DisneyWorld 2026</title>\n  <meta name="app-version" content="v4-photo" />', 1)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src)
print('Prepared v4 runtime build:', len(src))
