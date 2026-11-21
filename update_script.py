with open("generate_full_slides.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix 1: Quote box height & tag placement
old_quote_block = """    if "quote" in s:
        quote_lines = wrap_text(s["quote"], get_font(42, "bold"), 720)
        card_h = len(quote_lines) * 60 + 100
        card_y2 = min(content_y + card_h, 1260)
        draw.rounded_rectangle([134, content_y, 946, card_y2], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.text((174, content_y + 50), "\\n".join(quote_lines), fill="#1C1C1E", font=get_font(42, "bold"), spacing=20)
        
        # Tags below quote
        if "pills" in s:
            px = 134
            py = card_y2 + 40
            for p in s["pills"]:
                draw.rounded_rectangle([px, py, px + 246, py + 70], radius=18, fill=bg)
                draw.text((px + 36, py + 18), p, fill=col, font=get_font(28, "bold"))
                px += 276
        elif "tag" in s:
            draw.rounded_rectangle([180, card_y2 - 80, 560, card_y2 - 24], radius=16, fill=bg)
            draw.text((205, card_y2 - 68), s["tag"], fill=col, font=get_font(24, "bold"))"""

new_quote_block = """    if "quote" in s:
        quote_lines = wrap_text(s["quote"], get_font(42, "bold"), 720)
        card_h = len(quote_lines) * 64 + (180 if "tag" in s else 100)
        card_y2 = min(content_y + card_h, 1260)
        draw.rounded_rectangle([134, content_y, 946, card_y2], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.text((174, content_y + 45), "\\n".join(quote_lines), fill="#1C1C1E", font=get_font(42, "bold"), spacing=22)
        
        # Tags below quote
        if "pills" in s:
            px = 134
            py = card_y2 + 40
            for p in s["pills"]:
                draw.rounded_rectangle([px, py, px + 246, py + 70], radius=18, fill=bg)
                draw.text((px + 36, py + 18), p, fill=col, font=get_font(28, "bold"))
                px += 276
        elif "tag" in s:
            draw.rounded_rectangle([180, card_y2 - 76, 560, card_y2 - 22], radius=16, fill=bg)
            draw.text((205, card_y2 - 64), s["tag"], fill=col, font=get_font(24, "bold"))"""

# Fix 2: Box title & desc height
old_box_block = """    elif "box_title" in s:
        b_lines = wrap_text(s.get("box_desc", ""), get_font(30, "regular"), 700)
        box_h = len(b_lines) * 42 + 200
        draw.rounded_rectangle([134, content_y, 946, content_y + box_h], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.text((180, content_y + 45), s["box_title"], fill="#1C1C1E", font=get_font(36, "bold"))
        draw.text((180, content_y + 115), "\\n".join(b_lines), fill="#636366", font=get_font(30, "regular"), spacing=14)
        
        if "tag" in s:
            draw.rounded_rectangle([180, content_y + box_h - 75, 540, content_y + box_h - 25], radius=14, fill=bg)
            draw.text((205, content_y + box_h - 64), s["tag"], fill=col, font=get_font(24, "bold"))"""

new_box_block = """    elif "box_title" in s:
        b_lines = wrap_text(s.get("box_desc", ""), get_font(30, "regular"), 700)
        box_h = len(b_lines) * 44 + 230
        draw.rounded_rectangle([134, content_y, 946, content_y + box_h], radius=30, fill="#F9F9FB", outline="#E5E5EA", width=1)
        draw.text((180, content_y + 45), s["box_title"], fill="#1C1C1E", font=get_font(36, "bold"))
        draw.text((180, content_y + 115), "\\n".join(b_lines), fill="#636366", font=get_font(30, "regular"), spacing=14)
        
        if "tag" in s:
            draw.rounded_rectangle([180, content_y + box_h - 70, 560, content_y + box_h - 20], radius=14, fill=bg)
            draw.text((205, content_y + box_h - 58), s["tag"], fill=col, font=get_font(24, "bold"))"""

# Fix 3: Speech bubble styling
old_bubble_block = """    # 5. Live Speech Subtitle Bubble inside the card at bottom
    chunk = chunks[idx]
    clean_speech = chunk["text"]
    speech_lines = wrap_text(f"«{clean_speech}»", get_font(28, "medium"), 740)
    bubble_lines = speech_lines[:2] # display up to 2 lines
    bubble_h = len(bubble_lines) * 38 + 48
    draw.rounded_rectangle([134, 1630 - bubble_h, 946, 1650], radius=20, fill="#F2F2F7")
    draw.text((168, 1645 - bubble_h), "\\n".join(bubble_lines), fill="#636366", font=get_font(26, "medium"), spacing=8)"""

new_bubble_block = """    # 5. Live Speech Subtitle Bubble inside the card at bottom
    chunk = chunks[idx]
    clean_speech = chunk["text"]
    speech_lines = wrap_text(f"«{clean_speech}»", get_font(28, "medium"), 720)
    bubble_lines = speech_lines[:2] # display up to 2 lines
    bubble_h = len(bubble_lines) * 40 + 64
    by1 = 1640 - bubble_h
    by2 = 1650
    draw.rounded_rectangle([134, by1, 946, by2], radius=22, fill="#F9F9FB", outline="#E5E5EA", width=1)
    draw.text((168, by1 + 16), "ДАУЫС:", fill="#8E8E93", font=get_font(20, "bold"))
    draw.text((168, by1 + 46), "\\n".join(bubble_lines), fill="#2C2C2E", font=get_font(26, "medium"), spacing=8)"""

code = code.replace(old_quote_block, new_quote_block)
code = code.replace(old_box_block, new_box_block)
code = code.replace(old_bubble_block, new_bubble_block)

with open("generate_full_slides.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_full_slides.py updated successfully!")
