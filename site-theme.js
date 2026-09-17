(function(){
  'use strict';
  var root=document.documentElement;
  function read(){try{return localStorage.getItem('dravyaguna-theme')}catch(e){return null}}
  function write(v){try{localStorage.setItem('dravyaguna-theme',v)}catch(e){}}
  function preferred(){var saved=read();if(saved==='dark'||saved==='light')return saved;return window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function apply(theme){
    var dark=theme==='dark';
    root.classList.toggle('dark-mode',dark);
    var b=document.getElementById('themeToggle')||document.getElementById('globalThemeToggle');
    if(b){
      b.innerHTML='<span aria-hidden="true">'+(dark?'☀️':'🌙')+'</span><span>'+ (dark?'Light Mode':'Dark Mode') +'</span>';
      b.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');
      b.title=dark?'Switch to light mode':'Switch to dark mode';
      b.classList.add('theme-toggle');
    }
    var meta=document.querySelector('meta[name="theme-color"]');
    if(meta)meta.setAttribute('content',dark?'#0b1410':'#1b4332');
  }
  function init(){
    var theme=preferred();
    var existing=document.getElementById('themeToggle');
    var b=existing||document.getElementById('globalThemeToggle');
    if(!b){
      b=document.createElement('button');
      b.type='button';
      b.id='globalThemeToggle';
      b.className='theme-toggle';
      var nav=document.querySelector('.nav');
      if(nav)nav.appendChild(b);else document.body.appendChild(b);
    }
    b.onclick=function(){
      var next=root.classList.contains('dark-mode')?'light':'dark';
      write(next);
      apply(next);
    };
    apply(theme);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
