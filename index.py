import re
import html as _html
import streamlit as st
import llm_call

st.set_page_config(
    page_title="MenuMind AI",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&family=Space+Mono:wght@400&display=swap');

:root {
    --obsidian:   #0D0D0D;
    --charcoal:   #1C1C1C;
    --panel:      #222222;
    --border:     #2E2E2E;
    --border-mid: #3A3A3A;
    --gold:       #C9A84C;
    --gold-dim:   #8A6F2E;
    --gold-light: #E2C97E;
    --ivory:      #F5F0E8;
    --ivory-dim:  #A09888;
    --muted:      #706860;
}

.stApp { background-color: var(--obsidian); color: var(--ivory); }

#MainMenu,
footer,
.stAppDeployButton {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 800px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111 !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--ivory-dim) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #1a1a1a !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--ivory) !important;
    border-radius: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}
.sidebar-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.55rem;
    font-weight: 300;
    color: var(--ivory);
    letter-spacing: 0.1em;
}
.sidebar-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    margin-bottom: 1.5rem;
}
.sidebar-list {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    color: #484848;
    text-transform: uppercase;
    line-height: 2.3;
    margin-top: 1.5rem;
}

/* Masthead */
.masthead {
    text-align: center;
    padding: 2rem 0 1.75rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.25rem;
}
.masthead-eye {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.3em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.masthead-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: var(--ivory);
    letter-spacing: 0.05em;
    line-height: 1.1;
    margin: 0;
}
.masthead-title em { color: var(--gold); font-style: italic; }
.masthead-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    font-weight: 300;
    color: var(--muted);
    margin-top: 0.55rem;
    letter-spacing: 0.04em;
}

/* Cover card */
.cover-card {
    border: 1px solid var(--gold-dim);
    border-radius: 2px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    position: relative;
    margin-bottom: 2.5rem;
    background: #0f0e0b;
}
.cover-card::before {
    content: '';
    position: absolute;
    inset: 6px;
    border: 1px solid rgba(139,111,46,0.22);
    border-radius: 1px;
    pointer-events: none;
}
.cover-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.35em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.cover-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 300;
    color: var(--ivory);
    letter-spacing: 0.07em;
    line-height: 1.15;
    margin: 0 0 0.85rem;
}
.cover-concept {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 0.92rem;
    color: var(--muted);
    line-height: 1.7;
    max-width: 440px;
    margin: 0 auto 1.1rem;
}
.cover-cuisine {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1rem;
    color: var(--gold-light);
    letter-spacing: 0.07em;
}
.cover-ornament {
    color: var(--gold-dim);
    font-size: 0.9rem;
    margin: 0.9rem 0 0;
    opacity: 0.7;
    letter-spacing: 0.55em;
}

/* Section label */
.sec-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.3em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin: 0 0 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Menu cards */
.menu-grid {
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.menu-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.4rem 1.6rem;
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
    transition: border-color 0.2s;
}
.menu-card:hover { border-color: var(--border-mid); }
.menu-index {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 300;
    color: var(--gold-dim);
    line-height: 1;
    min-width: 28px;
    padding-top: 2px;
    user-select: none;
}
.menu-body { flex: 1; }
.menu-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    font-weight: 400;
    color: var(--gold-light);
    letter-spacing: 0.03em;
    margin: 0 0 0.45rem;
    line-height: 1.3;
}
.menu-desc {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem;
    font-weight: 300;
    color: var(--ivory-dim);
    line-height: 1.75;
    margin: 0;
}

/* Footer rule */
.footer-rule {
    border: none;
    border-top: 1px solid var(--border);
    margin: 3rem 0 1.5rem;
}
.footer-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    color: #383830;
    text-align: center;
    text-transform: uppercase;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--obsidian); }
