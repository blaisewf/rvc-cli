import torch
import sys

path = sys.argv[1]
model_data = torch.load(path, map_location="cpu")

print("Loaded model from %s" % path)

data = model_data
print(data)
epochs = data.get("info", "None")
sr = data.get("sr", "None")
f0 = data.get("f0", "None")
version = data.get("version", "None")


print(f"Epochs: {epochs}\nSampling rate: {sr}\nf0: {f0}\nVersion: {version}")
