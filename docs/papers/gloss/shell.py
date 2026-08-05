CSS = r"""
:root{
  --paper:#F7F8F9; --paper-raised:#FFFFFF; --paper-sunk:#EDF1F3;
  --ink:#12171C; --slate:#5A6672; --mist:#DDE3E6;
  --verdigris:#1F7A6B; --verdigris-soft:#E2F0ED;
  --amber:#A8621B; --amber-soft:#F6ECDF;
  --shadow:rgba(18,23,28,.14); --backdrop:rgba(18,23,28,.42);
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --col:min(740px,92vw); --col-wide:min(880px,94vw);
  --s1:.25rem; --s2:.5rem; --s3:.75rem; --s4:1rem; --s5:1.5rem; --s6:2rem; --s7:3rem; --s8:4.5rem;
  --r:6px;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#12171C; --paper-raised:#1A2128; --paper-sunk:#0D1216;
    --ink:#DCE3E7; --slate:#94A2AD; --mist:#2B343C;
    --verdigris:#4FB3A0; --verdigris-soft:#17302C;
    --amber:#D99B5C; --amber-soft:#33251A;
    --shadow:rgba(0,0,0,.55); --backdrop:rgba(0,0,0,.62);
  }
}
:root[data-theme="dark"]{
  --paper:#12171C; --paper-raised:#1A2128; --paper-sunk:#0D1216;
  --ink:#DCE3E7; --slate:#94A2AD; --mist:#2B343C;
  --verdigris:#4FB3A0; --verdigris-soft:#17302C;
  --amber:#D99B5C; --amber-soft:#33251A;
  --shadow:rgba(0,0,0,.55); --backdrop:rgba(0,0,0,.62);
}
:root[data-theme="light"]{
  --paper:#F7F8F9; --paper-raised:#FFFFFF; --paper-sunk:#EDF1F3;
  --ink:#12171C; --slate:#5A6672; --mist:#DDE3E6;
  --verdigris:#1F7A6B; --verdigris-soft:#E2F0ED;
  --amber:#A8621B; --amber-soft:#F6ECDF;
  --shadow:rgba(18,23,28,.14); --backdrop:rgba(18,23,28,.42);
}

*{box-sizing:border-box;}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--serif); font-size:1.0625rem; line-height:1.66;
  -webkit-text-size-adjust:100%; overflow-x:hidden;
}
main{
  width:var(--col); margin:0 auto; padding:var(--s7) 0 var(--s8);
  display:flex; flex-direction:column; gap:var(--s5);
}
p{margin:0; text-wrap:pretty;}
a{color:var(--verdigris); text-underline-offset:2px;}
:focus-visible{outline:2px solid var(--verdigris); outline-offset:2px; border-radius:2px;}

/* ---- document header --------------------------------------------------- */
.doc-header{display:flex; flex-direction:column; gap:var(--s3); padding-bottom:var(--s5);
  border-bottom:1px solid var(--mist);}
.eyebrow{font-family:var(--mono); font-size:.6875rem; letter-spacing:.13em;
  text-transform:uppercase; color:var(--verdigris); margin:0;}
h1{font-family:var(--serif); font-size:clamp(1.7rem,4.2vw,2.4rem); line-height:1.2;
  font-weight:600; margin:0; text-wrap:balance; letter-spacing:-.011em;}
.doc-subtitle{font-size:1.0625rem; color:var(--slate); line-height:1.5;}
.doc-lineage{font-family:var(--mono); font-size:.75rem; color:var(--slate); line-height:1.6;}
.doc-meta{display:grid; grid-template-columns:auto 1fr; gap:var(--s1) var(--s4);
  margin:var(--s2) 0 0; font-size:.8125rem;}
.doc-meta dt{font-family:var(--mono); font-size:.6875rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--slate); padding-top:.28em;}
.doc-meta dd{margin:0; color:var(--ink);}
.doc-note{font-size:.875rem; line-height:1.6; color:var(--slate);
  background:var(--paper-sunk); border-radius:var(--r); padding:var(--s4);
  border-left:2px solid var(--verdigris);}

/* ---- headings ---------------------------------------------------------- */
h2,h3{font-family:var(--serif); font-weight:600; margin:var(--s6) 0 0;
  text-wrap:balance; line-height:1.28; letter-spacing:-.008em;}
h2{font-size:1.5rem; padding-bottom:var(--s2); border-bottom:2px solid var(--verdigris);}
h3{font-size:1.1875rem; color:var(--ink);}
h2:first-of-type{margin-top:var(--s4);}
.sec-num{font-family:var(--mono); font-size:.72em; font-weight:400; color:var(--verdigris);
  letter-spacing:.04em; vertical-align:.12em; margin-right:.15em;}

/* ---- prose ------------------------------------------------------------- */
ul,ol{margin:0; padding-left:1.3rem; display:flex; flex-direction:column; gap:var(--s3);}
li{padding-left:.15rem;}
li::marker{color:var(--verdigris); font-family:var(--mono); font-size:.85em;}
strong{font-weight:600;}
code{font-family:var(--mono); font-size:.86em; background:var(--paper-sunk);
  padding:.1em .34em; border-radius:3px; border:1px solid var(--mist);
  word-break:break-word;}
blockquote{margin:0; padding:var(--s4) var(--s5); background:var(--paper-raised);
  border:1px solid var(--mist); border-left:3px solid var(--slate); border-radius:var(--r);}
blockquote.template-quote{border-left-color:var(--verdigris); background:var(--verdigris-soft);}
blockquote p{font-size:.9688rem; line-height:1.6;}
.plain-words{font-size:.9375rem; line-height:1.6; color:var(--slate); font-style:italic;
  border-left:2px solid var(--amber); padding:var(--s2) 0 var(--s2) var(--s4);
  background:linear-gradient(90deg,var(--amber-soft),transparent 70%); border-radius:0 var(--r) var(--r) 0;}
.plain-words em{font-style:normal; font-family:var(--mono); font-size:.78rem;
  letter-spacing:.07em; text-transform:uppercase; color:var(--amber); margin-right:.35em;}

/* ---- wide content ------------------------------------------------------ */
.scroll-x{overflow-x:auto; width:var(--col-wide); margin-left:calc((var(--col) - var(--col-wide))/2);
  max-width:100vw; -webkit-overflow-scrolling:touch;}
table{border-collapse:collapse; width:100%; font-size:.875rem; font-family:var(--mono);
  font-variant-numeric:tabular-nums;}
th,td{text-align:left; padding:var(--s2) var(--s3); border-bottom:1px solid var(--mist);
  vertical-align:top; line-height:1.45;}
thead th{font-size:.6875rem; letter-spacing:.07em; text-transform:uppercase;
  color:var(--verdigris); border-bottom:2px solid var(--verdigris); white-space:nowrap;}
tbody tr:last-child td{border-bottom:none;}
tbody tr:hover{background:var(--paper-sunk);}
td code,th code{background:none; border:none; padding:0;}
pre.code{margin:0; padding:var(--s4); background:var(--paper-sunk); border:1px solid var(--mist);
  border-radius:var(--r); font-family:var(--mono); font-size:.8125rem; line-height:1.65;
  overflow-x:auto;}
pre.code code{background:none; border:none; padding:0;}

/* ---- math (Tier 1) ----------------------------------------------------- */
.math{white-space:nowrap; font-family:var(--serif);}
.math.math-flow{white-space:normal;}   /* multi-term expression: break at operators, never mid-symbol */
.math i{font-style:italic;}
sub,sup{font-size:.75em; line-height:0; position:relative;}
sub{bottom:-.25em;} sup{top:-.5em;}
math{font-size:1.05em; color:inherit;}

/* ---- figures ----------------------------------------------------------- */
.paper-figure{margin:0; width:var(--col-wide); margin-left:calc((var(--col) - var(--col-wide))/2);
  max-width:100vw; display:flex; flex-direction:column; gap:var(--s3);}
.paper-figure img{width:100%; height:auto; display:block; border:1px solid var(--mist);
  border-radius:var(--r); background:var(--paper-raised); cursor:zoom-in;}
.paper-figure figcaption{font-size:.8125rem; line-height:1.6; color:var(--slate);}
/* Theme-paired figures. Every selector is scoped to .paper-figure so it
   out-specifies `.paper-figure img{display:block}` (0,1,1); an unscoped
   `.fig-dark{display:none}` (0,1,0) loses to it and shows both images. */
.paper-figure .fig-dark{display:none;}
@media (prefers-color-scheme:dark){
  .paper-figure .fig-light{display:none;}
  .paper-figure .fig-dark{display:block;}
}
:root[data-theme="dark"] .paper-figure .fig-light{display:none;}
:root[data-theme="dark"] .paper-figure .fig-dark{display:block;}
:root[data-theme="light"] .paper-figure .fig-light{display:block;}
:root[data-theme="light"] .paper-figure .fig-dark{display:none;}
.paper-figure figcaption strong{color:var(--ink);}
/* 1000 is the number the vendored annotations.css documents for this overlay;
   its .pg-annot-toggle sits at 900 expressly so an open figure covers it. */
#figure-lightbox{position:fixed; inset:0; z-index:1000; background:var(--backdrop);
  display:flex; align-items:center; justify-content:center; padding:var(--s5);}
#figure-lightbox img{max-width:96vw; max-height:92vh; border-radius:var(--r);
  background:var(--paper-raised); box-shadow:0 20px 60px var(--shadow);}
#figure-lightbox .lb-close{position:absolute; top:var(--s4); right:var(--s4);}

/* ---- gloss terms ------------------------------------------------------- */
.gloss-term{display:inline; background:none; border:none; padding:0; margin:0;
  font:inherit; color:var(--amber); cursor:pointer; text-align:left;
  border-bottom:1px dotted var(--amber); border-radius:0;}
.gloss-term:hover,.gloss-term:focus-visible{background:var(--amber-soft); border-bottom-style:solid;}
.gloss-term--active{background:var(--amber-soft); border-bottom-style:solid;}
code .gloss-term{font-family:var(--mono);}

/* ---- popover ----------------------------------------------------------- */
.gloss-popover{position:absolute; z-index:80; width:min(330px,86vw);
  background:var(--paper-raised); border:1px solid var(--mist);
  border-top:2px solid var(--amber); border-radius:var(--r);
  box-shadow:0 10px 32px var(--shadow); padding:var(--s4); font-family:var(--serif);}
.gloss-popover[hidden]{display:none;}
.gloss-popover-term{font-family:var(--mono); font-size:.6875rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--amber); margin-bottom:var(--s2); padding-right:1.4rem;}
.gloss-popover-expansion{font-size:.9063rem; line-height:1.55;}
.gloss-popover-close{position:absolute; top:var(--s2); right:var(--s2); background:none;
  border:none; color:var(--slate); font-size:1.15rem; line-height:1; cursor:pointer;
  padding:var(--s1) var(--s2); border-radius:3px; font-family:var(--mono);}
.gloss-popover-close:hover{color:var(--ink); background:var(--paper-sunk);}

/* ---- glossary panel ---------------------------------------------------- */
#gloss-panel-toggle{position:fixed; top:var(--s4); right:var(--s4); z-index:60;
  font-family:var(--mono); font-size:.75rem; letter-spacing:.04em;
  background:var(--paper-raised); color:var(--ink); border:1px solid var(--mist);
  border-radius:99px; padding:var(--s2) var(--s4); cursor:pointer;
  box-shadow:0 2px 10px var(--shadow);}
#gloss-panel-toggle:hover{border-color:var(--verdigris); color:var(--verdigris);}
.gloss-backdrop{position:fixed; inset:0; background:var(--backdrop); z-index:88;}
.gloss-backdrop[hidden]{display:none;}
.gloss-panel{position:fixed; top:0; right:0; height:100%; width:min(460px,92vw); z-index:90;
  background:var(--paper-raised); border-left:1px solid var(--mist);
  box-shadow:-8px 0 40px var(--shadow); overflow-y:auto; padding:var(--s6) var(--s5);}
.gloss-panel[hidden]{display:none;}
.gloss-panel h2{margin:0 0 var(--s5); font-size:1.25rem; border-bottom:2px solid var(--verdigris);
  padding-bottom:var(--s2);}
.gloss-panel table{font-family:var(--serif); font-size:.875rem;}
.gloss-panel th{font-family:var(--mono);}
.gloss-panel td:first-child{font-family:var(--mono); font-size:.78rem; color:var(--amber);
  white-space:normal; width:34%;}
.gloss-panel-close{position:absolute; top:var(--s4); right:var(--s4); background:none;
  border:none; color:var(--slate); font-size:1.3rem; line-height:1; cursor:pointer;
  padding:var(--s1) var(--s2); border-radius:3px; font-family:var(--mono);}
.gloss-panel-close:hover{color:var(--ink); background:var(--paper-sunk);}

@media (max-width:620px){
  main{padding-top:var(--s8);}
  .doc-meta{grid-template-columns:1fr; gap:0 0;}
  .doc-meta dt{padding-top:var(--s2);}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important;}}
"""

