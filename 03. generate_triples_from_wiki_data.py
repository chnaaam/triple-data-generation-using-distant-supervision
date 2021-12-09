import os
import time
from tqdm import tqdm
from config import load_config
import multiprocessing as mp

from ReDataGenerator.wiki_identifier_finder import WikiIdentifierFinder
from ReDataGenerator.sparql_query import SparqlQuery

from ReDataGenerator.utils import get_q_identifier_from_text, get_relation_from_p_identifier, get_object_from_q_identifier

def main():
    config = load_config(path="./data.cfg")

    process_num = int(config.generate_triples.process_num)

    finder = WikiIdentifierFinder(
        pages_path=config.generate_triples.path.pages,
        triples_path=config.generate_triples.path.triples
    )

    len_titles = len(finder.get_all_titles())
    batch_titles = len_titles // process_num + 1
    all_titles = finder.get_all_titles()

    process_list = []

    q = mp.Queue()

    for title in all_titles:
        q.put(title)

    for _ in range(process_num):
        proc = mp.Process(target=run, args=(config.generate_triples.path.triples, q))
        proc.start()

        process_list.append(proc)

    while True:
        if q.empty():
            break

        print(f"Left Title : {q.qsize()}/{len_titles}")
        time.sleep(1)

def run(store_path, q: mp.Queue):
    while True:

        try:
            title = q.get()

            q_identifier = get_q_identifier_from_text(txt=title)

            triple_buffer = []
            if q_identifier:
                triples = SparqlQuery.get_triples(q_identifier=q_identifier)

                for rel_id, obj_id in triples:
                    rel = get_relation_from_p_identifier(rel_id)
                    obj = get_object_from_q_identifier(obj_id)

                    if rel is None or obj is None:
                        continue

                    triple_buffer.append((title, rel, obj, q_identifier, rel_id, obj_id))
            else:
                pass

            if triple_buffer:
                print("Title : ", title)
                with open(os.path.join(store_path, f"{title}.txt"), "w", encoding="utf-8") as fp:
                    for triple in triple_buffer:
                        fp.write(f"{triple[0]},{triple[1]},{triple[2]},{triple[3]},{triple[4]},{triple[5]}\n")

        except Exception as e:
            print("Error : ", e)

        time.sleep(0.2)
if __name__ == "__main__":
    main()