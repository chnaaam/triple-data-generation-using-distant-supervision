'''
미완성
'''

import os
import time
from tqdm import tqdm
from config import load_config
import matplotlib.pyplot as plt

import dash
import dash_cytoscape as cyto
import dash_html_components as html


def main():
    config = load_config(path="./data.cfg")

    triples_path = config.generate_relation_dataset.path.triples

    triple_file_name_list = os.listdir(triples_path)

    triple_list = []
    for triple_file_name in triple_file_name_list:
        with open(os.path.join(triples_path, triple_file_name), "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.replace("\n", "")
                triples = line.split(",")
                triple_list.append(triples[0:3])

    triple_list = triple_list[:100]

    for triple in triple_list:
        subj = triple[0]
        rel = triple[1]
        obj = triple[2]
        print(subj, rel, obj)
    #     break


    app = dash.Dash(__name__)

    subject_nodes = [{'data': {'id': subj, 'label': subj}} for subj, _, _ in triple_list]
    object_nodes = [{'data': {'id': obj, 'label': obj}} for obj, _, _ in triple_list]

    edges = [{'data': {'source': subj, 'target': obj}} for subj, _, obj in triple_list]

    elements = subject_nodes + object_nodes + edges

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-9',
            elements=elements,
            style={'width': '100vw', 'height': '100vh'},
            layout={
                'name': 'cose'
            }
        )
    ])

    app.run_server(debug=True)

if __name__ == "__main__":
    main()