JS = r"""
(function(){
  "use strict";
  var pop   = document.getElementById('gloss-popover');
  var popT  = pop.querySelector('.gloss-popover-term');
  var popE  = pop.querySelector('.gloss-popover-expansion');
  var panel = document.getElementById('gloss-panel');
  var back  = document.getElementById('gloss-backdrop');
  var toggle= document.getElementById('gloss-panel-toggle');
  var active= null;

  function closePopover(){
    pop.hidden = true;
    if(active){ active.classList.remove('gloss-term--active');
                active.setAttribute('aria-expanded','false'); active = null; }
  }
  function closePanel(){
    panel.hidden = true; back.hidden = true; toggle.setAttribute('aria-expanded','false');
  }
  function closeLightbox(){
    var lb = document.getElementById('figure-lightbox');
    if(lb) lb.remove();
  }
  function closeAll(){ closePopover(); closePanel(); closeLightbox(); }

  window.closeGlossPopover  = closePopover;
  window.closeGlossPanel    = closePanel;
  window.closeFigureLightbox= closeLightbox;
  window.closeGlossSurfaces = closeAll;

  function openPopover(btn){
    var entry = GLOSS_TERMS[btn.getAttribute('data-term-id')];
    if(!entry) return;
    closePanel(); closeLightbox();
    if(active === btn){ closePopover(); return; }
    closePopover();
    popT.textContent = entry.term;
    popE.textContent = entry.expansion;
    pop.hidden = false;
    var r = btn.getBoundingClientRect();
    var w = pop.offsetWidth, h = pop.offsetHeight;
    var left = r.left + window.scrollX + r.width/2 - w/2;
    left = Math.max(8 + window.scrollX, Math.min(left, window.scrollX + document.documentElement.clientWidth - w - 8));
    var top = r.bottom + window.scrollY + 8;
    if(r.bottom + h + 16 > window.innerHeight && r.top - h - 8 > 0){
      top = r.top + window.scrollY - h - 8;
    }
    pop.style.left = left + 'px';
    pop.style.top  = top + 'px';
    active = btn;
    btn.classList.add('gloss-term--active');
    btn.setAttribute('aria-expanded','true');
  }

  function openLightbox(img){
    closePopover(); closePanel(); closeLightbox();
    var lb = document.createElement('div');
    lb.id = 'figure-lightbox';
    var close = document.createElement('button');
    close.className = 'gloss-panel-close lb-close';
    close.setAttribute('aria-label','Close figure');
    close.textContent = '×';
    var big = document.createElement('img');
    big.src = img.currentSrc || img.src;      // reuse the loaded data URI, never a second copy
    big.alt = img.alt;
    lb.appendChild(big); lb.appendChild(close);
    document.body.appendChild(lb);
  }

  document.addEventListener('click', function(e){
    var term = e.target.closest && e.target.closest('.gloss-term');
    if(term){ e.preventDefault(); openPopover(term); return; }
    if(e.target.closest && e.target.closest('.gloss-popover-close')){ closePopover(); return; }
    if(e.target.closest && e.target.closest('#gloss-panel-toggle')){
      var open = panel.hidden;
      closeAll();
      if(open){ panel.hidden = false; back.hidden = false; toggle.setAttribute('aria-expanded','true'); }
      return;
    }
    if(e.target.closest && e.target.closest('.gloss-panel-close')){ closePanel(); closeLightbox(); return; }
    if(e.target.id === 'gloss-backdrop'){ closePanel(); return; }
    if(e.target.id === 'figure-lightbox'){ closeLightbox(); return; }
    var fimg = e.target.closest && e.target.closest('.paper-figure img');
    if(fimg){ openLightbox(fimg); return; }
    if(!e.target.closest || !e.target.closest('.gloss-popover')) closePopover();
  });

  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape') closeAll();
  });

  // Glossary panel rows render from the same GLOSS_TERMS object as the popovers.
  var rows = document.getElementById('gloss-panel-rows');
  Object.keys(GLOSS_TERMS).forEach(function(id){
    var tr = document.createElement('tr');
    var td1= document.createElement('td'); td1.textContent = GLOSS_TERMS[id].term;
    var td2= document.createElement('td'); td2.textContent = GLOSS_TERMS[id].expansion;
    tr.appendChild(td1); tr.appendChild(td2); rows.appendChild(tr);
  });
})();
"""
