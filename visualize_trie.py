from graphviz import Digraph

def build_trie_graph(trie, theme, num_words):
    dot = Digraph(comment="Trie Visualization")
    dot.attr(rankdir="TB")

    # Root metadata nodes
    dot.node("theme", f"Theme: {theme}", shape="box", style="filled", fillcolor="lightblue")
    dot.node("count", f"Words: {num_words}", shape="box", style="filled", fillcolor="lightyellow")
    dot.node("root", "ROOT", shape="circle")

    dot.edge("theme", "count")
    dot.edge("count", "root")

    def dfs(node, parent_id):
        for char, child in node.children.items():
            node_id = f"{parent_id}_{char}"
            label = char + (" ✓" if child.is_end_of_word else "")
            dot.node(node_id, label)
            dot.edge(parent_id, node_id)
            dfs(child, node_id)

    dfs(trie.root, "root")
    return dot
