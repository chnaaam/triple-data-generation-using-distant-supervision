import copy
import os
from tqdm import tqdm
import json
from config import load_config
import pandas as pd
import yaml

SUBJECT_LABEL_LIST = ["Person", "Organization", "Location", "Event"]

def is_duplicate_boundary(pred_start, pred_end, prev_start, prev_end):
    if pred_start <= prev_start <= pred_end:
        return True
    elif pred_start <= prev_end <= pred_end:
        return True
    elif prev_start <= pred_start <= prev_end:
        return True
    elif prev_start <= pred_end <= prev_end:
        return True
    else:
        return False

def main():
    config = load_config(path="./data.cfg")

    source_path = config.extract_data_from_entity_annotated_data.path.source_path
    dest_path = config.extract_data_from_entity_annotated_data.path.dest_path

    for file_idx, file_name in enumerate(os.listdir(os.path.join(source_path))):
        relation_counter = 0

        if not file_name.startswith("revision2-"):
            continue

        file_full_path = os.path.join(source_path, file_name)

        with open(file_full_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        buffer = []
        for d in tqdm(data):
            for i in range(len(d["entity"])):
                if d["entity"][i][-1] == "StudyField":
                    d["entity"][i][-1] = "Study Field"

            # unknown_idx_list = []
            # for i in range(len(d["entity"])):
            #     if d["entity"][i][-1] == "Unknown":
            #         unknown_idx_list.append(i)
            #
            # d["entity"] = d["entity"][::-1]
            # for idx in unknown_idx_list:
            #     del d["entity"][idx]
            #
            # d["entity"] = d["entity"][::-1]

            entities = d["entity"]

            try:
                is_contained = False
                for r in d["relation"]:
                    if r[-1] == "date_of_birth" or r[-1] == "date_of_death":
                        is_contained = True

                if not is_contained:
                    if entities[0][-1] == "Person" and entities[1][-1] == "Date" and entities[2][-1] == "Date":
                        d["relation"].append([entities[0][0], entities[0][1], entities[1][0], entities[1][1], "date_of_birth"])
                        d["relation"].append([entities[0][0], entities[0][1], entities[2][0], entities[2][1], "date_of_death"])
            except:
                pass

            relations = d["relation"]
            relation_buffer = []

            for r_e1_s, r_e1_e, r_e2_s, r_e2_e, label in relations:
                r_e1_s = int(r_e1_s)
                r_e1_e = int(r_e1_e)
                r_e2_s = int(r_e2_s)
                r_e2_e = int(r_e2_e)

                if label == "locate_in":
                    label = "locate_at"

                for i in range(len(entities) - 1):
                    for j in range(i + 1, len(entities)):
                        e1_s, e1_e, e1_label = entities[i]
                        e2_s, e2_e, e2_label = entities[j]

                        if e1_label == "Study Field":
                            e1_label = "StudyField"

                        if e2_label == "Study Field":
                            e2_label = "StudyField"

                        if e1_label == "Unknown":
                            continue

                        if e2_label == "Unknown":
                            continue

                        e1_s = int(e1_s)
                        e1_e = int(e1_e)
                        e2_s = int(e2_s)
                        e2_e = int(e2_e)

                        if not (e1_label in SUBJECT_LABEL_LIST or e2_label in SUBJECT_LABEL_LIST):
                            continue

                        if is_duplicate_boundary(e1_s, e1_e, r_e1_s, r_e1_e):
                            if is_duplicate_boundary(e2_s, e2_e, r_e2_s, r_e2_e):
                                # print(e1_label, e2_label)
                                relation_buffer.append([e1_s, e1_e, e2_s, e2_e, label])

                                # for debugging
                                relation_counter += 1
                                break

                        if is_duplicate_boundary(e2_s, e2_e, r_e1_s, r_e1_e):
                            if is_duplicate_boundary(e1_s, e1_e, r_e2_s, r_e2_e):
                                # print(e1_label, e2_label)
                                relation_buffer.append([e2_s, e2_e, e1_s, e1_e, label])

                                # for debugging
                                relation_counter += 1


            if relation_buffer:
                d["relation"] = relation_buffer
                buffer.append(d)

        print("Relation Counter : ", relation_counter)

        if buffer:
            with open(os.path.join(dest_path, f"dataset-{file_idx}.json"), "w", encoding="utf-8") as fp:
                json.dump(buffer, fp, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    main()