::-webkit-scrollbar-thumb { background: var(--border-mid); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


def parse_name(raw: str) -> tuple[str, str]:
    clean = re.sub(r'\*{1,3}', '', raw).strip()
    lines = [l.strip() for l in clean.splitlines() if l.strip()]
    return (lines[0], " ".join(lines[1:])) if len(lines) > 1 else (lines[0] if lines else clean, "")


def parse_menu_items(menu_text: str) -> list[dict]:
    """
    Parse numbered menu items from LLM output.
    Each item is expected in the format:
      1. **Menu Name** - Description of the menu
    Returns a list of dicts with "name" and "desc" keys.
    """
    if not menu_text or not menu_text.strip():
        return []

    lines = menu_text.strip().splitlines()
    item_pattern = re.compile(r'^\s*(?:\d+[\.\)]|[-*+])\s+')

    # Drop everything before the first item marker.
    start = next((i for i, l in enumerate(lines) if item_pattern.match(l)), 0)
    lines = lines[start:]

    items = []
    current_item = None
    current_desc_lines: list[str] = []

    for line in lines:
        if not line.strip():
            continue

        if item_pattern.match(line):
            if current_item is not None:
                name, desc = split_name_desc(current_item)
                extra_desc = " ".join(dl.strip() for dl in current_desc_lines if dl.strip())
                if desc and extra_desc:
                    desc = f"{desc} {extra_desc}"
                elif not desc:
                    desc = extra_desc
                items.append({"name": name, "desc": desc})

            current_item = item_pattern.sub('', line).strip()
            current_desc_lines = []
        else:
            if current_item is not None:
                current_desc_lines.append(line.strip())

    if current_item is not None:
        name, desc = split_name_desc(current_item)
        extra_desc = " ".join(dl.strip() for dl in current_desc_lines if dl.strip())
        if desc and extra_desc:
            desc = f"{desc} {extra_desc}"
        elif not desc:
            desc = extra_desc
        items.append({"name": name, "desc": desc})

    if not items:
        name, desc = split_name_desc(menu_text.strip())
        return [{"name": name or "Menu", "desc": desc}]

    return items


def split_name_desc(raw: str) -> tuple[str, str]:
    """Split a menu line into (name, description) using heuristics."""
    raw = raw.strip()
    if not raw:
        return "", ""

    # Already formatted with bold item text
    # Try: **name** description (closing asterisks present, then description)
    m = re.match(r'^\*{1,2}(.+?)\*{1,2}\s+(.+)$', raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    
    # Try: **name** or **name (closing asterisks present, no description)
    m = re.match(r'^\*{1,2}(.+?)(?:\*{1,2})?\s*$', raw)
    if m:
        return m.group(1).strip(), ""

    # Explicit separators are often a reliable name/description boundary.
    separator_match = re.split(r'\s+(?:[-–—:])\s+', raw, maxsplit=1)
    if len(separator_match) == 2:
        return separator_match[0].strip(), separator_match[1].strip()

    if '  ' in raw:
        left, right = raw.split('  ', 1)
        return left.strip(), right.strip()

    # If the whole line reads like a menu item with ingredients, keep it as the title.
    words = raw.split()
    if len(words) <= 5:
        return raw, ""

    # If the line is longer and contains common connectors, treat it as a full item name.
    if re.search(r'\b(with|in|of|on|over|and|&|with a|with an|served with|topped with)\b', raw, flags=re.IGNORECASE):
        return raw, ""

    # Try to split when there is a clear description start.
    name_extenders = {'with', 'in', 'of', 'on', 'over', 'and', '&'}
    hard_starters = {
        'slow','rich','tender','crispy','fresh','delicate','silky','velvety',
        'marinated','grilled','infused','topped','garnished','served','made',
        'braised','stuffed','filled','drizzled','fried','steamed','baked',
        'roasted','coated','poached','smoked','spiced','seasoned',
        'featuring','accompanied','finished','paired','studded','glazed',
    }

    for i in range(3, min(12, len(words))):
        w = words[i].lower().rstrip(',-')
        if w in name_extenders:
            continue
        if w in hard_starters or (w.endswith('ed') and i >= 3) or (words[i] in {'A','An','The'} and i >= 3):
            return " ".join(words[:i]), " ".join(words[i:])

    for i in range(4, min(10, len(words))):
        w = words[i].lower().rstrip(',-')
        if words[i][0].islower() and w not in name_extenders:
            return " ".join(words[:i]), " ".join(words[i:])

    return raw, ""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">MenuMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">AI Restaurant Identity Studio</div>', unsafe_allow_html=True)
    st.markdown("---")
    cuisine = st.selectbox("Cuisine", ["Indian", "Italian", "Chinese", "Mexican", "Japanese"])
    st.markdown("""
    <div class="sidebar-list">
    — Generates<br>Restaurant name<br>Brand concept<br>Curated menu
    </div>""", unsafe_allow_html=True)

# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-eye">AI · Culinary Identity Studio</div>
    <h1 class="masthead-title">Menu<em>Mind</em></h1>
    <p class="masthead-sub">Generate luxury restaurant identities and culinary frameworks in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── Main ───────────────────────────────────────────────────────────────────────
if cuisine:
    with st.spinner(f"Crafting your {cuisine} identity..."):
        result = llm_call.resturant_name_and_menu(cuisine)

    name, concept = parse_name(result['restaurant_name'])
    name_s    = _html.escape(name)
    concept_s = _html.escape(concept)
    cuisine_s = _html.escape(cuisine)

    concept_block = f'<div class="cover-concept">{concept_s}</div>' if concept_s else ""

    # Cover card
    st.markdown(f"""
    <div class="cover-card">
        <div class="cover-label">Your Restaurant</div>
        <div class="cover-name">{name_s}</div>
        {concept_block}
        <div class="cover-cuisine">{cuisine_s} Cuisine</div>
        <div class="cover-ornament">✦ &nbsp; ✦ &nbsp; ✦</div>
    </div>
    """, unsafe_allow_html=True)

    # Menu section label
    st.markdown('<div class="sec-label">Curated Menu</div>', unsafe_allow_html=True)

    # Menu cards — each card shows menu name as title and menu desc as description
    items = parse_menu_items(result['menu'])
    cards_html = '<div class="menu-grid">'
    for i, item in enumerate(items, 1):
        n = _html.escape(item['name'])
        d = _html.escape(item['desc'])
        cards_html += f"""
        <div class="menu-card">
            <div class="menu-index">{i:02d}</div>
            <div class="menu-body">
                <div class="menu-name">{n}</div>
                <p class="menu-desc">{d}</p>
            </div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


    # Footer
    st.markdown(f"""
    <hr class="footer-rule">
    <div class="footer-text">{name_s} &nbsp;·&nbsp; {cuisine_s} Cuisine &nbsp;·&nbsp; MenuMind AI</div>
    """, unsafe_allow_html=True)