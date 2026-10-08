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


def main():
    # Pre-compile regex patterns once outside the loop to avoid re-compiling 3,000+ times across files
    patterns = []
    for icon, url in social.items():
        pattern = re.compile(rf'<a href="#"><i class="fab fa-{re.escape(icon)}"></i></a>')
        replacement = f'<a href="{url}" target="_blank" rel="noopener noreferrer"><i class="fab fa-{icon}"></i></a>'
        patterns.append((pattern, replacement))

    for label, page in labels.items():
        pattern_chevron = re.compile(
            rf'<a href="#"><i class="fas fa-chevron-right me-2"></i>{re.escape(label)}</a>'
        )
        replacement_chevron = f'<a href="../../pages/{page}"><i class="fas fa-chevron-right me-2"></i>{label}</a>'
        patterns.append((pattern_chevron, replacement_chevron))

        pattern_plain = re.compile(rf'<a href="#">{re.escape(label)}</a>')
        replacement_plain = f'<a href="../../pages/{page}">{label}</a>'
        patterns.append((pattern_plain, replacement_plain))

    for path in ROOT.glob('projects/*/index.html'):
        text = path.read_text(encoding='utf-8')
        # Fast pre-check: skip files that contain no unlinked anchor tags
        if 'href="#"' not in text:
            continue

        original = text
        for pattern, replacement in patterns:
            text = pattern.sub(replacement, text)

        if text != original:
            path.write_text(text, encoding='utf-8')

    print('rewired footer links with targeted replacements')


if __name__ == '__main__':
    main()
