from pathlib import Path

p = Path('quiz.html')
s = p.read_text(encoding='utf-8')

old = "function pickDistractors(correct, candidates, count=3){const c=uniqueValues(candidates).filter(v=>norm(v)!==norm(correct));return shuffle(c).slice(0,count)}"
new = "function pickDistractors(correct,candidates,count=3){const seen=new Set();const c=uniqueValues(candidates).filter(v=>{const k=norm(v);if(!k||k===norm(correct)||seen.has(k))return false;seen.add(k);return true});return shuffle(c).slice(0,count)}"
if old in s:
    s=s.replace(old,new,1)

old = "const correct=clean(answer);if(!correct)return null;const opts=pickDistractors(correct,candidates,3);if(opts.length<3)return null;\n return {id,plantId:plant.id,plantName:plant.name,question:prompt,options:shuffle([correct,...opts]),answer:correct,explanation};"
new = "const correct=clean(answer);if(!correct)return null;const opts=pickDistractors(correct,candidates,3);if(opts.length<3)return null;const uniqueOpts=[];const seen=new Set();[correct,...opts].forEach(v=>{const k=norm(v);if(k&&!seen.has(k)){seen.add(k);uniqueOpts.push(v)}});if(uniqueOpts.length<4)return null;\n return {id,plantId:plant.id,plantName:plant.name,question:prompt,options:shuffle(uniqueOpts),answer:correct,explanation};"
if old in s:
    s=s.replace(old,new,1)

needle = "let plants=[], questionBank=[], activeQuestions=[], usedQuestionIds=new Set(), currentQ=0,score=0,answered=false,round=1,selectedId='all';"
inject = """let plants=[], questionBank=[], activeQuestions=[], usedQuestionIds=new Set(), currentQ=0,score=0,answered=false,round=1,selectedId='all';
const QUIZ_STATE_KEY='dravyaGuna97.quizState.v2';
function saveQuizState(){try{sessionStorage.setItem(QUIZ_STATE_KEY,JSON.stringify({selectedId,round,currentQ,score,answered,activeQuestionIds:activeQuestions.map(q=>q.id),usedQuestionIds:[...usedQuestionIds],savedAt:Date.now()}))}catch(e){}}
function readQuizState(){try{const raw=sessionStorage.getItem(QUIZ_STATE_KEY);return raw?JSON.parse(raw):null}catch(e){return null}}
function clearQuizState(){try{sessionStorage.removeItem(QUIZ_STATE_KEY)}catch(e){}}
function restoreQuizState(){const saved=readQuizState();if(!saved||!Array.isArray(saved.activeQuestionIds)||!saved.activeQuestionIds.length)return false;const ids=new Set(saved.activeQuestionIds);const restored=questionBank.filter(q=>ids.has(q.id));if(restored.length!==saved.activeQuestionIds.length)return false;selectedId=plants.some(p=>p.id===saved.selectedId)||saved.selectedId==='all'?saved.selectedId:'all';$('plantSelect').value=selectedId;round=Number(saved.round)||1;activeQuestions=saved.activeQuestionIds.map(id=>questionBank.find(q=>q.id===id)).filter(Boolean);usedQuestionIds=new Set(Array.isArray(saved.usedQuestionIds)?saved.usedQuestionIds:[]);currentQ=Math.min(Math.max(Number(saved.currentQ)||0,0),Math.max(activeQuestions.length-1,0));score=Math.max(Number(saved.score)||0,0);answered=false;$('modePill').textContent=selectedId==='all'?'Whole Series • 10 questions per round':`${plants.find(p=>p.id===selectedId)?.name||'Selected Plant'} • Focused Practice`;loadQuestion();return true}"
if needle in s and "QUIZ_STATE_KEY" not in s:
    s=s.replace(needle,inject,1)

old = "plants=source;populateSelector();startRound(true);"
new = "plants=source;populateSelector();questionBank=buildQuestionBank(plants);if(!restoreQuizState())startRound(true);"
if old in s:
    s=s.replace(old,new,1)

old = "if(first||!questionBank.length){questionBank=buildQuestionBank(plants);usedQuestionIds.clear();round=1}"
new = "if(first||!questionBank.length){questionBank=buildQuestionBank(plants);usedQuestionIds.clear();round=1}"
# kept intentionally identical: loadData now restores before starting a new round

old = "currentQ=0;score=0;round=round||1;loadQuestion();"
new = "currentQ=0;score=0;round=round||1;loadQuestion();saveQuizState();"
if old in s:
    s=s.replace(old,new,1)

old = "shuffle(q.options).forEach(text=>{"
new = "shuffle(uniqueValues(q.options)).forEach(text=>{"
if old in s:
    s=s.replace(old,new,1)

old = "$('quizExplanation').hidden=false;$('nextBtn').style.display='block';$('progressBar').style.width=`${((currentQ+1)/activeQuestions.length)*100}%`}"
new = "$('quizExplanation').hidden=false;$('nextBtn').style.display='block';$('progressBar').style.width=`${((currentQ+1)/activeQuestions.length)*100}%`;saveQuizState()}"
if old in s:
    s=s.replace(old,new,1)

old = "function nextQuestion(){currentQ++;if(currentQ<activeQuestions.length)loadQuestion();else showRoundResult()}"
new = "function nextQuestion(){currentQ++;if(currentQ<activeQuestions.length){loadQuestion();saveQuizState()}else{showRoundResult();saveQuizState()}}"
if old in s:
    s=s.replace(old,new,1)

old = "$('plantSelect').addEventListener('change',e=>{selectedId=e.target.value;round=1;usedQuestionIds.clear();$('modePill').textContent=selectedId==='all'?'Whole Series • 10 questions per round':`${plants.find(p=>p.id===selectedId)?.name||'Selected Plant'} • Focused Practice`;restoreQuizCard();makeRoundQuestions()});"
new = "$('plantSelect').addEventListener('change',e=>{selectedId=e.target.value;round=1;usedQuestionIds.clear();clearQuizState();$('modePill').textContent=selectedId==='all'?'Whole Series • 10 questions per round':`${plants.find(p=>p.id===selectedId)?.name||'Selected Plant'} • Focused Practice`;restoreQuizCard();makeRoundQuestions()});"
if old in s:
    s=s.replace(old,new,1)

old = "$('restartBtn').addEventListener('click',()=>{round=1;usedQuestionIds.clear();restoreQuizCard();makeRoundQuestions()});"
new = "$('restartBtn').addEventListener('click',()=>{round=1;usedQuestionIds.clear();clearQuizState();restoreQuizCard();makeRoundQuestions()});"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('quiz.html hardened')
