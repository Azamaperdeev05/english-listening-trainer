import json
import os

path = '/Users/azamat/Movies/CapCut/User Data/Projects/com.lveditor.draft/0921/draft_info.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

texts = {}
for t in data.get('materials', {}).get('texts', []):
    content_raw = t.get('content', '')
    try:
        obj = json.loads(content_raw)
        txt = obj.get('text', '')
    except Exception:
        txt = content_raw
    texts[t['id']] = txt

subtitles = []
for track in data.get('tracks', []):
    if track.get('type') == 'text':
        for seg in track.get('segments', []):
            mat_id = seg.get('material_id')
            timerange = seg.get('target_timerange', {})
            start_us = timerange.get('start', 0)
            dur_us = timerange.get('duration', 0)
            subtitles.append({
                'start_ms': start_us // 1000,
                'end_ms': (start_us + dur_us) // 1000,
                'dur_ms': dur_us // 1000,
                'start_s': start_us / 1000000,
                'end_s': (start_us + dur_us) / 1000000,
                'text': texts.get(mat_id, '').strip()
            })

subtitles.sort(key=lambda s: s['start_ms'])

def format_srt_time(ms):
    hrs = ms // 3600000
    rem = ms % 3600000
    mins = rem // 60000
    rem = rem % 60000
    secs = rem // 1000
    millis = rem % 1000
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

srt_lines = []
for idx, sub in enumerate(subtitles, 1):
    start_fmt = format_srt_time(sub['start_ms'])
    end_fmt = format_srt_time(sub['end_ms'])
    srt_lines.append(f"{idx}\n{start_fmt} --> {end_fmt}\n{sub['text']}\n")

srt_content = "\n".join(srt_lines)
with open("til_bilimi_subtitles.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

with open("/Users/azamat/Downloads/til_bilimi_subtitles.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

with open("til_bilimi_subtitles.json", "w", encoding="utf-8") as f:
    json.dump(subtitles, f, ensure_ascii=False, indent=2)

print(f"Successfully exported {len(subtitles)} subtitles to til_bilimi_subtitles.srt and til_bilimi_subtitles.json")
