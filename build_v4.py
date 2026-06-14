"""
build_v4.py  –  enciclopedia_progresiva_metal_gear_v4.html
  • Cada segmento muestra el artwork de SU juego (mg1 en el de mg, mgs3 en el de mgs3…)
  • Panel derecho compacto: cabe sin scroll en cualquier pantalla normal
  • Panel izquierdo: bordes correctos de punta a punta
"""

import os, base64, re, io, sys
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')

CHARS_DIR = "C:/Users/algpa/Desktop/croquis_metal-gear/wiki_chars"
HTML_IN   = "C:/Users/algpa/Desktop/croquis_metal-gear/enciclopedia_progresiva_metal_gear.html"
HTML_OUT  = "C:/Users/algpa/Desktop/croquis_metal-gear/index.html"

# ── Funciones base64 ─────────────────────────────────────────────────────
def make_img_tag(fname, w, h, cls, pixelated=False):
    """Cover-crop al tamaño w×h (encode a 2×). Para retratos de personaje."""
    fpath = f"{CHARS_DIR}/{fname}"
    if not os.path.exists(fpath):
        print(f"  FALTA: {fname}")
        return ""
    img = Image.open(fpath)
    if img.mode == 'P':    img = img.convert('RGBA')
    if img.mode not in ('RGB','RGBA'): img = img.convert('RGB')
    tw, th = w*2, h*2
    ia = img.width / img.height
    ta = tw / th
    rsmp = Image.NEAREST if pixelated else Image.LANCZOS
    if ia > ta:
        nh = th; nw = int(nh * ia)
    else:
        nw = tw; nh = int(nw / ia)
    img = img.resize((nw, nh), rsmp)
    left = (nw - tw) // 2
    vtop = max(0, int((nh - th) * 0.22))
    img  = img.crop((left, vtop, left+tw, vtop+th))
    buf  = io.BytesIO()
    ext  = fname.lower().rsplit('.',1)[-1]
    if ext in ('png','gif') or pixelated:
        img.convert('RGBA').save(buf, 'PNG', optimize=True); mime = 'image/png'
    else:
        img.convert('RGB').save(buf, 'JPEG', quality=78, optimize=True); mime = 'image/jpeg'
    b64 = base64.b64encode(buf.getvalue()).decode()
    pix_style = ' style="image-rendering:pixelated"' if pixelated else ''
    return f'<img class="{cls}"{pix_style} src="data:{mime};base64,{b64}">'

