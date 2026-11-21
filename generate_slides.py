import os
import shutil
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1920
OUTPUT_DIR = "slides_part1"

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"

def get_font(size, weight="bold"):
    index = 1 if weight == "bold" else (10 if weight == "medium" else 0)
    return ImageFont.truetype(FONT_PATH, size=size, index=index)

def create_base_canvas(slide_index, total_slides=11):
    img = Image.new("RGB", (WIDTH, HEIGHT), "#F2F2F7")
    draw = ImageDraw.Draw(img)

    # Top Header
    draw.text((70, 110), "ЖАЛПЫ ТІЛ БІЛІМІ", fill="#8E8E93", font=get_font(24, "bold"))
    
    # Counter Badge
    counter_str = f"{slide_index:02d} / {total_slides:02d}"
    draw.rounded_rectangle([910, 100, 1010, 144], radius=14, fill="#E5E5EA")
    draw.text((926, 110), counter_str, fill="#636366", font=get_font(22, "bold"))

    # Card Drop Shadow
    card_x1, card_y1, card_x2, card_y2 = 70, 170, 1010, 1700
    card_r = 44
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([card_x1 + 2, card_y1 + 10, card_x2 + 2, card_y2 + 10], radius=card_r, fill=(0, 0, 0, 16))
    img.paste(Image.alpha_composite(Image.new("RGBA", (WIDTH, HEIGHT), (242, 242, 247, 255)), shadow).convert("RGB"), (0, 0))

    # Main White Card
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=card_r, fill="#FFFFFF", outline="#E5E5EA", width=2)

    # Bottom Audio Track Bar Placeholder
    draw.rounded_rectangle([70, 1750, 1010, 1758], radius=4, fill="#E5E5EA")
    draw.text((70, 1774), "00:00", fill="#8E8E93", font=get_font(24, "regular"))
    draw.text((950, 1774), "01:55", fill="#8E8E93", font=get_font(24, "regular"))

    return img, draw

# ==================== SLIDES ====================

def make_slide_1():
    img, draw = create_base_canvas(1)
    # Badge
    draw.rounded_rectangle([134, 250, 310, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "КІРІСПЕ", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 370), "Бейнедәріс топтамасы", fill="#007AFF", font=get_font(34, "bold"))

    heading = "Сәлеметсіздер ме,\nқұрметті\nтыңдармандар!"
    draw.text((134, 460), heading, fill="#1C1C1E", font=get_font(68, "bold"), spacing=24)

    # Decorative Card
    draw.rounded_rectangle([134, 860, 946, 1260], radius=32, fill="#F8F9FA", outline="#E5E5EA", width=1)
    draw.text((180, 915), "Тіл білімі мен грек философиясы", fill="#1C1C1E", font=get_font(38, "bold"))
    draw.text((180, 985), "Әлемдік лингвистиканың іргелі теориялық\nнегіздері мен көне ойшылдар мұрасына шолу.", fill="#636366", font=get_font(30, "regular"), spacing=16)

    draw.rounded_rectangle([180, 1140, 460, 1196], radius=16, fill="#EBF5FF")
    draw.text((205, 1152), "1-дәріс: Іргелі теория", fill="#007AFF", font=get_font(24, "bold"))

    img.save(f"{OUTPUT_DIR}/slide_01.png")

