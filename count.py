import os
import pandas as pd

BASE_DIR = "/mnt/c/Users/bence/Downloads/How2Sign"
SPLITS = ["train", "val", "test"]
ID_COLUMN = "SENTENCE_NAME"

for split in SPLITS:
    csv_path = os.path.join(BASE_DIR, f"how2sign_{split}.csv")
    video_dir = os.path.join(BASE_DIR, f"{split}_rgb_front_clips", "raw_videos")
    
    df = pd.read_csv(csv_path, sep='\t')
    
    try:
        existing_files = set(os.listdir(video_dir))
    except FileNotFoundError:
        existing_files = set()
        
    df['file_name'] = df[ID_COLUMN].astype(str) + '.mp4'
    
    valid_count = df['file_name'].isin(existing_files).sum()
    total_csv_count = len(df)
    
    print(f"{split.upper()}:")
    print(f"  Pairs: {valid_count}")
