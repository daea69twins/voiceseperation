#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
The goal is to take the original code from the asteroid library for an inherited, custom Dataset object 
and fit it to our needs.

Original code:
https://github.com/daea69twins/voiceseperation/wiki/Time-Log/_edit
"""


import numpy as np
import pandas as pd
import soundfile as sf
import torch
from torch import hub
from torch.utils.data import Dataset, DataLoader
import random as random
import os
import shutil
import zipfile


class CustomMixture(Dataset):
    """Dataset class for source separation tasks.

    Args:
        csv_dir (str): The path to the metadata file's parent directory.

        sample_rate (int) : The sample rate of the sources and mixtures.

    References
        [1] "Asteroid: the {PyTorch}-based audio source separation toolkit for researchers",
        Manuel Pariente and Samuele Cornell and Joris Cosentino and Sunit Sivasankaran and
        Efthymios Tzinis and Jens Heitkaemper and Michel Olvera and Fabian-Robert Stöter and
        Mathieu Hu and Juan M. Martín-Doñas and David Ditter and Ariel Frank and Antoine Deleforge
        and Emmanuel Vincent. 2020
        
        
        @inproceedings{Pariente2020Asteroid,
        title={Asteroid: the {PyTorch}-based audio source separation toolkit for researchers},
        author={Manuel Pariente and Samuele Cornell and Joris Cosentino and Sunit Sivasankaran and
            Efthymios Tzinis and Jens Heitkaemper and Michel Olvera and Fabian-Robert Stöter and
            Mathieu Hu and Juan M. Martín-Doñas and David Ditter and Ariel Frank and Antoine Deleforge
            and Emmanuel Vincent},
        year={2020},
        booktitle={Proc. Interspeech},
        }
    """


    def __init__(
        self, csv_dir, dataset_name, sample_rate=22040, 
    ):
        self.csv_dir = csv_dir

        # Get the csv corresponding to the dataset (specific character)
        md_file = [f for f in os.listdir(csv_dir) if dataset_name in f][0]
        self.csv_path = os.path.join(self.csv_dir, md_file)

        self.sample_rate = sample_rate
        
        # Open csv file
        self.df = pd.read_csv(self.csv_path)
        

    def __len__(self):
        return len(self.df)
    

    def __getitem__(self, idx):
        # Get the row in dataframe
        row = self.df.iloc[idx]
        
        # Get mixture path
        mixture_path = row["mixture_path"]
        self.mixture_path = mixture_path
        sources_list = []
        
        start = 0
        stop = None  

        # Read sources
        source_path = row["source_char_path"]
        s, _ = sf.read(source_path, dtype="float32", start=start, stop=stop)
        sources_list.append(s)
        source_path = row["source_other_path"]
        s, _ = sf.read(source_path, dtype="float32", start=start, stop=stop)
        sources_list.append(s)
            
        # Read the mixture
        mixture, _ = sf.read(mixture_path, dtype="float32", start=start, stop=stop)
        # Convert to torch tensor
        mixture = torch.from_numpy(mixture)
        
        # Stack sources (this puts the sources in the same array, but does not combine them)
        sources = np.vstack(sources_list)
        # Convert sources to tensor
        sources = torch.from_numpy(sources)
        print("sources.shape:", sources.shape)
        sources = np.swapaxes(sources, 0, 1)
        mixture = np.swapaxes(mixture, 0, 1)

        print("sources.shape:", sources.shape)

        
        return mixture, sources

