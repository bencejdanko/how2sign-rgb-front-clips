import os
import pandas as pd

BASE_DIR = "/mnt/c/Users/bence/Downloads/How2Sign"
OUTPUT_DIR = os.path.join(BASE_DIR, "hf_tar_shards")
SPLITS = ["train", "val", "test"]
ID_COLUMN = "SENTENCE_NAME"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for split in SPLITS:
    csv_path = os.path.join(BASE_DIR, f"how2sign_{split}.csv")
    df = pd.read_csv(csv_path, sep='\t')
    
    video_dir = os.path.join(BASE_DIR, f"{split}_rgb_front_clips", "raw_videos")
    
    try:
        existing_files = set(os.listdir(video_dir))
    except FileNotFoundError:
        existing_files = set()
        
    df['file_name'] = df[ID_COLUMN].astype(str) + '.mp4'
    missing_df = df[~df['file_name'].isin(existing_files)]
    
    dropped_files_path = os.path.join(OUTPUT_DIR, f"missing_{split}.txt")
    with open(dropped_files_path, 'w') as f:
        for file_name in missing_df['file_name']:
            f.write(f"{file_name}\n")
            
    print(f"{split.upper()}: Found {len(missing_df)} missing files. Wrote to {dropped_files_path}")