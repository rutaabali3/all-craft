from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
social = {
    'facebook-f': 'https://www.facebook.com/',
    'twitter': 'https://twitter.com/',
    'instagram': 'https://www.instagram.com/',
    'linkedin-in': 'https://www.linkedin.com/',
    'youtube': 'https://www.youtube.com/',
}
labels = {
    'Careers': 'careers.html',
    'Press': 'press.html',
    'FAQ': 'faq.html',
    'Shipping': 'shipping.html',
    'Returns': 'returns.html',
    'Privacy Policy': 'privacy-policy.html',
    'Terms of Service': 'terms-of-service.html',
    'Cookie Policy': 'cookie-policy.html',
}

replacements = []
for icon, url in social.items():
    pattern = re.compile(rf'<a href="#"><i class="fab fa-{re.escape(icon)}"></i></a>')
    repl = f'<a href="{url}" target="_blank" rel="noopener noreferrer"><i class="fab fa-{icon}"></i></a>'
    replacements.append((pattern, repl))

for label, page in labels.items():
    pattern1 = re.compile(rf'<a href="#"><i class="fas fa-chevron-right me-2"></i>{re.escape(label)}</a>')
    repl1 = f'<a href="../../pages/{page}"><i class="fas fa-chevron-right me-2"></i>{label}</a>'
    replacements.append((pattern1, repl1))

    pattern2 = re.compile(rf'<a href="#">{re.escape(label)}</a>')
    repl2 = f'<a href="../../pages/{page}">{label}</a>'
    replacements.append((pattern2, repl2))

for path in ROOT.glob('projects/*/index.html'):
    text = path.read_text(encoding='utf-8')
    original = text
    for pattern, repl in replacements:
        text = pattern.sub(repl, text)
    if text != original:
        path.write_text(text, encoding='utf-8')
print('rewired footer links with targeted replacements')
