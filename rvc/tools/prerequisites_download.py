import os
import wget

URL_BASE = "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main"
MODELS_DOWNLOAD = [
    (
        "pretrained/",
        [
            "D32k.pth",
            "D40k.pth",
            "D48k.pth",
            "G32k.pth",
            "G40k.pth",
            "G48k.pth",
            "f0D32k.pth",
            "f0D40k.pth",
            "f0D48k.pth",
            "f0G32k.pth",
            "f0G40k.pth",
            "f0G48k.pth",
        ],
    ),
    (
        "pretrained_v2/",
        [
            "D32k.pth",
            "D40k.pth",
            "D48k.pth",
            "G32k.pth",
            "G40k.pth",
            "G48k.pth",
            "f0D32k.pth",
            "f0D40k.pth",
            "f0D48k.pth",
            "f0G32k.pth",
            "f0G40k.pth",
            "f0G48k.pth",
        ],
    ),
]

INDIVIDUAL_FILES = [
    "hubert_base.pt",
    "rmvpe.pt",
    "rmvpe.onnx",
    "ffmpeg.exe",
    "ffprobe.exe",
]

FOLDER_MAPPING = {
    "pretrained/": "rvc/pretraineds/pretrained/",
    "pretrained_v2/": "rvc/pretraineds/pretrained_v2/",
}

for file_name in INDIVIDUAL_FILES:
    destination_path = os.path.join(file_name)
    url = f"{URL_BASE}/{file_name}"
    if not os.path.exists(destination_path):
        os.makedirs(os.path.dirname(destination_path) or ".", exist_ok=True)
        print(f"\nDownloading {url} to {destination_path}...")
        wget.download(url, out=destination_path)

for remote_folder, file_list in MODELS_DOWNLOAD:
    local_folder = FOLDER_MAPPING.get(remote_folder, "")
    for file in file_list:
        destination_path = os.path.join(local_folder, file)
        url = f"{URL_BASE}/{remote_folder}{file}"
        if not os.path.exists(destination_path):
            os.makedirs(os.path.dirname(destination_path) or ".", exist_ok=True)
            print(f"\nDownloading {url} to {destination_path}...")
            wget.download(url, out=destination_path)


print("\nAll downloads completed successfully.")
