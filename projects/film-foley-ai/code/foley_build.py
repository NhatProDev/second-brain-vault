"""Procedural Foley build for the 0-60s demo.

Reads work/cue_sheet.csv, synthesizes each cue, writes stems to work/stems/
and a loudness-normalized mix to out/foley_mix.wav.
"""
import csv, os
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt

SR = 48000
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def db(x):
    return 10 ** (x / 20)


def bp(x, lo, hi, order=4):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=4):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=4):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def noise(n):
    return rng.standard_normal(n)


def brown(n):
    b = np.cumsum(noise(n))
    b = hp(b, 20, 2)
    return b / (np.abs(b).max() + 1e-9)


def pink(n):
    # Voss-ish via filtering white noise with 1/f approximation
    w = noise(n)
    return lp(w, 3000, 1) * 0.6 + lp(w, 600, 1) * 0.8 + lp(w, 150, 1)


def env_ad(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1.0) * np.exp(-np.maximum(t - a, 0) / d)
    return e


def fade(x, fi=0.01, fo=0.02):
    n = len(x)
    i, o = int(fi * SR), int(fo * SR)
    if i:
        x[:i] *= np.linspace(0, 1, i)[:, None] if x.ndim == 2 else np.linspace(0, 1, i)
    if o:
        x[-o:] *= np.linspace(1, 0, o)[:, None] if x.ndim == 2 else np.linspace(1, 0, o)
    return x


def crackle(n, rate, decay=0.003, lo=1500, hi=8000):
    """Dense random micro-impulses -> paper / plastic / crunch texture."""
    imp = np.zeros(n)
    k = rng.poisson(rate * n / SR)
    pos = rng.integers(0, n, k)
    imp[pos] = rng.standard_normal(k) * rng.uniform(0.2, 1.0, k)
    kern = np.exp(-np.arange(int(decay * SR * 5)) / (decay * SR)) * noise(int(decay * SR * 5))
    x = np.convolve(imp, kern)[:n]
    return bp(x, lo, hi)


def smooth_rand_env(n, rate_hz, floor=0.0):
    e = lp(np.abs(noise(n)), rate_hz, 2)
    e = e / (e.max() + 1e-9)
    return floor + (1 - floor) * e


# ---------- sound designers' "library" ----------
def footstep(surface="hard", level=0.0):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f0 = rng.uniform(70, 95)
    thud = np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.035)
    heel = bp(noise(n), 300, 3500) * env_ad(n, 0.001, 0.018)
    toe = np.zeros(n)
    off = int(rng.uniform(0.045, 0.07) * SR)
    toe[off:] = (bp(noise(n - off), 800, 5000) * env_ad(n - off, 0.001, 0.012)) * 0.5
    x = 0.8 * thud + heel + toe
    if surface == "wet":
        sp = hp(noise(n), 1200) * env_ad(n, 0.004, 0.09) * 0.9
        sp *= smooth_rand_env(n, 60, 0.3)
        x = 0.6 * x + sp
    return x / (np.abs(x).max() + 1e-9) * db(level)


def cloth(dur, level=0.0, bright=False):
    n = int(dur * SR)
    x = bp(noise(n), 400 if not bright else 900, 3000 if not bright else 6000)
    x *= smooth_rand_env(n, 6, 0.05) * np.hanning(n) ** 0.5
    return fade(x / (np.abs(x).max() + 1e-9) * db(level))


def paper(dur, level=0.0, rate=220):
    n = int(dur * SR)
    x = crackle(n, rate, 0.002, 1200, 9000) + 0.25 * bp(noise(n), 2000, 7000)
    x *= smooth_rand_env(n, 8, 0.1)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level))


def plastic(dur, level=0.0):
    n = int(dur * SR)
    x = crackle(n, 500, 0.0012, 2500, 12000)
    x *= smooth_rand_env(n, 10, 0.15)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level))


def bite(level=0.0):
    n = int(0.22 * SR)
    x = crackle(n, 900, 0.0015, 700, 7000) * env_ad(n, 0.005, 0.06)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level), 0.002, 0.02)


