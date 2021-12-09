import copy
import os
import json
from tqdm import tqdm
from config import load_config

def main():
    config = load_config(path="./data.cfg")

    pages_path = config.generate_relation_dataset.path.pages
    triples_path = config.generate_relation_dataset.path.triples
    dataset_path = config.generate_relation_dataset.path.dataset

    triple_file_name_list = os.listdir(triples_path)

    i = 0 # for debugging
    dataset = []

    for triple_file_name in tqdm(triple_file_name_list):

        triple_path = os.path.join(triples_path, triple_file_name)
        page_path = os.path.join(pages_path, triple_file_name)

        triple_list = []
        sentence_list = []

        with open(triple_path, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.replace("\n", "")

                triple_list.append(line.split(",")[:3])

        with open(page_path, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.replace("\n", "")

                sentence_list.append(line)

        # with open(os.path.join(dataset_path, triple_file_name), "w", encoding="utf-8") as fp:
        #     for sentence in sentence_list:
        #         for triple in triple_list:
        #             subj, rel, obj = triple
        #
        #             if subj in sentence and obj in sentence:
        #                 print(subj, rel, obj, sentence)


        for sentence in sentence_list:
            data = {
                "sentence": sentence,
                "entity": [],
                "relation": []
            }

            for triple in triple_list:
                subj, rel, obj = triple

                if subj not in sentence:
                    break

                if subj in sentence and obj in sentence:
                    subj_idxes = find_word_idx(sentence, subj)
                    obj_idxes = find_word_idx(sentence, obj)

                    if not(len(subj_idxes) == 1 and len(obj_idxes) == 1):
                        continue

                    subj_idxes = subj_idxes[0]
                    obj_idxes = obj_idxes[0]

                    data["entity"].append([subj_idxes[0], subj_idxes[1], "Unknown"])
                    data["entity"].append([obj_idxes[0], obj_idxes[1], "Unknown"])

                    data["relation"].append([subj_idxes[0], subj_idxes[1], obj_idxes[0], obj_idxes[1], rel])

            if data["entity"]:

                data["entity"] = list(set(tuple(row) for row in data["entity"]))
                entities = copy.deepcopy(data["entity"])

                if "가가미 겐스케(1974년 11월 21일 ~ )는 일본의 축구 선수이다." in sentence:
                    print()

                for i, e1 in enumerate(data["entity"]):
                    for j, e2 in enumerate(data["entity"]):
                        if i == j:
                            continue

                        e1_x, e1_y = e1[0], e1[1]
                        e2_x, e2_y = e2[0], e2[1]

                        if (e1_x <= e2_x <= e1_y) \
                                or (e1_x <= e2_y <= e1_y) \
                                or (e2_x <= e1_x <= e2_y) \
                                or (e2_x <= e1_y <= e2_y):
                            if e1_y - e1_x > e2_y - e2_x:
                                for ei, e in enumerate(entities):
                                    if e[0] == e2[0] and e[1] == e2[1]:
                                        del entities[ei]
                                        _e = e
                                        break

                            else:
                                for ei, e in enumerate(entities):
                                    if e[0] == e1[0] and e[1] == e1[1]:
                                        del entities[ei]
                                        _e = e
                                        break

                            relations = copy.deepcopy(data["relation"])
                            for ri, r in reversed(list(enumerate(relations))):
                                if (_e[0] == r[0] and _e[1] == r[1]) or (_e[0] == r[2] and _e[1] == r[3]):
                                    del data["relation"][ri]


                data["entity"] = list(set(tuple(row) for row in entities))

                relations = data["relation"]
                for ri1, r1 in reversed(list(enumerate(relations))):
                    for ri2, r2 in reversed(list(enumerate(relations))):

                        if ri1 == ri2:
                            continue

                        s1x, s1y, o1x, o1y = r1[0], r1[1], r1[2], r1[3]
                        s2x, s2y, o2x, o2y = r2[0], r2[1], r2[2], r2[3]

                        if (s1x == s2x) and (s1y == s2y) and  (o1x == o2x) and  (o1y == o2y):
                            del data["relation"][ri1]
                            break

                dataset.append(data)

        # i += 1
        # if i == 100:
        #     break
    print("Result Dataset List : ", len(dataset))

    with open(os.path.join(dataset_path, "data.json"), "w", encoding="utf-8") as fp:
        json.dump(dataset, fp, indent=4, ensure_ascii=False)

def find_word_idx(sentence, word):
    pos_buffer = []
    res = []
    len_word = len(word)

    forced_idx = 0
    while True:
        res_idx = sentence.find(word)

        if res_idx == -1:
            break

        if forced_idx == 5:
            break

        pos_buffer.append((res_idx, res_idx + len_word))
        sentence = list(sentence)
        sentence[res_idx: res_idx + len_word] = "ｗ" * len_word
        sentence = ''.join(sentence)

        forced_idx += 1

    return pos_buffer




if __name__ == "__main__":
    main()