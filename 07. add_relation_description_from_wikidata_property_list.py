import os
import requests
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup

from config import load_config

WIKIDATA_PROPERTIES_LIST_URL = "https://www.wikidata.org/wiki/Wikidata:Database_reports/List_of_properties/all"


def main():
    config = load_config(path="./data.cfg")

    rel_excel_path = config.add_relation_description_from_wikidata.path.rel_excel_path
    rel_excel_with_desc_path = config.add_relation_description_from_wikidata.path.rel_excel_with_desc_path


    # parse wikidata
    req = requests.get(WIKIDATA_PROPERTIES_LIST_URL)
    bs_obj = BeautifulSoup(req.text, "html.parser")

    # wikitable sortable jquery-tablesorter
    wiki_properties_table = bs_obj.find("table", class_="wikitable").find("tbody").find_all("tr")[1:]
    # print(len(wiki_properties_table))
    # return
    properties = defaultdict(str)

    for property_tr in wiki_properties_table:
        property_td = property_tr.find_all("td")

        id = property_td[0].text
        description = property_td[2].text

        properties[id] = description

    # load excel
    relation_list = []
    df = pd.read_excel(rel_excel_path)

    for idx, row in df.iterrows():
        # For debugging
        # print(row["relation"], row["id"], row["count"], properties[row["id"]])
        # break
        relation_list.append((row["relation"], row["id"], row["count"], properties[row["id"]]))

    relation_df = pd.DataFrame(relation_list, columns=["relation", "id", "count", "description"])
    relation_df.to_excel(rel_excel_with_desc_path)





if __name__ == "__main__":
    main()