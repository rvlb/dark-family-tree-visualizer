import json
from family_tree import FamilyTree

with open("dark_dataset.json", mode="r") as f:
    dataset = json.load(f)

ft = FamilyTree(dataset["characters"])

ft.color_mapping_list = [
    (lambda n: n[0] in ft.marriage_edges.keys(), "blue"),
    (lambda n: n[0] in ft.get_descendants_from("Silja Tiedemann"), "red"),
    (lambda n: n[0] == "Bartosz Tiedemann", "yellow"),
]

root_node = list(ft.persons_marriages_mapping["Silja Tiedemann"])[0]
ft.plot_graph(root_node=root_node, label_offset_y=25)