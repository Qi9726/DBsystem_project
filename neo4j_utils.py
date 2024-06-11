from neo4j import GraphDatabase
from dash import Dash, html
import dash_cytoscape as cyto


uri, user, password = "bolt://localhost:7687", "homework", "homework2"

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_co_author(faculty_name='Jiawei Han', school='Carnegie Mellon University'):
    q = 'MATCH (cmu:FACULTY)-[:AFFILIATION_WITH]-(:INSTITUTE{name:"'+school+'"}), p = shortestPath((:FACULTY{name:"'+faculty_name+'"})-[r:INTERESTED_IN*]-(cmu) ) RETURN p LIMIT 5'
    with driver.session(database='academicworld') as session:
        result = session.run(q).graph()
        nodes, edges = [], []
        for r in result.relationships: 
            edges.append({'data':{'source':r.nodes[0].element_id, 'label':r.type, 'target':r.nodes[1].element_id}})

        for n in result.nodes: 
            nodes.append({'data':{'id':n.element_id, 'label': n['name']}})

    return nodes + edges

def faculty_keyword(string):
    # Connect to Neo4j graph database
    q = "Match (univ:INSTITUTE)-[affi:AFFILIATION_WITH]- (f:FACULTY) " \
            "-[i:INTERESTED_IN]-(k:KEYWORD where k.name CONTAINS '{}') " \
            "Return f.name as name, f.position as position, univ.name as university, i.score as score ORDER " \
            "BY score DESC limit 100".format(string)

    with driver.session(database='academicworld') as session:
        result = session.run(q).data()
        return result


if __name__ == '__main__':
	#print (pub_cnt())
	print(faculty_keyword('data mining'))

