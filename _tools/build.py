#!/usr/bin/env python3
"""smokyDuck — builds the 6 pages + 404. Run: python3 build.py
Voices and work come from data/*.json, settings from assets/js/config.js."""
import json, os, html, datetime, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "https://smokyduckstudio.com/"
TODAY = datetime.date.today().isoformat()
E = html.escape
NAV = [("services.html", "Services"), ("voices.html", "Voices"), ("work.html", "Work"), ("contact.html", "Contact")]

ORG = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": BASE + "#org", "name": "SmokyDuck Studio", "alternateName": "SmokyDuck Studio – Indic & Global Multimedia Localization", "slogan": "Indic & Global Multimedia Localization",
       "url": BASE, "email": "hello@smokyduckstudio.com", "logo": BASE + "assets/img/logo-512.png",
       "description": "Hindi dubbing studio and Indian language localisation company: human voice-over, dubbing, translation, subtitling and e-learning localisation in all Indian languages, plus separate AI services.",
       "areaServed": ["IN", "GB", "US", "AE"], "knowsLanguage": ["hi","bn","mr","te","ta","gu","ur","kn","ml","or","pa","as","en"]}

def head(title, desc, path, extra=None, robots="index,follow"):
    url = BASE + ("" if path == "index.html" else path)
    ld = [ORG] + (extra or []) if path == "index.html" else (extra or [])
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in ld)
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0a0a">
<meta property="og:type" content="website"><meta property="og:site_name" content="SmokyDuck Studio – Indic &amp; Global Multimedia Localization">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/site.css?v=5">
{ldh}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="grain" aria-hidden="true"></div><div class="cursor" aria-hidden="true"></div>
"""

def nav(active):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<nav class="nav" aria-label="Main"><a class="logo" href="index.html">smoky<span class="d">D</span>uck.</a>
<div class="links">{links}</div><button class="menu-btn" type="button" aria-expanded="false" aria-controls="mmenu">Menu</button></nav>
<div class="mmenu" id="mmenu"><a href="index.html">Home</a>{mlinks}</div>
<main id="main">
"""

FOOT = """</main>
<footer id="contact"><div class="wrap">
<div class="rv"><h2>Ready to<br>go global?</h2>
<a class="mail u" data-email href="mailto:hello@smokyduckstudio.com">hello@smokyduckstudio.com</a>
<a class="wa u" href="https://wa.me/918866666447" target="_blank" rel="noopener">WhatsApp +91 88666 66447 →</a></div>
<div class="foot"><nav><a class="u" data-social="instagram" href="#">Instagram</a><a class="u" data-social="linkedin" href="#">LinkedIn</a><a class="u" data-social="youtube" href="#">YouTube</a><a class="u" href="legal.html">Privacy &amp; Terms</a></nav>
<span class="c">© <span data-year>2026</span> SmokyDuck Studio – Indic &amp; Global Multimedia Localization</span></div>
</div></footer>
<div class="consent" id="consent" role="dialog" aria-label="Cookies"><p style="margin:0">May we use Google Analytics to see which pages are useful? It sets cookies only if you allow it.</p>
<button class="btn" data-consent="yes" type="button">Allow</button><button class="btn" data-consent="no" type="button">No thanks</button></div>
<script src="assets/js/config.js?v=5"></script>
<script src="assets/js/site.js?v=5" defer></script>
<script src="assets/js/data.js?v=5" defer></script>
</body>
</html>
"""

def pagehead(label, h1, lede):
    return f'<header class="head"><div class="wrap rv"><p class="label">( {label} )</p><h1>{h1}</h1><p>{lede}</p></div></header>'

LANGS = "Hindi · Bengali · Marathi · Telugu · Tamil · Gujarati · Urdu · Kannada · Malayalam · Odia · Punjabi · Assamese · and every other Indian language, plus English"

