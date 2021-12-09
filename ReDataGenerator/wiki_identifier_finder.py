import os
from tqdm import tqdm
from collections import defaultdict
from ReDataGenerator.utils import get_q_identifier_from_text


class WikiIdentifierFinder():
    def __init__(self, pages_path, triples_path):
        self.triple_titles = defaultdict(str)
        self.titles = defaultdict(str)

        triple_file_list = os.listdir(triples_path)
        file_list = os.listdir(pages_path)

        for triple_file in tqdm(triple_file_list):
            self.triple_titles[triple_file.replace(".txt", "")] = ""

        for file in tqdm(file_list):
            file = file.replace(".txt", "")

            if file not in self.triple_titles:
                self.titles[file] = ""

    def get_all_titles(self):
        return list(self.titles.keys())

    def get_identifier(self, title):
        return get_q_identifier_from_text(txt=title)
