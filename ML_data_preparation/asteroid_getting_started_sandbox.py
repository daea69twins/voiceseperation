#!/usr/bin/env python
# coding: utf-8

# In[1]:


# original code:
# https://github.com/asteroid-team/asteroid/blob/master/notebooks/00_GettingStarted.ipynb

# Asteroid is based on PyTorch and PyTorch-Lightning.
from torch import optim
from pytorch_lightning import Trainer

# We train the same model architecture that we used for inference above.
from asteroid.models import ConvTasNet

# In this example we use Permutation Invariant Training (PIT) and the SI-SDR loss.
from asteroid.losses import pairwise_neg_sisdr, PITLossWrapper

# MiniLibriMix is a tiny version of LibriMix (https://github.com/JorisCos/LibriMix),
# which is a free speech separation dataset.
from asteroid.data import LibriMix

# Asteroid's System is a convenience wrapper for PyTorch-Lightning.
from asteroid.engine import System

from custom_dataset_sandbox import CustomMixture

from torch.utils.data import DataLoader


# In[2]:


# This will automatically download MiniLibriMix from Zenodo on the first run.
# train_loader, val_loader = LibriMix.loaders_from_mini(task="sep_clean", batch_size=16)

# train_loader, val_loader = LibriMix.mini_from_download(task="sep_clean")#, {"num_workers": 8})
csv_path = "C:/Users/ZaknafeinII/Desktop/University_of_Iowa/4_Senior/Spring/ECE4890_SD/voiceseperation/ML_data_preparation/MiniLibriMix/metadata"
train_loader = DataLoader(CustomMixture(csv_path, "example_train"), num_workers=4, batch_size=1)
val_loader = DataLoader(CustomMixture(csv_path, "example_val"), num_workers=4, batch_size=1)

# train_loader = LibriMix("C:/Users/ZaknafeinII/Desktop/University_of_Iowa/4_Senior/Spring/ECE4890_SD/voiceseperation/ML_data_preparation/MiniLibriMix/metadata/test_libri/", task="sep_clean", sample_rate=16000, n_src=2, segment=3, return_id=False)
# val_loader = LibriMix("C:/Users/ZaknafeinII/Desktop/University_of_Iowa/4_Senior/Spring/ECE4890_SD/voiceseperation/ML_data_preparation/MiniLibriMix/metadata/test_libri/", task="sep_clean", sample_rate=16000, n_src=2, segment=3, return_id=False)
# Tell DPRNN that we want to separate to 2 sources.
model = ConvTasNet(n_src=2)

# PITLossWrapper works with any loss function.
loss = PITLossWrapper(pairwise_neg_sisdr, pit_from="pw_mtx")

optimizer = optim.Adam(model.parameters(), lr=1e-3)

system = System(model, optimizer, loss, train_loader, val_loader)


# In[3]:


# from torch import cuda
# import torch
# print(cuda.device_count())
# print(torch.version.cuda)
# print(torch.cuda.is_available())

# print(type(model))

# print(type(train_loader))
# print(type(val_loader))

# train_loader.__getitem__(0)
# val_loader.__getitem__(0)


# In[4]:


# Train for 1 epoch using a single GPU. If you're running this on Google Colab,
# be sure to select a GPU runtime (Runtime → Change runtime type → Hardware accelarator).
# trainer = Trainer(max_epochs=1, gpus=0, auto_select_gpus=False, log_every_n_steps=1)
trainer = Trainer(max_epochs=1, gpus=1, auto_select_gpus=True)
# maybe look into this link?:
# https://stackoverflow.com/questions/64837376/how-to-efficiently-run-multiple-pytorch-processes-models-at-once-traceback
# maybe need to make sure the DataLoader opens to the GPU?

# trainer = Trainer()
import gc
gc.collect()
# trainer = Trainer(log_every_n_steps=1)
trainer.fit(system)


# In[ ]:
