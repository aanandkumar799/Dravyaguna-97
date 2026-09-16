(()=>{
  const clean=v=>String(v??'').trim();
  const normalize=v=>clean(v).replace(/\s+/g,' ');
  const splitItems=v=>{
    const s=clean(v); if(!s)return [];
    if(s.includes('•'))return s.split('•').map(normalize).filter(Boolean);
    if(s.includes('||'))return s.split('||').map(normalize).filter(Boolean);
    if(s.includes(';'))return s.split(';').map(normalize).filter(Boolean);
    return s.split(/\n+/).map(normalize).filter(Boolean);
  };
  const makeCard=(label,answer,index)=>{
    const article=document.createElement('button');article.type='button';article.className='quick-flashcard';article.setAttribute('aria-label',`Flashcard ${index+1}: ${label}`);
    const inner=document.createElement('span');inner.className='quick-flashcard-inner';
    const front=document.createElement('span');front.className='quick-flashcard-face quick-flashcard-front';front.innerHTML=`<span class="quick-flashcard-label">${label}</span><span class="quick-flashcard-question">Tap to reveal</span><span class="quick-flashcard-hint">↻ Flip card</span>`;
    const back=document.createElement('span');back.className='quick-flashcard-face quick-flashcard-back';back.innerHTML=`<span class="quick-flashcard-label">Answer</span><span class="quick-flashcard-answer"></span>`;back.querySelector('.quick-flashcard-answer').textContent=answer;
    inner.append(front,back);article.append(inner);article.addEventListener('click',()=>article.classList.toggle('is-flipped'));return article;
  };
  const build=()=>{
    if(document.querySelector('.quick-flashcard-panel'))return true;
    const section=[...document.querySelectorAll('.plant-section')].find(s=>/student zone/i.test(s.querySelector('h2')?.textContent||''));
    if(!section)return false;
    const rows=[...section.querySelectorAll('.info-row')];
    const wanted=['Quick Revision','Exam Points','Viva Questions','Identification Points','Mnemonics'];
    const entries=[];
    rows.forEach(row=>{
      const label=clean(row.querySelector('.info-label')?.textContent);const value=clean(row.querySelector('.info-value')?.textContent);
      if(!wanted.some(w=>label.toLowerCase()===w.toLowerCase())||!value||/not available/i.test(value))return;
      splitItems(value).forEach(item=>entries.push({label,item}));
    });
    if(!entries.length)return false;
    const panel=document.createElement('div');panel.className='quick-flashcard-panel';panel.setAttribute('aria-label','Quick Revision Flashcards');
    panel.innerHTML='<div class="quick-flashcard-header"><h3>🃏 Quick Revision Flashcards</h3><span class="quick-flashcard-count"></span></div><div class="quick-flashcard-deck"></div><div class="quick-flashcard-actions"><button type="button" data-flip-all>Flip All</button><button type="button" data-reset-cards>Reset</button></div>';
    const deck=panel.querySelector('.quick-flashcard-deck');entries.slice(0,20).forEach((e,i)=>deck.appendChild(makeCard(e.label,e.item,i)));
    panel.querySelector('.quick-flashcard-count').textContent=`${deck.children.length} cards • Tap a card to flip`;
    panel.querySelector('[data-flip-all]').addEventListener('click',()=>deck.querySelectorAll('.quick-flashcard').forEach(c=>c.classList.add('is-flipped')));
    panel.querySelector('[data-reset-cards]').addEventListener('click',()=>deck.querySelectorAll('.quick-flashcard').forEach(c=>c.classList.remove('is-flipped')));
    const quickRow=rows.find(r=>/^Quick Revision$/i.test(clean(r.querySelector('.info-label')?.textContent)));
    (quickRow||rows[rows.length-1]||section).insertAdjacentElement('afterend',panel);
    return true;
  };
  if(build())return;
  const observer=new MutationObserver(()=>{if(build())observer.disconnect()});observer.observe(document.getElementById('plant-content')||document.body,{childList:true,subtree:true});
  setTimeout(()=>observer.disconnect(),10000);
})();