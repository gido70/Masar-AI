/* مسار: عارض داخلي لملفات PDF والفيديو والصور، فلا يخرج الزائر من المنصة (13 أكتوبر 2026) */
(function(){
  let box,body,title,dl,yt,opened=false;
  function ensure(){
    if(box) return;
    box=document.createElement('div');box.className='vw';box.innerHTML='<div class="vw-in" role="dialog" aria-modal="true"><div class="vw-bar"><b class="vw-t"></b><a class="vw-dl" download>⬇ تنزيل</a><a class="vw-yt" target="_blank" rel="noopener">افتح في يوتيوب</a><button type="button" class="vw-x" aria-label="إغلاق">✕</button></div><div class="vw-b"></div></div>';
    document.body.appendChild(box);
    body=box.querySelector('.vw-b');title=box.querySelector('.vw-t');dl=box.querySelector('.vw-dl');yt=box.querySelector('.vw-yt');
    box.querySelector('.vw-x').onclick=()=>history.back();
    box.addEventListener('click',e=>{if(e.target===box)history.back();});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&opened)history.back();});
    window.addEventListener('popstate',()=>{if(opened)close();});
  }
  function open(t){ensure();title.textContent=t||'';body.innerHTML='';dl.style.display='none';yt.style.display='none';box.classList.add('on');document.documentElement.style.overflow='hidden';if(!opened){history.pushState({vw:1},'');opened=true;}}
  function close(){opened=false;box.classList.remove('on');body.innerHTML='';document.documentElement.style.overflow='';}
  const BASE=(document.currentScript&&document.currentScript.src||'').replace(/assets\/site\.js.*$/,'');
  let IDX=null;
  function pagesIndex(){return IDX?Promise.resolve(IDX):fetch(BASE+'assets/pdfpages/index.json').then(r=>r.json()).then(j=>IDX=j).catch(()=>({}));}
  async function showPdf(href,t){
    open(t);dl.href=href;dl.style.display='';
    if(navigator.pdfViewerEnabled){body.innerHTML='<iframe class="vw-pdf" src="'+href+'#view=FitH"></iframe>';return;}
    body.innerHTML='<p class="vw-tip">للكتابة في خانات الملف: نزّله وافتحه في Adobe Acrobat Reader.</p>';
    const idx=await pagesIndex();const rel=href.replace(BASE,'').replace(/^\.\.\//,'').split(/[?#]/)[0];const info=idx[rel];
    if(!info){body.insertAdjacentHTML('beforeend','<p class="vw-msg">لا تتوفر معاينة لهذا الملف. استخدم زر «تنزيل».</p>');return;}
    let h='';for(let i=1;i<=info.pages;i++){h+='<img class="vw-pg" loading="lazy" src="'+BASE+info.dir+'/'+String(i).padStart(2,'0')+'.jpg" alt="صفحة '+i+'">';}
    body.insertAdjacentHTML('beforeend',h);
  }
  function ytId(u){const m=u.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{11})/);return m&&m[1];}
  function showYt(id,t){open(t);yt.href='https://youtu.be/'+id;yt.style.display='';body.innerHTML='<div class="vw-v"><iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>';}
  function showImg(href,t){open(t);dl.href=href;dl.style.display='';body.innerHTML='<img class="vw-img" src="'+href+'" alt="">';}
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href]');if(!a||a.hasAttribute('data-out')||a.classList.contains('vw-dl')||a.classList.contains('vw-yt'))return;
    const href=a.getAttribute('href');const t=a.getAttribute('data-title')||a.textContent.trim().replace(/^[^\p{L}\d]+/u,'').slice(0,80);
    const id=ytId(href);
    if(id){e.preventDefault();return showYt(id,t);}
    if(/\.pdf(\?|#|$)/i.test(href)){e.preventDefault();return showPdf(a.href,t);}
    if(/\.(png|jpe?g|webp)(\?|#|$)/i.test(href)){e.preventDefault();return showImg(a.href,t);}
  });
  if('serviceWorker' in navigator){const base=document.querySelector('link[rel="manifest"]');if(base){navigator.serviceWorker.register(base.href.replace(/manifest\.webmanifest.*$/,'sw.js')).catch(()=>{});}}
})();
