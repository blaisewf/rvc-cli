import os
import faiss
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from configs.config import Config

config = Config()


def generate_index(rvc_version, logs_path):
    feature_dir = (
        "%s/3_feature256" % (logs_path)
        if rvc_version == "v1"
        else "%s/3_feature768" % (logs_path)
    )
    listdir_res = list(os.listdir(feature_dir))
    if len(listdir_res) == 0 or os.path.exists(feature_dir):
        return "Please perform the feature extraction first."
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
                    batch_size=256 * config.n_cpu,
                    compute_labels=False,
                    init="random",
                )
                .fit(big_npy)
                .cluster_centers_
            )
        except Exception as error:
            print(f"Error: {error}")

    np.save("%s/total_fea.npy" % logs_path, big_npy)
    n_ivf = min(int(16 * np.sqrt(big_npy.shape[0])), big_npy.shape[0] // 39)

    index = faiss.index_factory(
        256 if rvc_version == "v1" else 768, "IVF%s,Flat" % n_ivf
    )
    yield "\n".join(infos)
    index_ivf = faiss.extract_index_ivf(index)
    index_ivf.nprobe = 1
    index.train(big_npy)
    faiss.write_index(
        index,
        "%s/trained_IVF%s_Flat_nprobe_%s_%s_%s.index"
        % (logs_path, n_ivf, index_ivf.nprobe, logs_path, rvc_version),
    )

    batch_size_add = 8192
    for i in range(0, big_npy.shape[0], batch_size_add):
        index.add(big_npy[i : i + batch_size_add])
    faiss.write_index(
        index,
        "%s/added_IVF%s_Flat_nprobe_%s_%s_%s.index"
        % (logs_path, n_ivf, index_ivf.nprobe, logs_path, rvc_version),
    )
    print("Files generated successfully!")
