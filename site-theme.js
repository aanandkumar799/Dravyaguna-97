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
  if(l)l.textContent=dark?'Light mode':'Dark mode';
}
function save(theme){try{localStorage.setItem(KEY,theme)}catch(e){}}
function mount(){
  if(document.getElementById('dgThemeToggle'))return;
  var b=document.createElement('button');b.id='dgThemeToggle';b.type='button';b.innerHTML='<span id="dgThemeIcon" aria-hidden="true">🌙</span><span id="dgThemeLabel">Dark mode</span>';
  b.addEventListener('click',function(){var next=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';save(next);apply(next)});
  document.body.appendChild(b);apply(getTheme());
}
function init(){apply(getTheme());if(document.body)mount();else document.addEventListener('DOMContentLoaded',mount,{once:true})}
init();
window.DravyaGunaTheme={get:getTheme,set:function(t){if(t!=='dark'&&t!=='light')t=systemTheme();save(t);apply(t)}};
})();