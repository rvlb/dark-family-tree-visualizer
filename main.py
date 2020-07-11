import networkx as nx
import matplotlib.pyplot as plt
import uuid
import math
from collections import defaultdict

characters = [
    {
        "name": "Jonas Kahnwald",
        "parents": ["Mikkel Nielsen", "Hannah Kahnwald"],
    },
    {
        "name": "Martha Nielsen",
        "parents": ["Ulrich Nielsen", "Katharina Nielsen"],
    },
    {
        "name": "The Unknown",
        "parents": ["Martha Nielsen", "Jonas Kahnwald"],
    },
    {
        "name": "Mikkel Nielsen",
        "parents": ["Ulrich Nielsen", "Katharina Nielsen"],
    },
    {
        "name": "Magnus Nielsen",
        "parents": ["Ulrich Nielsen", "Katharina Nielsen"],
    },
    {
        "name": "Ulrich Nielsen",
        "parents": ["Tronte Nielsen", "Jana Nielsen"],
    },
    {
        "name": "Tronte Nielsen",
        "parents": ["Agnes Nielsen", "The Unknown"],
    },
    {
        "name": "Silja Tiedemann",
        "parents": ["Egon Tiedemann", "Hannah Kahnwald"],
    },
    {
        "name": "Agnes Nielsen",
        "parents": ["Silja Tiedemann", "Bartosz Tiedemann"],
    },
    {
        "name": "Hanno Tauber",
        "parents": ["Silja Tiedemann", "Bartosz Tiedemann"],
    },
    {
        "name": "Claudia Tiedemann",
        "parents": ["Egon Tiedemann", "Doris Tiedemann"],
    },
    {
        "name": "Regina Tiedemann",
        "parents": ["Claudia Tiedemann", "Bernd Doppler"],
    },
    {
        "name": "Bartosz Tiedemann",
        "parents": ["Regina Tiedemann", "Boris Niewald"],
    },
    {
        "name": "Charlotte Doppler",
        "parents": ["Hanno Tauber", "Elisabeth Doppler"],
    },
    {
        "name": "Elisabeth Doppler",
        "parents": ["Peter Doppler", "Charlotte Doppler"],
    },
    {
        "name": "Peter Doppler",
        "parents": ["Helge Doppler", "Ulla Schmidt"],
    },
    {
        "name": "Helge Doppler",
        "parents": ["Greta Doppler", "Anatol Veliev"],
    },
]

nodes = set()
characters_marriages_mapping = defaultdict(set)
marriage_edges = defaultdict(set)
children_edges = defaultdict(set)
labels = dict()

for char in characters:
    char_name = char["name"]
    nodes.add((char_name, 300))
    labels[char_name] = char_name
    # Add parents marriage edge
    if "parents" in char.keys():
        parents = sorted(char["parents"])
        # Create marriage hash
        marriage_hash = uuid.uuid5(uuid.NAMESPACE_OID, " ".join(parents))
        for p in parents:
            nodes.add((p, 300))
            marriage_edges[marriage_hash].add((p, marriage_hash))
            characters_marriages_mapping[p].add(marriage_hash)
            labels[p] = p
        # Add marriage nodes to set
        nodes.update((p, 300) for p in parents)
        nodes.add((marriage_hash, 10))
        # Add child node to set
        nodes.add((char_name, 300))
        children_edges[marriage_hash].add((marriage_hash, char_name))

def children_from_knot(current, children_set=None):
    if children_set is None:
        children_set = set()
    if current in children_set:
        return children_set
    children_set.add(current)
    marriages = characters_marriages_mapping[current]
    for marriage in marriages:
        for child_edge in children_edges[marriage]:
            children_set.update(
                children_from_knot(child_edge[1], children_set=children_set)
            )
    return children_set

# Why start from Silja? We could start from Jonas & Martha's child, but them we
# would never be able to reach Silja and her descendents, because both her parents
# exist in the Origin World. However, because she was conceived through time travelling,
# which was never invented in Origin World, she can't exist there.
impossible_children = children_from_knot("Silja Tiedemann")

marriage_edges_set = set()
for edges in marriage_edges.values():
    marriage_edges_set.update(edges)

children_edges_set = set()
for edges in children_edges.values():
    children_edges_set.update(edges)

G = nx.DiGraph()
G.add_edges_from(children_edges_set | marriage_edges_set)
positions = nx.nx_agraph.graphviz_layout(G)

def orthogonal_projection(a, b, c):
    abx = b[0] - a[0]
    aby = b[1] - a[1]
    acx = c[0] - a[0]
    acy = c[1] - a[1]
    t = (abx*acx + aby*acy) / (abx*abx + aby*aby)
    return (a[0] + t*abx, a[1] + t*aby)

for marriage_hash, edges in marriage_edges.items():
    edges_list = [edge[0] for edge in edges]
    marriage_member_0 = positions[edges_list[0]]
    marriage_member_1 = positions[edges_list[1]]
    projection = orthogonal_projection(
        marriage_member_0,
        marriage_member_1,
        positions[marriage_hash]
    )
    positions[marriage_hash] = projection

def get_node_color(node):
    # Check if it's a character node or a marriage node
    if node[0] in marriage_edges.keys():
        return "blue"
    if node[0] in impossible_children:
        return "red"
    # Bartosz is a special case because Regina exists in the Origin World
    # and Boris Niewald probably does too. However, both them only met
    # while Regina was being bullied by Katharina and Ulrich, the latter
    # which doesn't exist in the Origin World. As we can't conclude his
    # true status, he gets a special color here
    if node[0] == "Bartosz Tiedemann":
        return "yellow"
    return "green"

nx.draw_networkx_nodes(
    G,
    pos=positions,
    nodelist=[n[0] for n in nodes],
    node_size=[n[1] for n in nodes],
    node_color=[get_node_color(n) for n in nodes]
)
nx.draw_networkx_labels(
    G,
    pos={k: (x, y + 26) for k, (x, y) in positions.items()},
    labels=labels,
    font_size=8,
    font_weight="bold",
)
nx.draw_networkx_edges(G, pos=positions, edgelist=marriage_edges_set, edge_color="cyan", arrows=False)
nx.draw_networkx_edges(G, pos=positions, edgelist=children_edges_set, edge_color="blue", arrows=True)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.show()
