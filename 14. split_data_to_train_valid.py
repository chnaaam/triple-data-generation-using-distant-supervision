import os
from tqdm import tqdm
import json
from config import load_config
from collections import defaultdict
import pandas as pd
import yaml
import random

def main():
    config = load_config(path="./data.cfg")

    source_path = config.split_data_to_train_valid.path.source_path
    dest_path = config.split_data_to_train_valid.path.dest_path

    train_data_size = config.split_data_to_train_valid.dataset.train * 0.1
    valid_data_size = config.split_data_to_train_valid.dataset.valid * 0.1

    buffer = []
    for file_idx, file_name in enumerate(os.listdir(os.path.join(source_path))):

        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        for d in tqdm(data):
            sentence = d["sentence"]
            entities = d["entity"]
            relations = d["relation"]

            # if sentence.startswith("100여 기 이상의 고인돌이 강화도에서"):
            #     print()

            for r in relations:
                subj = []
                obj = []

                for e in entities:
                    e_s, e_e, e_l = e[0], e[1], e[2]

                    if int(r[0]) == int(e_s) and int(r[1]) == int(e_e):
                        subj = e
                    elif int(r[2]) == int(e_s) and int(r[3]) == int(e_e):
                        obj = e

                buffer.append([sentence] + subj + obj + [r[-1]])

    print("Dataset Length : ", len(buffer))
    random.shuffle(buffer)

    len_train = int(len(buffer) * train_data_size)
    len_valid = int(len(buffer) * valid_data_size)

    train_dataset = buffer[:len_train + len_valid]
    # valid_dataset = buffer[len_train: len_train + len_valid]
    test_dataset = buffer[len_train + len_valid: ]

    print("Train Dataset Length : ", len(train_dataset))
    # print("Valid Dataset Length : ", len(valid_dataset))
    print("Test Dataset Length : ", len(test_dataset))

    with open(os.path.join(dest_path, "train.json"), "w", encoding="utf-8") as fp:
        json.dump(train_dataset, fp, indent=4, ensure_ascii=False)

    # with open(os.path.join(dest_path, "valid.json"), "w", encoding="utf-8") as fp:
    #     json.dump(valid_dataset, fp, indent=4, ensure_ascii=False)

    with open(os.path.join(dest_path, "test.json"), "w", encoding="utf-8") as fp:
        json.dump(test_dataset, fp, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()