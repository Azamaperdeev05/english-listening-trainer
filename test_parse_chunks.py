import json

with open('til_bilimi_subtitles.json') as f:
    subs = json.load(f)

curr_start = 0.0
curr_texts = []
chunks = []

for s in subs:
    curr_texts.append(s['text'])
    dur = s['end_s'] - curr_start
    if dur >= 15.0 or (dur >= 10.0 and any(k in s['text'] for k in ['бөлім', 'дәуір', 'ғасыр', 'демокрит', 'платон', 'аристотель', 'қорытынды'])):
        chunks.append({
            'start_s': curr_start,
            'end_s': s['end_s'],
            'dur_s': round(s['end_s'] - curr_start, 2),
            'text': ' '.join(curr_texts)
        })
        curr_start = s['end_s']
        curr_texts = []

if curr_texts:
    chunks.append({
        'start_s': curr_start,
        'end_s': subs[-1]['end_s'],
        'dur_s': round(subs[-1]['end_s'] - curr_start, 2),
        'text': ' '.join(curr_texts)
    })

print(f"Total chunks: {len(chunks)}")
total_dur = sum(c['dur_s'] for c in chunks)
print(f"Total duration: {total_dur:.2f}s (target: {subs[-1]['end_s']:.2f}s)")

with open('chunks_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Saved chunks_metadata.json")
