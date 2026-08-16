from pathlib import Path
from bs4 import BeautifulSoup
import html

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"
PAGES.mkdir(exist_ok=True)

PAGE_STYLE = """
:root { --ink:#243447; --muted:#617184; --line:#dbe4ec; --brand:#2f6fed; --accent:#e95d8a; --paper:#f7fafc; }
* { box-sizing:border-box; }
body { margin:0; font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:linear-gradient(135deg,#f7fbff,#fff7fa); line-height:1.7; }
.site-header { background:linear-gradient(120deg,#dcecff,#ffe2ed); border-bottom:1px solid var(--line); }
.nav { max-width:1120px; margin:auto; padding:18px 24px; display:flex; justify-content:space-between; gap:20px; align-items:center; flex-wrap:wrap; }
.brand { color:var(--ink); text-decoration:none; font-weight:800; letter-spacing:.02em; }
.nav-links { display:flex; gap:16px; flex-wrap:wrap; }
.nav-links a { color:var(--ink); text-decoration:none; font-size:.95rem; }
.nav-links a:hover { color:var(--brand); }
.container { max-width:900px; margin:0 auto; padding:64px 24px 80px; }
.eyebrow { color:var(--brand); font-weight:700; text-transform:uppercase; letter-spacing:.12em; font-size:.75rem; }
h1 { font-size:clamp(2rem,5vw,3.4rem); line-height:1.1; margin:.5rem 0 1rem; }
h2 { margin-top:2.2rem; line-height:1.25; }
.lede { color:var(--muted); font-size:1.1rem; max-width:700px; }
.card { background:rgba(255,255,255,.82); border:1px solid var(--line); border-radius:18px; padding:26px; margin:18px 0; box-shadow:0 14px 34px rgba(35,64,95,.06); }
.card h3 { margin-top:0; }
a { color:var(--brand); }
.site-footer { border-top:1px solid var(--line); background:#eef5fb; padding:28px 24px; color:var(--muted); }
.footer-inner { max-width:1120px; margin:auto; display:flex; justify-content:space-between; gap:18px; flex-wrap:wrap; }
.footer-inner a { margin-right:14px; }
@media (max-width:640px) { .container { padding-top:42px; } .nav { padding:16px; } }
"""
(PAGES / "styles.css").write_text(PAGE_STYLE.strip() + "\n", encoding="utf-8")

content = {
    "privacy-policy": ("Privacy Policy", "How we handle information when you browse All Craft.", [
        ("Information we collect", "All Craft is a static product showcase. We do not ask you to create an account or submit payment details through these pages. If you contact us, we may receive the information you choose to include in your message, such as your name, email address, and request details."),
        ("How information is used", "Information submitted through a contact channel is used only to respond to the request, provide support, and improve the site. We do not sell personal information or use it for unrelated marketing without an appropriate consent mechanism."),
        ("Cookies and third-party services", "The site may load third-party libraries, fonts, icons, or media services. Those providers may process limited technical information under their own policies. See the Cookie Policy for more detail."),
        ("Your choices", "You may request clarification about information you have shared with us or ask that a support conversation be deleted, subject to records we must retain for legitimate operational or legal reasons."),
    ]),
    "terms-of-service": ("Terms of Service", "The terms that apply to use of the All Craft product showcase.", [
        ("Use of the site", "You may browse, link to, and use this site for lawful informational purposes. You must not interfere with site operation, attempt unauthorized access, scrape in a way that harms availability, or use the site to mislead others."),
        ("Product information", "Product descriptions, images, availability, pricing examples, and other content are provided for presentation and may change without notice. A product page is not a payment or fulfillment contract unless a separate checkout explicitly states otherwise."),
        ("Intellectual property", "The site structure, original copy, branding, and visual assets are protected by applicable intellectual-property laws. Third-party marks remain the property of their respective owners."),
        ("Disclaimer and changes", "The site is provided on an as-available basis. We may update content, features, or these terms as the project evolves. Continued use after an update constitutes acceptance of the revised terms where permitted by law."),
    ]),
    "cookie-policy": ("Cookie Policy", "A plain-language explanation of cookies and similar technologies.", [
        ("What cookies are", "Cookies are small text files stored by a browser. Similar technologies can remember preferences, support basic functionality, or provide aggregate technical information."),
        ("How we use them", "All Craft aims to use only the storage needed for site functionality and user preferences. Embedded third-party services may set their own cookies when loaded; those services control their own cookie behavior."),
        ("Managing cookies", "You can block or remove cookies through your browser settings. Blocking some cookies may affect preferences or embedded content, but the main static pages should remain accessible."),
    ]),
    "faq": ("Frequently Asked Questions", "Answers to common questions about the All Craft catalog.", [
        ("Can I purchase directly from these pages?", "These pages are primarily a catalog and product-information experience. Follow an explicitly provided product or contact link for the current purchasing route."),
        ("Are prices guaranteed?", "No. Where a page shows a starting price, it is an illustrative catalog value and may not reflect current availability, taxes, shipping, or seller pricing."),
        ("How can I request help?", "Use the Contact section on a product page or the contact details shown in the site footer. Include the product name and the issue so the request can be routed efficiently."),
        ("Where are shipping and return rules?", "See the Shipping and Returns pages for the general information currently published by All Craft. Seller-specific rules may override general catalog guidance."),
    ]),
    "shipping": ("Shipping Information", "General guidance for delivery questions and order support.", [
        ("Delivery estimates", "Delivery timing depends on the seller, destination, stock status, and shipping method shown at checkout. Treat any estimate as a planning guide rather than a guarantee."),
        ("Address accuracy", "Check the shipping address before submitting an order through the relevant seller. Contact the seller promptly if an address needs correction after submission."),
        ("Delays or damage", "For a delayed, missing, or damaged parcel, keep the packaging and order information and contact the seller or carrier using the order-specific support route."),
    ]),
    "returns": ("Returns and Refunds", "General guidance for product returns and refund requests.", [
        ("Seller policy controls", "Return windows, eligibility, restocking charges, and refund timing are determined by the seller and the order channel. Review the policy shown before completing a purchase."),
        ("Starting a return", "Use the seller’s order support process and include the order number, product name, reason for return, and photographs where damage or incorrect fulfillment is involved."),
        ("Condition and packaging", "Unless the seller states otherwise, keep the item, accessories, and packaging in the condition required by the applicable return policy."),
    ]),
    "careers": ("Careers", "Opportunities to contribute to the All Craft project.", [
        ("Current status", "All Craft is an evolving catalog project. If a role is available, it will be announced through the project’s official contact channels rather than through an unverified third-party listing."),
        ("Expressing interest", "For general collaboration or portfolio inquiries, use the Contact section on a product page and describe your skills, availability, and the type of work you would like to support."),
    ]),
    "press": ("Press and Media", "Reference information for journalists, creators, and partners.", [
        ("About the project", "All Craft is a structured showcase of stationery, office, school, and craft products, organized into focused subprojects with topic-specific visual assets."),
        ("Media requests", "For interviews, corrections, attribution questions, or partnership requests, use the site contact route and include the publication, deadline, and specific material requested."),
    ]),
    "sitemap": ("Sitemap", "A directory of the main pages available across the All Craft project.", [
        ("Core pages", "<a href=\"../index.html\">All Craft home</a> · <a href=\"privacy-policy.html\">Privacy Policy</a> · <a href=\"terms-of-service.html\">Terms of Service</a> · <a href=\"cookie-policy.html\">Cookie Policy</a> · <a href=\"faq.html\">FAQ</a>"),
        ("Support pages", "<a href=\"shipping.html\">Shipping</a> · <a href=\"returns.html\">Returns</a> · <a href=\"careers.html\">Careers</a> · <a href=\"press.html\">Press</a>"),
        ("Product catalog", "Browse the product directories under <code>projects/</code> from the All Craft home page. Each subproject includes links back to its sections and the shared informational pages."),
    ]),
}


