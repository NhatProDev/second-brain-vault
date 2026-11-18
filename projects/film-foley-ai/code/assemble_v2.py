"""Assemble v2: MMAudio per-shot Foley as the main layer, v1 synthetic hits as
sync support only where the AI layer misses hit points.

Delivery: 48 kHz / 24-bit, -24 LKFS integrated, true peak <= -2 dBTP.
"""
import csv, os, sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN = r"C:\Users\ACER\sfx-tools\gen\small_44k"
SR, N = 48000, 48000 * 60
meter_blk = 0.4

shots = list(csv.DictReader(open(os.path.join(HERE, "shots.csv"), encoding="utf-8")))
scores = list(csv.DictReader(open(os.path.join(HERE, "gen_scores.csv"), encoding="utf-8")))
overrides = {}  # id -> seed, filled by hand after review
if len(sys.argv) > 1:
    for kv in sys.argv[1].split(","):
        k, v = kv.split("=")
        overrides[k] = int(v)


def db(x):
    return 10 ** (x / 20)


def scene_target(t):
    if t >= 44.88:
        return -25.0   # rain exterior
    if 29.03 <= t < 44.88:
        return -33.0   # quiet interior
    return -27.0       # day exterior


def lufs(x, sr):
    try:
        return pyln.Meter(sr, block_size=min(meter_blk, len(x) / sr * 0.9)).integrated_loudness(x)
    except Exception:
        return -70.0


ai = np.zeros((N, 2))
support = np.zeros((N, 2))
v1 = {k: sf.read(os.path.join(HERE, "stems", f"{k}.wav"))[0] for k in ("BG", "FEET", "PROPS", "CLOTH")}
log = []

for s in shots:
    sid, s0, s1 = s["id"], float(s["start"]), float(s["end"])
    cand = [r for r in scores if r["id"] == sid]
    if not cand:
        continue
    pick = overrides.get(sid) or int(min(cand, key=lambda r: float(r["penalty"]))["seed"])
    r = next(c for c in cand if int(c["seed"]) == pick)
    y, sr = sf.read(os.path.join(GEN, f"{sid}_s{pick}.flac"))
    if y.ndim == 1:
        y = np.stack([y, y], 1)
    y = resample_poly(y, SR, sr, axis=0)
    a, b = int(s0 * SR), min(int(s1 * SR), N)
    y = y[: b - a]
    # loudness-match each shot to its scene target
    g = scene_target(s0) - lufs(y, SR)
    y = y * db(np.clip(g, -20, 20))
    f = int(0.008 * SR)
    y[:f] *= np.linspace(0, 1, f)[:, None]
    y[-f:] *= np.linspace(1, 0, f)[:, None]
    ai[a:a + len(y)] += y
    tonal = float(r["harm"]) > 0.6 or float(r["voiced"]) > 0.15
    align = r["align"]
    align = float(align) if align not in ("", "nan") else None
    # v1 support: synthetic hits under the AI layer only where AI misses sync
    if align is not None and align < 0.6:
        for k, lvl in (("FEET", -4), ("PROPS", -4), ("CLOTH", -8)):
            support[a:b] += v1[k][a:b] * db(lvl)
    if tonal:  # AI shot unusable -> fall back to v1 for the whole shot
        ai[a:b] *= 0
        for k in ("BG", "FEET", "PROPS", "CLOTH"):
            support[a:b] += v1[k][a:b]
    log.append((sid, pick, round(g, 1), align, tonal))

mix = ai + support
m = pyln.Meter(SR)
gain = db(-24.0 - m.integrated_loudness(mix))
mix, ai, support = mix * gain, ai * gain, support * gain
# true-peak estimate via 4x oversampling, soft limit to -2 dBTP
tp = 20 * np.log10(np.abs(resample_poly(mix, 4, 1, axis=0)).max() + 1e-9)
if tp > -2:
    ceil = db(-2.3)
    mix = np.tanh(mix / ceil) * ceil
    tp = 20 * np.log10(np.abs(resample_poly(mix, 4, 1, axis=0)).max() + 1e-9)

os.makedirs(os.path.join(ROOT, "out", "v2_stems"), exist_ok=True)
sf.write(os.path.join(ROOT, "out", "v2_stems", "FX_AI_Foley.wav"), ai.astype(np.float32), SR, subtype="PCM_24")
sf.write(os.path.join(ROOT, "out", "v2_stems", "FX_Synth_Support.wav"), support.astype(np.float32), SR, subtype="PCM_24")
sf.write(os.path.join(ROOT, "out", "foley_mix_v2.wav"), mix.astype(np.float32), SR, subtype="PCM_24")
for row in log:
    print(row)
print("integrated LUFS", round(m.integrated_loudness(mix), 2), "true peak dBTP ~", round(tp, 2))
