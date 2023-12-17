import os
import json
import pathlib
from random import shuffle

from rvc.configs.config import Config
config = Config()
now_dir = os.getcwd()

def config_generator(rvc_version, sampling_rate, model_path):
    if rvc_version == "v1" or sampling_rate == "40000":
        config_path = "v1/%s.json" % sampling_rate
    else:
        config_path = "v2/%s.json" % sampling_rate
    config_save_path = os.path.join(model_path, "config.json")
    if not pathlib.Path(config_save_path).exists():
        with open(config_save_path, "w", encoding="utf-8") as f:
            json.dump(
                config.json_config[config_path],
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
            f.write("\n")

def filelist_generator(f0method, model_path, rvc_version, sampling_rate):
    gt_wavs_dir = "%s/0_gt_wavs" % (model_path)
    feature_dir = (
        "%s/3_feature256" % (model_path)
        if rvc_version == "v1"
        else "%s/3_feature768" % (model_path)
    )
    if f0method:
        f0_dir = "%s/2a_f0" % (model_path)
        f0nsf_dir = "%s/2b-f0nsf" % (model_path)
        names = (
            set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)])
            & set([name.split(".")[0] for name in os.listdir(feature_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0_dir)])
            & set([name.split(".")[0] for name in os.listdir(f0nsf_dir)])
        )
    else:
        names = set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)]) & set(
            [name.split(".")[0] for name in os.listdir(feature_dir)]
        )
    opt = []
    for name in names:
        if f0method:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s/%s.wav.npy|%s/%s.wav.npy|%s"
                % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    feature_dir.replace("\\", "\\\\"),
                    name,
                    f0_dir.replace("\\", "\\\\"),
                    name,
                    f0nsf_dir.replace("\\", "\\\\"),
                    name,
                    0,
                )
            )
        else:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s"
                % (
                    gt_wavs_dir.replace("\\", "\\\\"),
                    name,
                    feature_dir.replace("\\", "\\\\"),
                    name,
                    0,
                )
            )
    fea_dim = 256 if rvc_version == "v1" else 768
    if f0method:
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s/logs/mute/2a_f0/mute.wav.npy|%s/logs/mute/2b-f0nsf/mute.wav.npy|%s"
                % (now_dir, sampling_rate, now_dir, fea_dim, now_dir, now_dir, 0)
            )
    else:
        for _ in range(2):
            opt.append(
                "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s"
                % (now_dir, sampling_rate, now_dir, fea_dim, 0)
            )
    shuffle(opt)
    with open("%s/filelist.txt" % model_path, "w") as f:
        f.write("\n".join(opt))