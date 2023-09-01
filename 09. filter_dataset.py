import json
import os
from collections import defaultdict

import pandas as pd
from nlp.engines import NlpEngine
from tqdm import tqdm

from config import load_config

FILTER_NE_TAGS = ["Person", "Location", "Organization", "Event"]
NE_TAG_MAPPER = {
    "PS": "Person",
    "LC": "Location",
    "OG": "Organization",
    "EV": "Event",
}


def main():
    config = load_config(path="./data.cfg")

    source_path = config.filter_dataset.path.source_path
    dest_path = config.filter_dataset.path.dest_path

    engine = NlpEngine(task="ner")

    for file_name in os.listdir(os.path.join(source_path)):
        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        buffer = []
        for d in tqdm(data):
            sentence = d["sentence"]

            try:
                pred = engine.run(sentence=sentence)

                is_contained_tag = False
                for p in pred:
                    if NE_TAG_MAPPER[p.label] in FILTER_NE_TAGS:
                        is_contained_tag = True

                if is_contained_tag:
                    buffer.append(d)

            except:
                pass

        print("Dataset Length : ", len(buffer))
        with open(os.path.join(dest_path, file_name), "w", encoding="utf-8") as fp:
            json.dump(buffer, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
