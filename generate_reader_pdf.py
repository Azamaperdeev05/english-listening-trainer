import os
import pypdfium2 as pdfium
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

# ---------------------------------------------------------
# FONT REGISTRATION (Apple Helvetica Neue)
# ---------------------------------------------------------
pdfmetrics.registerFont(TTFont('HN', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('HN-Bold', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('HN-Italic', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=2))
pdfmetrics.registerFont(TTFont('HN-BoldItalic', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=3))
pdfmetrics.registerFont(TTFont('HN-Light', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=7))
pdfmetrics.registerFont(TTFont('HN-Medium', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=10))

pdfmetrics.registerFontFamily('HN', normal='HN', bold='HN-Bold', italic='HN-Italic', boldItalic='HN-BoldItalic')

# ---------------------------------------------------------
# DIMENSIONS & PALETTE (Apple Mobile Reader Viewport)
# ---------------------------------------------------------
PAGE_W = 390
PAGE_H = 844

COLOR_BG = colors.HexColor('#FFFFFF')
COLOR_TEXT_PRIMARY = colors.HexColor('#1C1C1E')
COLOR_TEXT_SECONDARY = colors.HexColor('#636366')
COLOR_TEXT_MUTED = colors.HexColor('#8E8E93')
COLOR_DIVIDER = colors.HexColor('#E5E5EA')

COLOR_BLUE = colors.HexColor('#007AFF')
COLOR_BLUE_BG = colors.HexColor('#F2F7FF')
COLOR_BLUE_BORDER = colors.HexColor('#D0E2FF')
COLOR_HOME_BAR = colors.HexColor('#D1D1D6')

# ---------------------------------------------------------
# CANVAS WITH RUNNING HEADER & FOOTER
# ---------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()

        # Top Running Header
        top_y = PAGE_H - 34
        self.setFont('HN-Medium', 7.5)
        self.setFillColor(COLOR_TEXT_MUTED)
        self.drawString(20, top_y, "АУДИОДӘРІС МӘТІНІ • ТОЛЫҚ ТРАНСКРИПТ")

        # Page Number top-right
        page_str = f"{self._pageNumber} / {total_pages}"
        self.drawRightString(PAGE_W - 20, top_y, page_str)

        # Hairline separator
        self.setStrokeColor(COLOR_DIVIDER)
        self.setLineWidth(0.5)
        self.line(20, top_y - 6, PAGE_W - 20, top_y - 6)

        # Bottom iOS Home Indicator
        self.setFillColor(COLOR_HOME_BAR)
        self.roundRect((PAGE_W - 120) / 2, 12, 120, 4, 2, fill=1, stroke=0)

        self.restoreState()


# ---------------------------------------------------------
# STYLES
# ---------------------------------------------------------
style_badge = ParagraphStyle(
    'Badge',
    fontName='HN-Bold',
    fontSize=8,
    leading=10,
    textColor=COLOR_BLUE,
    spaceAfter=4,
    keepWithNext=True
)

style_sec_title = ParagraphStyle(
    'SecTitle',
    fontName='HN-Bold',
    fontSize=14.5,
    leading=18.5,
    textColor=COLOR_TEXT_PRIMARY,
    spaceAfter=8,
    keepWithNext=True
)

style_body = ParagraphStyle(
    'Body',
    fontName='HN',
    fontSize=10,
    leading=15,
    textColor=COLOR_TEXT_PRIMARY,
    spaceAfter=8,
    alignment=TA_LEFT
)

style_cover_badge = ParagraphStyle(
    'CoverBadge',
    fontName='HN-Bold',
    fontSize=8.5,
    leading=11,
    textColor=COLOR_BLUE,
    spaceAfter=6
)

style_cover_title = ParagraphStyle(
    'CoverTitle',
    fontName='HN-Bold',
    fontSize=20,
    leading=24,
    textColor=COLOR_TEXT_PRIMARY,
    spaceAfter=8
)

style_cover_sub = ParagraphStyle(
    'CoverSub',
    fontName='HN',
    fontSize=10.5,
    leading=14.5,
    textColor=COLOR_TEXT_SECONDARY,
    spaceAfter=12
)

style_audio_meta = ParagraphStyle(
    'AudioMeta',
    fontName='HN-Medium',
    fontSize=9,
    leading=12,
    textColor=COLOR_BLUE,
    alignment=TA_LEFT
)


def build_text_pdf(source_md='elevenlabs_audio_script.md', output_pdf='til_bilimi_okylgan_matin.pdf'):
    # Parse source MD for audio script
    with open(source_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    for i, line in enumerate(lines):
        if '### Кіріспе' in line:
            start_idx = i
            break

    audio_lines = lines[start_idx:]

    sections = []
    curr_title = ''
    curr_paragraphs = []

    for line in audio_lines:
        line_str = line.strip()
        if line_str.startswith('### '):
            if curr_title:
                sections.append((curr_title, curr_paragraphs))
            curr_title = line_str.replace('### ', '').strip()
            curr_paragraphs = []
        elif line_str == '---':
            continue
        elif line_str:
            curr_paragraphs.append(line_str)

    if curr_title:
        sections.append((curr_title, curr_paragraphs))

    # Build Document Story
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=20,
        rightMargin=20,
        topMargin=46,
        bottomMargin=32
    )

    story = []

    # Title Hero Block
    story.append(Paragraph("АУДИОДӘРІСТІҢ ТОЛЫҚ МӘТІНІ", style_cover_badge))
    story.append(Paragraph("Жалпы тіл білімі және көне грек философиясы", style_cover_title))
    story.append(Paragraph("Дыбысталған дикторлық оқу мәтіні. Барлық сандар мен ғасырлар қазақ тілінде толықтай жазылған академиялық транскрипт.", style_cover_sub))
    story.append(Paragraph("<b>Ұзақтығы:</b> 14 минут 57 секунд &nbsp;•&nbsp; <b>Құрамы:</b> 11 негізгі тарау", style_audio_meta))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_DIVIDER, spaceAfter=14))

    # Add each section
    for idx, (title, paras) in enumerate(sections):
        # Extract section badge & clean title
        if '.' in title:
            badge_part, name_part = title.split('.', 1)
            badge_text = badge_part.strip().upper()
            title_text = name_part.strip()
        else:
            badge_text = f"{idx + 1}-БӨЛІМ".upper() if idx > 0 and idx < len(sections) - 1 else title.upper()
            title_text = title.strip()

        section_elements = []
        section_elements.append(Paragraph(f"<font color='{COLOR_BLUE}'><b>{badge_text}</b></font>", style_badge))
        section_elements.append(Paragraph(title_text, style_sec_title))
        
        # Add first paragraph attached to title to avoid orphan headings
        if paras:
            section_elements.append(Paragraph(paras[0], style_body))

        story.append(KeepTogether(section_elements))

        # Add remaining paragraphs
        for p_text in paras[1:]:
            story.append(Paragraph(p_text, style_body))

        story.append(Spacer(1, 8))
        if idx < len(sections) - 1:
            story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_DIVIDER, spaceAfter=12))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_pdf}!")


if __name__ == "__main__":
    build_text_pdf()
