from IPython.display import IFrame
import json
import uuid


def vis_network(nodes, edges, physics=False):
    html = """
    <html>
    <head>
      <script type="text/javascript" src="../lib/vis/dist/vis.js"></script>
      <link href="../lib/vis/dist/vis.css" rel="stylesheet" type="text/css">

      <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">

    <script type="text/javascript">
    function onClickHandler(){{
      console.log('click detected!');
    }}

    function draw() {{
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

      var options = {{
          layout: {{
              improvedLayout: false,
              hierarchical: {{
                  enabled: true,
                  blockShifting: false,
                  levelSeparation: 400,
                  nodeSpacing: 300,
                  direction: 'LR',
                  sortMethod: 'directed'
              }}
          }},
          nodes: {{
              shape: 'dot',
              font: {{
                  size: 14
              }},
              size: 25
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics}
          }},
          groups:{{
              'Job': {{
                  shape: 'icon',
                  icon: {{
                      face: 'FontAwesome',
                      code: '\uf085',
                      size: 40,
                      color: '#a815de'
                  }}
              }},
              'Dataset': {{
                  shape: 'icon',
                  icon: {{
                      face: 'FontAwesome',
                      code: '\uf15c',
                      size: 40,
                      color: '#f0a30a'
                  }}
              }}
          }}
      }};

      var network = new vis.Network(container, data, options);

      network.once("afterDrawing", function() {{
        console.log('here from afterDrawing event!');
        document.getElementById('{id}').click();
      }});
    }}

    </script>

    </head>

    <body onload="draw()">
    <div id="{id}"></div>
    </body>
    </html>
    """

#    unique_id = str(uuid.uuid4())
#    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))
#    filename = "figure/graph-{}.html".format(unique_id)

    html = html.format(id=1, nodes=json.dumps(
        nodes), edges=json.dumps(edges), physics=json.dumps(physics))
    filename = "figure/graph.html"

    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="400")


def draw(graph, options, physics=False, limit=100):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    query = """
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT {limit}
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
           id(n) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    """

    data = graph.run(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_label = list(node.labels())[0]
        prop_key = options.get(node_label)
        vis_label = node.properties.get(prop_key, "")
        cpu_consumption = node.properties.get("cpu", None)
        if cpu_consumption is not None:
            vis_label += ", cpu=" + str(round(cpu_consumption, 2))
        # TODO: Here use abbreviated label instead of full label.
        max_label_length = 15
        abbr_vis_label = vis_label[:max_label_length] + \
            '...' if len(vis_label) > max_label_length else vis_label

# return {"id": id, "label": abbr_vis_label, "group": node_label, "title":
# repr(node.properties)}
        return {"id": id, "label": abbr_vis_label, "group": node_label, "title": vis_label}

    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)

#            edges.append({"from": source_info["id"], "to": target_info[
#                "id"], "label": rel.type(), "title": repr(rel.properties)})

            edges.append({"from": source_info["id"], "to": target_info[
                "id"], "label": "", "title": rel.type() + ': ' + repr(rel.properties)})

    return vis_network(nodes, edges, physics=physics)