SERVICES = [
    ("Voice-Over", "Real human voice artists in every Indian language — for commercials, e-learning, explainers, documentaries, IVR and corporate films. Cast, directed and delivered as finished audio.",
     ["Commercials and brand films", "E-learning and training", "Documentary narration", "IVR and announcements"]),
    ("Dubbing", "A Hindi dubbing studio that also dubs into every other Indian language. Human dubbing for films, series, animation and YouTube — performed by native voice actors, synced to picture and mixed for broadcast.",
     ["Films, series and OTT", "Animation and character voices", "YouTube and digital content", "Lip-sync and voice matching"]),
    ("Translation", "Professional translation and localisation between English and all Indian languages, by native linguists. Documents, websites, apps, scripts, courses and marketing — not just for voice-over.",
     ["Indian language localisation", "E-learning localisation", "Websites, apps and documents", "Marketing and transcreation"]),
    ("Subtitling", "Accurate, perfectly timed subtitles and clean transcripts in any Indian language, delivered with your project or on their own.",
     ["Subtitles in all Indian languages", "SRT and VTT files", "Transcription", "Burned-in captions for social"]),
]

AI_SERVICES = [
    ("AI Dubbing", "Rapid voice synthesis and lip-syncing for quick-turnaround projects."),
    ("AI Video Generation", "Localised visual assets and adaptations using generative models."),
    ("AI Assisted Translation", "Machine translation with our glossaries, for high volumes and tight budgets."),
]

FAQ = [
    ("Which languages do you work in?", "All Indian languages — including Hindi, Bengali, Marathi, Telugu, Tamil, Gujarati, Urdu, Kannada, Malayalam, Odia, Punjabi and Assamese — plus English. Tell us the pair you need."),
    ("Are your voice-overs done by real people?", "Yes. Our voice-over and dubbing services use real human voice artists only. AI voices are a separate service that you choose explicitly."),
    ("What's the difference between your human and AI services?", "Human services are performed by voice artists and linguists. AI services are faster and cheaper, for projects where speed and volume matter more than performance. They are quoted separately, and we never mix them without telling you."),
    ("Do you localise e-learning courses?", "Yes. E-learning localisation is a core service: translated course content, quizzes and on-screen text, plus human voice-over and subtitles, in any Indian language."),
    ("Do you translate without voice-over?", "Yes. Translation is a service on its own — documents, websites, apps, courses and marketing in any Indian language."),
    ("How do you price?", "Voice-over and dubbing per finished minute, translation per word. Send the script or file and we'll quote the same day where we can."),
    ("Will you sign an NDA?", "Yes, before you share any files."),
    ("Who owns the recordings?", "You do, once paid, for the usage agreed in the quote. We never clone or reuse a voice without the artist's written consent."),
]

def faq_html(items): return "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in items)
def faq_ld(items): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}

PAGES = {}

PAGES["index.html"] = lambda: head("SmokyDuck Studio – Indic & Global Multimedia Localization | Hindi Dubbing Studio",
    "SmokyDuck Studio is a Hindi dubbing studio and Indian language localisation company: human voice-over, dubbing, translation and e-learning localisation in every Indian language.", "index.html") + nav("") + f"""
<header class="hero"><div class="glow" aria-hidden="true"></div>
<h1 class="rv">smoky<span class="d">D</span>uck.</h1>
<p class="tagline rv">Indic &amp; Global Multimedia Localization</p>
<p class="tagline2 rv"><span>Global Voices.</span> <span>Human Craft.</span> <span>AI Speed.</span></p>
<p class="scroll" aria-hidden="true">Scroll to explore</p></header>

<section class="sec"><div class="wrap about">
<div><p class="label rv">( Who We Are )</p>
<h2 class="rv">SmokyDuck Studio is a Hindi dubbing studio and Indian language localisation company. Real voice artists and native linguists who make your content sound like it was made here — not translated.</h2></div>
<div class="reel big rv"><video controls playsinline preload="metadata" poster="assets/media/voices-reel.jpg" src="assets/media/voices-reel.mp4" aria-label="Gagan, co-founder, on SmokyDuck Studio"></video></div>
</div></section>

<section class="sec light"><div class="wrap">
<p class="label rv" style="color:#5f5f5a">( Human Studio )</p><h2 class="big rv">Our Services</h2>
<div class="rows rv">{"".join(f'<a class="row" href="services.html#{t.lower().replace("-","").replace(" ","")}"><span class="n">0{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></a>' for i,(t,d,_) in enumerate(SERVICES))}</div>
</div></section>

<section class="sec"><div class="wrap statement">
<p class="label rv">( Languages )</p>
<p class="langs rv">{LANGS}</p>
</div></section>

<section class="sec marq" style="border-top:1px solid var(--line)"><div class="bg" aria-hidden="true"><span>AI Studio • AI Studio • AI Studio • AI Studio •&nbsp;</span></div>
<div class="wrap two">
<div class="rv"><p class="label">( Separate from our human studio )</p><h2>The AI Advantage.</h2><p class="muted" style="font-size:20px;font-weight:300;max-width:440px">For projects where speed and volume matter most, we run a separate set of AI services — clearly labelled and quoted on their own.</p>
<a class="btn" href="services.html#ai" style="margin-top:20px">AI services</a></div>
<div class="ai-list rv">{"".join(f'<div><h4>{i+1}. {t}</h4><p class="muted">{d}</p></div>' for i,(t,d) in enumerate(AI_SERVICES))}</div>
</div></section>

""" + FOOT

PAGES["services.html"] = lambda: head("Hindi Dubbing, Voice-Over & E-learning Localisation | SmokyDuck Studio – Indic & Global Multimedia Localization",
    "Hindi dubbing, voice-over, translation, subtitling and e-learning localisation in all Indian languages by real voice artists and native linguists, plus separate AI services.", "services.html", [faq_ld(FAQ)]) + nav("services.html") + \
    pagehead("Services", "What we <em>do.</em>", "Two studios. Our human studio — real voice artists and native linguists in every Indian language. And a separate AI studio for speed and scale.") + f"""
<section class="sec light"><div class="wrap"><p class="label rv" style="color:#5f5f5a">( Human Studio )</p><h2 class="big rv" style="font-size:clamp(44px,6vw,84px)">Real people.</h2><div class="rows">
{"".join(f'<div class="row rv" id="{t.lower().replace("-","").replace(" ","")}"><span class="n">0{i+1}</span><div><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in l)}</ul></div></div>' for i,(t,d,l) in enumerate(SERVICES))}
</div></div></section>
<section class="sec" id="ai"><div class="wrap two">
<div class="rv"><p class="label">( AI Studio )</p><h2>AI services.</h2><p class="muted" style="font-size:20px;font-weight:300;max-width:440px">A separate offering for fast, high-volume work. Quoted on its own and never mixed into our human services without your say.</p></div>
<div class="ai-list rv">{"".join(f'<div><h4>{i+1}. {t}</h4><p class="muted">{d}</p></div>' for i,(t,d) in enumerate(AI_SERVICES))}</div>
</div></section>
<section class="sec" style="border-top:1px solid var(--line)"><div class="wrap statement">
<p class="label rv">( Questions )</p>
<div class="rv">{faq_html(FAQ)}</div>
</div></section>
""" + FOOT

