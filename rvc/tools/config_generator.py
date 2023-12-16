import os
import json
import pathlib

from rvc.configs.config import Config
config = Config()

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