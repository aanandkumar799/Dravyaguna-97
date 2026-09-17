(function(){
  'use strict';
  var root=document.documentElement;
  function read(){try{return localStorage.getItem('dravyaguna-theme')}catch(e){return null}}
  function write(v){try{localStorage.setItem('dravyaguna-theme',v)}catch(e){}}
  function preferred(){var saved=read();if(saved==='dark'||saved==='light')return saved;return window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function apply(theme){var dark=theme==='dark';root.classList.toggle('dark-mode',dark);var b=document.getElementById('globalThemeToggle');if(b){b.innerHTML=dark?'☀️ Light Mode':'🌙 Dark Mode';b.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');b.title=dark?'Switch to light mode':'Switch to dark mode'}var meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.setAttribute('content',dark?'#0b1410':'#1b4332')}
  function init(){
    var theme=preferred();
    apply(theme);
    var existing=document.getElementById('themeToggle');
    if(existing){existing.addEventListener('click',function(){setTimeout(function(){var dark=root.classList.contains('dark-mode');write(dark?'dark':'light');apply(dark?'dark':'light')},0)});}
    var b=document.getElementById('globalThemeToggle');
    if(!b){
      b=document.createElement('button');
      b.type='button';
      b.id='globalThemeToggle';
      b.className='dg-theme-toggle';
      b.addEventListener('click',function(){var next=root.classList.contains('dark-mode')?'light':'dark';write(next);apply(next)});
      (document.body||document.documentElement).appendChild(b);
    }
    apply(theme);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
