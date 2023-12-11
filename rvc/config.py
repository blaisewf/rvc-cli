import torch
import json
from multiprocessing import cpu_count

global usefp16
usefp16 = False

def use_fp32_config():
    usefp16 = False
    device_capability = 0
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        device_capability = torch.cuda.get_device_capability(device)[0]
        if device_capability >= 7:
            usefp16 = True
            for config_file in ["32k.json", "40k.json", "48k.json"]:
                with open(f"python/configs/{config_file}", "r") as d:
                    data = json.load(d)

                if "train" in data and "fp16_run" in data["train"]:
                    data["train"]["fp16_run"] = True

                with open(f"python/configs/{config_file}", "w") as d:
                    json.dump(data, d, indent=4)

        else:
            for config_file in ["32k.json", "40k.json", "48k.json"]:
                with open(f"configs/{config_file}", "r") as f:
                    data = json.load(f)

                if "train" in data and "fp16_run" in data["train"]:
                    data["train"]["fp16_run"] = False

                with open(f"configs/{config_file}", "w") as d:
                    json.dump(data, d, indent=4)

    else:
        return (usefp16, device_capability)


class Config:
    def __init__(self):
        self.device = "cuda:0"
        self.is_half = True
        self.n_cpu = 0
        self.gpu_name = None
        self.gpu_mem = None
        self.x_pad, self.x_query, self.x_center, self.x_max = self.device_config()
    @staticmethod
    def has_mps() -> bool:
        if not torch.backends.mps.is_available():
            return False
        try:
            torch.zeros(1).to(torch.device("mps"))
            return True
        except Exception:
            return False

    def device_config(self) -> tuple:
        if torch.cuda.is_available():
            i_device = int(self.device.split(":")[-1])
            self.gpu_name = torch.cuda.get_device_name(i_device)
            if (
                ("16" in self.gpu_name and "V100" not in self.gpu_name.upper())
                or "P40" in self.gpu_name.upper()
                or "1060" in self.gpu_name
                or "1070" in self.gpu_name
                or "1080" in self.gpu_name
            ):
                self.is_half = False
            else:
                use_fp32_config()
            self.gpu_mem = int(
                torch.cuda.get_device_properties(i_device).total_memory
                / 1024
                / 1024
                / 1024
                + 0.4
            )
        elif self.has_mps():
            self.device = "mps"
            self.is_half = False
            use_fp32_config()
        else:
            self.device = "cpu"
            self.is_half = False
            use_fp32_config()

        if self.n_cpu == 0:
            self.n_cpu = cpu_count()

        if self.is_half:
            x_pad = 3
            x_query = 10
            x_center = 60
            x_max = 65
        else:
            x_pad = 1
            x_query = 6
            x_center = 38
            x_max = 41

        if self.gpu_mem != None and self.gpu_mem <= 4:
            x_pad = 1
            x_query = 5
            x_center = 30
            x_max = 32

        return x_pad, x_query, x_center, x_max
