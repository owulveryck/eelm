#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synthèse vocale de la narration d'un chapitre.

    python3 outils/video/synthese.py <dossier-video-du-chapitre>

Lit script.py (liste SCENES), produit un mp3 par phrase dans build/audio/
et le manifeste build/narration.json. Les mp3 déjà présents ne sont pas
refaits : on peut donc corriger une phrase et relancer sans tout repayer.
"""
import json, os, subprocess, sys, time

ICI = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
CHAP = os.path.abspath(sys.argv[1])
BUILD = os.path.join(CHAP, "build")
AUD = os.path.join(BUILD, "audio")
os.makedirs(AUD, exist_ok=True)
sys.path[:0] = [CHAP, ICI]
import gtts, script                                             # noqa: E402

VOIX = getattr(script, "VOIX", "fr-FR-Chirp3-HD-Charon")
RATE = getattr(script, "RATE", 0.92)

def duree(p):
    r = subprocess.run(["ffprobe", "-v", "0", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(r.stdout.strip())

items = []
for si, (sid, titre, phrases) in enumerate(script.SCENES):
    for pi, texte in enumerate(phrases):
        mp3 = os.path.join(AUD, "%02d-%02d.mp3" % (si, pi))
        if not os.path.exists(mp3):
            for essai in range(4):
                try:
                    gtts.synth(texte, mp3, voix=VOIX, rate=RATE)
                    break
                except SystemExit as e:
                    if essai == 3:
                        raise
                    print("  nouvel essai (%s)" % str(e)[:60]); time.sleep(4)
        items.append({"scene": sid, "titre": titre, "si": si, "pi": pi, "texte": texte,
                      "mp3": os.path.relpath(mp3, BUILD), "duree": round(duree(mp3), 3)})
        if len(items) % 20 == 0:
            print("  %d phrases" % len(items)); sys.stdout.flush()

json.dump({"voix": VOIX, "rate": RATE, "items": items},
          open(os.path.join(BUILD, "narration.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
tot = sum(i["duree"] for i in items)
print("%d phrases · %.1f s de parole (%.1f min)" % (len(items), tot, tot / 60))
