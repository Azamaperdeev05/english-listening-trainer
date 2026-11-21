import subprocess
import os

slides = [
    ("slides_part1/slide_01.png", 3.50),
    ("slides_part1/slide_02.png", 9.70),
    ("slides_part1/slide_03.png", 10.60),
    ("slides_part1/slide_04.png", 9.40),
    ("slides_part1/slide_05.png", 18.20),
    ("slides_part1/slide_06.png", 4.60),
    ("slides_part1/slide_07.png", 11.80),
    ("slides_part1/slide_08.png", 11.00),
    ("slides_part1/slide_09.png", 16.50),
    ("slides_part1/slide_10.png", 14.90),
    ("slides_part1/slide_11.png", 4.66),
]

total_dur = sum(d for _, d in slides)
print(f"Total calculated duration: {total_dur:.2f}s")

concat_file = "slides_concat.txt"
with open(concat_file, "w") as f:
    for path, dur in slides:
        abs_path = os.path.abspath(path)
        f.write(f"file '{abs_path}'\n")
        f.write(f"duration {dur:.2f}\n")
    # Repeat last file for ffmpeg concat quirk
    f.write(f"file '{os.path.abspath(slides[-1][0])}'\n")

output_video = "til_bilimi_1_bolim_video.mp4"
audio_file = "audio_part1.mp3"

vf_filter = f"drawbox=x=70:y=1750:w='min(940,(t/{total_dur:.2f})*940)':h=8:color=0x007AFF:t=fill"

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
    "-preset", "medium",
    "-crf", "19",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", f"{total_dur:.2f}",
    output_video
]

print("Running FFmpeg...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("FFmpeg return code:", res.returncode)
if res.returncode != 0:
    print("FFmpeg error:", res.stderr)
else:
    print(f"Successfully generated: {output_video}")

