import os
from tqdm import tqdm
import json
from config import load_config
import pandas as pd
import yaml

FILTER_NE_TAGS = ["Person", "Location", "Organization", "Event"]
REVERSE_REL_TAG = [
    "follows",
]

def main():
    config = load_config(path="./data.cfg")

    source_path = config.filter_dataset_using_merged_relations.path.source_path
    dest_path = config.filter_dataset_using_merged_relations.path.dest_path

    with open("./relations.cfg", "r", encoding="utf-8") as fp:
        person = yaml.load(fp, yaml.FullLoader)


    for file_name in os.listdir(os.path.join(source_path)):
        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        buffer = []
        for d in tqdm(data):
            relation = d["relation"]

            relation_buffer = []
            for r in relation:
                if r[-1] in person.keys():
                    r[-1] = person[r[-1]]
                    relation_buffer.append(r)

            if relation_buffer:
                d["relation"] = relation_buffer

                buffer.append(d)


        print("Dataset Length : ", len(buffer))
        with open(os.path.join(dest_path, f"revision-{file_name}"), "w", encoding="utf-8") as fp:
            json.dump(buffer, fp, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    main()