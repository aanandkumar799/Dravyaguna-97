(function(){
'use strict';
var cfg=window.DRAVYAGUNA_FIREBASE_CONFIG||{},auth=null,db=null,user=null,firebaseReady=false;
function configured(){return !!(cfg.apiKey&&cfg.projectId&&cfg.appId&&cfg.apiKey.indexOf('REPLACE_')!==0&&cfg.projectId.indexOf('REPLACE_')!==0&&cfg.appId.indexOf('REPLACE_')!==0)}
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function status(t,type){var e=document.getElementById('dgStatus');if(e){e.textContent=t;e.className='status show '+(type||'')}}
function setAccess(v){var fs=document.getElementById('dgFields');if(fs)fs.disabled=!v}
function busy(v){var b=document.getElementById('dgSubmit');if(!b)return;b.disabled=v;b.textContent=v?'Submitting…':'Send feedback →'}
function providerOk(){return !!(user&&user.providerData&&user.providerData.some(function(p){return p.providerId==='google.com'})&&user.email&&user.emailVerified===true)}
function loginUI(){
 var e=document.getElementById('dgLogin');if(!e)return;setAccess(providerOk());
 if(!providerOk()){e.innerHTML='<div class="dg-feedback-login"><div><strong>Sign in to send feedback</strong><span>Continue with your verified Google account.</span></div><button type="button" class="dg-google-btn" id="dgGoogle">Continue with Google</button></div>';var b=document.getElementById('dgGoogle');if(b)b.onclick=googleLogin;return}
 e.innerHTML='<div class="dg-feedback-login"><div><strong>'+esc(user.displayName||'Signed-in user')+'</strong><span>'+esc(user.email)+'</span></div><button type="button" class="dg-signout" id="dgSignout">Sign out</button></div>';
 var sb=document.getElementById('dgSignout');if(sb)sb.onclick=function(){auth.signOut().catch(function(){status('Could not sign out. Please try again.','err')})};
}
function initFirebase(){
 if(!configured()){loginUI();status('Feedback storage is not configured. Please try again later.','err');return}
 if(!window.firebase){loginUI();status('Google sign-in could not load. Please refresh the page.','err');return}
 try{
  if(window.firebase.apps&&window.firebase.apps.length)window.firebase.app();else window.firebase.initializeApp(cfg);
  auth=window.firebase.auth();db=window.firebase.firestore();firebaseReady=true;
  auth.onAuthStateChanged(function(u){user=u||null;loginUI()});
  auth.setPersistence(window.firebase.auth.Auth.Persistence.LOCAL).catch(function(e){console.warn('Auth persistence:',e)});
  auth.getRedirectResult().catch(function(e){if(e&&e.code&&e.code!=='auth/no-auth-event')console.warn('Redirect result:',e)});
  loginUI();
 }catch(e){console.error(e);firebaseReady=false;loginUI();status('Google sign-in could not start. Please refresh the page.','err')}
}
function googleLogin(){
 if(!firebaseReady||!auth)return status('Google sign-in is not ready yet. Please wait a moment and try again.','err');
 var p=new firebase.auth.GoogleAuthProvider();p.setCustomParameters({prompt:'select_account'});status('Opening Google sign-in…','loading');
 var mobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
 (mobile?auth.signInWithRedirect(p):auth.signInWithPopup(p)).catch(function(e){console.error(e);if(e&&e.code==='auth/popup-blocked')return auth.signInWithRedirect(p);status(e&&e.code==='auth/unauthorized-domain'?'This website domain is not authorized in Firebase Authentication.':'Google sign-in failed. Please try again.','err')});
}
function bindForm(){
 var form=document.getElementById('dgFeedbackForm');if(!form||form.dataset.bound==='1')return;form.dataset.bound='1';
 document.querySelectorAll('.rating button').forEach(function(b){b.addEventListener('click',function(){var n=Number(b.dataset.rating),box=b.parentElement,input=document.getElementById('dgRating');if(input)input.value=n;box.classList.remove('invalid');box.querySelectorAll('button').forEach(function(x){x.classList.toggle('active',Number(x.dataset.rating)<=n);x.setAttribute('aria-checked',Number(x.dataset.rating)===n?'true':'false')})})});
 var msg=document.getElementById('dgMessage'),count=document.getElementById('dgCount');if(msg&&count)msg.addEventListener('input',function(){count.textContent=msg.value.length});
 form.addEventListener('submit',submit);
}
function submit(ev){
 ev.preventDefault();
 if(!providerOk())return status('Please sign in with Google before submitting feedback.','err');
 if(!firebaseReady||!db)return status('Feedback service is not ready. Please refresh and try again.','err');
 var rating=Number(document.getElementById('dgRating').value),message=document.getElementById('dgMessage').value.trim(),category=document.getElementById('dgCategory').value;
 if(!category)return status('Please choose a feedback category.','err');
 if(!rating){document.querySelector('.rating').classList.add('invalid');return status('Please select a rating.','err')}
 if(message.length<3)return status('Please enter a little more detail so the issue can be understood.','err');
 if(message.length>2000)return status('Feedback is limited to 2000 characters.','err');
 busy(true);
 user.getIdTokenResult().then(function(tokenResult){
   var claims=tokenResult&&tokenResult.claims||{};
   var provider=claims.firebase&&claims.firebase.sign_in_provider;
   if(claims.email_verified!==true || provider!=='google.com')throw new Error('verified-google-token-required');
   var payload={
     category:(category==='technical'?'bug':(category==='suggestion'?'feature':(category==='correction'||category==='image'?'content':'general'))),
     category_label:category,rating:rating,message:message,
     correction_area:document.getElementById('dgCorrection').value||null,
     user:{uid:user.uid,displayName:user.displayName||null,email:user.email||null,emailVerified:true,photoURL:user.photoURL||null},
     context:{page_url:location.href,page_path:location.pathname+location.search,page_title:document.title,referrer:document.referrer||'',language:navigator.language||''},
     status:'new',authProvider:'google.com',createdAt:firebase.firestore.FieldValue.serverTimestamp()
   };
   return db.collection('reviews').add(payload);
 }).then(function(){
   document.getElementById('dgFeedbackForm').reset();document.getElementById('dgRating').value='0';document.getElementById('dgCount').textContent='0';
   document.querySelectorAll('.rating button').forEach(function(x){x.classList.remove('active');x.setAttribute('aria-checked','false')});busy(false);status('Thanks! Your feedback has been submitted successfully.','ok');
 }).catch(function(e){
   console.error('Feedback submission failed:',e);busy(false);var code=e&&e.code?e.code:'unknown';
   if(code==='verified-google-token-required')status('Your Google session needs to be refreshed. Please sign out, sign in again, and submit once more.','err');
   else if(code==='permission-denied')status('Feedback is temporarily blocked by the Firestore security rules. Please try again after the Firebase rules deployment completes.','err');
   else status('Could not submit feedback ('+code+'). Please try again.','err');
 });
}
function init(){bindForm();initFirebase()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();