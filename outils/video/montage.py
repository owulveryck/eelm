#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique la vidéo d'un chapitre : images -> segments -> montage + son + sous-titres.

    python3 outils/video/montage.py <dossier-video-du-chapitre> [sortie.mp4]

Lit script.py, scenes.py et build/narration.json (produit par synthese.py).
Tout le travail intermédiaire reste dans build/ : relancer après avoir corrigé
une scène ne refait que ce qui a changé (effacer build/frames et build/segs
pour forcer un rendu complet).
"""
import json, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
CHAP = os.path.abspath(sys.argv[1])
BUILD = os.path.join(CHAP, "build")
os.environ.setdefault("VIDEO_BUILD", BUILD)
sys.path[:0] = [CHAP, ICI]
import canvas, scenes, script                                   # noqa: E402

FPS, LOOP = 12, 3.0            # images par seconde et durée d'une boucle d'animation
NFR = int(FPS * LOOP)
GAP, GAP_SCENE = 0.35, 0.9     # silence après une phrase / après la dernière d'une scène
SR = 24000
FRAMES = os.path.join(BUILD, "frames"); SEGS = os.path.join(BUILD, "segs")
WAV = os.path.join(BUILD, "wav")
for d in (FRAMES, SEGS, WAV):
    os.makedirs(d, exist_ok=True)
OUT = (os.path.abspath(sys.argv[2]) if len(sys.argv) > 2
       else os.path.join(os.path.dirname(CHAP), getattr(script, "SORTIE", "cours.mp4")))
SRT = os.path.splitext(OUT)[0] + ".srt"

def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        sys.exit("échec : %s\n%s" % (" ".join(a[:6]), r.stderr[-900:]))
    return r

man = json.load(open(os.path.join(BUILD, "narration.json"), encoding="utf-8"))["items"]

# -------------------------------------------------- 1. durées exactes (PCM)
# On décode chaque mp3 : enchaînés tels quels, leurs remplissages d'encodage
# décalent la bande son de plusieurs secondes sur vingt minutes.
for i, m in enumerate(man):
    w = os.path.join(WAV, os.path.basename(m["mp3"]).replace(".mp3", ".wav"))
    if not os.path.exists(w):
        sh("ffmpeg", "-y", "-v", "error", "-i", os.path.join(BUILD, m["mp3"]),
           "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", w)
    m["wav"] = w
    m["duree"] = int(sh("ffprobe", "-v", "0", "-select_streams", "a:0", "-show_entries",
                        "stream=duration_ts", "-of", "csv=p=0", w).stdout) / float(SR)
    dernier = (i == len(man) - 1) or (man[i + 1]["scene"] != m["scene"])
    m["gap"] = GAP_SCENE if dernier else GAP
    m["dur"] = m["duree"] + m["gap"]

# -------------------------------------------------- 2. images
todo = []
for m in man:
    f = scenes.SCENES[m["scene"]]
    svgs = []
    for k in range(NFR):
        c = canvas.C(); f(c, m["pi"], k / float(NFR))
        svgs.append(c.svg())
    m["anime"] = len(set(svgs)) > 1        # un plan fixe ne coûte qu'une image
    m["dir"] = os.path.join(FRAMES, "%02d-%02d" % (m["si"], m["pi"]))
    os.makedirs(m["dir"], exist_ok=True)
    keep = svgs if m["anime"] else svgs[:1]
    for k, sv in enumerate(keep):
        p = os.path.join(m["dir"], "%03d.svg" % k)
        if not os.path.exists(p[:-4] + ".png"):
            open(p, "w", encoding="utf-8").write(sv)
            todo.append(p)
    m["nfr"] = len(keep)

print("plans : %d  ·  animés : %d  ·  images à produire : %d"
      % (len(man), sum(1 for m in man if m["anime"]), len(todo)))
if todo:
    lst = os.path.join(BUILD, "_todo.txt")
    open(lst, "w").write("\n".join(todo))
    sh("sh", "-c", "xargs -P 8 -I{} inkscape --export-type=png --export-width=1920 {} "
                   "< %s 2>/dev/null" % lst)
    rate = [p for p in todo if not os.path.exists(p[:-4] + ".png")]
    if rate:
        sys.exit("images non rendues : %d (ex. %s)" % (len(rate), rate[0]))
print("images rendues.")

# -------------------------------------------------- 3. silences
sil = {}
for g in sorted({m["gap"] for m in man}):
    p = os.path.join(WAV, "silence-%03d.wav" % int(g * 100))
    if not os.path.exists(p):
        sh("ffmpeg", "-y", "-v", "0", "-f", "lavfi", "-i",
           "anullsrc=channel_layout=mono:sample_rate=%d" % SR, "-t", "%.3f" % g,
           "-c:a", "pcm_s16le", p)
    sil[g] = p

# -------------------------------------------------- 4. segments vidéo
# Nombre entier d'images calculé sur le temps cumulé : l'image et le son
# finissent alors exactement ensemble, sans dérive.
cum, prev = 0.0, 0
for m in man:
    cum += m["dur"]
    fin = int(round(cum * 24))
    m["frames24"] = fin - prev
    prev = fin
for i, m in enumerate(man):
    m["seg"] = os.path.join(SEGS, "%02d-%02d.mp4" % (m["si"], m["pi"]))
    if os.path.exists(m["seg"]):
        continue
    if m["anime"]:
        a = ["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-framerate", str(FPS),
             "-i", os.path.join(m["dir"], "%03d.png")]
    else:
        a = ["ffmpeg", "-y", "-v", "error", "-loop", "1",
             "-i", os.path.join(m["dir"], "000.png")]
    sh(*(a + ["-frames:v", str(m["frames24"]), "-vf", "fps=24,format=yuv420p",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", m["seg"]]))
    if (i + 1) % 20 == 0:
        print("  segments : %d/%d" % (i + 1, len(man)))
print("segments vidéo prêts.")

# -------------------------------------------------- 5. montage
lv, la = os.path.join(BUILD, "_video.txt"), os.path.join(BUILD, "_audio.txt")
open(lv, "w").write("".join("file '%s'\n" % m["seg"] for m in man))
open(la, "w").write("".join("file '%s'\nfile '%s'\n" % (m["wav"], sil[m["gap"]]) for m in man))
sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lv,
   "-c", "copy", os.path.join(BUILD, "_v.mp4"))
sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", la,
   "-c:a", "aac", "-b:a", "128k", os.path.join(BUILD, "_a.m4a"))

# -------------------------------------------------- 6. sous-titres
def tc(x):
    s = x % 60
    return "%02d:%02d:%02d,%03d" % (x // 3600, x % 3600 // 60, int(s), round((s - int(s)) * 1000))

srt, t0 = [], 0.0
for i, m in enumerate(man):
    srt.append("%d\n%s --> %s\n%s\n" % (i + 1, tc(t0), tc(t0 + m["duree"]), m["texte"]))
    t0 += m["dur"]
open(SRT, "w", encoding="utf-8").write("\n".join(srt))

# -------------------------------------------------- 7. fichier final
sh("ffmpeg", "-y", "-v", "error", "-i", os.path.join(BUILD, "_v.mp4"),
   "-i", os.path.join(BUILD, "_a.m4a"), "-i", SRT,
   "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy", "-c:a", "copy",
   "-c:s", "mov_text", "-metadata:s:s:0", "language=fra", "-movflags", "+faststart", OUT)
info = subprocess.run(["ffprobe", "-v", "0", "-show_entries", "stream=codec_type,duration",
                       "-of", "csv=p=0", OUT], capture_output=True, text=True).stdout
print("\n>>> %s\n%s" % (OUT, info))
print("durée visée : %.1f s (%.1f min)" % (t0, t0 / 60))
