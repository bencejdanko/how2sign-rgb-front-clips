# Prepare How2Sign

The original How2Sign data is hosted on Google Drive, which has currently run out of Google download "quota", making access difficult.

This repository contains some preparation scripts for uploading structured front-view clips to HuggingFace.

Data sourced from [How2Sign](https://how2sign.github.io/).

---

# Instructions

Make sure you have your data sourced to a single folder

```
# data located in /mnt/c/Users/bence/Downloads/How2Sign

# translations and mappings
how2sign_test.csv
how2sign_val.csv
how2sign_train.csv

# all videos
test_rgb_front_clips/raw_videos
train_rgb_front_clips/raw_videos
val_rgb_front_clips/raw_videos
```

# Ongoing issues

https://github.com/how2sign/how2sign.github.io/issues/23

- missing, missaligned annotations

# Huggingface Patterns for Datasets

## VideoFolder

https://huggingface.co/docs/datasets/video_dataset

## Approach

Our desired output is:

```
hf_ready/
├── train/
│   ├── metadata.csv
│   ├── video_001.mp4
│   ├── video_002.mp4
├── val/
│   ├── metadata.csv
│   ├── ...
```

## Commands

```bash
# create symlinks && metadata
python3 prepare.py
```


```bash
# upload to huggingface
huggingface-cli upload bdanko/how2sign /mnt/c/Users/bence/Downloads/How2Sign/hf_tar_shards --repo-type dataset
```