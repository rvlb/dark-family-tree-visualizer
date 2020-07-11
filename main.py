import json
from family_tree import FamilyTree

with open("dark_dataset.json", mode="r") as f:
    dataset = json.load(f)

ft = FamilyTree(dataset["characters"])

ft.color_mapping_list = [
    (lambda n: n[0] in ft.parentage_edges.keys(), "blue"),
    # This condition deals with descendants from the knot.Why start from Silja?
    # We could start from Jonas & Martha's child, but them we would never be able
    # to reach Silja and her descendents, because both her parents exist in the
    # Origin World. However, because she was conceived through time travelling,
    # which was never invented in Origin World, she can't exist there too.
    (lambda n: n[0] in ft.get_descendants_from("Silja Tiedemann"), "red"),
    # Bartosz is a special case because Regina exists in the Origin World
    # and Boris Niewald probably does too. However, both them only met
    # while Regina was being bullied by Katharina and Ulrich, the latter
    # which doesn't exist in the Origin World. As we can't conclude his
    # true status, he gets a special color here
    (lambda n: n[0] == "Bartosz Tiedemann", "yellow"),
]

root_node = list(ft.persons_parentages_mapping["Silja Tiedemann"])[0]
ft.plot_graph(root_node=root_node, label_offset_y=30)