def chew(dur, level=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    am = (0.5 + 0.5 * np.sin(2 * np.pi * 2.6 * t)) ** 3
    x = bp(noise(n), 200, 1400) * am + 0.2 * crackle(n, 80, 0.002, 600, 3000) * am
    return fade(x / (np.abs(x).max() + 1e-9) * db(level), 0.05, 0.1)


def squeeze(dur, level=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(25, 40) * t)
    x = bp(noise(n), 350, 1800) * trem * smooth_rand_env(n, 12, 0.2)
    x += 0.4 * crackle(n, 60, 0.003, 300, 1500)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level), 0.03, 0.08)


def sip(dur, level=0.0):
    n = int(dur * SR)
    x = bp(noise(n), 900, 4000)
    bub = (lp(noise(n), 20, 2) > 0).astype(float) * 0.7 + 0.3
    x *= lp(bub, 60, 2)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level), 0.05, 0.08)


def click(level=0.0, f=3200):
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.003) + bp(noise(n), 2000, 9000) * np.exp(-t / 0.0015)
    return x / (np.abs(x).max() + 1e-9) * db(level)


def snap(level=0.0):
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    x = click(0, 2400)[: n] if False else np.zeros(n)
    x[: int(0.03 * SR)] += click(0, 2400)
    x += 0.6 * np.sin(2 * np.pi * 300 * t) * np.exp(-t / 0.01)
    return x / (np.abs(x).max() + 1e-9) * db(level)


def rain_taps(dur, rate, lo, hi, decay, level=0.0):
    n = int(dur * SR)
    x = crackle(n, rate, decay, lo, hi)
    return fade(x / (np.abs(x).max() + 1e-9) * db(level), 0.03, 0.05)


# ---------- ambiences (stereo) ----------
def amb_day(n, level=0.0):
    ch = []
    for _ in range(2):
        traffic = lp(brown(n), 350) * 0.25
        wind = bp(pink(n), 250, 2500) * smooth_rand_env(n, 0.4, 0.3) * 0.4
        ch.append(traffic + wind)
    out = np.stack(ch, 1)
    # birds: sparse chirps, panned
    t_ = 0.3
    while t_ < n / SR - 0.5:
        k = rng.integers(2, 5)
        f0 = rng.uniform(3000, 5500)
        pan = rng.uniform(0.2, 0.8)
        for j in range(k):
            cn = int(rng.uniform(0.05, 0.11) * SR)
            tt = np.arange(cn) / SR
            f = f0 * (1 + rng.uniform(-0.25, 0.25) * tt / tt[-1])
            c = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(cn) * 0.08
            s = int((t_ + j * 0.13) * SR)
            if s + cn < n:
                out[s:s + cn, 0] += c * (1 - pan)
                out[s:s + cn, 1] += c * pan
        t_ += rng.uniform(1.0, 3.0)
    return out / (np.abs(out).max() + 1e-9) * db(level)


def room_tone(n, level=0.0):
    out = np.stack([lp(brown(n), 220) + 0.05 * bp(noise(n), 200, 2000) for _ in range(2)], 1)
    return out / (np.abs(out).max() + 1e-9) * db(level)


def rain(n, level=0.0):
    ch = []
    for _ in range(2):
        bed = bp(noise(n), 500, 9000) * 0.35
        drops = crackle(n, 900, 0.0012, 1500, 10000)
        heavy = crackle(n, 120, 0.004, 300, 3000) * 0.8
        ch.append(bed + drops / (np.abs(drops).max() + 1e-9) * 0.5 + heavy / (np.abs(heavy).max() + 1e-9) * 0.3)
    out = np.stack(ch, 1)
    return out / (np.abs(out).max() + 1e-9) * db(level)


# ---------- assembly ----------
stems = {k: np.zeros((N, 2)) for k in ("BG", "FEET", "PROPS", "CLOTH")}


def place(stem, t, x, pan=0.5):
    s = int(t * SR)
    if s >= N:
        return
    x = x[: N - s]
    if x.ndim == 1:
        stems[stem][s:s + len(x), 0] += x * np.sqrt(1 - pan)
        stems[stem][s:s + len(x), 1] += x * np.sqrt(pan)
    else:
        stems[stem][s:s + len(x)] += x


def steps(stem, times, surface, level, pan=0.5, jitter=1.5):
    for t in times:
        place(stem, t, footstep(surface, level + rng.uniform(-jitter, jitter)), pan)


with open(os.path.join(HERE, "cue_sheet.csv"), newline="", encoding="utf-8") as f:
    cues = list(csv.DictReader(f))

