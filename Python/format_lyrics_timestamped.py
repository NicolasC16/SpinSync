import re 
import textwrap 

lyrics_raw = """

"""

def format_for_lcd(text, cols=16):
    frames = []

    for line in text.splitlines():

        match = re.match(
            r"\[(\d+):(\d+\.\d+)\](.*)",
            line
        )

        if not match:
            continue

        minutes = int(match.group(1))
        seconds = float(match.group(2))

        # Convert to seconds for Arduino comparison
        timestamp = (minutes * 60) + seconds

        lyric = match.group(3).strip()

        if not lyric:
            continue

        wrapped = textwrap.wrap(
            lyric,
            width=cols,
            break_long_words=False,
            break_on_hyphens=False
        )

        for i in range(0, len(wrapped), 2):

            row1 = wrapped[i].ljust(cols)

            if i + 1 < len(wrapped):
                row2 = wrapped[i+1].ljust(cols)

            else:
                row2 = " " * cols

            frames.append(
                f"{timestamp:.2f}|{row1}|{row2}"
            )

    return frames

frames = format_for_lcd(lyrics_raw)

with open(
    "T1.TXT",
    "w",
    encoding="utf-8",
    newline="\n"
) as f:
    
    for frame in frames:
        f.write(frame + "\n")

print("Generated frames:")

for frame in frames:
    print(frame)