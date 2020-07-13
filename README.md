# Dark Family Tree Visualizer

A simple family tree visualizer for the Dark series (SPOILERS ALERT).

Logic contained in [family_tree.py](https://github.com/rvlb-19/dark-family-tree-visualizer/blob/master/family_tree.py) is context unaware, so you can provide your own custom dataset and it will do its best to generate a family tree.

You can check how it's done on [main.py](https://github.com/rvlb-19/dark-family-tree-visualizer/blob/master/main.py) and on [dark_dataset.json](https://github.com/rvlb-19/dark-family-tree-visualizer/blob/master/dark_dataset.json), but you should only do so if you have watched the entire series or don't care for spoilers.

## Documentation
Soon...

## Running with `pygraphviz`
1. You must install [graphviz](https://graphviz.org/download/) on your machine in order to use `pygraphviz`;
2. Install the packages listed in `requirements.txt` using `pip`;
3. In case `pygraphviz` fails, install the other packages separately and then install `pygraphviz` using [this](https://github.com/pygraphviz/pygraphviz/issues/100#issuecomment-385031539);
4. After installation, run `python main.py`.

## Running without `pygraphviz`
`pygraphviz` is required in order to use `pygraphviz_layout` from `networkx`. If you wish to use a different layout, you must change the following line on [family_tree.py](https://github.com/rvlb-19/dark-family-tree-visualizer/blob/master/family_tree.py):
```python
nx.nx_agraph.pygraphviz_layout(G, root=root_node)
```
You may use any of the layouts on [networkx Graph Layouts](https://networkx.github.io/documentation/stable/reference/drawing.html#module-networkx.drawing.layout).
