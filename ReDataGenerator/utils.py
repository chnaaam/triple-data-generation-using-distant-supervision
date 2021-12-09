import requests
import xml.etree.ElementTree as ET

URL_FOR_GET_IDENTIFIER_FROM_TEXT = "https://ko.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=xml"
URL_FOR_GET_TEXT_FROM_IDENTIFIER = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&format=xml&props=labels"


def get_q_identifier_from_text(txt):
    req = requests.get(url=URL_FOR_GET_IDENTIFIER_FROM_TEXT.format(txt), timeout=1)

    if req.status_code == 200:
        root = ET.fromstring(req.text)

        try:
            return root.find("query").find("pages").find("page").find("pageprops").get("wikibase_item")
        except:
            return None

def get_object_from_q_identifier(q_identifier):
    req = requests.get(url=URL_FOR_GET_TEXT_FROM_IDENTIFIER.format(q_identifier), timeout=1)

    if req.status_code == 200:
        root = ET.fromstring(req.text)

        try:
            labels = root.find("entities").find("entity").find("labels")

            for label in labels:
                if label.get("language") == "ko":
                    return label.get("value")

            return None
        except:
            return None
    else:
        return None

def get_relation_from_p_identifier(p_identifier):
    req = requests.get(url=URL_FOR_GET_TEXT_FROM_IDENTIFIER.format(p_identifier), timeout=1)

    if req.status_code == 200:
        root = ET.fromstring(req.text)

        try:
            labels = root.find("entities").find("entity").find("labels")

            for label in labels:
                if label.get("language") == "en":
                    return label.get("value")

            return None
        except:
            return None
    else:
        return None

if __name__ == "__main__":
    print(get_object_from_q_identifier("Q20145"))
    print(get_relation_from_p_identifier("P31"))