PAGES["voices.html"] = lambda: head("Voices of Our Artists | SmokyDuck Studio – Indic & Global Multimedia Localization",
    "Choose a voice and listen live: real human voice artists from SmokyDuck Studio across Indian languages.", "voices.html") + nav("voices.html") + \
    pagehead("Voices", "Voices of our <em>artists.</em>", "Pick a voice and press play.") + """
<section class="sec" style="padding-top:72px"><div class="wrap">
<div class="picker rv">
<label class="label" for="voice-select">( Choose a voice )</label>
<div class="picker-row"><select id="voice-select" aria-label="Choose a voice"></select>
<button class="play big" id="voice-play" type="button" aria-label="Play selected voice"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg></button></div>
<p class="picker-meta" id="voice-meta"></p>
<div class="picker-bar"><i id="voice-progress"></i></div>
</div>
<p class="muted rv" style="margin-top:72px">Need a specific voice, language or age? <a class="u" href="contact.html">Tell us</a> and we'll cast it.<br>Are you a voice artist? <a class="u" href="contact.html?formType=Artist">Send us your demo.</a></p>
</div></section>
<script>
(function(){var sel=document.getElementById("voice-select"),btn=document.getElementById("voice-play"),meta=document.getElementById("voice-meta"),bar=document.getElementById("voice-progress"),a=new Audio(),list=[];
var P='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>',S='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';
function show(){var v=list[sel.selectedIndex];if(!v)return;meta.textContent=[v.gender,v.languages,v.style].filter(Boolean).join("  ·  ");}
fetch("data/voices.json",{cache:"no-cache"}).then(function(r){return r.json()}).then(function(d){list=d.voices||[];sel.innerHTML=list.map(function(v,i){return '<option value="'+i+'">'+v.name+(v.gender?" — "+v.gender:"")+'</option>'}).join("");show();});
sel.addEventListener("change",function(){a.pause();a.removeAttribute("src");bar.style.width="0";show();btn.click();});
btn.addEventListener("click",function(){var v=list[sel.selectedIndex];if(!v)return;if(!a.src||a.src.indexOf(v.src)<0){a.src=v.src;}
if(a.paused){document.querySelectorAll("video,audio").forEach(function(m){m.pause()});a.play();}else a.pause();});
a.addEventListener("play",function(){btn.innerHTML=S;btn.classList.add("on")});a.addEventListener("pause",function(){btn.innerHTML=P;btn.classList.remove("on")});
a.addEventListener("ended",function(){btn.innerHTML=P;btn.classList.remove("on");bar.style.width="0"});
a.addEventListener("timeupdate",function(){bar.style.width=(a.currentTime/(a.duration||1)*100)+"%"});})();
</script>
""" + FOOT

PAGES["work.html"] = lambda: head("Portfolio: Hindi Dubbing & Voice-Over Samples | SmokyDuck Studio – Indic & Global Multimedia Localization",
    "Watch and listen: Hindi dubbing, animation dubbing, commercials and narration by the SmokyDuck Studio team.", "work.html") + nav("work.html") + \
    pagehead("Portfolio", "Featured <em>Projects.</em>", "Hindi dubbing, animation, commercials and narration by our team. Real voices, real projects.") + """
<section class="sec" style="padding-top:80px"><div class="wrap"><div data-work="all"></div></div></section>
""" + FOOT

NEEDS = ["Voice-over (human)", "Dubbing (human)", "Translation", "Subtitling", "AI services", "Something else"]
PAGES["contact.html"] = lambda: head("Contact | SmokyDuck Studio – Indic & Global Multimedia Localization",
    "Get a quote for voice-over, dubbing, translation or subtitling in any Indian language. Email, WhatsApp or send us your brief.", "contact.html") + nav("contact.html") + \
    pagehead("Contact", "Let's <em>talk.</em>", "Tell us what you're making. We'll reply with a price and a plan.") + f"""
<section class="sec light"><div class="wrap contact">
<div class="ways rv"><p class="label">( Write or call )</p>
<a class="u" data-email href="mailto:hello@smokyduckstudio.com">hello@smokyduckstudio.com</a><br>
<a class="u" href="https://wa.me/918866666447" target="_blank" rel="noopener">+91 88666 66447</a><br><span class="muted" style="font-size:14px">WhatsApp or call</span></div>
<form class="form rv" data-sd-form novalidate>
<input type="hidden" name="formType" value="Quote"><label class="hp" aria-hidden="true">Leave empty<input name="website_hp" tabindex="-1" autocomplete="off"></label>
<div class="f2"><div><label for="c-name">Name *</label><input id="c-name" name="name" autocomplete="name" required></div>
<div><label for="c-email">Email *</label><input id="c-email" name="email" type="email" autocomplete="email" required></div></div>
<div class="f2"><div><label for="c-company">Company</label><input id="c-company" name="company" autocomplete="organization"></div>
<div><label for="c-need">What do you need?</label><select id="c-need" name="services">{"".join(f"<option>{n}</option>" for n in NEEDS)}</select></div></div>
<div class="f2"><div><label for="c-lang">Languages</label><input id="c-lang" name="targetLanguages" placeholder="e.g. English → Tamil, Bengali"></div>
<div><label for="c-voice">Voice (optional)</label><input id="c-voice" name="voice" placeholder="A voice from our roster, or the sound you want"></div></div>
<div><label for="c-msg">Tell us about the project *</label><textarea id="c-msg" name="message" required placeholder="Length, deadline, where it will be used, a link to the script or video…"></textarea></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required><span>I agree SmokyDuck Studio may keep these details to reply to me (<a href="legal.html">privacy</a>).</span></label>
<div class="status" role="status" aria-live="polite"></div>
<div><button class="btn" type="submit">Send</button></div>
</form></div></section>
""" + FOOT

