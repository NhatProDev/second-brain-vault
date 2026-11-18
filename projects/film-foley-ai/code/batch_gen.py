"""Batch video-to-audio with MMAudio: load once, generate every shot x seed."""
import csv, sys, time
from pathlib import Path

import torch
import torchaudio

from mmaudio.eval_utils import all_model_cfg, generate, load_video, setup_eval_logging
from mmaudio.model.flow_matching import FlowMatching
from mmaudio.model.networks import get_my_mmaudio
from mmaudio.model.utils.features_utils import FeaturesUtils

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "small_44k"
SHOTS_CSV = Path(sys.argv[2])
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] else None
SEEDS = [1, 2]
NEG = "music, speech, talking, voice, singing, whoosh, swoosh, impact, cinematic effect"
ROOT = Path(__file__).parent
OUT = ROOT / "gen" / VARIANT
OUT.mkdir(parents=True, exist_ok=True)


@torch.inference_mode()
def main():
    setup_eval_logging()
    cfg = all_model_cfg[VARIANT]
    cfg.download_if_needed()
    seq_cfg = cfg.seq_cfg
    if torch.cuda.is_available():
        dev, dt = "cuda", torch.bfloat16
    else:
        dev, dt = "cpu", torch.float32
        torch.set_num_threads(14)
    net = get_my_mmaudio(cfg.model_name).to(dev, dt).eval()
    net.load_weights(torch.load(cfg.model_path, map_location=dev, weights_only=True))
    fm = FlowMatching(min_sigma=0, inference_mode="euler", num_steps=25)
    fu = FeaturesUtils(tod_vae_ckpt=cfg.vae_path, synchformer_ckpt=cfg.synchformer_ckpt,
                       enable_conditions=True, mode=cfg.mode,
                       bigvgan_vocoder_ckpt=cfg.bigvgan_16k_path, need_vae_encoder=False).to(dev, dt).eval()

    with open(SHOTS_CSV, newline="", encoding="utf-8") as f:
        shots = list(csv.DictReader(f))
    for s in shots:
        if ONLY and s["id"] not in ONLY:
            continue
        vid = ROOT / "shots" / f"{s['id']}.mp4"
        dur = float(s["end"]) - float(s["start"])
        info = load_video(vid, dur)
        clip = info.clip_frames.unsqueeze(0)
        sync = info.sync_frames.unsqueeze(0)
        seq_cfg.duration = info.duration_sec
        net.update_seq_lengths(seq_cfg.latent_seq_len, seq_cfg.clip_seq_len, seq_cfg.sync_seq_len)
        for seed in SEEDS:
            p = OUT / f"{s['id']}_s{seed}.flac"
            if p.exists():
                continue
            t0 = time.time()
            rng = torch.Generator(device=dev)
            rng.manual_seed(seed)
            a = generate(clip, sync, [s["prompt"]], negative_text=[NEG], feature_utils=fu,
                         net=net, fm=fm, rng=rng, cfg_strength=4.5)
            torchaudio.save(str(p), a.float().cpu()[0], seq_cfg.sampling_rate)
            print(f"{p.name} {info.duration_sec:.2f}s in {time.time()-t0:.1f}s", flush=True)
    print("peak VRAM GB", round(torch.cuda.max_memory_allocated() / 2**30, 2))


if __name__ == "__main__":
    main()