def page_html(slug, title, lede, sections):
    cards = "\n".join(f'<section class="card"><h2>{heading}</h2><p>{body}</p></section>' for heading, body in sections)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | All Craft</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header"><nav class="nav"><a class="brand" href="../index.html">All Craft</a><div class="nav-links"><a href="../index.html">Home</a><a href="faq.html">FAQ</a><a href="shipping.html">Shipping</a><a href="returns.html">Returns</a><a href="privacy-policy.html">Privacy</a><a href="terms-of-service.html">Terms</a></div></nav></header>
<main class="container"><div class="eyebrow">All Craft information</div><h1>{html.escape(title)}</h1><p class="lede">{html.escape(lede)}</p>{cards}</main>
<footer class="site-footer"><div class="footer-inner"><span>© 2026 All Craft</span><span><a href="privacy-policy.html">Privacy</a><a href="terms-of-service.html">Terms</a><a href="cookie-policy.html">Cookies</a><a href="sitemap.html">Sitemap</a></span></div></footer>
</body></html>'''

for slug, (title, lede, sections) in content.items():
    (PAGES / f"{slug}.html").write_text(page_html(slug, title, lede, sections), encoding="utf-8")

social = {
    "facebook-f": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "instagram": "https://www.instagram.com/",
    "linkedin-in": "https://www.linkedin.com/",
    "youtube": "https://www.youtube.com/",
}
text_targets = {
    "Careers": "careers.html",
    "Press": "press.html",
    "FAQ": "faq.html",
    "Shipping": "shipping.html",
    "Returns": "returns.html",
    "Privacy Policy": "privacy-policy.html",
    "Terms of Service": "terms-of-service.html",
    "Cookie Policy": "cookie-policy.html",
}

for html_path in ROOT.glob("projects/*/index.html"):
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    changed = False
    for anchor in soup.find_all("a", href="#"):
        icon = anchor.find("i")
        icon_classes = set(icon.get("class", [])) if icon else set()
        href = None
        for key, target in social.items():
            if f"fa-{key}" in icon_classes:
                href = target
                anchor["target"] = "_blank"
                anchor["rel"] = ["noopener", "noreferrer"]
                break
        if href is None:
            label = " ".join(anchor.stripped_strings)
            for text, target in text_targets.items():
                if label == text:
                    href = f"../../pages/{target}"
                    break
        if href:
            anchor["href"] = href
            changed = True
    if changed:
        html_path.write_text(str(soup), encoding="utf-8")

print(f"created {len(content)} site pages and rewired project footers")
