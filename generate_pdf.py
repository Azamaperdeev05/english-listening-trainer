import os
import pypdfium2 as pdfium
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

# ---------------------------------------------------------
# FONT REGISTRATION (Apple Native Helvetica Neue)
# ---------------------------------------------------------
pdfmetrics.registerFont(TTFont('HN', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('HN-Bold', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('HN-Italic', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=2))
pdfmetrics.registerFont(TTFont('HN-BoldItalic', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=3))
pdfmetrics.registerFont(TTFont('HN-Light', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=7))
pdfmetrics.registerFont(TTFont('HN-Medium', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=10))

pdfmetrics.registerFontFamily('HN', normal='HN', bold='HN-Bold', italic='HN-Italic', boldItalic='HN-BoldItalic')

# ---------------------------------------------------------
# DIMENSIONS & APPLE PALETTE (Mobile 9:19.5 Viewport)
# ---------------------------------------------------------
PAGE_W = 390
PAGE_H = 844
MARGIN_X = 18
CARD_W = PAGE_W - (MARGIN_X * 2)  # 354 pt

BG_COLOR = colors.HexColor('#F2F2F7')       # iOS Grouped Background
CARD_BG = colors.HexColor('#FFFFFF')        # Crisp Card White
CARD_BORDER = colors.HexColor('#E5E5EA')    # 1px boundary
DIVIDER_COLOR = colors.HexColor('#E5E5EA')

TEXT_PRIMARY = colors.HexColor('#1C1C1E')   # High-contrast label
TEXT_SECONDARY = colors.HexColor('#545458') # Secondary label
TEXT_MUTED = colors.HexColor('#8E8E93')     # Tertiary label

ACCENT_BLUE = colors.HexColor('#007AFF')
ACCENT_BLUE_LIGHT = colors.HexColor('#EBF3FF')
ACCENT_BLUE_BORDER = colors.HexColor('#CCE1FF')

ACCENT_INDIGO = colors.HexColor('#5856D6')
ACCENT_INDIGO_LIGHT = colors.HexColor('#F3F2FF')
ACCENT_INDIGO_BORDER = colors.HexColor('#DCD8FE')

ACCENT_TEAL = colors.HexColor('#30B0C7')
ACCENT_TEAL_LIGHT = colors.HexColor('#EAF8FA')

ACCENT_GREEN = colors.HexColor('#34C759')
ACCENT_GREEN_LIGHT = colors.HexColor('#EDFAF0')
ACCENT_GREEN_BORDER = colors.HexColor('#BEE8C7')

ACCENT_ORANGE = colors.HexColor('#FF9500')
ACCENT_ORANGE_LIGHT = colors.HexColor('#FFF6E8')
ACCENT_ORANGE_BORDER = colors.HexColor('#FFE4BD')

ACCENT_PURPLE = colors.HexColor('#AF52DE')
ACCENT_PURPLE_LIGHT = colors.HexColor('#F9F0FC')

HOME_BAR = colors.HexColor('#C7C7CC')

# ---------------------------------------------------------
# STYLES FACTORY
# ---------------------------------------------------------
def style(name, font='HN', size=10, leading=14.5, color=TEXT_PRIMARY, bold=False):
    return ParagraphStyle(
        name,
        fontName='HN-Bold' if bold else font,
        fontSize=size,
        leading=leading,
        textColor=color
    )

S_HEADER_TAG = style('HTag', font='HN-Bold', size=8.5, leading=11, color=ACCENT_BLUE)
S_HEADER_TITLE = style('HTitle', font='HN-Bold', size=16.5, leading=20.5, color=TEXT_PRIMARY)
S_HEADER_SUB = style('HSub', font='HN', size=9.2, leading=13.2, color=TEXT_SECONDARY)

# ---------------------------------------------------------
# DRAWING PRIMITIVES
# ---------------------------------------------------------
def draw_page_base(c, page_num, total_pages, category_tag):
    c.saveState()
    # iOS Background
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Top Status Pill
    clean_tag = category_tag.upper()
    font_name = 'HN-Bold'
    font_size = 7.5
    tw = c.stringWidth(clean_tag, font_name, font_size)
    pill_pad = 9
    pill_h = 18
    pill_w = tw + (pill_pad * 2)
    pill_x = MARGIN_X
    pill_y = PAGE_H - 40

    c.setFillColor(ACCENT_BLUE_LIGHT)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 9, fill=1, stroke=0)

    c.setFont(font_name, font_size)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(pill_x + pill_pad, pill_y + 5, clean_tag)

    # Page Counter (e.g. 01 / 12)
    page_str = f"{page_num:02d} / {total_pages:02d}"
    c.setFont('HN-Medium', 9)
    c.setFillColor(TEXT_MUTED)
    c.drawRightString(PAGE_W - MARGIN_X, pill_y + 5, page_str)

    # Hairline divider
    c.setStrokeColor(DIVIDER_COLOR)
    c.setLineWidth(0.5)
    c.line(MARGIN_X, pill_y - 7, PAGE_W - MARGIN_X, pill_y - 7)

    # Bottom Home Indicator (iOS Bar)
    c.setFillColor(HOME_BAR)
    c.roundRect((PAGE_W - 124) / 2, 12, 124, 4.5, 2.25, fill=1, stroke=0)
    c.restoreState()


class ItemBlock:
    def __init__(self, paragraph, gap_after=5):
        self.paragraph = paragraph
        self.gap_after = gap_after
        self.height = 0


class AppleCard:
    def __init__(self, bg_color=CARD_BG, border_color=CARD_BORDER, radius=14, pad_x=14, pad_y=12):
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius
        self.pad_x = pad_x
        self.pad_y = pad_y
        self.items = []
        self.total_h = 0

    def add_text(self, text, style_obj, gap_after=5):
        self.items.append(ItemBlock(Paragraph(text, style_obj), gap_after))

    def calculate_height(self, width=CARD_W):
        inner_w = width - (self.pad_x * 2)
        content_h = 0
        for i, item in enumerate(self.items):
            gap = item.gap_after if i < len(self.items) - 1 else 0
            w, h = item.paragraph.wrap(inner_w, 1000)
            item.height = h
            content_h += h + gap
        self.total_h = content_h + (self.pad_y * 2)
        return self.total_h

    def draw(self, c, x, y_top, width=CARD_W):
        h = self.total_h
        y_bottom = y_top - h

        c.saveState()
        c.setFillColor(self.bg_color)
        if self.border_color:
            c.setStrokeColor(self.border_color)
            c.setLineWidth(1)
            c.roundRect(x, y_bottom, width, h, self.radius, fill=1, stroke=1)
        else:
            c.roundRect(x, y_bottom, width, h, self.radius, fill=1, stroke=0)
        c.restoreState()

        curr_y = y_top - self.pad_y
        inner_w = width - (self.pad_x * 2)
        inner_x = x + self.pad_x

        for i, item in enumerate(self.items):
            item.paragraph.drawOn(c, inner_x, curr_y - item.height)
            gap = item.gap_after if i < len(self.items) - 1 else 0
            curr_y -= (item.height + gap)

        return y_bottom


def render_page(c, page_num, total_pages, category_tag, hero_tag, hero_title, hero_desc, cards, start_y=784):
    draw_page_base(c, page_num, total_pages, category_tag)

    curr_y = start_y

    if hero_tag:
        p_tag = Paragraph(f"<b>{hero_tag.upper()}</b>", S_HEADER_TAG)
        w, h = p_tag.wrap(CARD_W, 50)
        p_tag.drawOn(c, MARGIN_X, curr_y - h)
        curr_y -= (h + 3)

    if hero_title:
        p_title = Paragraph(hero_title, S_HEADER_TITLE)
        w, h = p_title.wrap(CARD_W, 100)
        p_title.drawOn(c, MARGIN_X, curr_y - h)
        curr_y -= (h + 3)

    if hero_desc:
        p_desc = Paragraph(hero_desc, S_HEADER_SUB)
        w, h = p_desc.wrap(CARD_W, 100)
        p_desc.drawOn(c, MARGIN_X, curr_y - h)
        curr_y -= (h + 10)
    else:
        curr_y -= 8

    # Calculate card heights and distribute dynamically
    for card in cards:
        card.calculate_height(CARD_W)

    total_cards_h = sum(card.total_h for card in cards)
    bottom_limit = 24
    available_space = curr_y - bottom_limit

    # Dynamic gap calculation
    if len(cards) > 1:
        gap = (available_space - total_cards_h) / (len(cards) - 1)
        gap = max(6, min(14, gap))
    else:
        gap = 0

    for card in cards:
        bottom_y = card.draw(c, MARGIN_X, curr_y, CARD_W)
        curr_y = bottom_y - gap

    c.showPage()


def build_pdf(filename="til_bilimi_apple_mobile.pdf"):
    c = canvas.Canvas(filename, pagesize=(PAGE_W, PAGE_H))
    TOTAL_PAGES = 12

    # =========================================================================
    # PAGE 1: COVER & NAVIGATION OVERVIEW
    # =========================================================================
    draw_page_base(c, 1, TOTAL_PAGES, "Мобильді оқулық-конспект")
    curr_y = 782

    # Hero Cover Card
    c_hero = AppleCard(bg_color=CARD_BG, border_color=CARD_BORDER, radius=16, pad_x=16, pad_y=14)
    c_hero.add_text("🏛 ЖАЛПЫ ТІЛ БІЛІМІ ЖӘНЕ ГРЕК ЛИНГВИСТИКАСЫ", style('P1', font='HN-Bold', size=8.5, leading=11, color=ACCENT_BLUE), gap_after=5)
    c_hero.add_text("Жалпы тіл білімі және грек философиясы", style('P2', font='HN-Bold', size=18, leading=22, color=TEXT_PRIMARY), gap_after=5)
    c_hero.add_text("Теориялық негіздер, тарихи дәуірлер, көне грек ілімдері және қазақша оқулықтар шолуының кешенді конспектісі.", style('P3', font='HN', size=9.5, leading=13.5, color=TEXT_SECONDARY), gap_after=0)
    c_hero.calculate_height(CARD_W)
    bottom_y = c_hero.draw(c, MARGIN_X, curr_y, CARD_W)
    curr_y = bottom_y - 10

    # Modules Table of Contents (Grouped iOS TableView)
    p_mod_title = Paragraph("<b>НЕГІЗГІ БӨЛІМДЕР МЕН ТАПСЫРМАЛАР ИНДЕКСІ</b>", style('ModH', font='HN-Bold', size=8, leading=10, color=TEXT_MUTED))
    w, h = p_mod_title.wrap(CARD_W, 30)
    p_mod_title.drawOn(c, MARGIN_X + 2, curr_y - h)
    curr_y -= (h + 6)

    # 11 Modules Table Container
    c_index = AppleCard(bg_color=CARD_BG, border_color=CARD_BORDER, radius=14, pad_x=12, pad_y=8)
    modules = [
        ("02", "Жалпы тіл білімі және оның 3 құрамдас бөлігі"),
        ("03", "Тіл білімі тарихы: Ежелгі заман және Орта ғасырлар"),
        ("04", "Жаңа дәуірден қазіргі кезеңге дейін & Қазақ лингвистикасы"),
        ("05", "«Жалпы тіл білімі» қазақша оқулықтар шолуы"),
        ("06", "Грек тілінің тарихы, әліпбиі (24 әріп) және кезеңдері"),
        ("07", "Грек ойшылдары (Диодор, Гераклит, Демокрит)"),
        ("08", "Платон («Кратил» диалогы) мен Аристотель ілімі"),
        ("09", "Грек лингвистикасының 4 мәселесі & Стоиктер мектебі"),
        ("10", "Аналогия мен Аномалия: Александрия vs Пергам"),
        ("11", "Биологиялық (Шлейхер) және Әлеуметтік (Соссюр) бағыттар"),
        ("12", "Грек тілінің әлемдік маңызы және қазіргі қолданысы"),
    ]

    for i, (num, mod_title) in enumerate(modules):
        gap = 4 if i < len(modules) - 1 else 0
        line_html = f"<font color='{ACCENT_BLUE}'><b>{num}</b></font> &nbsp; <b>{mod_title}</b>"
        c_index.add_text(line_html, style(f'ModL{i}', font='HN', size=8.5, leading=11.5, color=TEXT_PRIMARY), gap_after=gap)

    c_index.calculate_height(CARD_W)
    bottom_y = c_index.draw(c, MARGIN_X, curr_y, CARD_W)
    curr_y = bottom_y - 8

    # Bottom Metadata Pill
    c_bot = AppleCard(bg_color=ACCENT_BLUE_LIGHT, border_color=ACCENT_BLUE_BORDER, radius=11, pad_x=12, pad_y=7)
    c_bot.add_text("📱 <b>Apple Minimalist Form</b> • 12 толыққанды мобилді экрандық конспект", style('BotP', font='HN', size=8.5, leading=11, color=ACCENT_BLUE), gap_after=0)
    c_bot.calculate_height(CARD_W)
    c_bot.draw(c, MARGIN_X, curr_y, CARD_W)

    c.showPage()

    # =========================================================================
    # PAGE 2: ЖАЛПЫ ТІЛ БІЛІМІ ЖӘНЕ ОНЫҢ 3 БӨЛІГІ
    # =========================================================================
    cards_p2 = []

    c2_1 = AppleCard(radius=14, pad_x=14, pad_y=12)
    c2_1.add_text("<font color='#007AFF'><b>🌐 ЖАЛПЫ ТІЛ БІЛІМІ (GENERAL LINGUISTICS)</b></font>", style('C2_1T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=5)
    c2_1.add_text("Тілдің табиғатын, мәні мен қоғамдық қызметін, ішкі құрылымы мен деңгейлерін (фонетика, лексика, грамматика) және әлем тілдеріне ортақ даму заңдылықтарын зерттейтін тіл білімінің <b>іргелі теориялық саласы</b>.", style('C2_1B', font='HN', size=9.5, leading=14, color=TEXT_PRIMARY), gap_after=0)
    cards_p2.append(c2_1)

    c2_2 = AppleCard(radius=14, pad_x=14, pad_y=12)
    c2_2.add_text("<font color='#5856D6'><b>🧩 ТІЛ БІЛІМІНІҢ ҮШ ҚҰРАМДАС БӨЛІГІ</b></font>", style('C2_2T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=6)
    c2_2.add_text("<b>1. Тіл білімінің тарихы:</b> Лингвистикалық ой-пікірлердің, мектептер мен бағыттардың туу, қалыптасу және даму жолын зерттейді.<br/><br/><b>2. Зерттеу әдіс-тәсілдері:</b> Сипаттамалы, салыстырмалы-тарихи, салғастырмалы, құрылымдық (структуралық), лингвистикалық география әдістері.<br/><br/><b>3. Тіл теориясы:</b> Тілдік универсалияларды, тіл мен ойлаудың, тіл мен қоғамның қарым-қатынасын (глоттогония, социолингвистика, психолингвистика, когнитология) қарастырады.", style('C2_2B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p2.append(c2_2)

    c2_3 = AppleCard(bg_color=ACCENT_GREEN_LIGHT, border_color=ACCENT_GREEN_BORDER, radius=13, pad_x=14, pad_y=10)
    c2_3.add_text("<b>💡 НЕГІЗГІ МАҚСАТЫ</b>", style('C2_3T', font='HN-Bold', size=9.5, leading=12, color=ACCENT_GREEN), gap_after=3)
    c2_3.add_text("Жеке бір тілдің ерекшелігін емес, күллі адамзат тілінің әмбебап қағидаттары мен адам санасындағы тілдік кодтың әмбебап заңдылықтарын ашу.", style('C2_3B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p2.append(c2_3)

    render_page(c, 2, TOTAL_PAGES, "Теориялық кіріспе", "БӨЛІМ 01", "Жалпы тіл білімі және оның құрылымы", "Лингвистиканың пәндік анықтамасы мен үш негізгі құрамдас бөлігі", cards_p2)

    # =========================================================================
    # PAGE 3: ТІЛ БІЛІМІ ТАРИХЫ: ЕЖЕЛГІ ЖӘНЕ ОРТА ҒАСЫР
    # =========================================================================
    cards_p3 = []

    c3_1 = AppleCard(radius=14, pad_x=14, pad_y=11)
    c3_1.add_text("<font color='#007AFF'><b>🏛 1. ЕЖЕЛГІ ЗАМАН ЛИНГВИСТИКАСЫ (б.д. V ғ. дейін)</b></font>", style('C3_1T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c3_1.add_text("• <b>Египет & Месопотамия/Вавилон:</b> Жазу таңбалары, жазба мектептері.<br/>• <b>Көне Үндістан (Панини):</b> Көне санскриттің қатаң 4000-ға жуық ережесінен тұратын үлгілі құрылымдық грамматикасы жасалды.<br/>• <b>Көне Қытай:</b> Иероглифика, семантика мен сөздік құрастыру схоластикасы.<br/>• <b>Көне Грекия & Рим:</b> Зат пен сөз байланысы, сөз таптары, грамматика (Платон, Аристотель, Стоиктер, Александрия мектебі, Варрон).", style('C3_1B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p3.append(c3_1)

    c3_2 = AppleCard(radius=14, pad_x=14, pad_y=11)
    c3_2.add_text("<font color='#5856D6'><b>🌙 2. ОРТА ҒАСЫРЛАР ЛИНГВИСТИКАСЫ (V–XV ғғ.)</b></font>", style('C3_2T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c3_2.add_text("• <b>Араб халифаты:</b> Басра, Куфа, Бағдат грамматика мектептері.<br/>• <b>Әбу Насыр әл-Фараби & Ибн Сина:</b> Тіл мен логиканың арақатынасын талдаған философиялық-тілдік еңбектер жазды.<br/>• <b>Махмұд Қашқари («Диуани лұғат ат-түрк»):</b> Тұңғыш салыстырмалы-тарихи түркі сөздігі мен этнолингвистикалық шедеврі (1074 ж.).<br/>• <b>Махмұд Замахшари:</b> Араб-түркі грамматикасының озық жүйесі.<br/>• <b>Әлішер Науаи («Мухакамат ал-луғатайн»):</b> Түркі тілінің байлығы мен көркемдік қуатын парсы тілімен салғастыра қорғады.", style('C3_2B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p3.append(c3_2)

    render_page(c, 3, TOTAL_PAGES, "Лингвистика тарихы I", "БӨЛІМ 02", "Ежелгі заман және Орта ғасырлар", "Әлемдік өркениеттер және түркі топырағындағы іргелі лингвистика", cards_p3)

    # =========================================================================
    # PAGE 4: ЖАҢА ДӘУІР, XIX-XX ҒҒ. & ҚАЗАҚ ТІЛ БІЛІМІ
    # =========================================================================
    cards_p4 = []

    c4_1 = AppleCard(radius=13, pad_x=13, pad_y=9)
    c4_1.add_text("<font color='#007AFF'><b>⚙️ ҚАЙТА ӨРЛЕУ ЖӘНЕ ЖАҢА ДӘУІР (XV–XVIII ғғ.)</b></font>", style('C4_1T', font='HN-Bold', size=10, leading=13, color=TEXT_PRIMARY), gap_after=4)
    c4_1.add_text("Ұлт тілдерінің грамматикаларының жазылуы; Пор-Рояль әмбебап логикалық грамматикасы (А. Арно, К. Лансло); тіл философиясы (Бэкон, Декарт, Локк, Лейбниц).", style('C4_1B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p4.append(c4_1)

    c4_2 = AppleCard(radius=13, pad_x=13, pad_y=9)
    c4_2.add_text("<font color='#FF9500'><b>🔬 XIX ҒАСЫР: САЛЫСТЫРМАЛЫ-ТАРИХИ ТІЛ БІЛІМІ</b></font>", style('C4_2T', font='HN-Bold', size=10, leading=13, color=TEXT_PRIMARY), gap_after=4)
    c4_2.add_text("• <b>Компаративистика:</b> Ф. Бопп, Я. Гримм, Р. Раск, А. Востоков.<br/>• <b>Ағымдар:</b> В. Гумбольдт ілімі; биологиялық (А. Шлейхер); психологиялық (Г. Штейнталь, А. Потебня); Қазан мектебі (Б. де Куртенэ — фонема теориясы).<br/>• <b>Түркітану:</b> Шоқан Уәлиханов пен Ыбырай Алтынсариннің ғылыми көзқарастары.", style('C4_2B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p4.append(c4_2)

    c4_3 = AppleCard(radius=13, pad_x=13, pad_y=9)
    c4_3.add_text("<font color='#34C759'><b>🇰🇿 XX ҒАСЫР ЖӘНЕ ҚАЗАҚ ТІЛ БІЛІМІ</b></font>", style('C4_3T', font='HN-Bold', size=10, leading=13, color=TEXT_PRIMARY), gap_after=4)
    c4_3.add_text("• <b>Әлемдік деңгейде:</b> Ф. де Соссюр («Жалпы лингвистика курсы») және Структурализм (Прага, Копенгаген, АҚШ дескриптивтік, Лондон мектептері).<br/>• <b>Қазақ тіл білімінің іргетасы:</b> <b>Ахмет Байтұрсынұлы</b> (төте жазу әліпбиі, тұңғыш «Тіл – құрал» оқулығы, ұлттық лингвистикалық терминология), <b>Халел Досмұхамедұлы</b>, <b>Телжан Шонанұлы</b> және <b>Құдайберген Жұбанов</b>.", style('C4_3B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p4.append(c4_3)

    render_page(c, 4, TOTAL_PAGES, "Лингвистика тарихы II", "БӨЛІМ 03", "Жаңа дәуірден қазіргі кезеңге дейін", "Компаративистика, Соссюр структурализмі және Алаш зиялылары", cards_p4)

    # =========================================================================
    # PAGE 5: ҚАЗАҚША ӘДЕБИЕТТЕР ШОЛУЫ
    # =========================================================================
    cards_p5 = []

    c5_1 = AppleCard(radius=13, pad_x=14, pad_y=11)
    c5_1.add_text("<font color='#007AFF'><b>📚 1. ІРГЕЛІ КЛАССИКАЛЫҚ ОҚУЛЫҚТАР</b></font>", style('C5_1T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c5_1.add_text("• <b>Кәкен Аханов — «Тіл білімінің негіздері»:</b> Қазақ филологиясындағы тіл теориясы мен жалпы терминологияның классикалық оқулығы.<br/>• <b>Т. Қордабаев, Ғ. Қалиев — «Жалпы тіл білімі»:</b> Студенттерге арналған, тілдің жүйелік табиғатын баяндайтын іргелі оқулық.<br/>• <b>Әбдуали Хасенов — «Тіл білімі»:</b> Фонетика, лексика, грамматика мен тарихи даму заңдылықтары.<br/>• <b>Бектұрсын Қалиұлы — «Жалпы тіл білімі»:</b> Лингвистикалық ілімдер тарихы.", style('C5_1B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p5.append(c5_1)

    c5_2 = AppleCard(radius=13, pad_x=14, pad_y=11)
    c5_2.add_text("<font color='#5856D6'><b>💻 2. ЗАМАНАУИ УНИВЕРСИТЕТ БАСЫЛЫМДАРЫ</b></font>", style('C5_2T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c5_2.add_text("• <b>Ш. Жалмаханов — «Жалпы тіл білімі. Тіл білімінің тарихы» (2026 ж.):</b> Әлемдік лингвистика, түркітану және цифрлық/AI технологиялары қамтылған ең соңғы жаңа оқулық.<br/>• <b>Х.А. Ордабекова — «Тіл біліміне кіріспе» (2016 ж.):</b> Тілдің таңбалық-құрылымдық және антропоөзектік аспектілері.", style('C5_2B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p5.append(c5_2)

    c5_3 = AppleCard(radius=13, pad_x=14, pad_y=10)
    c5_3.add_text("<font color='#30B0C7'><b>🌍 3. ӘЛЕМДІК КЛАССИКА АУДАРМАСЫ</b></font>", style('C5_3T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=4)
    c5_3.add_text("• <b>В. Фромкин, Р. Родман, Н. Хайамс — «Тіл біліміне кіріспе» (2018 ж.):</b> «Рухани жаңғыру» жобасы аясында қазақшаға тәржімаланған психолингвистика, нейролингвистика және компьютерлік лингвистиканың озық 10-басылымы.", style('C5_3B', font='HN', size=8.8, leading=12.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p5.append(c5_3)

    render_page(c, 5, TOTAL_PAGES, "Әдебиеттер шолуы", "БӨЛІМ 04", "Қазақша «Жалпы тіл білімі» әдебиеттері", "Ғылыми-зерттеу негізінде сараланған іргелі оқулықтар мен басылымдар", cards_p5)

    # =========================================================================
    # PAGE 6: ГРЕК ТІЛІНІҢ ТАРИХЫ, ӘЛІПБИІ МЕН ДӘУІРЛЕРІ
    # =========================================================================
    cards_p6 = []

    c6_1 = AppleCard(radius=14, pad_x=14, pad_y=12)
    c6_1.add_text("<font color='#007AFF'><b>🔤 ДАУЫСТЫ-ДЫБЫСТЫҚ ЖАЗУ ЖӘНЕ 24 ӘРІП</b></font>", style('C6_1T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=5)
    c6_1.add_text("• <b>Жаңашылдығы:</b> Ежелгі Грецияда б.д.д. I мыңжылдықтың басында дауыссыз дыбыстармен қатар дауыстыларды да таңбалайтын жазу қалыптасты.<br/>• <b>24 әріптік алфавит:</b> Б.д.д. IV ғасырда 17 дауыссыз бен 7 дауысты дыбысты толық бейнелейтін кемел әліпби бекіді.<br/>• <b>Әлемдік мұра:</b> Осы грек жазуының негізінде латын алфавиті, кейіннен кириллица (славян/орыс әліпбиі) қалыптасып дамыды.", style('C6_1B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p6.append(c6_1)

    c6_2 = AppleCard(radius=14, pad_x=14, pad_y=12)
    c6_2.add_text("<font color='#5856D6'><b>🏛 «КОЙНЕ» ТІЛІ ЖӘНЕ ЛИНГВИСТИКАНЫҢ ҚОС КЕЗЕҢІ</b></font>", style('C6_2T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=5)
    c6_2.add_text("• <b>«Койне» (ортақ тіл):</b> Б.д.д. IV ғасырда эллинизм дәуірінде жергілікті диалектілер тоғысып, жалпыхалықтық ортақ грек тілі дүниеге келді.<br/>• <b>1. Философиялық дәуір (б.д.д. V – III ғғ.):</b> Тіл мәселелері табиғат пен ойлауды тану аясында, философия шеңберінде қаралды.<br/>• <b>2. Филологиялық / Александриялық дәуір (б.д.д. III – б.д. IV ғғ.):</b> Тіл білімі мен грамматика өз алдына дербес ғылым болып бөлінді.", style('C6_2B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p6.append(c6_2)

    render_page(c, 6, TOTAL_PAGES, "Көне Грек тілі", "БӨЛІМ 05", "Грек тілінің тарихы, әліпбиі мен кезеңдері", "24 әріптік вокалды жазу, «Койне» тілі және лингвистиканың қос кезеңі", cards_p6)

    # =========================================================================
    # PAGE 7: ГРЕК ОЙШЫЛДАРЫ: ДИОДОР, ГЕРАКЛИТ, ДЕМОКРИТ
    # =========================================================================
    cards_p7 = []

    c7_1 = AppleCard(radius=13, pad_x=14, pad_y=10)
    c7_1.add_text("<font color='#007AFF'><b>ДИОДОР СИЦИЛИЙСКИЙ</b></font> &nbsp;<font color='#8E8E93' size=8>(б.д.д. 90–21 жж.)</font>", style('C7_1T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=4)
    c7_1.add_text("• <b>Жұпыны өмір:</b> Адамдар алғашында жануарлармен қатар өте қарапайым әрі қауіпті күйде өмір сүрген.<br/>• <b>Қорғану және топтасу:</b> Жыртқыштардан сақтану үшін бір-біріне дауыстап белгі беріп топтасқан.<br/>• <b>Таңбаға айналу:</b> Бастапқы мағынасыз дауыстар уақыт өте заттар мен құбылыстардың тұрақты мағыналы атауына (символына) айналды.", style('C7_1B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p7.append(c7_1)

    c7_2 = AppleCard(radius=13, pad_x=14, pad_y=10)
    c7_2.add_text("<font color='#34C759'><b>ГЕРАКЛИТ ЭФЕССКИЙ</b></font> &nbsp;<font color='#8E8E93' size=8>(б.д.д. 540–480 жж.)</font>", style('C7_2T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=4)
    c7_2.add_text("• <b>Табиғи байланыс (фюсей):</b> Зат пен атау табиғи ажырамас бірлікте болады.<br/>• <b>Ішкі мән:</b> Атау заттың ішкі мәні мен болмысын туа біткен қалпында ашып тұрады деп тұжырымдады.", style('C7_2B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p7.append(c7_2)

    c7_3 = AppleCard(radius=13, pad_x=14, pad_y=10)
    c7_3.add_text("<font color='#FF9500'><b>ДЕМОКРИТ</b></font> &nbsp;<font color='#8E8E93' size=8>(б.д.д. 460–370 жж.)</font>", style('C7_3T', font='HN-Bold', size=11, leading=14, color=TEXT_PRIMARY), gap_after=4)
    c7_3.add_text("• <b>Шартты келісім:</b> Зат пен атау байланысы табиғи емес, адамдардың <b>шартты келісіміне және әдет-ғұрпына</b> байланысты.<br/>• <b>Дәлелдейтін 4 уәжі:</b><br/>&nbsp;&nbsp;1) <i>Көпмағыналылық:</i> бір сөздің бірнеше мағынасы болады;<br/>&nbsp;&nbsp;2) <i>Синонимия:</i> бір ұғымның бірнеше бөлек атауы бар;<br/>&nbsp;&nbsp;3) <i>Сөзді ауыстыру:</i> сөзді басқа балама сөзбен ауыстыруға болады;<br/>&nbsp;&nbsp;4) <i>Атаусыз ұғымдар:</i> көптеген ұғымдардың тіпті сөздік атауы жоқ.", style('C7_3B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p7.append(c7_3)

    render_page(c, 7, TOTAL_PAGES, "Антикалық ойшылдар I", "БӨЛІМ 06", "Грек философтары тіл туралы не деді? (I)", "Диодор, Гераклит және Демокриттің тіл табиғаты туралы тұжырымдары", cards_p7)

    # =========================================================================
    # PAGE 8: ПЛАТОН МЕН АРИСТОТЕЛЬ
    # =========================================================================
    cards_p8 = []

    c8_1 = AppleCard(radius=14, pad_x=15, pad_y=14)
    c8_1.add_text("<font color='#007AFF'><b>🏛 ПЛАТОН — «КРАТИЛ» ДИАЛОГЫ</b></font> &nbsp;<font color='#8E8E93' size=8.5>(б.д.д. 428–348 жж.)</font>", style('C8_1T', font='HN-Bold', size=11.5, leading=15, color=TEXT_PRIMARY), gap_after=6)
    c8_1.add_text("• <b>Диалог мәні:</b> Кратилдің (атау затқа табиғатынан сай келеді) және Гермогеннің (атау тек келісім бойынша қойылады) көзқарастарын сараптады.<br/>• <b>Ішкі мақсаттылық:</b> Тілде ретсіздік емес, ішкі үйлесім бар. Бастапқыда дыбыс пен мағына арасында табиғи байланыс болып, ұрпақтар қолдана келе ол <b>қоғамдық-тарихи дәстүрге</b> айналған.<br/>• <b>Синтаксистік жаңалығы:</b> Тіл тарихында тұңғыш рет сөздерді <b>есімдер</b> (сөйлемдегі бастауыш) және <b>етістіктер</b> (баяндауыш) деп синтаксистік жағынан бөлді.", style('C8_1B', font='HN', size=9.8, leading=14.2, color=TEXT_PRIMARY), gap_after=0)
    cards_p8.append(c8_1)

    c8_2 = AppleCard(radius=14, pad_x=15, pad_y=14)
    c8_2.add_text("<font color='#5856D6'><b>⚖️ АРИСТОТЕЛЬ ЖӘНЕ ДЫБЫСТАР ЖІКТЕЛІСІ</b></font> &nbsp;<font color='#8E8E93' size=8.5>(б.д.д. 384–322 жж.)</font>", style('C8_2T', font='HN-Bold', size=11.5, leading=15, color=TEXT_PRIMARY), gap_after=6)
    c8_2.add_text("• <b>Сөйлеу — адамның басты белгісі:</b> Адамның жануардан басты өзгешелігі – оның сөйлейтіндігінде. Жануарлар дауыспен тек эмоцияны білдірсе, адам сөйлеу арқылы жақсылық пен жамандықты, әділеттілік пен әділетсіздікті таниды.<br/>• <b>Шартты таңба:</b> Зат пен сөздің қатынасын <b>саналы, шартты (келісімді)</b> деп санады.<br/>• <b>Фонетикалық негіз:</b> Тіл дыбыстарын тұңғыш рет <b>дауысты</b> және <b>дауыссыз</b> деп жіктеді.", style('C8_2B', font='HN', size=9.8, leading=14.2, color=TEXT_PRIMARY), gap_after=0)
    cards_p8.append(c8_2)

    render_page(c, 8, TOTAL_PAGES, "Антикалық ойшылдар II", "БӨЛІМ 07", "Платон мен Аристотельдің тіл ілімі", "«Кратил» диалогы, бастауыш пен баяндауыш және дыбыстар жүйесі", cards_p8)

    # =========================================================================
    # PAGE 9: ГРЕК ФИЛОСОФТАРЫ КӨТЕРГЕН 4 МӘСЕЛЕ ЖӘНЕ САЛАЛЫҚ ҒАЛЫМДАР
    # =========================================================================
    cards_p9 = []

    c9_1 = AppleCard(radius=13, pad_x=14, pad_y=11)
    c9_1.add_text("<font color='#007AFF'><b>1. ҮШ ІРГЕЛІ ТЕОРИЯЛЫҚ МӘСЕЛЕ</b></font>", style('C9_1T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c9_1.add_text("• <b>Тілдің шығуы (глоттогония):</b> Тіл табиғи жолмен туды ма («фюсей»), әлде адамдардың келісімі арқылы жасалды ма («тесей»)?<br/>• <b>Сөз бен заттың қатынасы:</b> Атау заттың ішкі мәнін аша ма, әлде еркін қойылған шартты таңба ма?<br/>• <b>Аналогия мен аномалия:</b> Тілде қатаң грамматикалық заңдылық басым ба, әлде ауытқулар ма?", style('C9_1B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p9.append(c9_1)

    c9_2 = AppleCard(radius=13, pad_x=14, pad_y=11)
    c9_2.add_text("<font color='#34C759'><b>2. ЖЕКЕЛЕГЕН ЛИНГВИСТИКАЛЫҚ САЛАЛАР МЕН ҒАЛЫМДАР</b></font>", style('C9_2T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=5)
    c9_2.add_text("• <b>Анаксимен:</b> «Риторика» еңбегі арқылы стилистика негіздерін қалады.<br/>• <b>Парменид:</b> Грамматикалық мағына мен логикалық мағынаның арасын ажыратты.<br/>• <b>Продик:</b> Синонимиканы және сөз мағынасы реңктерін зерттеді.<br/>• <b>Протагор:</b> Зат есім тегін (род), етістік шақтарын және сөйлем түрлерін белгіледі.<br/>• <b>Стоиктер мектебі (Хрисипп, Кратес):</b> «Сөз таптары» терминін енгізді, **этимология** ғылымының негізін салды, септіктерді жүйеледі, 24 әріпті дауысты-дауыссызға бөлді.", style('C9_2B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p9.append(c9_2)

    render_page(c, 9, TOTAL_PAGES, "Лингвистика салалары", "БӨЛІМ 08", "Грек ойшылдары көтерген 4 мәселе", "Теориялық дилеммалар мен дербес тілдік салалардың негізін қалаушылар", cards_p9)

    # =========================================================================
    # PAGE 10: АНАЛОГИЯ МЕН АНОМАЛИЯЛЫҚ ТАЛДАУ
    # =========================================================================
    cards_p10 = []

    c10_1 = AppleCard(radius=13, pad_x=14, pad_y=10)
    c10_1.add_text("<font color='#007AFF'><b>📍 ПАЙДА БОЛУЫ ЖӘНЕ ТАРАЛУЫ</b></font>", style('C10_1T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=4)
    c10_1.add_text("Александрия кітапханасы төңірегіндегі <b>Александрия грамматистер мектебі</b> мен <b>Пергам мектебі</b> арасында туындады. Кейін Римге өтіп (Юлий Цезарь мен Цицерон), Араб халифатына жетті (Басра мен Куфа мектептері).", style('C10_1B', font='HN', size=9.2, leading=13.2, color=TEXT_PRIMARY), gap_after=0)
    cards_p10.append(c10_1)

    c10_2 = AppleCard(bg_color=CARD_BG, border_color=ACCENT_BLUE_BORDER, radius=13, pad_x=14, pad_y=11)
    c10_2.add_text("<font color='#007AFF'><b>📐 АНАЛОГИЯ (АНАЛОГИЗМ) — АРИСТАРХ (б.д.д. II ғ.)</b></font>", style('C10_2T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=4)
    c10_2.add_text("• <b>Өкілдері:</b> Аристарх, Юлий Цезарь, Басра лингвистері.<br/>• <b>Тұжырымы:</b> Тіл – іштей жарасым тапқан жүйе (гармония). Мысалы: грек және латын тілдерінде зат есімдердің <b>3 грамматикалық родқа</b> бөлінуі — жүйеліліктің айқын белгісі.<br/>• <b>Талабы:</b> Тілде заңдылық үстем, ауытқулар мен варваризмдерді жойып, қатаң нормаға бағындыру керек.", style('C10_2B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p10.append(c10_2)

    c10_3 = AppleCard(bg_color=CARD_BG, border_color=ACCENT_ORANGE_BORDER, radius=13, pad_x=14, pad_y=11)
    c10_3.add_text("<font color='#FF9500'><b>🌊 АНОМАЛИЯ (АНОМАЛИЗМ) — КРАТЕС (б.д.д. 170 ж.)</b></font>", style('C10_3T', font='HN-Bold', size=10.5, leading=13.5, color=TEXT_PRIMARY), gap_after=4)
    c10_3.add_text("• <b>Өкілдері:</b> Кратес, Цицерон, Куфа лингвистері.<br/>• <b>Тұжырымы:</b> Тілде заңдылықтан гөрі ауытқулар (аномалия), форма мен мазмұн сәйкессіздігі көп. Тіл халықтың еркін сөйлеу қолданысынан туады.<br/>• <b>Талабы:</b> Тілді жасанды түрде «түзеймін» деу — тілдің табиғатына қайшы іс.", style('C10_3B', font='HN', size=9, leading=13, color=TEXT_PRIMARY), gap_after=0)
    cards_p10.append(c10_3)

    render_page(c, 10, TOTAL_PAGES, "Ғылыми дискуссия", "БӨЛІМ 09", "Аналогия мен аномалиялық талдау", "Александрия мен Пергам мектептерінен бастау алған ғасырлар пікірталасы", cards_p10)

    # =========================================================================
    # PAGE 11: БИОЛОГИЯЛЫҚ ЖӘНЕ ӘЛЕУМЕТТІК БАҒЫТТАР
    # =========================================================================
    cards_p11 = []

    c11_1 = AppleCard(radius=14, pad_x=15, pad_y=13)
    c11_1.add_text("<font color='#34C759'><b>🌿 1. БИОЛОГИЯЛЫҚ (НАТУРАЛИСТІК) БАҒЫТ</b></font>", style('C11_1T', font='HN-Bold', size=11, leading=14.5, color=TEXT_PRIMARY), gap_after=5)
    c11_1.add_text("• <b>Негізін салушы:</b> Август Шлейхер (1821–1868).<br/>• <b>Тұжырымы:</b> Тілді адам қоғамынан тыс, өзіндік заңымен туып, өсіп-өнетін, қартайып өлетін <b>биологиялық организм</b> деп қарастырды.<br/>• <b>Дарвинизм:</b> Ч. Дарвиннің эволюциялық ілімін тілге көшіріп, «тілдер де тіршілік үшін күреседі, мықты тілдер әлсіздерді жояды» деді.<br/>• <b>Кезеңдері:</b> 1) Тарихқа дейінгі өсу; 2) Тарихи кезеңдегі құлдырау (бүліну).", style('C11_1B', font='HN', size=9.5, leading=13.8, color=TEXT_PRIMARY), gap_after=0)
    cards_p11.append(c11_1)

    c11_2 = AppleCard(radius=14, pad_x=15, pad_y=13)
    c11_2.add_text("<font color='#007AFF'><b>👥 2. ӘЛЕУМЕТТІК (СОЦИОЛОГИЯЛЫҚ) БАҒЫТ</b></font>", style('C11_2T', font='HN-Bold', size=11, leading=14.5, color=TEXT_PRIMARY), gap_after=5)
    c11_2.add_text("• <b>Өкілдері:</b> Ф. де Соссюр, Антуан Мейе, Жозеф Вандриес т.б.<br/>• <b>Тұжырымы:</b> Биологиялық көзқарасқа қарсы шығып, тілді <b>адам қоғамының әлеуметтік жемісі әрі қарым-қатынас құралы</b> деп дәлелдеді.<br/>• <b>Ұжымдық сипаты:</b> Тілді жеке адам жасай да, өзгерте де алмайды, ол – ұжымдық сананың жемісі. Өзгерістер қоғамдық-тарихи факторларға тікелей тәуелді.", style('C11_2B', font='HN', size=9.5, leading=13.8, color=TEXT_PRIMARY), gap_after=0)
    cards_p11.append(c11_2)

    c11_3 = AppleCard(bg_color=ACCENT_BLUE_LIGHT, border_color=ACCENT_BLUE_BORDER, radius=13, pad_x=14, pad_y=11)
    c11_3.add_text("<b>📌 ҒЫЛЫМИ ТҮЙІН</b>", style('C11_3T', font='HN-Bold', size=10, leading=13, color=ACCENT_BLUE), gap_after=4)
    c11_3.add_text("Биологиялық мектеп тіл мен қоғамды алшақтатса, әлеуметтік бағыт тілдің адамсыз және қоғамсыз өмір сүрмейтінін дәлелдеп, қазіргі лингвистиканың іргетасын орнатты.", style('C11_3B', font='HN', size=9.2, leading=13.2, color=TEXT_PRIMARY), gap_after=0)
    cards_p11.append(c11_3)

    render_page(c, 11, TOTAL_PAGES, "Лингвистика бағыттары", "БӨЛІМ 10", "Биологиялық және әлеуметтік бағыттар", "XIX ғ. соңы мен XX ғ. басындағы тіл табиғатына екі түрлі ғылыми көзқарас", cards_p11)

    # =========================================================================
    # PAGE 12: ГРЕК ТІЛІНІҢ ӘЛЕМДІК МАҢЫЗЫ МЕН ОРНЫ
    # =========================================================================
    cards_p12 = []

    c12_1 = AppleCard(radius=14, pad_x=15, pad_y=12)
    c12_1.add_text("<font color='#007AFF'><b>🌐 1. АНТИКАЛЫҚ ӘЛЕМНІҢ ЛИНГВА ФРАНКАСЫ</b></font>", style('C12_1T', font='HN-Bold', size=11, leading=14.5, color=TEXT_PRIMARY), gap_after=5)
    c12_1.add_text("• <b>Халықаралық мәртебесі:</b> Көне дәуірде грек тілі Жерорта теңізі алабында және күллі антикалық өркениетте негізгі халықаралық қарым-қатынас тілі (лингва франка) болды.<br/>• <b>Еуропа грамматикасының анасы:</b> Александриялық <b>Дионисий Фракийскийдің «Грамматика өнері»</b> атты еңбегі барлық кейінгі еуропалық және орыс грамматикаларының төл іргетасы («анасы») болып табылды.", style('C12_1B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p12.append(c12_1)

    c12_2 = AppleCard(radius=14, pad_x=15, pad_y=12)
    c12_2.add_text("<font color='#5856D6'><b>🧬 2. ӘЛЕМДІК ҒЫЛЫМИ ТЕРМИНОЛОГИЯ ҚОРЫ</b></font>", style('C12_2T', font='HN-Bold', size=11, leading=14.5, color=TEXT_PRIMARY), gap_after=5)
    c12_2.add_text("Грек тілінің сөзжасамдық түбірлері, префикстері мен категориялары осы күнге дейін әлемдік ғылымда (<b>медицина, лингвистика, философия, астрономия, биология</b>) негізгі терминологиялық қор болып табылады.", style('C12_2B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p12.append(c12_2)

    c12_3 = AppleCard(bg_color=ACCENT_BLUE_LIGHT, border_color=ACCENT_BLUE_BORDER, radius=14, pad_x=15, pad_y=12)
    c12_3.add_text("<b>🏛 3. ҚАЗІРГІ ТАҢДАҒЫ РЕСМИ ОРНЫ</b>", style('C12_3T', font='HN-Bold', size=11, leading=14, color=ACCENT_BLUE), gap_after=4)
    c12_3.add_text("• Грекия Республикасы мен Кипрдің мемлекеттік тілі.<br/>• Еуропалық Одақтың (ЕО) 24 ресми тілінің бірі.<br/>• 3000 жылдан астам үздіксіз жазба тарихы бар әлемдегі ең көне тірі тілдердің қатарында.", style('C12_3B', font='HN', size=9.2, leading=13.5, color=TEXT_PRIMARY), gap_after=0)
    cards_p12.append(c12_3)

    render_page(c, 12, TOTAL_PAGES, "Әлемдік ықпал", "БӨЛІМ 11", "Грек тілінің маңызы мен қазіргі орны", "Антикалық мәртебе, еуропалық грамматика және қазіргі ресми мәртебесі", cards_p12)

    c.save()
    print(f"Successfully generated {filename} with {TOTAL_PAGES} pages!")

if __name__ == "__main__":
    build_pdf()
