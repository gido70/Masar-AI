"""مشاهد إعلان الحقيبة (0$)، بأدوات مشاهد الوحدة 8 نفسها (بلا تقريب، وسطر بجانب الصور التي فيها كتابة، وخط أميري)."""
import sys, os
sys.path.insert(0, '../ads-unit-8'); import make_scenes as M
R='../..'; A8='../ads-unit-8/_assets'
CERT=f'{R}/resources/ads/ads-certificate-sample.png'; CHECK=f'{R}/assets/pdfpages/ads_ads-unit-8/16.jpg'; PDF8=f'{R}/assets/pdfpages/ads_ads-unit-8/03.jpg'
M.TEXTY.update([CERT,CHECK,PDF8,f'{A8}/method-card.png',f'{A8}/costlog.png',f'{A8}/rejected.png',f'{A8}/phones3.png',f'{A8}/packages-4.png'])
U=M.U; L=M.LOOK
S={
 'promo-2':[(0,U(0,'broll-1a.mp4'),0.5,'قبل: مبهر… ولا يبقى منه شيء',''),(3.22,M.AD,6.0,'بعد: إعلان كامل','فكرة · بصيرة · رمز · صوت')],
 'promo-3':[(0,L[0],2.0,'تسع وحدات',''),(0.7,L[3],2.0,'تسع وحدات',''),(1.45,M.MAJ,0.5,'الفكرة والموجز','الوحدات 0–2'),(2.3,M.TEMPL,0,'الفكرة والموجز','الوحدات 0–2'),
            (3.21,M.SB,0,'اللقطات والصوت','الوحدات 3–6'),(4.1,M.POUR,0.5,'اللقطات والصوت','الوحدات 3–6'),(5.02,f'{A8}/phones3.png',0,'النسخ والبيع','الوحدتان 7 و8'),(6.3,f'{A8}/packages-4.png',0,'النسخ والبيع','الوحدتان 7 و8')],
 'promo-4':[(0,PDF8,0,'فيديو وملف لكل وحدة',''),(2.84,M.WB,0,'كراسة بأمثلة محلولة',''),(5.15,CHECK,0,'امتحان لكل وحدة',''),(6.57,f'{A8}/method-card.png',0,'بطاقة الطريقة',''),(9.17,CERT,0,'شهادة باسمك','')],
 'promo-5':[(0,M.STUDY,0,'دراسة محكّمة · 1999','إعلانات مطبوعة · الإبداع والتذكر لا المبيعات'),(4.04,f'{A8}/rejected.png',0,'إنتاج حقيقي بأخطائه',''),(8.22,f'{A8}/costlog.png',0,'وتكلفته','')],
}
if __name__=='__main__':
    for n in (sys.argv[1:] or S): M.scene(n, f'{n}.mp3', S[n])
