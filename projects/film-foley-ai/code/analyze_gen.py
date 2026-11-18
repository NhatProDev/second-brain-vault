"""Score MMAudio candidates without listening.

For each shot/seed: loudness, peak, tonality (voice/music leak risk),
voiced-pitch ratio (speech risk), and onset alignment with cue-sheet hit points.
Writes work/gen_scores.csv and prints the pick per shot.
"""
import csv, os, sys
import numpy as np
import librosa
import pyloudnorm as pyln

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\ACER\sfx-tools\gen\small_44k"

shots = list(csv.DictReader(open(os.path.join(HERE, "shots.csv"), encoding="utf-8")))
cues = list(csv.DictReader(open(os.path.join(HERE, "cue_sheet.csv"), encoding="utf-8")))
HIT_CUES = {"bite", "run", "shuffle", "click", "paper_hit", "wet_run", "wet_slow", "device_handling", "crouch"}
# explicit hit times (seconds, absolute) used by v1 for sync-critical events
HITS = [6.75, 7.7, 16.9, 17.3, 17.65, 17.97, 18.16, 18.33, 25.5, 33.75, 34.05, 35.65,
        43.4, 44.0, 44.4] + list(np.arange(44.95, 47.0, 0.33)) + [47.2, 47.6, 48.1]


def score(path, s0, s1):
    y, sr = librosa.load(path, sr=None, mono=True)
    m = pyln.Meter(sr, block_size=min(0.4, len(y) / sr * 0.9))
    try:
        lufs = m.integrated_loudness(y)
    except Exception:
        lufs = float("nan")
    peak = 20 * np.log10(np.abs(y).max() + 1e-9)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    flat = librosa.feature.spectral_flatness(S=S).mean()
    # harmonic share from HPSS: high = tonal content (music / voice / whistles)
    H, P = librosa.decompose.hpss(S)
    harm = float((H ** 2).sum() / ((H ** 2).sum() + (P ** 2).sum() + 1e-9))
    f0, vflag, vprob = librosa.pyin(y, fmin=80, fmax=500, sr=sr, frame_length=2048)
    voiced = float(np.nanmean(vflag.astype(float)))
    hits = [h - s0 for h in HITS if s0 <= h < s1]
    align = float("nan")
    if hits:
        on = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=False)
        if len(on):
            d = [np.min(np.abs(on - h)) for h in hits]
            align = float(np.mean(np.array(d) < 0.06))  # share of hits with onset within ~1.5 frames
        else:
            align = 0.0
    return dict(lufs=round(lufs, 1), peak=round(peak, 1), flat=round(float(flat), 4),
                harm=round(harm, 3), voiced=round(voiced, 3), align=align)


rows = []
for s in shots:
    s0, s1 = float(s["start"]), float(s["end"])
    for seed in (1, 2):
        p = os.path.join(GEN, f"{s['id']}_s{seed}.flac")
        if not os.path.exists(p):
            continue
        r = dict(id=s["id"], seed=seed, **score(p, s0, s1))
        # lower is better: tonal/voiced content is a leak risk; reward alignment
        pen = r["harm"] * 2 + r["voiced"] * 3 + (0 if r["peak"] < -1 else 1)
        if not np.isnan(r["align"]):
            pen -= r["align"] * 1.5
        r["penalty"] = round(pen, 3)
        rows.append(r)

with open(os.path.join(HERE, "gen_scores.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

for sid in dict.fromkeys(r["id"] for r in rows):
    cand = [r for r in rows if r["id"] == sid]
    best = min(cand, key=lambda r: r["penalty"])
    flag = " <-- CHECK (tonal/voiced)" if best["harm"] > 0.6 or best["voiced"] > 0.15 else ""
    print(sid, "pick s%d" % best["seed"], {k: best[k] for k in ("lufs", "harm", "voiced", "align")}, flag)
