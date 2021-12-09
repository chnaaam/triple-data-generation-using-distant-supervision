import os
from tqdm import tqdm
from kss import split_sentences

from config import load_config


def main():
    config = load_config("./data.cfg")
    document = {
        "title": "",
        "sentences": []
    }

    is_new_document = False

    with open(config.split_wiki_dump.path.source, "r", encoding="utf-8") as fp:
        for line in tqdm(fp.readlines()):
            line = line.replace("\n", "")

            if not line:
                is_new_document = True

                if document["title"] == "":
                    continue

                if document["sentences"]:
                    try:
                        with open(os.path.join(config.split_wiki_dump.path.destination, document["title"] + ".txt"), "w", encoding="utf-8") as fp:
                            for sentence in document["sentences"]:
                                fp.write(sentence + "\n")
                    except:
                        pass

                document = {
                    "title": "",
                    "sentences": []
                }

            else:
                if line[-1] == ":" and is_new_document == True:
                    is_new_document = False
                    document["title"] = line[:-1].replace("/", "").replace("*", "")
                else:
                    sentences = split_sentences(line)
                    for sentence in sentences:
                        if len(sentence.split()) > 2:
                            document["sentences"].append(sentence)


if __name__ == "__main__":
    main()