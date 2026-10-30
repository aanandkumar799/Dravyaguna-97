(function(){
'use strict';
var KEY='dg-theme';
function systemTheme(){return window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
function getTheme(){try{var v=localStorage.getItem(KEY);return v==='dark'||v==='light'?v:systemTheme()}catch(e){return systemTheme()}}
function apply(theme){
  document.documentElement.setAttribute('data-theme',theme);
  document.documentElement.style.colorScheme=theme;
  var b=document.getElementById('dgThemeToggle'),i=document.getElementById('dgThemeIcon'),l=document.getElementById('dgThemeLabel');
  if(!b)return;
  var dark=theme==='dark';
  b.setAttribute('aria-pressed',String(dark));
  b.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');
  if(i)i.textContent=dark?'☀️':'🌙';
  if(l)l.textContent=dark?'Light mode':'Dark mode';var m=document.getElementById('themeColor');if(m)m.setAttribute('content',dark?'#0b1411':'#1b4332');
}
function save(theme){try{localStorage.setItem(KEY,theme)}catch(e){}}
function mount(){
  if(document.getElementById('dgThemeToggle'))return;
  var b=document.createElement('button');b.id='dgThemeToggle';b.type='button';b.className='nav-theme-toggle';b.innerHTML='<span id="dgThemeIcon" aria-hidden="true">🌙</span><span id="dgThemeLabel">Dark mode</span>';
  b.addEventListener('click',function(){var next=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';save(next);apply(next)});
  var header=document.querySelector('.site-header .header-inner, header .header-inner');
  var nav=header&&header.querySelector('.nav');
  if(header)header.appendChild(b);
  else if(nav)nav.appendChild(b);
  else document.body.appendChild(b);
  apply(getTheme());
}
function init(){apply(getTheme());if(document.body)mount();else document.addEventListener('DOMContentLoaded',mount,{once:true})}
init();
window.DravyaGunaTheme={get:getTheme,set:function(t){if(t!=='dark'&&t!=='light')t=systemTheme();save(t);apply(t)}};
})();(function(){try{if(/plant\.html$/.test(location.pathname)){var id=new URLSearchParams(location.search).get('id');if(id&&/^[a-z0-9-]+$/i.test(id))localStorage.setItem('dg97-last-plant',JSON.stringify(id))}}catch(e){}})();

/* Install button: shown only while the app can be installed; removed once installed. */
(function(){
'use strict';
var KEY='dg97-installed',deferred=null,btns=[];
var ua=navigator.userAgent||'';
var ios=/iphone|ipad|ipod/i.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
var iosSafari=ios&&/safari/i.test(ua)&&!/crios|fxios|edgios|gsa/i.test(ua);
function standalone(){return !!(window.matchMedia&&(matchMedia('(display-mode: standalone)').matches||matchMedia('(display-mode: minimal-ui)').matches||matchMedia('(display-mode: window-controls-overlay)').matches))||navigator.standalone===true}
function flagged(){try{return localStorage.getItem(KEY)==='1'}catch(e){return false}}
function flag(v){try{if(v)localStorage.setItem(KEY,'1');else localStorage.removeItem(KEY)}catch(e){}}
function canShow(){if(standalone())return false;if(deferred)return true;return iosSafari&&!flagged()}
function each(f){for(var i=0;i<btns.length;i++)f(btns[i])}
function update(){var show=canShow();each(function(b){b.hidden=!show;b.classList.toggle('is-installed',!show)})}
function removeBtn(){flag(true);deferred=null;each(function(b){b.hidden=true;b.classList.add('is-installed')})}
addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;flag(false);update()});
addEventListener('appinstalled',removeBtn);
function onClick(){
  if(standalone()){removeBtn();return}
  if(deferred){var d=deferred;deferred=null;d.prompt();if(d.userChoice)d.userChoice.then(function(c){if(c&&c.outcome==='accepted')removeBtn();else update()});else update();return}
  if(iosSafari){alert('To install DravyaGuna 97: tap the Share button in Safari, then choose \u201cAdd to Home Screen\u201d.');flag(true);update()}
}
function make(id,cls,label){var b=document.createElement('button');b.id=id;b.type='button';b.className=cls;b.hidden=true;b.setAttribute('aria-label','Install DravyaGuna 97 app');b.textContent=label;return b}
function mount(){
  var head=document.getElementById('install');
  if(!head){
    head=make('install','install-nav dg-install-btn','\ud83d\udcf2 Install app');
    var nav=document.querySelector('.site-header .nav, header .nav');
    var header=document.querySelector('.site-header .header-inner, header .header-inner');
    if(nav)nav.appendChild(head);else if(header)header.appendChild(head);else head=null;
  }
  if(head){head.classList.add('dg-install-head');btns.push(head)}
  var fab=make('dgInstallFab','dg-install-fab','\ud83d\udcf2 Install app');
  if(document.querySelector('.lp-tab'))fab.classList.add('dg-install-fab--tabbar');if(!head)fab.classList.add('dg-install-fab--only');
  document.body.appendChild(fab);btns.push(fab);
  each(function(b){b.addEventListener('click',onClick)});
  if(window.matchMedia){try{matchMedia('(display-mode: standalone)').addEventListener('change',update)}catch(e){}}
  if(navigator.getInstalledRelatedApps){navigator.getInstalledRelatedApps().then(function(a){if(a&&a.length)removeBtn()}).catch(function(){})}
  update();
}
if(document.body)mount();else document.addEventListener('DOMContentLoaded',mount,{once:true});
})();
