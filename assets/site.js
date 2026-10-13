/* مسار: عارض داخلي لملفات PDF والفيديو والصور، فلا يخرج الزائر من المنصة (13 أكتوبر 2026) */
(function(){
  const PDFJS='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/';
  let box,body,title,dl,yt,pdfLib=null,opened=false;
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
  function loadPdfJs(){
    if(pdfLib) return Promise.resolve(pdfLib);
    return new Promise((res,rej)=>{const s=document.createElement('script');s.src=PDFJS+'pdf.min.js';s.onload=()=>{window.pdfjsLib.GlobalWorkerOptions.workerSrc=PDFJS+'pdf.worker.min.js';pdfLib=window.pdfjsLib;res(pdfLib);};s.onerror=rej;document.head.appendChild(s);});
  }
  async function showPdf(href,t){
    open(t);dl.href=href;dl.style.display='';
    body.innerHTML='<p class="vw-msg">جارٍ فتح الملف…</p><p class="vw-tip">للكتابة في خانات الملف: نزّله ثم افتحه في Adobe Acrobat Reader.</p>';
    try{
      const lib=await loadPdfJs();const doc=await lib.getDocument(href).promise;
      body.querySelector('.vw-msg').remove();
      const w=Math.min(body.clientWidth-24,980);
      for(let i=1;i<=doc.numPages;i++){
        if(!opened) return;
        const pg=await doc.getPage(i);const v1=pg.getViewport({scale:1});const sc=w/v1.width;const ratio=window.devicePixelRatio||1;
        const vp=pg.getViewport({scale:sc*ratio});const c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;c.style.width=(vp.width/ratio)+'px';c.className='vw-pg';body.appendChild(c);
        await pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise;
      }
    }catch(e){body.innerHTML='<p class="vw-msg">تعذّر عرض الملف هنا. استخدم زر «تنزيل».</p>';}
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
