from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_URL = "https://query.wikidata.org/sparql"

PREFIX = """
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
"""

QUERY = """SELECT ?rel ?object WHERE {wd:%s ?rel ?object .}"""

class SparqlQuery:

    @classmethod
    def get_triples(cls, q_identifier):
        triples = []

        sparql = SPARQLWrapper(SPARQL_URL)
        sparql.setQuery(PREFIX + QUERY % q_identifier)
        sparql.setReturnFormat(JSON)

        result = sparql.query().convert()

        for r in result["results"]["bindings"]:
            rel = r["rel"]["value"]
            obj = r["object"]["value"]
            print(rel, obj)
            if obj.startswith("http://www.wikidata.org/entity/Q"):
                rel = rel.split("/")[-1]
                obj = obj.split("/")[-1]

                triples.append((rel, obj))

        return triples