def make_img_contain(fname, size, cls):
    """Contain (sin recorte) dentro de un canvas cuadrado transparente. Para logos."""
    fpath = f"{CHARS_DIR}/{fname}"
    if not os.path.exists(fpath):
        print(f"  FALTA: {fname}")
        return ""
    img = Image.open(fpath).convert('RGBA')
    tw = th = size * 2
    ia = img.width / img.height
    if ia > 1:      nw = tw; nh = int(nw / ia)
    else:           nh = th; nw = int(nh * ia)
    img = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    canvas.paste(img, ((tw - nw) // 2, (th - nh) // 2), img)
    buf = io.BytesIO()
    canvas.save(buf, 'PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img class="{cls}" src="data:image/png;base64,{b64}">'

# ── Mapa: (nombre_personaje, game_id) → archivo ─────────────────────────
SEG_PORTRAITS = {
    # Big Boss
    ("Big Boss", "mg"):    "mg__Big_Boss_(MG).jpg",
    ("Big Boss", "mg2"):   "mg2__Big_Boss_(MG2).gif",
    ("Big Boss", "mgs3"):  "mgs3__MGS3_Big_Boss_Artwork.jpg",
    ("Big Boss", "po"):    "po__SnakeFOX.jpg",
    ("Big Boss", "pw"):    "pw__Mgspw-naked-snake-cg.jpg",
    ("Big Boss", "mgs4"):  "mgs4__Big_Boss_MGS4_infobox.png",
    ("Big Boss", "gz"):    "gz__Big_Boss_GZ.jpg",
    ("Big Boss", "tpp"):   "tpp__Big_Boss_TPP.jpg",
    # Solid Snake
    ("Solid Snake", "mg"):   "mg__Solid_Snake_(MG).jpg",
    ("Solid Snake", "mg2"):  "mg2__Solid_Snake_(MG2).gif",
    ("Solid Snake", "mgs1"): "mgs1__Solid_Snake's_sneaking_Suit.jpg",
    ("Solid Snake", "mgs2"): "mgs2__SnakeSubArt.jpg",
    ("Solid Snake", "mgs4"): "mgs4__Solid_Snake_(GOTP).JPG",
    # The Boss
    ("The Boss", "mgs3"): "mgs3__MGS3_The_Boss_Artwork.jpg",
    # Revolver Ocelot
    ("Revolver Ocelot", "mgs1"): "mgs1__Ocelot_(Twin_Snakes).jpeg",
    ("Revolver Ocelot", "mgs2"): "mgs2__Ocelot_old.jpg",
    ("Revolver Ocelot", "mgs3"): "mgs3__MGS3_Ocelot_Artwork.jpg",
    ("Revolver Ocelot", "mgs4"): "mgs4__LiquidOcelotMGS4.jpg",
    ("Revolver Ocelot", "tpp"):  "tpp__Ocelot_MGSV.png",
    # Liquid Snake
    ("Liquid Snake", "mgs1"): "mgs1__Liquid.jpg",
    # Solidus Snake
    ("Solidus Snake", "mgs2"): "mgs2__Solidus_Snake.jpg",
    # Gray Fox
    ("Gray Fox", "mg"):   "mg__Gray_Fox_(MG).jpg",
    ("Gray Fox", "mg2"):  "mg2__Gray_Fox_(MG2).gif",
    ("Gray Fox", "mgs1"): "mgs1__Grayfox.jpg",
    # Hal Otacon Emmerich
    ("Hal «Otacon» Emmerich", "mgs1"): "mgs1__Hal_Emmerich.jpg",
    ("Hal «Otacon» Emmerich", "mgs2"): "mgs2__Otacon.jpg",
    ("Hal «Otacon» Emmerich", "mgs4"): "mgs4__OtaconMGS4.jpg",
    # Raiden
    ("Raiden", "mgs2"):  "mgs2__Raiden.jpg",
    ("Raiden", "mgs4"):  "mgs4__Ninja_Raiden.jpg",
    ("Raiden", "rising"):"rising__Tumblr_m8sl44Pa5m1r6hu3go2_1280.jpg",
    # EVA
    ("EVA", "mgs3"): "mgs3__Metal_Gear_Solid_3_Cast_Eva.jpg",
    ("EVA", "mgs4"): "mgs4__Mgs4-eva.jpg",
    # Roy Campbell
    ("Roy Campbell", "mg2"):  "mg2__Campbell_(MG2).gif",
    ("Roy Campbell", "mgs1"): "mgs1__Colonel_Campbell.jpg",
    ("Roy Campbell", "po"):   "po__CampbellFOX.jpg",
    ("Roy Campbell", "mgs4"): "mgs4__MGS4_-_Campbell.jpeg",
    # Major Zero
    ("Major Zero", "mgs3"): "mgs3__MGS3_Zero_Yojji_Shinkawa.png",
    # Para-Medic
    ("Para-Medic", "mgs3"): "mgs3__MGS3_Para-Medic_Yojji_Shinkawa.png",
    # Sigint
    ("Sigint", "mgs3"): "mgs3__MGS3_Sigint_Yojji_Shinkawa.png",
    # Kazuhira Miller
    ("Kazuhira Miller", "mg2"):  "mg2__Miller_(MG2).gif",
    ("Kazuhira Miller", "pw"):   "pw__Kazmiller.jpg",
    ("Kazuhira Miller", "gz"):   "gz__Miller_GZ.jpg",
    ("Kazuhira Miller", "tpp"):  "gz__Miller_GZ.jpg",
    # Naomi Hunter
    ("Naomi Hunter", "mgs1"): "mgs1__Naomi.jpg",
    ("Naomi Hunter", "mgs4"): "mgs4__NaomiHunterMGS4.jpg",
    # Meryl
    ("Meryl Silverburgh", "mgs1"): "mgs1__Meryl_Sylverburgh.jpg",
    ("Meryl Silverburgh", "mgs4"): "mgs4__MerrylMGS4-2.jpg",
    # Huey
    ("Huey Emmerich", "pw"):  "pw__Huey_def_up_a_01_fix.jpg",
    ("Huey Emmerich", "gz"):  "gz__Huey_GZ.jpg",
    ("Huey Emmerich", "tpp"): "gz__Huey_GZ.jpg",
    # Paz
    ("Paz Ortega Andrade", "pw"):  "pw__Paz_Ortega_Andrade.jpg",
    ("Paz Ortega Andrade", "gz"):  "gz__Paz_GZ.jpg",
    ("Paz Ortega Andrade", "tpp"): "gz__Paz_GZ.jpg",
    # Chico
    ("Chico", "pw"): "pw__Chico_def_up_fix.jpg",
    ("Chico", "gz"): "gz__Chico_GZ.jpg",
    # Volgin
    ("Yevgeny Borisovitch Volgin", "mgs3"): "mgs3__MGS3_Volgin_Artwork.jpg",
    # Skull Face
    ("Skull Face", "gz"):  "gz__Skull_Face.png",
    ("Skull Face", "tpp"): "gz__Skull_Face.png",
    # Venom Snake
    ("Venom Snake", "tpp"): "tpp__Venom_Snake.png",
    # Quiet
    ("Quiet", "tpp"): "tpp__Quiet.png",
    # Vamp
    ("Vamp", "mgs2"): "mgs2__Vamp.jpg",
    ("Vamp", "mgs4"): "mgs4__VampMGS4.jpg",
    # Sunny
    ("Sunny Emmerich", "mgs4"):  "mgs4__Sunny.png",
    ("Sunny Emmerich", "rising"):"rising__Mgr-Sunny.png",
    # Gene (secret)
    ("Gene", "po"): "po__GeneFOX.jpg",
    # ── Metal Gear units ──
    ("TX-55 Metal Gear",                             "mg"):    "mech__TX55.png",
    ("Metal Gear D",                                 "mg2"):   "mech__MetalGearD.jpg",
    ("Metal Gear REX",                               "mgs1"):  "mech__REX.jpg",
    ("Metal Gear REX",                               "mgs4"):  "mech__REX.jpg",
    ("Metal Gear RAY",                               "mgs2"):  "mech__RAY.jpg",
    ("Metal Gear RAY",                               "mgs4"):  "mech__RAY.jpg",
    ("Arsenal Gear &amp; GW",                        "mgs2"):  "mech__ArsenalGear.jpg",
    ("Arsenal Gear &amp; GW",                        "mgs4"):  "mech__ArsenalGear.jpg",
    ("Shagohod &amp; el concepto de Granin",         "mgs3"):  "mech__Shagohod.png",
    ("ICBMG / RAXA",                                 "po"):    "mech__RAXA.jpg",
    ("Peace Walker &amp; Metal Gear ZEKE",           "pw"):    "mech__ZEKE.jpg",
    ("Sahelanthropus &amp; los parásitos vocales", "tpp"): "mech__Sahelanthropus.png",
    ("Metal Gear EXCELSUS",                          "rising"):"mech__EXCELSUS.jpg",
}

# ── Logos de organizaciones: (nombre_h3, game_id) → archivo ─────────────
# Estos usan make_img_contain (sin recorte, fondo transparente)
ORG_LOGOS = {
    ("FOXHOUND",                                        "mg"):    "org__FOXHOUND_premgs1.png",
    ("FOXHOUND",                                        "mg2"):   "org__FOXHOUND_premgs1.png",
    ("FOXHOUND",                                        "mgs1"):  "org__FOXHOUND.png",
    ("FOX",                                             "mgs3"):  "org__FOX.webp",
    ("FOX",                                             "po"):    "org__FOX.webp",
    ("Outer Heaven",                                    "mg"):    "org__OuterHeaven.png",
    ("Outer Heaven",                                    "mgs4"):  "org__OuterHeaven.png",
    ("Outer Heaven",                                    "tpp"):   "org__OuterHeaven.png",
    ("Militaires Sans Frontières",                      "pw"):    "org__MSF.png",
    ("Militaires Sans Frontières",                      "gz"):    "org__MSF.png",
    ("XOF",                                             "gz"):    "org__XOF.jpg",
    ("XOF",                                             "tpp"):   "org__XOF.jpg",
    ("Zanzibar Land",                                   "mg2"):   "org__ZanzibarLand.jpg",
    ("Unidad Cobra",                                    "mgs3"):  "org__CobraUnit.png",
    ("Dead Cell · Sons of Liberty · Ejército Gurlukovich", "mgs2"): "org__DeadCell.jpg",
    ("Diamond Dogs",                                    "tpp"):   "org__DiamondDogs.jpg",
}

# ── Pre-generar todas las imágenes ───────────────────────────────────────
print("Generando retratos de personaje (150×200 → encode 300×400)...")
IMG_CACHE = {}
for (char, game), fname in SEG_PORTRAITS.items():
    if fname not in IMG_CACHE:
        pix = fname.lower().endswith('.gif') or fname.startswith('mg2__')
        tag = make_img_tag(fname, 150, 200, "seg-portrait", pixelated=pix)
        if tag:
            IMG_CACHE[fname] = tag
            print(f"  OK  [{game}] {char}")
        else:
            IMG_CACHE[fname] = ""

print("\nGenerando logos de organización (80×80 contain)...")
ORG_CACHE = {}
for (org, game), fname in ORG_LOGOS.items():
    if fname not in ORG_CACHE:
        tag = make_img_contain(fname, 80, "org-emblem")
        if tag:
            ORG_CACHE[fname] = tag
            print(f"  OK  [{game}] {org}")
        else:
            ORG_CACHE[fname] = ""

total_ok = len([v for v in IMG_CACHE.values() if v]) + len([v for v in ORG_CACHE.values() if v])
print(f"\n{total_ok} imágenes totales generadas\n")

# ── Sistema de hiperenlaces entre entradas ───────────────────────────────
# ANCHOR_MAP: texto H3 exacto → slug usado como id="e-{slug}"
ANCHOR_MAP = {
    "Big Boss":                                              "big-boss",
    "Solid Snake":                                           "solid-snake",
    "The Boss":                                              "the-boss",
    "Revolver Ocelot":                                       "ocelot",
    "Liquid Snake":                                          "liquid-snake",
    "Solidus Snake":                                         "solidus",
    "Gray Fox":                                              "gray-fox",
    "Hal «Otacon» Emmerich":                       "otacon",
    "Raiden":                                                "raiden",
    "EVA":                                                   "eva",
    "Roy Campbell":                                          "campbell",
    "Major Zero":                                            "zero",
    "Para-Medic":                                            "paramedic",
    "Sigint":                                                "sigint",
    "Kazuhira Miller":                                       "miller",
    "Naomi Hunter":                                          "naomi",
    "Meryl Silverburgh":                                     "meryl",
    "Huey Emmerich":                                         "huey",
    "Paz Ortega Andrade":                                    "paz",
    "Chico":                                                 "chico",
    "Yevgeny Borisovitch Volgin":                            "volgin",
    "Vamp":                                                  "vamp",
    "Sunny Emmerich":                                        "sunny",
    "Gene":                                                  "gene",
    "Skull Face":                                            "skull-face",
    "Venom Snake":                                           "venom-snake",
    "Quiet":                                                 "quiet",
    "Steven Armstrong":                                      "armstrong",
    "Los Filósofos":                                    "filosofos",
    "Los Patriots":                                          "patriots",
    "FOX":                                                   "fox",
    "FOXHOUND":                                              "foxhound",
    "Outer Heaven":                                          "outer-heaven",
    "Zanzibar Land":                                         "zanzibar",
    "Philanthropy":                                          "philanthropy",
    "Dead Cell · Sons of Liberty · Ejército Gurlukovich": "dead-cell",
    "Unidad Cobra":                                          "cobra",
    "Militaires Sans Frontières":                       "msf",
    "Cipher":                                                "cipher",
    "XOF":                                                   "xof",
    "Diamond Dogs":                                          "diamond-dogs",
    "Rat Patrol Team 01 · Paradise Lost":               "rat-patrol",
    "World Marshal · Desperado · Maverick":        "world-marshal",
    "TX-55 Metal Gear":                                      "tx55",
    "Metal Gear D":                                          "metal-gear-d",
    "Metal Gear REX":                                        "rex",
    "Metal Gear RAY":                                        "ray",
    "Arsenal Gear &amp; GW":                                 "arsenal",
    "Shagohod &amp; el concepto de Granin":                  "shagohod",
    "ICBMG / RAXA":                                          "icbmg",
    "Peace Walker &amp; Metal Gear ZEKE":                    "peace-walker",
    "Sahelanthropus &amp; los parásitos vocales":       "sahelanthropus",
    "FOXDIE":                                                "foxdie",
    "Nanomáquinas &amp; sistema SOP":                   "sop",
    "OILIX":                                                 "oilix",
    "Terapia génica &amp; soldados del genoma":         "genome",
    "Tecnología ciborg / exoesqueletos":                 "cyborg",
    "Metal Gear EXCELSUS":                                   "excelsus",
}

# LINK_ALIASES: slug → textos a buscar en <p> (ordenados de más largo a más corto)
LINK_ALIASES = {
    "big-boss":       ["Big Boss", "Naked Snake"],
    "solid-snake":    ["Solid Snake", "Old Snake"],
    "the-boss":       ["The Boss"],
    "ocelot":         ["Liquid Ocelot", "Revolver Ocelot", "Ocelot"],
    "liquid-snake":   ["Liquid Snake"],
    "solidus":        ["Solidus Snake", "Solidus"],
    "gray-fox":       ["Gray Fox", "Frank Jaeger", "Null"],
    "otacon":         ["Otacon"],
    "raiden":         ["Raiden"],
    "eva":            ["EVA"],
    "campbell":       ["Roy Campbell", "Campbell"],
    "zero":           ["Major Zero"],
    "paramedic":      ["Para-Medic"],
    "sigint":         ["Sigint"],
    "miller":         ["Kazuhira Miller", "Miller"],
    "naomi":          ["Naomi Hunter", "Naomi"],
    "meryl":          ["Meryl Silverburgh", "Meryl"],
    "huey":           ["Huey Emmerich", "Huey"],
    "paz":            ["Paz Ortega Andrade"],
    "chico":          ["Chico"],
    "volgin":         ["Volgin"],
    "vamp":           ["Vamp"],
    "sunny":          ["Sunny Emmerich", "Sunny"],
    "gene":           ["Gene"],
    "skull-face":     ["Skull Face"],
    "venom-snake":    ["Venom Snake"],
    "quiet":          ["Quiet"],
    "armstrong":      ["Steven Armstrong", "Armstrong"],
    "filosofos":      ["los Filósofos", "Filósofos"],
    "patriots":       ["los Patriots", "Patriots"],
    "foxhound":       ["FOXHOUND"],
    "outer-heaven":   ["Outer Heaven"],
    "zanzibar":       ["Zanzibar Land"],
    "philanthropy":   ["Philanthropy"],
    "dead-cell":      ["Dead Cell"],
    "cobra":          ["Unidad Cobra"],
    "msf":            ["Militaires Sans Frontières", "MSF"],
    "cipher":         ["Cipher"],
    "xof":            ["XOF"],
    "diamond-dogs":   ["Diamond Dogs"],
    "rat-patrol":     ["Rat Patrol"],
    "tx55":           ["TX-55"],
    "metal-gear-d":   ["Metal Gear D"],
    "rex":            ["Metal Gear REX"],
    "ray":            ["Metal Gear RAY"],
    "arsenal":        ["Arsenal Gear"],
    "shagohod":       ["Shagohod"],
    "icbmg":          ["ICBMG", "RAXA"],
    "peace-walker":   ["Metal Gear ZEKE", "Peace Walker", "ZEKE"],
    "sahelanthropus": ["Sahelanthropus"],
    "foxdie":         ["FOXDIE"],
    "sop":            ["sistema SOP", "SOP"],
    "oilix":          ["OILIX"],
    "genome":         ["soldados del genoma"],
    "cyborg":         ["exoesqueleto"],
    "excelsus":       ["Metal Gear EXCELSUS", "EXCELSUS"],
}

# Pre-compilar regex de linkificación: todas las aliases, longest-first
_link_pairs = []
for eid, texts in LINK_ALIASES.items():
    for t in texts:
        _link_pairs.append((t, eid))
_link_pairs.sort(key=lambda x: -len(x[0]))
_link_text_to_id = {}
for t, eid in _link_pairs:
    if t not in _link_text_to_id:
        _link_text_to_id[t] = eid
_LINK_RE = re.compile('(' + '|'.join(re.escape(t) for t, _ in _link_pairs) + ')')

def linkify_html(html_src):
    """Reemplaza nombres de entidades en nodos de texto de <p> con <a class="e-link">."""
    P_RE = re.compile(r'(<p(?:\s[^>]*)?>)(.*?)(</p>)', re.DOTALL)

    def process_p(m):
        p_open, content, p_close = m.group(1), m.group(2), m.group(3)
        parts = re.split(r'(<[^>]+>)', content)
        result = []
        link_depth = 0
        for part in parts:
            if re.match(r'<a[\s>]', part, re.I):
                link_depth += 1
                result.append(part)
            elif re.match(r'</a>', part, re.I):
                link_depth = max(0, link_depth - 1)
                result.append(part)
            elif part.startswith('<'):
                result.append(part)
            elif link_depth == 0 and part.strip():
                def sub_entity(em):
                    txt = em.group(0)
                    eid = _link_text_to_id.get(txt)
                    if eid:
                        return f'<a class="e-link" href="#e-{eid}" data-target="e-{eid}">{txt}</a>'
                    return txt
                result.append(_LINK_RE.sub(sub_entity, part))
            else:
                result.append(part)
        return p_open + ''.join(result) + p_close

    return P_RE.sub(process_p, html_src)

# ── Insertar imágenes en cada segmento de cada ficha ────────────────────
print("Procesando HTML...")
with open(HTML_IN, encoding='utf-8') as f:
    html = f.read()

SEG_RE = re.compile(
    r'(<div class="seg gated" data-game="([^"]+)"[^>]+><div class="g-body">)',
    re.DOTALL
)

inserted = 0

def process_card(card_html, char_name):
    """Inserta imágenes/logos en los segmentos de una ficha."""
    global inserted

    def replace_seg(m):
        global inserted
        full_match = m.group(1)
        game_id    = m.group(2)
        key = (char_name, game_id)
        img = ""
        if key in SEG_PORTRAITS:
            img = IMG_CACHE.get(SEG_PORTRAITS[key], "")
        elif key in ORG_LOGOS:
            img = ORG_CACHE.get(ORG_LOGOS[key], "")
        if img:
            inserted += 1
            return full_match + "\n        " + img
        return full_match

    return SEG_RE.sub(replace_seg, card_html)


# Procesar carta a carta
CARD_RE = re.compile(r'(<article\b[^>]*class="card[^"]*"[^>]*>)(.*?)(</article>)', re.DOTALL)
H3_RE   = re.compile(r'<h3>(?:<span[^>]*>)?([^<\n]+?)(?:</span>)?(?:\s*<span|</h3>)')

MORE_DIV = '\n    <div class="more-ahead">↓ Más información más adelante</div>'

def replace_card(m):
    card_open = m.group(1)
    card_body = m.group(2)
    card_close= m.group(3)
    h3 = H3_RE.search(card_body)
    if h3:
        char_name = h3.group(1).strip()
        card_body = process_card(card_body, char_name)
        slug = ANCHOR_MAP.get(char_name)
        if slug:
            card_open = card_open[:-1] + f' id="e-{slug}">'
    # Inyectar .more-ahead antes del último </div> (cierre del g-body externo)
    last_div = card_body.rfind('</div>')
    if last_div >= 0:
        card_body = card_body[:last_div] + MORE_DIV + '\n  ' + card_body[last_div:]
    return card_open + card_body + card_close

html = CARD_RE.sub(replace_card, html)
print(f"  {inserted} imágenes insertadas en segmentos")

# Linkificación: insertar <a class="e-link"> en todos los <p>
html = linkify_html(html)
print("  Hiperenlaces insertados en párrafos")

# ── CSS adicional ────────────────────────────────────────────────────────
EXTRA_CSS = """
  /* ===== v4: Ocultar completamente en lugar de difuminar ===== */
  /* Tarjetas y segmentos bloqueados desaparecen del DOM visible */
  article.gated.locked,
  .seg.gated.locked,
  details.gated.locked,
  li.gated.locked { display:none !important; }
  /* Textos spoiler inline dentro de entradas desbloqueadas: mantener blur */
  .t-extra.locked { display:inline !important; }

  /* ===== v4: Indicador "más adelante" con estética censurada ===== */
  .more-ahead{
    display:none; clear:both;
    margin:12px 0 2px; padding:12px 14px;
    background:var(--panel); border:1px solid var(--line2);
    position:relative; overflow:hidden; min-height:44px;
    border-radius:2px;
  }
  /* Fondo: texto bloqueado difuminado */
  .more-ahead::before{
    content:'██████ ███ ████████ ██ █████ ████ ███ ██████ ████████ ██ ███████';
    display:block; font-family:var(--mono); font-size:11px;
    color:var(--dim); letter-spacing:.05em; line-height:1.7;
    filter:blur(4px) saturate(.3); opacity:.45;
    white-space:nowrap; overflow:hidden; pointer-events:none;
  }
  /* Texto superpuesto en ámbar */
  .more-ahead::after{
    content:'▶ MÁS INFORMACIÓN MÁS ADELANTE';
    position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
    font-family:var(--mono); font-size:9px; letter-spacing:.18em;
    color:var(--amber); opacity:.65; white-space:nowrap; pointer-events:none;
  }

  /* ===== v4: Contener floats en segmentos (fix Gray Fox) ===== */
  .seg .g-body{ display:flow-root; }

  /* ===== v4: Retratos de personaje ===== */
  .seg-portrait{
    width:80px; height:107px; object-fit:cover;
    float:right; margin:0 0 8px 10px;
    border:1px solid var(--line2); opacity:.92;
    cursor:pointer; transition:opacity .15s;
  }
  .seg-portrait:hover{ opacity:1; }

  /* ===== v4: Logos de organización ===== */
  .org-emblem{
    width:80px; height:80px; object-fit:contain;
    float:right; margin:0 0 8px 10px;
    padding:6px; box-sizing:border-box;
    background:rgba(255,255,255,.04);
    border:1px solid var(--line2); opacity:.82;
    cursor:pointer; transition:opacity .15s;
  }
  .org-emblem:hover{ opacity:1; }

  /* ===== v4: Modal de artwork ===== */
  #artModal{
    display:none; position:fixed; inset:0; z-index:1000;
    background:rgba(0,0,17,.85); backdrop-filter:blur(4px);
    align-items:center; justify-content:center;
  }
  #artModal.open{ display:flex; }
  #artModalInner{
    position:relative; display:flex; flex-direction:column;
    align-items:center; gap:10px; padding:12px;
  }
  #artModalImg{
    max-width:88vw; max-height:80vh;
    object-fit:contain;
    border:1px solid var(--line);
    box-shadow:0 0 60px rgba(0,0,0,.9);
  }
  #artModalCaption{
    font-family:var(--mono); font-size:10px; letter-spacing:.12em;
    color:var(--dim); text-transform:uppercase;
  }
  #artModalClose{
    position:absolute; top:-8px; right:-8px;
    background:var(--panel2); border:1px solid var(--line);
    color:var(--dim); font-size:14px; width:26px; height:26px;
    cursor:pointer; display:flex; align-items:center; justify-content:center;
    line-height:1;
  }
  #artModalClose:hover{ color:var(--cyan); }

  /* ===== v4: Modal de búsqueda ===== */
  #srchModal{
    display:none; position:fixed; inset:0; z-index:1000;
    background:rgba(0,0,17,.75); backdrop-filter:blur(4px);
    align-items:flex-start; justify-content:center; padding-top:10vh;
  }
  #srchModal.open{ display:flex; }
  #srchBox{
    width:min(560px,90vw); max-height:70vh;
    background:var(--panel2); border:1px solid var(--line);
    display:flex; flex-direction:column; overflow:hidden;
  }
  .sb-head{
    display:flex; align-items:center;
    border-bottom:1px solid var(--line2);
  }
  #srchInput{
    flex:1; background:transparent; border:none; outline:none;
    color:var(--fg); font-family:var(--mono); font-size:13px;
    padding:14px 16px; letter-spacing:.03em;
  }
  #srchClose{
    background:none; border:none; color:var(--dim);
    font-size:16px; padding:0 16px; cursor:pointer; line-height:1;
  }
  #srchClose:hover{ color:var(--cyan); }
  #srchResults{
    list-style:none; margin:0; padding:4px 0;
    overflow-y:auto; flex:1;
  }
  .sr-item{
    display:flex; align-items:baseline; gap:10px;
    padding:9px 16px; cursor:pointer;
    border-bottom:1px solid rgba(255,255,255,.04);
  }
  .sr-item:hover{ background:rgba(95,211,227,.07); }
  .sr-type{
    font-size:8px; letter-spacing:.14em; text-transform:uppercase;
    color:var(--amber); font-family:var(--mono); min-width:72px; flex-shrink:0;
  }
  .sr-name{ font-size:13px; color:var(--fg); }
  .sr-empty{ padding:18px 16px; color:var(--dim); font-family:var(--mono); font-size:11px; list-style:none; }

  /* ===== v4: Botón de búsqueda ===== */
  #srchBtn{
    position:fixed; top:10px; left:0; z-index:201;
    width:112px; padding:6px 8px;
    background:var(--panel2);
    border:1px solid var(--line); border-left:none;
    color:var(--dim); font-family:var(--mono);
    font-size:10px; letter-spacing:.1em; text-transform:uppercase;
    cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px;
  }
  #srchBtn:hover{ color:var(--cyan); }

  /* ===== v4: Panel derecho COMPACTO (sin scroll) ===== */
  .access{
    position:fixed !important;
    right:0; top:50%; transform:translateY(-50%);
    z-index:200;
    width:160px;
    background:rgba(10,17,28,.97);
    border:1px solid var(--line); border-right:none;
    backdrop-filter:blur(6px);
    padding:7px 6px 6px;
  }
  /* Sobreescribir border-top:none del original */
  .access{ border-top:1px solid var(--line) !important; }
  .access .a-head{ display:block; margin-bottom:5px; }
  .access .a-title{ font-size:8.5px; letter-spacing:.22em; }
  .access .a-count{ font-size:9px; display:block; margin-top:2px; }
  .rail{ flex-direction:column; gap:2px; }
  .rail-item{
    padding:3px 6px; border-radius:3px;
    font-size:10.5px; gap:5px;
  }
  .rail-n{ width:13px; height:13px; font-size:9px; flex-shrink:0; }
  .rail-txt{ font-size:10.5px; gap:4px; flex-wrap:nowrap; }
  .rail-yr{ display:none; }
  .a-hint{ display:none; }
  .a-actions{ flex-direction:row; gap:4px; margin-top:5px; flex-wrap:nowrap; }
  .a-actions button{ font-size:9px; padding:2px 5px; flex:1; letter-spacing:.04em; }

  /* ===== v4: Panel izquierdo (bordes correctos) ===== */
  nav.secs{
    position:fixed !important;
    left:0; top:50%; transform:translateY(-50%);
    z-index:200;
    display:flex; flex-direction:column;
    width:112px;
    background:var(--panel2);
    border:1px solid var(--line); border-left:none;
  }
  nav.secs a{
    display:block; width:100%; box-sizing:border-box;
    padding:11px 6px;
    font-family:var(--mono); font-size:9.5px; letter-spacing:.09em;
    text-transform:uppercase; text-align:center; line-height:1.35;
    color:var(--dim); text-decoration:none;
    border:none;
    border-bottom:1px solid var(--line);
  }
  nav.secs a:last-child{ border-bottom:none; }
  nav.secs a:hover,nav.secs a:focus-visible{
    color:var(--cyan); background:rgba(95,211,227,.07); outline:none;
  }

  /* ===== v4: Margen de contenido ===== */
  .wrap{ padding-left:118px !important; padding-right:176px !important; }

  /* ===== v4: Hiperenlaces entre entradas ===== */
  .e-link{
    color:var(--cyan); text-decoration:none;
    border-bottom:1px dotted rgba(95,211,227,.45);
    cursor:pointer; transition:opacity .15s, border-color .15s;
  }
  .e-link:hover{ opacity:.8; border-bottom-color:var(--cyan); }
  .e-link.e-sealed{
    color:var(--amber); border-bottom-color:rgba(240,180,0,.3);
    opacity:.55; cursor:default;
  }
  .gated.locked .e-link{
    color:var(--amber) !important; border-bottom-color:rgba(240,180,0,.2) !important;
    opacity:.4 !important; pointer-events:none !important; cursor:default !important;
  }

  /* ===== Elementos solo-móvil: ocultos en escritorio ===== */
  #mobileHeader, #mobileOverlay { display:none; }

  /* ══════════════════════════════════════════════════════
     TABLET  (768 – 1023 px)
  ══════════════════════════════════════════════════════ */
  @media (min-width:768px) and (max-width:1023px){
    nav.secs{ width:96px; }
    .access { width:144px; }
    .wrap   { padding-left:102px !important; padding-right:160px !important; }
    #srchBtn{ width:96px; font-size:9px; }
  }

  /* ══════════════════════════════════════════════════════
     MÓVIL  (≤ 767 px)
  ══════════════════════════════════════════════════════ */
  @media (max-width:767px){

    /* Ocultar paneles de escritorio */
    nav.secs { display:none !important; }
    .access  { display:none !important; }
    #srchBtn { display:none !important; }

    /* ── Header fijo superior ── */
    #mobileHeader{
      display:flex !important;
      position:fixed; top:0; left:0; right:0; z-index:500;
      height:44px;
      background:rgba(10,17,28,.97);
      border-bottom:1px solid var(--line);
      backdrop-filter:blur(6px);
      align-items:center; padding:0 8px; gap:6px;
    }
    #mobileSearchBtn, #mobileGamesBtn{
      width:36px; height:36px; flex-shrink:0;
      display:flex; align-items:center; justify-content:center;
      background:transparent; border:1px solid var(--line2);
      color:var(--dim); cursor:pointer; font-size:16px;
      font-family:var(--mono); line-height:1;
    }
    #mobileSearchBtn:active,#mobileGamesBtn:active{
      color:var(--cyan); border-color:var(--cyan);
    }
    #mobileHeaderTitle{
      flex:1; font-family:var(--mono); font-size:8.5px;
      letter-spacing:.2em; text-transform:uppercase;
      color:var(--dim); text-align:center;
      white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    }

    /* ── Tab bar de secciones (parte inferior) ── */
    nav.secs{
      display:flex !important;
      position:fixed !important;
      bottom:0; left:0; right:0; top:auto !important;
      transform:none !important;
      width:100% !important; height:50px;
      flex-direction:row !important;
      background:rgba(10,17,28,.97);
      border-top:1px solid var(--line) !important;
      border-left:none !important; border-right:none !important; border-bottom:none !important;
      overflow-x:auto; overflow-y:hidden;
      scrollbar-width:none; -ms-overflow-style:none;
      z-index:500;
    }
    nav.secs::-webkit-scrollbar{ display:none; }
    nav.secs a{
      flex:1 0 auto !important; height:50px !important;
      width:auto !important;
      padding:0 16px !important;
      display:flex !important; align-items:center !important; justify-content:center !important;
      text-align:center !important; line-height:1.25 !important;
      white-space:nowrap !important;
      border-bottom:none !important; border-right:1px solid var(--line2) !important;
      font-size:8.5px !important; letter-spacing:.1em !important;
    }
    nav.secs a:last-child{ border-right:none !important; }
    nav.secs a:active{ color:var(--cyan); background:rgba(95,211,227,.1); }

    /* ── Drawer de juegos (desliza desde la derecha) ── */
    .access{
      display:flex !important;
      position:fixed !important;
      right:0 !important; top:0 !important; bottom:0 !important; left:auto !important;
      width:min(280px,88vw) !important; max-height:100vh !important;
      transform:translateX(calc(min(280px,88vw) + 8px)) !important;
      transition:transform .28s cubic-bezier(.4,0,.2,1);
      background:rgba(10,17,28,.99) !important;
      border-left:1px solid var(--line) !important; border-right:none !important;
      border-top:none !important;
      flex-direction:column; overflow-y:auto;
      padding:52px 10px 10px !important;
      z-index:601;
      scrollbar-width:thin;
    }
    .access.mob-open{ transform:translateX(0) !important; }

    /* Rail dentro del drawer: columna */
    .rail{ flex-direction:column !important; gap:3px !important; }
    .rail-item{ padding:5px 8px !important; }
    .rail-yr{ display:inline !important; }
    .rail-txt{ font-size:11px !important; }
    .a-actions{ flex-direction:column !important; gap:4px !important; margin-top:8px; }
    .a-actions button{ font-size:10px !important; padding:5px 8px !important; }
    .a-hint{ display:block !important; font-size:9px; margin-top:6px; }
    .a-count{ display:block; font-size:10px; margin-top:2px; }

    /* ── Overlay oscuro ── */
    #mobileOverlay{
      display:none; position:fixed; inset:0; z-index:600;
      background:rgba(0,0,0,.55); backdrop-filter:blur(1px);
    }
    #mobileOverlay.mob-open{ display:block; }

    /* ── Contenido: compensar header + tab bar ── */
    .wrap{
      padding-left:12px !important; padding-right:12px !important;
      padding-top:52px !important; padding-bottom:62px !important;
    }

    /* ── Imágenes más pequeñas ── */
    .seg-portrait{ width:62px; height:83px; }
    .org-emblem  { width:62px; height:62px; }

    /* ── Modal de búsqueda: pantalla completa en móvil ── */
    #srchModal{
      padding-top:0 !important;
      align-items:flex-start; justify-content:stretch;
    }
    #srchBox{ width:100% !important; max-height:90vh; border-left:none; border-right:none; }
    #srchInput{ font-size:16px; } /* evitar zoom automático en iOS */

    /* ── Modal artwork: adaptado ── */
    #artModalImg{ max-width:95vw; max-height:70vh; }
  }

  /* ── Móvil pequeño (≤ 420 px) ── */
  @media (max-width:420px){
    nav.secs a{ font-size:7.5px !important; padding:0 11px !important; }
    .wrap{ padding-left:8px !important; padding-right:8px !important; }
    #mobileHeaderTitle{ display:none; }
  }
"""
html = html.replace('</style>', EXTRA_CSS + '</style>', 1)

# ── Inyección JS: updateMoreAhead ────────────────────────────────────────
JS_MORE_AHEAD_FN = """
  // v4: muestra el indicador "más adelante" en tarjetas parcialmente desbloqueadas
  function updateMoreAhead(){
    document.querySelectorAll('.card').forEach(function(card){
      var ma = card.querySelector('.more-ahead');
      if(!ma) return;
      if(card.classList.contains('locked')){ ma.style.display='none'; return; }
      ma.style.display = card.querySelector('.seg.locked') ? '' : 'none';
    });
  }
  // v4: actualiza estado visual de hiperenlaces entre entradas
  function updateEntityLinks(){
    document.querySelectorAll('.e-link').forEach(function(a){
      var tid = a.getAttribute('data-target');
      var target = tid ? document.getElementById(tid) : null;
      if(target && target.classList.contains('locked')){
        a.classList.add('e-sealed');
      } else {
        a.classList.remove('e-sealed');
      }
    });
  }
"""

# Insertar la función antes de update()
html = html.replace('  function update(){', JS_MORE_AHEAD_FN + '  function update(){', 1)

# Llamar updateMoreAhead() al final de update(), tras la línea del contador
html = html.replace(
    "' registros desbloqueados';",
    "' registros desbloqueados';\n    updateMoreAhead();\n    updateEntityLinks();"
)

# ── Nivel de acceso: renombrar etiqueta ─────────────────────────────────
html = html.replace(
    'Nivel de acceso — Juegos completados',
    'Juegos completados'
)

# ── Inyección HTML: modales y botón de búsqueda ─────────────────────────
MODAL_HTML = """
<!-- Modal artwork -->
<div id="artModal">
  <div id="artModalInner">
    <button id="artModalClose">✕</button>
    <img id="artModalImg" src="" alt="">
    <p id="artModalCaption"></p>
  </div>
</div>
<!-- Modal búsqueda -->
<div id="srchModal">
  <div id="srchBox">
    <div class="sb-head">
      <input id="srchInput" type="text" placeholder="Buscar personaje, organización, evento…" autocomplete="off" spellcheck="false">
      <button id="srchClose">✕</button>
    </div>
    <ul id="srchResults"></ul>
  </div>
</div>
<!-- Botón búsqueda (escritorio) -->
<button id="srchBtn" title="Buscar (Ctrl+K)">⌕ Buscar</button>
<!-- Móvil: header superior + overlay del drawer -->
<div id="mobileHeader">
  <button id="mobileSearchBtn" title="Buscar">⌕</button>
  <span id="mobileHeaderTitle">Metal Gear · Enciclopedia</span>
  <button id="mobileGamesBtn" title="Juegos">≡</button>
</div>
<div id="mobileOverlay"></div>
"""
# El JS extra va en script propio DESPUÉS del modal HTML para que los
# elementos del DOM existan cuando se ejecute
JS_EXTRA = """
  // ── Navegación por hiperenlaces entre entradas ──
  document.addEventListener('click', function(e){
    var link = e.target.closest('.e-link');
    if(!link) return;
    e.preventDefault();
    if(link.classList.contains('e-sealed')) return;
    if(link.closest('.gated.locked')) return;
    var tid = link.getAttribute('data-target');
    var target = tid ? document.getElementById(tid) : null;
    if(!target) return;
    target.scrollIntoView({behavior:'smooth', block:'center'});
    var old = target.style.outline;
    target.style.outline = '1px solid var(--amber)';
    setTimeout(function(){ target.style.outline = old; }, 1800);
  });

  // ── Modal de artwork ──
  (function(){
    var modal   = document.getElementById('artModal');
    var mImg    = document.getElementById('artModalImg');
    var mCap    = document.getElementById('artModalCaption');
    var mClose  = document.getElementById('artModalClose');

    function openArt(imgEl){
      mImg.src = imgEl.src;
      var body = imgEl.closest('.g-body');
      var src  = body && body.querySelector('.s-src');
      mCap.textContent = src ? src.textContent.trim() : '';
      modal.classList.add('open');
    }
    document.querySelectorAll('.seg-portrait,.org-emblem').forEach(function(img){
      img.addEventListener('click', function(){ openArt(this); });
    });
    mClose.addEventListener('click', function(){ modal.classList.remove('open'); });
    modal.addEventListener('click', function(e){ if(e.target===modal) modal.classList.remove('open'); });
  })();

  // ── Modal de búsqueda ──
  (function(){
    var modal  = document.getElementById('srchModal');
    var input  = document.getElementById('srchInput');
    var list   = document.getElementById('srchResults');
    var btn    = document.getElementById('srchBtn');
    var close  = document.getElementById('srchClose');

    function openSearch(){
      modal.classList.add('open');
      input.value = ''; input.focus(); doSearch('');
    }
    btn.addEventListener('click', openSearch);
    close.addEventListener('click', function(){ modal.classList.remove('open'); });
    modal.addEventListener('click', function(e){ if(e.target===modal) modal.classList.remove('open'); });
    input.addEventListener('input', function(){ doSearch(this.value.trim().toLowerCase()); });

    document.addEventListener('keydown', function(e){
      if((e.ctrlKey||e.metaKey)&&e.key==='k'){ e.preventDefault(); openSearch(); }
      if(e.key==='Escape'){
        document.getElementById('artModal').classList.remove('open');
        modal.classList.remove('open');
      }
    });

    function doSearch(q){
      var results = [];
      // Tarjetas visibles (personajes, organizaciones, tecnologías…)
      document.querySelectorAll('.card:not(.locked)').forEach(function(card){
        var h3 = card.querySelector('h3');
        if(!h3) return;
        var name = h3.textContent.replace(/\\s+/g,' ').trim();
        if(!q || name.toLowerCase().indexOf(q)>=0){
          var zone = card.closest('.zone');
          var sec  = zone ? zone.querySelector('h2').textContent.replace(/^\\d+/,'').trim() : '';
          results.push({name:name, sec:sec, el:card});
        }
      });
      // Eventos (details)
      document.querySelectorAll('.evt:not(.locked)').forEach(function(evt){
        var sum = evt.querySelector('summary');
        if(!sum) return;
        var name = sum.textContent.trim();
        if(!q || name.toLowerCase().indexOf(q)>=0)
          results.push({name:name, sec:'Eventos', el:evt});
      });
      // Línea cronológica
      document.querySelectorAll('.chrono li:not(.locked)').forEach(function(li){
        var yr = li.querySelector('.ev-yr');
        if(!yr) return;
        var txt = yr.textContent.trim();
        if(!q || txt.toLowerCase().indexOf(q)>=0)
          results.push({name:txt, sec:'Cronología', el:li});
      });

      list.innerHTML = '';
      if(!results.length){
        var li = document.createElement('li');
        li.className = 'sr-empty';
        li.textContent = q ? 'Sin resultados para «'+q+'»' : 'Empieza a escribir…';
        list.appendChild(li); return;
      }
      results.forEach(function(r){
        var li = document.createElement('li');
        li.className = 'sr-item';
        li.innerHTML = '<span class="sr-type">'+r.sec+'</span><span class="sr-name">'+r.name+'</span>';
        li.addEventListener('click', function(){
          modal.classList.remove('open');
          r.el.scrollIntoView({behavior:'smooth', block:'center'});
          var old = r.el.style.outline;
          r.el.style.outline = '2px solid var(--amber)';
          setTimeout(function(){ r.el.style.outline = old; }, 2000);
        });
        list.appendChild(li);
      });
    }
  })();

  // ── Móvil: drawer de juegos ──
  (function(){
    var overlay  = document.getElementById('mobileOverlay');
    var panel    = document.querySelector('.access');
    var gBtn     = document.getElementById('mobileGamesBtn');
    var sBtn     = document.getElementById('mobileSearchBtn');
    var srchBtn  = document.getElementById('srchBtn');
    if(!overlay || !panel || !gBtn) return;

    function openDrawer(){
      panel.classList.add('mob-open');
      overlay.classList.add('mob-open');
      document.body.style.overflow = 'hidden';
    }
    function closeDrawer(){
      panel.classList.remove('mob-open');
      overlay.classList.remove('mob-open');
      document.body.style.overflow = '';
    }
    gBtn.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);

    // Cerrar con Escape también cierra el drawer
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') closeDrawer();
    });

    // Botón de búsqueda del header móvil
    if(sBtn && srchBtn){
      sBtn.addEventListener('click', function(){ srchBtn.click(); });
    }

    // Si el drawer está abierto y el usuario marca un juego, actualizar counter
    panel.addEventListener('change', function(){
      // Disparar actualización visual inmediata
      var counter = document.querySelector('.a-count');
      if(counter) counter.style.transition = 'color .2s';
    });
  })();
"""

# Inyectar modal HTML + script extra juntos, justo antes de </body>
# (el script propio va DESPUÉS del modal para que los IDs existan en el DOM)
html = html.replace(
    '</body>',
    MODAL_HTML + '\n<script>\n' + JS_EXTRA.strip() + '\n</script>\n</body>',
    1
)

# ── Guardar v4 ───────────────────────────────────────────────────────────
with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(html)

kb = os.path.getsize(HTML_OUT) // 1024
print(f"\nGuardado: {HTML_OUT}  ({kb} KB)")
print("Done.")
