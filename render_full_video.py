import json
import os
import subprocess
import time

with open("chunks_metadata.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Ensure last slide fills exact audio length
total_target = 897.62
cur_sum = sum(c["dur_s"] for c in chunks)
diff = total_target - cur_sum
chunks[-1]["dur_s"] = round(chunks[-1]["dur_s"] + diff, 2)

print(f"Total chunks: {len(chunks)}")
print(f"Adjusted total duration: {sum(c['dur_s'] for c in chunks):.2f}s (target: {total_target:.2f}s)")

concat_file = "slides_full_concat.txt"
with open(concat_file, "w", encoding="utf-8") as f:
    for i, c in enumerate(chunks):
        slide_path = os.path.abspath(f"slides_full/slide_{i+1:02d}.png")
        f.write(f"file '{slide_path}'\n")
        f.write(f"duration {c['dur_s']:.2f}\n")
    # Repeat last file for ffmpeg concat quirk
    last_path = os.path.abspath(f"slides_full/slide_{len(chunks):02d}.png")
    f.write(f"file '{last_path}'\n")

print(f"Written {concat_file}")

output_video = "til_bilimi_tolyk_video_apple.mp4"
audio_file = "til_bilimi_tolyk_audio.mp3"

vf_filter = f"drawbox=x=70:y=1750:w='min(940,(t/{total_target:.2f})*940)':h=8:color=0x007AFF:t=fill"

cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_file,
    "-i", audio_file,
    "-vf", vf_filter,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "25",
    "-preset", "fast",
    "-crf", "20",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", f"{total_target:.2f}",
    output_video
]

print("Starting FFmpeg full video rendering...")
start_t = time.time()
res = subprocess.run(cmd, capture_output=True, text=True)
elapsed = time.time() - start_t

print(f"FFmpeg finished in {elapsed:.1f} seconds! Return code: {res.returncode}")
if res.returncode != 0:
    print("FFmpeg error:", res.stderr[-1000:])
else:
    size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"SUCCESS! Output: {output_video} ({size_mb:.2f} MB)")

