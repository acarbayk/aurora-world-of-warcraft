"""Turn extracted column lines into clean paragraphs / Aurora description HTML."""
import re, pathlib
from collections import Counter
from xml.sax.saxutils import escape

PAGES = pathlib.Path("/home/claude/wow/pages")
_mode_cache = {}

SMALL = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with", "vs"}
ARTIST = re.compile(r"^[A-ZÀ-Ý’'\-]+(?: [A-ZÀ-Ý’'\-]+){1,3}(?:, BLIZZARD ARTIST)?$")


def indent(s):
    return len(s) - len(s.lstrip(" "))


def col_mode(page, col):
    key = (page, col)
    if key not in _mode_cache:
        txt = (PAGES / page).read_text().split("=====RIGHT=====")[col]
        c = Counter(indent(l) for l in txt.split("\n") if l.strip())
        _mode_cache[key] = c.most_common(1)[0][0] if c else 0
    return _mode_cache[key]


def is_label(text):
    """'Using a Higher-Level Spell Slot.' style run-in heading at para start."""
    m = re.match(r"^((?:[A-Z0-9][\w’'\-:]*|\(\w+\))(?: (?:[A-Z0-9(][\w’'\-:)]*|" +
                 "|".join(SMALL) + r"))*)\. (.*)$", text, re.S)
    if not m:
        return None
    words = m.group(1).split()
    if len(words) > 7:
        return None
    return m.group(1), m.group(2)


def clean(s):
    return (s.replace("⁠", "").replace("­", "").replace("——", "—")
             .replace("  ", " ").strip())


def paragraphs(lines):
    """lines: [page, col, text]. Returns list of paragraph strings."""
    paras = []
    cur = None
    for page, col, raw in lines:
        if not raw.strip():
            continue
        base = col_mode(page, col)
        ind = indent(raw)
        txt = clean(raw)
        if ind >= base + 8:          # captions floating over art
            continue
        if ARTIST.match(txt):        # artist credits
            continue
        new_para = (ind >= base + 2 or cur is None or
                    (is_label(txt) and cur.rstrip().endswith((".", ":"))))
        if new_para:
            if cur is not None:
                paras.append(cur)
            cur = txt
        else:
            if cur.endswith("-") and not cur.endswith(" -"):
                cur += txt
            else:
                cur += " " + txt
    if cur:
        paras.append(cur)
    return [clean(p) for p in paras]


def to_html(paras, first_indent=False):
    out = []
    for i, p in enumerate(paras):
        cls = ' class="indent"' if (i > 0 or first_indent) else ""
        lab = is_label(p)
        if lab:
            out.append(f"<p{cls}><strong><em>{escape(lab[0])}.</em></strong> {escape(lab[1])}</p>")
        else:
            out.append(f"<p{cls}>{escape(p)}</p>")
    return out


def plain(paras):
    return " ".join(paras)


def slug(name):
    s = name.upper().replace("’", "").replace("'", "")
    s = re.sub(r"[^A-Z0-9]+", "_", s).strip("_")
    return s