PAGES["legal.html"] = lambda: head("Privacy & Terms | SmokyDuck Studio – Indic & Global Multimedia Localization", "How SmokyDuck Studio handles your data, and the terms for our services.", "legal.html") + nav("") + \
    pagehead("Legal", "Privacy &amp; <em>Terms.</em>", f"Last updated {TODAY}.") + """
<section class="sec" style="padding-top:40px"><div class="wrap prose">
<h2>Privacy</h2>
<p>SmokyDuck Studio runs smokyduckstudio.com. Questions about your data: hello@smokyduckstudio.com.</p>
<p><strong>What we collect.</strong> What you send through the contact form or by email or WhatsApp (your name, email, company and project details), and the files you share for a project. If you allow it, Google Analytics records anonymous page visits.</p>
<p><strong>Why.</strong> To reply to you, quote, deliver and invoice work. We don't sell your data or add you to mailing lists.</p>
<p><strong>Who sees it.</strong> Our team, and the voice artists or linguists working on your project under confidentiality. We use Google (email, Drive, Sheets) and GitHub Pages (hosting) to run the business.</p>
<p><strong>Voice artists.</strong> We never publish, share or clone an artist's voice without their written consent.</p>
<p><strong>Your rights.</strong> You can ask us to show, correct or delete your data at any time, under India's DPDP Act 2023, the UK GDPR or the EU GDPR. We reply within 30 days.</p>
<p><strong>Cookies.</strong> The site works without cookies. Analytics cookies are set only if you choose “Allow”.</p>
<h2>Terms</h2>
<p><strong>Quotes.</strong> Each project's scope, price, deadline and usage rights are set out in its quote, valid for 30 days.</p>
<p><strong>Your material.</strong> You confirm you have the right to give us the scripts and media for the work.</p>
<p><strong>Usage.</strong> Recordings are licensed for the media, region and period in the quote. Wider use needs a new licence. Recordings may not be used to train AI or create a synthetic voice without the artist's written consent.</p>
<p><strong>Ownership.</strong> Once paid in full, the delivered files are yours, within the agreed usage.</p>
<p><strong>Confidentiality.</strong> We keep your files private and will sign your NDA.</p>
<p><strong>Liability.</strong> Our liability for a project is limited to its fee. These terms are governed by the laws of India.</p>
</div></section>
""" + FOOT

def notfound():
    s = head("Page not found | SmokyDuck Studio – Indic & Global Multimedia Localization", "This page doesn't exist.", "404.html", robots="noindex") + nav("") + \
        pagehead("404", "Dead <em>air.</em>", 'This page doesn\'t exist. <a class="u" href="index.html" style="color:#f4f4f0">Back home →</a>') + FOOT
    s = re.sub(r'(href|src)="(?!https?:|mailto:|#|/)([^"]+)"', r'\1="/\2"', s)
    return s
PAGES["404.html"] = notfound

if __name__ == "__main__":
    for p, fn in PAGES.items():
        open(os.path.join(OUT, p), "w", encoding="utf-8").write(fn())
    urls = [p for p in PAGES if p != "404.html"]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f'  <url><loc>{BASE}{"" if p=="index.html" else p}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    print("built", len(PAGES), "pages")
