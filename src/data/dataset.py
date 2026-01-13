import os
from natsort import natsorted
import torch
import torchvision.transforms as T
from torch.utils.data import Dataset
import glob

class MyDataset(Dataset):
    def __init__(self, dir_path, image_width=224, image_height=224, transform=None):
        self.dir_path = dir_path
        self.files = self._get_files(dir_path)
        self.transform = transform or T.ToTensor()
        self.image_width = image_width
        self.image_height = image_height

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        return idx

    def apply_transform(self, img, transform):
        return transform(img) if transform else img

    def _get_files(self, dir_path):
        return natsorted(glob.glob(os.path.join(dir_path, "*.png")))



class Random64Dataset(Dataset):
    def __init__(self, n=1024, channels=1, size=64):
        self.n = n
        self.channels = channels
        self.size = size

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        x = torch.rand(self.channels, self.size, self.size) 
        return x