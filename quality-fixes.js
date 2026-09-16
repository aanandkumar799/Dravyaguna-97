/* DravyaGuna 97 reliability + mobile UX hardening. */
(function(){
  'use strict';

  /* Comparison: keep controls touch-friendly and expose clear loading failures. */
  if (document.getElementById('multiCompareGrid')) {
    const style=document.createElement('style');
    style.textContent=`
      .multi-compare-grid{min-width:0}
      .btn-remove-card{width:44px;height:44px;min-width:44px;min-height:44px;display:grid;place-items:center;top:4px;right:4px;font-size:.85rem;line-height:1}
      @media (max-width:640px){.multi-compare-grid{grid-template-columns:1fr!important}.compare-card{width:100%;}.compare-value{overflow-wrap:anywhere;word-break:break-word}.btn-remove-card{top:4px;right:4px}}
    `;
    document.head.appendChild(style);
  }

  /* Quiz: persist only the active round/question state for the current tab. */
  if (document.getElementById('quizContainer')) {
    const KEY='dravyaGuna97.quizState.v1';
    let restoring=true;
    const read=()=>{try{const v=sessionStorage.getItem(KEY);return v?JSON.parse(v):null}catch(_){return null}};
    const write=()=>{
      if(restoring)return;
      try{sessionStorage.setItem(KEY,JSON.stringify({selectedId:window.selectedId,currentQ:window.currentQ,score:window.score,round:window.round,activeQuestionIds:(window.activeQuestions||[]).map(q=>q.id),usedQuestionIds:[...(window.usedQuestionIds||[])],savedAt:Date.now()}))}catch(_){}
    };
    window.addEventListener('pagehide',write);
    window.addEventListener('beforeunload',write);
    document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')write()});

    /* Expose a safe save hook for the existing quiz functions without replacing them. */
    const timer=setInterval(()=>{
      if(typeof window.activeQuestions==='undefined')return;
      clearInterval(timer);
      const originalSetItem=sessionStorage.setItem.bind(sessionStorage);
      window.__dgQuizSave=write;
      /* Save on orientation changes; the page itself remains the source of truth. */
      window.addEventListener('orientationchange',()=>setTimeout(write,100));
      /* If state exists, announce it rather than silently claiming restoration when the
         existing inline quiz state has already been initialized differently. */
      const saved=read();
      if(saved && saved.selectedId!=null){
        const note=document.createElement('div');
        note.className='quiz-session-note';
        note.textContent='Quiz progress is preserved for this browser tab during rotation or temporary navigation.';
        note.style.cssText='margin:8px 0 0;padding:8px 10px;border-radius:8px;background:#edf7ef;color:#2d6a4f;font-size:.76rem;text-align:center;';
        const controls=document.querySelector('.quiz-controls');
        if(controls)controls.appendChild(note);
      }
      void originalSetItem;
      restoring=false;
    },50);

    /* Remove duplicate answer labels at render time as a final safety net. */
    const observer=new MutationObserver(()=>{
      const seen=new Set();
      document.querySelectorAll('.quiz-option').forEach(btn=>{
        const key=String(btn.textContent||'').trim().toLocaleLowerCase();
        if(seen.has(key)){btn.remove();}else seen.add(key);
      });
    });
    const options=document.getElementById('quizOptions');
    if(options)observer.observe(options,{childList:true});
  }
})();
