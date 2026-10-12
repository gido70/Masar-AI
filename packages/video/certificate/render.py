"""قالب شهادة حقيبة مسار الفيديو (2000×1414). التشغيل من هذا المجلد بعد نسخ masar_logo.png وخطوط studio/fonts إليه: python render.py"""
from playwright.sync_api import sync_playwright
import os
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':2000,'height':1414})
    pg.goto('file://'+os.path.abspath('cert.html'));pg.wait_for_timeout(600)
    pg.screenshot(path='cert.png');b.close()
