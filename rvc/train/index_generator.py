import os
import sys
import faiss
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from multiprocessing import cpu_count
from process_ckpt import extract_small_model

rvc_version = sys.argv[1]
logs_path = sys.argv[2]
sampling_rate = sys.argv[3]
model_name = sys.argv[4]


def train_index(exp_dir1, version19):
    exp_dir = "logs/%s" % (exp_dir1)
    os.makedirs(exp_dir, exist_ok=True)
    feature_dir = (
        "%s/3_feature256" % (exp_dir)
        if version19 == "v1"
        else "%s/3_feature768" % (exp_dir)
    )
    if not os.path.exists(feature_dir):
        return "请先进行特征提取!"
    listdir_res = list(os.listdir(feature_dir))
    if len(listdir_res) == 0:
        return "请先进行特征提取！"
    infos = []
    npys = []
    for name in sorted(listdir_res):
        phone = np.load("%s/%s" % (feature_dir, name))
        npys.append(phone)
    big_npy = np.concatenate(npys, 0)
    big_npy_idx = np.arange(big_npy.shape[0])
    np.random.shuffle(big_npy_idx)
    big_npy = big_npy[big_npy_idx]
    if big_npy.shape[0] > 2e5:
        infos.append("Trying doing kmeans %s shape to 10k centers." % big_npy.shape[0])
        yield "\n".join(infos)
        try:
            big_npy = (
                MiniBatchKMeans(
                    n_clusters=10000,
                    verbose=True,
                    batch_size=256 * cpu_count(),
                    compute_labels=False,
                    init="random",
                )
                .fit(big_npy)
                .cluster_centers_
            )
        except Exception as error:
            print(error)


def find_latest_file(folder_path, prefix):
    files = [
        f
        for f in os.listdir(folder_path)
        if f.startswith(prefix) and f.endswith(".pth")
    ]
    if not files:
        return None

    numbers = [int(f[len(prefix) : -4]) for f in files]
    latest_number = max(numbers)

    latest_file = os.path.join(folder_path, f"{prefix}{latest_number}.pth")
    return latest_file


g_path = find_latest_file(logs_path, "G_")


train_index(logs_path, rvc_version)
extract_small_model(g_path, model_name, sampling_rate, 1, "", rvc_version)