def make_slide_2():
    img, draw = create_base_canvas(2)
    draw.rounded_rectangle([134, 250, 330, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "ТАҚЫРЫП", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 350), "Бүгінгі дәріс тақырыбы:", fill="#8E8E93", font=get_font(34, "bold"))

    # Block 1
    draw.rounded_rectangle([134, 430, 946, 850], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
    draw.rounded_rectangle([174, 475, 360, 523], radius=12, fill="#007AFF")
    draw.text((195, 485), "БАСТЫ БАҒЫТ", fill="#FFFFFF", font=get_font(20, "bold"))
    
    t1 = "Тіл білімінің іргелі\nтеориялық негіздері"
    draw.text((174, 555), t1, fill="#1C1C1E", font=get_font(56, "bold"), spacing=18)
    draw.text((174, 730), "Тіл табиғаты мен зерттеу әдіс-тәсілдері", fill="#636366", font=get_font(30, "regular"))

    # Block 2
    draw.rounded_rectangle([134, 890, 946, 1310], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
    draw.rounded_rectangle([174, 935, 400, 983], radius=12, fill="#5856D6")
    draw.text((195, 945), "ТАРИХИ КЕЗЕҢ", fill="#FFFFFF", font=get_font(20, "bold"))

    t2 = "Көне грек философия-\nсындағы тіл ілімдері"
    draw.text((174, 1015), t2, fill="#1C1C1E", font=get_font(56, "bold"), spacing=18)
    draw.text((174, 1190), "Антикалық ойшылдар мен таным тұжырымдары", fill="#636366", font=get_font(30, "regular"))

    img.save(f"{OUTPUT_DIR}/slide_02.png")

def make_slide_3():
    img, draw = create_base_canvas(3)
    draw.rounded_rectangle([134, 250, 420, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "БАСТЫ БАҒЫТТАР", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 350), "Біз нені сараптаймыз?", fill="#1C1C1E", font=get_font(56, "bold"))

    items = [
        ("01", "Тілдің жаратылысы", "Адам тілінің шығу тегі мен табиғи қызметі"),
        ("02", "Жүйелік табиғаты", "Тілдік деңгейлердің ішкі өзара байланысы"),
        ("03", "Әлемдік лингвистиканың\nқалыптасу жолы", "Көне дәуірден бүгінге дейінгі даму тарихы")
    ]

    y = 470
    for num, title, desc in items:
        draw.rounded_rectangle([134, y, 946, y + 215], radius=26, fill="#F9F9FB", outline="#E5E5EA", width=1)
        # Number badge
        draw.rounded_rectangle([164, y + 36, 238, y + 110], radius=18, fill="#EBF5FF")
        draw.text((180, y + 52), num, fill="#007AFF", font=get_font(32, "bold"))
        # Text
        draw.text((264, y + 38), title, fill="#1C1C1E", font=get_font(38, "bold"), spacing=12)
        desc_y = y + 138 if "\n" in title else y + 104
        draw.text((264, desc_y), desc, fill="#636366", font=get_font(26, "regular"))
        y += 245

    img.save(f"{OUTPUT_DIR}/slide_03.png")

def make_slide_4():
    img, draw = create_base_canvas(4)
    draw.rounded_rectangle([134, 250, 300, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "1-БӨЛІМ", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 360), "01", fill="#E5E5EA", font=get_font(130, "bold"))

    heading = "Жалпы тіл білімі\nжәне оның үш\nқұрамдас бөлігі"
    draw.text((134, 520), heading, fill="#1C1C1E", font=get_font(64, "bold"), spacing=22)

    draw.rounded_rectangle([134, 980, 946, 1300], radius=28, fill="#F8F9FA", outline="#E5E5EA", width=1)
    draw.text((180, 1030), "Теориялық лингвистиканың өзегі", fill="#007AFF", font=get_font(32, "bold"))
    draw.text((180, 1090), "Тіл туралы ғылымның іргелі негізін құрайтын\nүш басты бағытты кезең-кезеңімен талдау.", fill="#3A3A3C", font=get_font(30, "regular"), spacing=16)

    img.save(f"{OUTPUT_DIR}/slide_04.png")

def make_slide_5():
    img, draw = create_base_canvas(5)
    draw.rounded_rectangle([134, 250, 360, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "АНЫҚТАМАСЫ", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 350), "Жалпы тіл білімі\nдегеніміз не?", fill="#1C1C1E", font=get_font(56, "bold"), spacing=16)

    draw.rounded_rectangle([134, 540, 946, 1140], radius=32, fill="#F9F9FB", outline="#E5E5EA", width=1)
    
    body = ("«Тілдің табиғаты мен қоғамдық\n"
            "қызметін, оның ішкі құрылымын:\n"
            "фонетика, лексика мен\n"
            "грамматиканы және ортақ даму\n"
            "заңдылықтарын зерттейтін\n"
            "іргелі ғылым саласы.»")
    draw.text((174, 595), body, fill="#1C1C1E", font=get_font(44, "bold"), spacing=22)

    tags = ["Фонетика", "Лексика", "Грамматика"]
    px = 134
    for tag in tags:
        draw.rounded_rectangle([px, 1190, px + 246, 1260], radius=18, fill="#EBF5FF")
        draw.text((px + 36, 1208), tag, fill="#007AFF", font=get_font(28, "bold"))
        px += 276

    img.save(f"{OUTPUT_DIR}/slide_05.png")

def make_slide_6():
    img, draw = create_base_canvas(6)
    draw.rounded_rectangle([134, 250, 340, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "ҚҰРЫЛЫМЫ", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 345), "Бұл пән негізгі\nүш бөліктен тұрады:", fill="#1C1C1E", font=get_font(56, "bold"), spacing=16)

    items = [
        ("1", "Тіл білімінің тарихы", "Ой-пікірлер мен бағыттардың даму жолы", "#007AFF", "#EBF5FF"),
        ("2", "Зерттеу әдіс-тәсілдері", "Сипаттамалы, салыстырмалы және құрылымдық", "#34C759", "#EAF8EE"),
        ("3", "Тіл теориясы", "Универсалиялар, таным және глоттогония", "#AF52DE", "#F7EDFC")
    ]

    y = 570
    for num, title, desc, col, bg in items:
        draw.rounded_rectangle([134, y, 946, y + 205], radius=26, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.rounded_rectangle([164, y + 35, 244, y + 115], radius=20, fill=bg)
        draw.text((188, y + 50), num, fill=col, font=get_font(42, "bold"))

        draw.text((270, y + 42), title, fill="#1C1C1E", font=get_font(40, "bold"))
        draw.text((270, y + 104), desc, fill="#636366", font=get_font(26, "regular"))
        y += 235

    img.save(f"{OUTPUT_DIR}/slide_06.png")

def make_slide_7():
    img, draw = create_base_canvas(7)
    draw.rounded_rectangle([134, 250, 430, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "1-ҚҰРАМДАС БӨЛІК", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 360), "01", fill="#E5E5EA", font=get_font(100, "bold"))
    draw.text((134, 470), "Тіл білімінің тарихы", fill="#1C1C1E", font=get_font(58, "bold"))

    draw.rounded_rectangle([134, 570, 946, 1040], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
    
    t = ("Лингвистикалық\n"
         "ой-пікірлердің, мектептер\n"
         "мен бағыттардың туу,\n"
         "қалыптасу және даму\n"
         "жолын зерделейді.")
    draw.text((180, 630), t, fill="#1C1C1E", font=get_font(48, "bold"), spacing=26)

    # Sub-card
    draw.rounded_rectangle([134, 1080, 946, 1290], radius=24, fill="#EBF5FF")
    draw.text((180, 1120), "Басты зерделеу нысаны:", fill="#007AFF", font=get_font(26, "bold"))
    draw.text((180, 1166), "Тіл туралы ғылыми танымның эволюциясы", fill="#1C1C1E", font=get_font(32, "bold"))

    img.save(f"{OUTPUT_DIR}/slide_07.png")

def make_slide_8():
    img, draw = create_base_canvas(8)
    draw.rounded_rectangle([134, 250, 430, 304], radius=16, fill="#EAF8EE")
    draw.text((156, 262), "2-ҚҰРАМДАС БӨЛІК", fill="#34C759", font=get_font(26, "bold"))

    draw.text((134, 350), "02", fill="#E5E5EA", font=get_font(100, "bold"))
    draw.text((134, 455), "Зерттеу әдіс-тәсілдері", fill="#1C1C1E", font=get_font(56, "bold"))

    methods = [
        ("Сипаттамалы әдіс", "Тіл құбылыстарын нақты сипаттау"),
        ("Салыстырмалы-тарихи әдіс", "Тілдердің туыстығы мен тарихын зерттеу"),
        ("Құрылымдық әдіс", "Тілді тұтас таңбалар жүйесі деп тану"),
        ("Лингвогеография әдісі", "Диалектілер мен тілдердің таралу картасы")
    ]

    y = 545
    for name, sub in methods:
        draw.rounded_rectangle([134, y, 946, y + 150], radius=22, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.rounded_rectangle([158, y + 30, 168, y + 120], radius=5, fill="#34C759")
        draw.text((190, y + 30), name, fill="#1C1C1E", font=get_font(36, "bold"))
        draw.text((190, y + 84), sub, fill="#636366", font=get_font(26, "regular"))
        y += 175

    img.save(f"{OUTPUT_DIR}/slide_08.png")

def make_slide_9():
    img, draw = create_base_canvas(9)
    draw.rounded_rectangle([134, 250, 430, 304], radius=16, fill="#F7EDFC")
    draw.text((156, 262), "3-ҚҰРАМДАС БӨЛІК", fill="#AF52DE", font=get_font(26, "bold"))

    draw.text((134, 350), "03", fill="#E5E5EA", font=get_font(100, "bold"))
    draw.text((134, 455), "Тіл теориясы", fill="#1C1C1E", font=get_font(58, "bold"))

    draw.rounded_rectangle([134, 550, 946, 1280], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
    draw.text((180, 600), "Зерттейтін басты өрістері:", fill="#8E8E93", font=get_font(28, "bold"))

    branches = [
        "Тілдік универсалиялар (ортақ заңдар)",
        "Тіл мен ойлау бірлігі",
        "Глоттогония (тілдің шығу тегі)",
        "Социолингвистика (қоғам мен тіл)",
        "Когнитивтік лингвистика (таным мен тіл)"
    ]

    by = 665
    for b in branches:
        draw.rounded_rectangle([180, by + 12, 194, by + 26], radius=6, fill="#AF52DE")
        draw.text((218, by), b, fill="#1C1C1E", font=get_font(32, "bold"))
        by += 105

    img.save(f"{OUTPUT_DIR}/slide_09.png")

def make_slide_10():
    img, draw = create_base_canvas(10)
    draw.rounded_rectangle([134, 250, 370, 304], radius=16, fill="#FFF2E8")
    draw.text((156, 262), "БАСТЫ МАҚСАТ", fill="#FF9500", font=get_font(26, "bold"))

    draw.text((134, 350), "Жалпы тіл білімінің\nбасты мақсаты:", fill="#1C1C1E", font=get_font(56, "bold"), spacing=16)

    draw.rounded_rectangle([134, 530, 946, 1240], radius=32, fill="#F9F9FB", outline="#E5E5EA", width=1)
    
    quote = ("«Жеке бір тілдің\n"
             "ерекшелігін ғана емес,\n"
             "күллі адамзат баласына\n"
             "ортақ сөйлеу тілінің\n"
             "әмбебап қағидаттарын\n"
             "ашу болып табылады.»")
    draw.text((180, 600), quote, fill="#1C1C1E", font=get_font(48, "bold"), spacing=24)

    draw.rounded_rectangle([180, 1100, 520, 1160], radius=16, fill="#FFF2E8")
    draw.text((210, 1115), "ӘМБЕБАП ҚАҒИДАТТАР", fill="#FF9500", font=get_font(24, "bold"))

    img.save(f"{OUTPUT_DIR}/slide_10.png")

def make_slide_11():
    img, draw = create_base_canvas(11)
    draw.rounded_rectangle([134, 250, 400, 304], radius=16, fill="#EBF5FF")
    draw.text((156, 262), "КЕЛЕСІ БӨЛІМДЕ", fill="#007AFF", font=get_font(26, "bold"))

    draw.text((134, 350), "2-бөлім алда:", fill="#8E8E93", font=get_font(34, "bold"))
    draw.text((134, 420), "Көне грек\nфилософиясы", fill="#1C1C1E", font=get_font(60, "bold"), spacing=18)

    draw.rounded_rectangle([134, 610, 946, 1260], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
    draw.text((180, 660), "Антикалық ойшылдар мен ілімдер:", fill="#8E8E93", font=get_font(28, "bold"))

    philosophers = [
        ("Диодор Сицилийский", "Дыбыстық белгілер және топтасу қажеттілігі"),
        ("Демокрит", "«Тесей» (шарттылық) және сөздің пайда болуы"),
        ("Платон", "«Кратил» диалогы: зат пен атаудың байланысы"),
        ("Аристотель", "«Поэтика»: сөз таптары мен логикалық санаттар")
    ]

    py = 720
    for name, desc in philosophers:
        draw.text((180, py), f"• {name}", fill="#007AFF", font=get_font(34, "bold"))
        draw.text((205, py + 46), desc, fill="#636366", font=get_font(26, "regular"))
        py += 120

    img.save(f"{OUTPUT_DIR}/slide_11.png")

print("Regenerating refined slides...")
make_slide_1()
make_slide_2()
make_slide_3()
make_slide_4()
make_slide_5()
make_slide_6()
make_slide_7()
make_slide_8()
make_slide_9()
make_slide_10()
make_slide_11()
print("All 11 refined slides generated!")
