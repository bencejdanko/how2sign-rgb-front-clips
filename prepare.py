import os
import pandas as pd
import tarfile
import json
import io
from tqdm import tqdm

BASE_DIR = "/mnt/c/Users/bence/Downloads/How2Sign"
OUTPUT_DIR = os.path.join(BASE_DIR, "hf_tar_shards")
SPLITS = ["train", "val", "test"]
ID_COLUMN = "SENTENCE_NAME"
SHARD_SIZE = 1000 

os.makedirs(OUTPUT_DIR, exist_ok=True)

for split in SPLITS:
    csv_path = os.path.join(BASE_DIR, f"how2sign_{split}.csv")
    df = pd.read_csv(csv_path, sep='\t')
    
    video_dir = os.path.join(BASE_DIR, f"{split}_rgb_front_clips", "raw_videos")
    
    existing_files = set(os.listdir(video_dir))
    df['file_name'] = df[ID_COLUMN].astype(str) + '.mp4'
    valid_df = df[df['file_name'].isin(existing_files)].copy()
    
    records = valid_df.to_dict(orient='records')
    total_records = len(records)
    
    num_shards = (total_records + SHARD_SIZE - 1) // SHARD_SIZE
    print(f"\nPacking {split} split into {num_shards} tar shards...")
    
    for shard_idx in tqdm(range(num_shards), desc=f"{split} shards"):
        shard_records = records[shard_idx * SHARD_SIZE : (shard_idx + 1) * SHARD_SIZE]
        tar_filename = os.path.join(OUTPUT_DIR, f"{split}-{shard_idx:04d}.tar")
        
        with tarfile.open(tar_filename, "w") as tar:
            for row in shard_records:
                video_id = str(row[ID_COLUMN])
                mp4_name = row['file_name']
                mp4_path = os.path.join(video_dir, mp4_name)
                
                tar.add(mp4_path, arcname=mp4_name)
                
                json_name = f"{video_id}.json"
                json_data = json.dumps(row).encode('utf-8')
                
                info = tarfile.TarInfo(name=json_name)
                info.size = len(json_data)
                tar.addfile(tarinfo=info, fileobj=io.BytesIO(json_data))