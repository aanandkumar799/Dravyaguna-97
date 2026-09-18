(function(){
'use strict';
var cfg=window.DRAVYAGUNA_FIREBASE_CONFIG||{},auth=null,db=null,user=null,firebaseReady=false,V='10.12.5';

function configured(){return !!(cfg.apiKey&&cfg.projectId&&cfg.appId&&cfg.apiKey.indexOf('REPLACE_')!==0&&cfg.projectId.indexOf('REPLACE_')!==0&&cfg.appId.indexOf('REPLACE_')!==0)}
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function context(){return{page_url:location.href,page_path:location.pathname+location.search,page_title:document.title,referrer:document.referrer||'',language:navigator.language||'',timestamp:new Date().toISOString()}}
function status(t,type){var e=document.getElementById('dgStatus');if(e){e.textContent=t;e.className='dg-status show '+(type||'')}}
function busy(v){var b=document.getElementById('dgSubmit');if(!b)return;b.disabled=v;b.innerHTML=v?'<span class="dg-spinner" aria-hidden="true"></span><span>Submitting…</span>':'<span>Send Suggestion</span><span aria-hidden="true">→</span>'}

function bindForm(){
 var form=document.getElementById('dgFeedbackForm');if(!form||form.dataset.bound==='1')return;
 form.dataset.bound='1';
 document.querySelectorAll('.dg-rating button').forEach(function(b){
   b.addEventListener('click',function(){
     var n=Number(b.dataset.rating),box=b.parentElement,input=document.getElementById('dgRating');
     if(input)input.value=n;
     box.classList.remove('invalid');
     box.querySelectorAll('button').forEach(function(x){
       var active=Number(x.dataset.rating)<=n;
       x.classList.toggle('active',active);
       x.setAttribute('aria-checked',Number(x.dataset.rating)===n?'true':'false');
     });
   });
 });
 var msg=document.getElementById('dgMessage'),count=document.getElementById('dgCount');
 if(msg&&count)msg.addEventListener('input',function(){count.textContent=msg.value.length});
 form.addEventListener('submit',submit);
}

function loginUI(){
 var e=document.getElementById('dgLogin');if(!e)return;
 if(!user){
   e.innerHTML='<div class="dg-feedback-login"><div><strong>Google verification required</strong><span>Sign in with the Google account already available in your browser. Anonymous feedback is disabled.</span></div><button type="button" class="dg-google-btn" id="dgGoogle">Continue with Google</button></div>';
   var b=document.getElementById('dgGoogle');if(b)b.onclick=googleLogin;
   var em=document.getElementById('dgEmail');if(em)em.value='Sign in with Google to continue';
   return;
 }
 var providerOk=user.providerData&&user.providerData.some(function(p){return p.providerId==='google.com';});
 if(!providerOk||!user.email||user.emailVerified!==true){
   e.innerHTML='<div class="dg-feedback-login"><div><strong>Verified Google account required</strong><span>Please sign in with a Google account whose email is verified.</span></div><button type="button" class="dg-google-btn" id="dgGoogle">Verify with Google</button></div>';
   var rb=document.getElementById('dgGoogle');if(rb)rb.onclick=googleLogin;
   var rem=document.getElementById('dgEmail');if(rem)rem.value='Google verification required';
   return;
 }
 e.innerHTML='<div class="dg-feedback-login"><div class="dg-user"><div class="dg-avatar">'+(user.photoURL?'<img src="'+esc(user.photoURL)+'" alt="">':'👤')+'</div><div class="dg-user-text"><strong>'+esc(user.displayName||'Verified Google user')+'</strong><span>'+esc(user.email)+' • Verified Google account</span></div></div><button type="button" class="dg-signout" id="dgSignout">Sign out</button></div>';
 var sb=document.getElementById('dgSignout');if(sb)sb.onclick=function(){auth.signOut()};
 var em2=document.getElementById('dgEmail');if(em2)em2.value=user.email;
}

function loadFirebase(){
 return Promise.all(['firebase-app-compat.js','firebase-auth-compat.js','firebase-firestore-compat.js'].map(function(n){
   return new Promise(function(ok,no){var s=document.createElement('script');s.src='https://www.gstatic.com/firebase/'+V+'/'+n;s.onload=ok;s.onerror=no;document.head.appendChild(s)})
 })).then(function(){
   if(window.firebase.apps&&window.firebase.apps.length)window.firebase.app();else window.firebase.initializeApp(cfg);
   auth=window.firebase.auth();db=window.firebase.firestore();
   auth.onAuthStateChanged(function(u){user=u||null;loginUI()});
   loginUI();
 });
}

function googleLogin(){
 if(!firebaseReady||!auth)return status('Google verification is still loading. Please try again.','err');
 var p=new firebase.auth.GoogleAuthProvider();p.setCustomParameters({prompt:'select_account'});
 status('Opening Google sign-in…','loading');
 var mobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
 (mobile?auth.signInWithRedirect(p):auth.signInWithPopup(p)).catch(function(e){
   console.error('Google sign-in failed',e);
   if(e&&e.code==='auth/popup-blocked')return auth.signInWithRedirect(p);
   status(e&&e.message||'Google sign-in failed. Please try again.','err');
 });
}

function submit(ev){
 ev.preventDefault();
 if(!user||!db)return status('Please sign in with Google before submitting feedback.','err');
 var providerOk=user.providerData&&user.providerData.some(function(p){return p.providerId==='google.com';});
 if(!providerOk||!user.email||user.emailVerified!==true)return status('A verified Google account is required to submit feedback.','err');
 var rating=Number(document.getElementById('dgRating').value),message=document.getElementById('dgMessage').value.trim();
 if(!rating){document.querySelector('.dg-rating').classList.add('invalid');return status('Please select a rating.','err')}
 if(!message)return status('Please enter your feedback details.','err');
 if(message.length>2000)return status('Feedback is limited to 2000 characters.','err');
 busy(true);
 var payload={
   category:document.getElementById('dgCategory').value,
   rating:rating,
   message:message.slice(0,2000),
   correction_area:document.getElementById('dgCorrection').value||null,
   user:{uid:user.uid,isAnonymous:!!user.isAnonymous,displayName:user.displayName||null,email:user.email||null,emailVerified:!!user.emailVerified,photoURL:user.photoURL||null},
   context:context(),
   status:'new',
   authProvider:'google.com',
   createdAt:firebase.firestore.FieldValue.serverTimestamp()
 };
 db.collection('reviews').add(payload)
 .then(function(){
   return db.collection('reviewUsers').doc(user.uid).set({
     uid:user.uid,isAnonymous:!!user.isAnonymous,displayName:user.displayName||null,email:user.email||null,
     emailVerified:!!user.emailVerified,photoURL:user.photoURL||null,lastSubmittedAt:firebase.firestore.FieldValue.serverTimestamp()
   },{merge:true});
 })
 .then(function(){
   document.getElementById('dgFeedbackForm').reset();
   document.getElementById('dgRating').value='0';
   document.getElementById('dgCount').textContent='0';
   document.querySelectorAll('.dg-rating button').forEach(function(x){x.classList.remove('active');x.setAttribute('aria-checked','false')});
   busy(false);
   status('Thanks! Your feedback has been submitted.','ok');
 })
 .catch(function(e){
   console.error('Feedback submission failed',e);
   busy(false);
   status('Could not submit feedback. '+(e&&e.code?'('+e.code+') ':'')+'Please try again.','err');
 });
}

function init(){
 bindForm();
 if(!configured()){loginUI();status('Google-verified feedback storage is not configured right now.','err');return}
 loadFirebase().then(function(){firebaseReady=true;loginUI()})
 .catch(function(e){console.error('Firebase initialization failed',e);loginUI();status('Google-verified feedback is unavailable right now. Please try again later.','err')});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();