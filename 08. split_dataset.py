import os
from tqdm import tqdm
from collections import defaultdict
import json
from config import load_config
import pandas as pd

def chunks(data, n):
    for i in range(0, len(data), n):
        yield data[i:i + n]

def main():
    config = load_config(path="./data.cfg")

    size = config.split_dataset.size
    source_path = config.split_dataset.path.source_path
    dest_path = config.split_dataset.path.dest_path

    with open(os.path.join(source_path, "data.json"), "r", encoding="utf-8") as fp:
        data = json.load(fp)

    for i, d in enumerate(chunks(data, size)):
        with open(os.path.join(dest_path, f"data_{i}.json"), "w", encoding="utf-8") as fp:
            json.dump(d, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()