import pandas as pd
import random
from py2neo import authenticate, Graph, Node, Relationship


def add_node(graph, node_props):
    name = node_props['name']
    node = Node('Person', uid=name)
    graph.merge(node)
    node['name'] = name
    graph.push(node)
    return node


def add_relationship(graph, src, dst, timestamp):
    src_node = add_node(graph, src)
    dst_node = add_node(graph, dst)

    print("Adding src=%s, dst=%s with timestamp=%s" % (src_node, dst_node, timestamp))

    rel = Relationship(src_node, 'SENT_EMAIL_TO',
                       dst_node, timestamp=str(timestamp))
    graph.create(rel)


def add_event_to_graph(graph, event):
    src = {'name': str(event['src'])}
    dst = {'name': str(event['dst'])}
    timestamp = str(event['time'])
    add_relationship(graph, src, dst, timestamp)


def reset_graph_schema(graph):
    constraints = graph.schema.get_uniqueness_constraints('Person')

    if constraints is not None:
        graph.schema.drop_uniqueness_constraint(
            'Person', constraints)

    graph.schema.create_uniqueness_constraint('Person', 'name')


def create_graph():
    # Log-in to Neo4j server.
    # Update: No need to do this anymore, now that I've removed authn reqmt
    # from the server.
    #authenticate('localhost:7474', 'neo4j', 'admin')

    # Create lineage graph.
    graph = Graph()

    # BTW we do not need to clear the graph anymore if we
    # don't want to, now that we have uniqueness constraints.
    # FIXME: put it back?
    #graph.delete_all()

    #reset_graph_schema(graph)

    return graph


def build_temporal_graph(graph_filename):
    # TODO: Go through log in chunks so that we don't read the whole thing
    # into memory.
    df = pd.read_csv(graph_filename, sep=' ')
    if df is None:
        print('Could not read \"%s\" as CSV.  Aborting!', event_logs_filename)
        return None

    if df.empty:
        print('No events of interest in \"%s\".  Aborting!', event_logs_filename)
        return None

    graph = create_graph()
    for _, event in df.iterrows():
        add_event_to_graph(graph, event)

    return graph