for c in cues:
    a, b, stem, cue = float(c["start"]), float(c["end"]), c["stem"], c["cue"]
    d = b - a
    n = int(d * SR)
    if cue == "amb_day":
        place(stem, a, fade(amb_day(n, -20), 0.02, 0.02))
    elif cue == "amb_day_muffled":
        x = amb_day(n, -24)
        x = np.stack([lp(x[:, 0], 1500), lp(x[:, 1], 1500)], 1)
        place(stem, a, fade(x, 0.02, 0.02))
    elif cue == "room_tone":
        place(stem, a, fade(room_tone(n, -30), 0.02, 0.05))
    elif cue == "rain":
        x = rain(n, -23)
        light_from = int((58.0 - a) * SR)
        g = np.ones(n)
        g[light_from:] = np.linspace(1, db(-6), n - light_from)
        place(stem, a, fade(x * g[:, None], 0.01, 0.01))
    elif cue == "steps_distant":
        steps(stem, np.arange(a, b, 0.52), "hard", -34, 0.35)
        steps(stem, np.arange(a + 0.25, b, 0.55), "hard", -36, 0.6)
    elif cue == "shuffle":
        steps(stem, [16.9, 17.3, 17.65], "hard", -22, 0.55)
    elif cue == "run":
        steps(stem, [17.97, 18.16, 18.33], "hard", -18, 0.65, 1.0)
    elif cue == "wet_run":
        if stem == "FEET":
            steps(stem, np.arange(a, b, 0.33), "wet", -18, 0.5, 1.5)
        else:
            place(stem, a, cloth(d, -26, bright=True))
    elif cue == "wet_slow":
        steps(stem, [47.2, 47.6, 48.1], "wet", -19, 0.5, 1.0)
    elif cue in ("turn", "bag", "crouch", "peek", "gesture", "shove"):
        lvl = {"turn": -24, "bag": -27, "crouch": -24, "peek": -30, "gesture": -26, "shove": -20}[cue]
        place(stem, a, cloth(d, lvl))
        if cue == "crouch":
            steps("FEET", [25.5], "hard", -24)
    elif cue == "bite":
        place(stem, a, bite(-18), 0.4)
    elif cue == "chew":
        place(stem, a, chew(d, -32), 0.4)
    elif cue == "squeeze":
        place(stem, a, squeeze(d, -24))
    elif cue == "straw_sip":
        place(stem, a, sip(d, -26))
    elif cue == "plastic_bags":
        place(stem, a, plastic(d, -20), 0.6)
    elif cue == "paper":
        place(stem, a, paper(d, -24, 150))
    elif cue == "paper_hit":
        x = paper(d, -16, 400)
        x[: int(0.02 * SR)] += footstep("hard", -22)[: int(0.02 * SR)]  # body thump
        place(stem, a, x)
    elif cue == "click":
        place(stem, a, click(-22))
    elif cue == "device_handling":
        place(stem, a, plastic(d, -32))
        for t in (43.4, 44.0):
            place(stem, t, click(-22))
        place(stem, 44.4, snap(-18))
    elif cue == "rain_on_board":
        lvl = -16 if a < 49 else -22
        place(stem, a, rain_taps(d, 45, 1200, 4500, 0.004, lvl))
    elif cue == "board_lift":
        place(stem, a, paper(d, -20, 90))
    elif cue == "rain_on_wood":
        place(stem, a, rain_taps(d, 30, 600, 3500, 0.006, -20))
    else:
        print("unhandled cue", cue)

os.makedirs(os.path.join(HERE, "stems"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)

mix = sum(stems.values())
meter = pyln.Meter(SR)
TARGET = -24.0
gain = db(TARGET - meter.integrated_loudness(mix))
mix *= gain
# soft safety limiter to keep sample peak under -2 dBFS
ceil = db(-2)
mix = np.tanh(mix / ceil) * ceil
for k, v in stems.items():
    sf.write(os.path.join(HERE, "stems", f"{k}.wav"), (v * gain).astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(ROOT, "out", "foley_mix.wav"), mix.astype(np.float32), SR, subtype="PCM_24")
print("integrated LUFS:", round(meter.integrated_loudness(mix), 2), "peak dBFS:", round(20 * np.log10(np.abs(mix).max()), 2))
