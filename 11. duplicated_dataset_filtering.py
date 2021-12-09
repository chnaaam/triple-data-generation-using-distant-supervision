import os
from tqdm import tqdm
import json
from config import load_config
import pandas as pd
import yaml

FILTER_SENTENCE = [
    # "축구 선수이다."
    "정이다.",
    "시이다.",
    "군이다.",
    "촌이다.",
    "역이다.",
    "신호장이다.",
    "배우이다.",
    "구니이다.",
    ")이다."
]

def main():
    config = load_config(path="./data.cfg")

    source_path = config.duplicated_dataset_filtering.path.source_path
    dest_path = config.duplicated_dataset_filtering.path.dest_path

    for file_name in os.listdir(os.path.join(source_path)):
        if not file_name.startswith("revision2-"):
            continue

        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        buffer = data[:657]
        for d in tqdm(data[657:]):
            sentence = d["sentence"]

            is_contained_duplicated_text = False

            for filter in FILTER_SENTENCE:
                if filter in sentence:
                    is_contained_duplicated_text = True

            if not is_contained_duplicated_text:
                d["sentence"] = sentence

                buffer.append(d)


        print("Dataset Length : ", len(buffer))
        with open(os.path.join(dest_path, file_name), "w", encoding="utf-8") as fp:
            json.dump(buffer, fp, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    main()