import os
from tqdm import tqdm
from collections import defaultdict
from config import load_config
import pandas as pd


def main():
    config = load_config(path="./data.cfg")

    triples_path = config.get_relation_list.path.triples
    store_rel_path = config.get_relation_list.path.store_rel

    triple_file_name_list = os.listdir(triples_path)

    relation_list = []
    relation_counter = defaultdict()

    for triple_file_name in tqdm(triple_file_name_list):
        triple_path = os.path.join(triples_path, triple_file_name)

        with open(triple_path, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.replace("\n", "")

                triple = line.split(",")
                relation_list.append((triple[1], triple[4]))

    for relation, relation_id in relation_list:
        if relation.upper() == relation.lower():
            continue

        if not relation_id.startswith("P"):
            continue

        if relation not in relation_counter:
            relation_counter[relation] = {}

            relation_counter[relation].setdefault("id", relation_id)
            relation_counter[relation].setdefault("count", 1)
        else:
            relation_counter[relation]["count"] += 1

    sorted_relation_counter = sorted(relation_counter.items(), key= lambda x: x[1]["count"], reverse=True)
    relation_list = []

    for relation, attr in list(sorted_relation_counter):
        relation_list.append((relation, attr["id"], attr["count"]))

    relation_df = pd.DataFrame(relation_list, columns=["relation", "id", "count"])
    relation_df.to_excel(store_rel_path)

if __name__ == "__main__":
    main()