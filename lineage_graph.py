import pandas as pd
from py2neo import authenticate, Graph, Node, Relationship


def add_job_node(graph, job):
    # TODO: Use a hash instead, and store the original info in a KV store.
    pid = job['pid']
    name = job['name']
    job_node = Node('Job', uid=('PID=' + str(pid) + ',CLI=' + name))
    graph.merge(job_node)
    job_node['name'] = name
    job_node['pid'] = pid
    graph.push(job_node)
    return job_node


def add_dataset_node(graph, dataset):
    # TODO: Use a combo of dataset name and hash of contents as uid?
    dataset_node = Node('Dataset', name=dataset['name'])
    graph.merge(dataset_node)
    return dataset_node


# Edges are directed to a data lineage relationship.
# Read events: Dataset-[IS_READ_BY]->Job
def add_read_relationship(graph, job, dataset, timestamp):
    dataset_node = add_dataset_node(graph, dataset)
    job_node = add_job_node(graph, job)
    rel = Relationship(dataset_node, 'IS_READ_BY',
                       job_node, timestamp=timestamp)
    graph.create(rel)


# Edges are directed to a data lineage relationship.
# Write events: Job-[WRITES_TO]->Dataset
def add_write_relationship(graph, job, dataset, timestamp):
    dataset_node = add_dataset_node(graph, dataset)
    job_node = add_job_node(graph, job)
    rel = Relationship(job_node, 'WRITES_TO',
                       dataset_node, timestamp=timestamp)
    graph.create(rel)


def add_relationship(graph, job, dataset, timestamp, action):
    if action == 'read':
        add_read_relationship(graph, job, dataset, timestamp)
    elif action == 'write':
        add_write_relationship(graph, job, dataset, timestamp)
    else:
        print('Skipping \"%s\"', action)


def add_event_to_graph(graph, event):
    if event['Action'] not in ['read', 'write']:
        print('Skipping \"%s\"', event['Action'])
        return

    # TODO: Process user either via UID or User Name
    job = {'name': event['Command Line'], 'pid': event['PID']}
    dataset = {'name': event['Path']}
    timestamp = event['Time']
    add_relationship(graph, job, dataset, timestamp, event['Action'])


def reset_graph_schema(graph):
    # TODO: Use uid for dataset as well.
    graph.schema.drop_uniqueness_constraint(
        'Dataset', graph.schema.get_uniqueness_constraints('Dataset'))
    graph.schema.drop_uniqueness_constraint(
        'Job', graph.schema.get_uniqueness_constraints('Job'))

    graph.schema.create_uniqueness_constraint('Dataset', 'name')
    graph.schema.create_uniqueness_constraint('Job', 'uid')


def create_graph():
    # Log-in to Neo4j server.
    authenticate('localhost:7474', 'neo4j', 'admin')

    # Create lineage graph.
    graph = Graph()

    # BTW we do not need to clear the graph anymore if we
    # don't want to, now that we have uniqueness constraints.
    graph.delete_all()

    reset_graph_schema(graph)

    return graph


def build_lineage_graph(event_logs_filename):
    # TODO: Go through log in chunks so that we don't read the whole thing
    # into memory.
    df = pd.read_csv(event_logs_filename)
    if df is None:
        print('Could not read \"%s\" as CSV.  Aborting!', event_logs_filename)
        return None

    # We just want reads and writes.
    df = df[(df['Action'] == 'read') | (df['Action'] == 'write')]

    if df.empty:
        print('No events of interest in \"%s\".  Aborting!', event_logs_filename)
        return None

    graph = create_graph()
    for _, event in df.iterrows():
        add_event_to_graph(graph, event)

    return graph