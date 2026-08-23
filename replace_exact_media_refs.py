import os, re, urllib.parse

# Base URL (no trailing slash)
BASE = "https://teethandhairstorage.blob.core.windows.net/media"

# Exact mappings: relative path -> absolute URL (filename will be URL-encoded)
audio_files = [
    "01 Ghost Lust.mp3",
    "02 Shark Bites.mp3",
    "03 Explorers.mp3",
    "04 Feed Off The Fever.mp3",
    "05 Clean Luvs Dirty.mp3",
    "06 Don't Touch It.mp3",
    "07 Too Fast Two Furious.mp3",
    "08 Veinzz.mp3",
    "09 Ghost Lust.mp3",
    "dummy-audio.mp3",
]
video_files = [
    "MVI_0178.mp4",
    "MVI_0178.webm",
    "MVI_0179.mp4",
    "MVI_0179.webm",
    "MVI_0180.mp4",
    "MVI_0180.webm",
    "MVI_0453.mp4",
    "MVI_0453.webm",
    "MVI_0526.mp4",
    "MVI_0526.webm",
    "MVI_0527.mp4",
    "MVI_0527.webm",
    "MVI_0528.mp4",
    "MVI_0528.webm",
    "MVI_0691.mp4",
    "MVI_0691.webm",
]

# Build replacement map for both "audio/<name>" and "Video/<name>"
replacements = {}
for name in audio_files:
    encoded = urllib.parse.quote(name, safe=':@+$,;=()!*')
    replacements[f"audio/{name}"] = f"{BASE}/audio/{encoded}"
    # also handle ./audio/ and leading slashes if present
    replacements[f"./audio/{name}"] = f"{BASE}/audio/{encoded}"
    replacements[f"/audio/{name}"] = f"{BASE}/audio/{encoded}"

for name in video_files:
    encoded = urllib.parse.quote(name, safe=':@+$,;=()!*')
    replacements[f"Video/{name}"] = f"{BASE}/Video/{encoded}"
    replacements[f"./Video/{name}"] = f"{BASE}/Video/{encoded}"
    replacements[f"/Video/{name}"] = f"{BASE}/Video/{encoded}"

# Files to scan
EXTS = (".html", ".htm", ".js", ".css")

def replace_in_text(text):
    changed = False
    # Replace longer keys first to avoid partial overlaps
    for k in sorted(replacements.keys(), key=len, reverse=True):
        if k in text:
            text_new = text.replace(k, replacements[k])
            if text_new != text:
                changed = True
                text = text_new
    return text, changed

def process_file(path, dry_run=False):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        print(f"Skip (read err): {path} -> {e}")
        return False
    new, changed = replace_in_text(text)
    if changed and not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"Updated: {path}")
    elif changed and dry_run:
        print(f"Would update: {path}")
    return changed

def walk(root=".", dry_run=False):
    any_changed = False
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for name in filenames:
            if name.lower().endswith(EXTS):
                p = os.path.join(dirpath, name)
                if process_file(p, dry_run=dry_run):
                    any_changed = True
    if not any_changed:
        print("No changes needed.")
    return any_changed

if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    walk(dry_run=dry)
