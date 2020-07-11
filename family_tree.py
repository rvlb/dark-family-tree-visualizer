import networkx as nx
import matplotlib.pyplot as plt
import uuid
from collections import defaultdict

class FamilyTree:
    def __init__(
        self,
        dataset,
        dataset_person_label_key="name",
        dataset_person_parents_key="parents",
        color_mapping_list=None,
        default_node_color="green",
    ):
        self.nodes = set()
        self.persons_marriages_mapping = defaultdict(set)
        self.marriage_edges = defaultdict(set)
        self.children_edges = defaultdict(set)
        self.labels = dict()

        self._generate_nodes_and_edges(dataset, dataset_person_label_key, dataset_person_parents_key)

        self.color_mapping_list = color_mapping_list if color_mapping_list is not None else []
        self.default_node_color = default_node_color

    def _generate_nodes_and_edges(
        self, persons, person_label_key, person_parents_key, person_node_size=300, marriage_node_size=10
    ):
        for person in persons:
            person_label_value = person[person_label_key]
            self.nodes.add((person_label_value, person_node_size))
            self.labels[person_label_value] = person_label_value
            # Add parents marriage edge
            if person_parents_key in person.keys():
                parents = sorted(person[person_parents_key])
                # Create marriage hash
                marriage_hash = uuid.uuid5(uuid.NAMESPACE_OID, " ".join(parents))
                for p in parents:
                    self.nodes.add((p, person_node_size))
                    self.marriage_edges[marriage_hash].add((p, marriage_hash))
                    self.persons_marriages_mapping[p].add(marriage_hash)
                    self.labels[p] = p
                # Add marriage nodes to set
                self.nodes.update((p, person_node_size) for p in parents)
                self.nodes.add((marriage_hash, marriage_node_size))
                # Add child node to set
                self.nodes.add((person_label_value, person_node_size))
                self.children_edges[marriage_hash].add((marriage_hash, person_label_value))

    def _get_node_color(self, node):
        for (color_lambda, color) in self.color_mapping_list:
            if color_lambda(node):
                return color
        return self.default_node_color

    @staticmethod
    def _orthogonal_projection(a, b, c):
        abx = b[0] - a[0]
        aby = b[1] - a[1]
        acx = c[0] - a[0]
        acy = c[1] - a[1]
        t = (abx*acx + aby*acy) / (abx*abx + aby*aby)
        return (a[0] + t*abx, a[1] + t*aby)

    def _adjust_marriage_nodes_positions(self, positions):
        for marriage_hash, edges in self.marriage_edges.items():
            edges_list = [edge[0] for edge in edges]
            marriage_member_0 = positions[edges_list[0]]
            marriage_member_1 = positions[edges_list[1]]
            projection = self._orthogonal_projection(
                marriage_member_0,
                marriage_member_1,
                positions[marriage_hash],
            )
            positions[marriage_hash] = projection
        return positions

    def get_descendants_from(self, current, descendants_set=None):
        if descendants_set is None:
            descendants_set = set()
        if current in descendants_set:
            return descendants_set
        descendants_set.add(current)
        for marriage in self.persons_marriages_mapping[current]:
            for child_edge in self.children_edges[marriage]:
                descendants_set.update(
                    self.get_descendants_from(child_edge[1], descendants_set=descendants_set)
                )
        return descendants_set

    def plot_graph(self, root_node=None, label_offset_x=0, label_offset_y=0):
        marriage_edges_set = set()
        for edges in self.marriage_edges.values():
            marriage_edges_set.update(edges)

        children_edges_set = set()
        for edges in self.children_edges.values():
            children_edges_set.update(edges)

        G = nx.DiGraph()
        G.add_edges_from(children_edges_set | marriage_edges_set)

        positions = self._adjust_marriage_nodes_positions(
            nx.nx_agraph.pygraphviz_layout(G, root=root_node)
        )

        nx.draw_networkx_nodes(
            G,
            pos=positions,
            nodelist=[n[0] for n in self.nodes],
            node_size=[n[1] for n in self.nodes],
            node_color=[self._get_node_color(n) for n in self.nodes]
        )
        nx.draw_networkx_labels(
            G,
            pos={k: (x + label_offset_x, y + label_offset_y) for k, (x, y) in positions.items()},
            labels=self.labels,
            font_size=8,
            font_weight="bold",
        )
        nx.draw_networkx_edges(G, pos=positions, edgelist=marriage_edges_set, edge_color="blue", arrows=False)
        nx.draw_networkx_edges(G, pos=positions, edgelist=children_edges_set, edge_color="blue", arrows=True)

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.show()
