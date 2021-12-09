import os
from tqdm import tqdm
import json
from config import load_config
from collections import defaultdict
import pandas as pd
import yaml

def main():
    config = load_config(path="./data.cfg")

    source_path = config.analysis_dataset.path.source_path

    entity_dict = defaultdict(int)
    relation_dict = defaultdict(int)

    for file_idx, file_name in enumerate(os.listdir(os.path.join(source_path))):

        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        for d in tqdm(data):
            entities = d["entity"]
            relations = d["relation"]

            for entity in entities:
                entity_dict[entity[-1]] += 1

            for relation in relations:
                relation_dict[relation[-1]] += 1


    print(entity_dict)
    print(relation_dict)

    print("Entity Length : ", len(entity_dict))
    print("Relation Length : ", len(relation_dict))



if __name__ == "__main__":
    main()