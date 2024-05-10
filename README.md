# Snerfs
Implementation of paper: Representing Scenes as Neural Radiance Fields for View Synthesis.

## Installation

```
git clone https://github.com/Zihan53/Snerfs.git
cd Snerfs
conda create --name Snerfs python=3.9
conda activate Snerfs
pip install -r requirements.txt # Change the last line in requirements.txt for gpu training
```

## How to run
Train
```
python train_nerf.py
```

Test
```
python train_nerf.py --test
```

Change config in configs/default.json

## Dataset

We use BlenderNerf, a Blender add-on for rendering nerf required format dataset: https://github.com/maximeraafat/BlenderNeRF

## Results

https://github.com/Zihan53/Snerfs/assets/58449144/ffcae748-e93c-436a-9d79-4a74c29c7190


