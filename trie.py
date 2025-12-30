from graphviz import Digraph
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end_of_word = True
        node.word = word

    def search_prefix(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results: List[str] = []
        self._collect(node, results)
        return results

    def _collect(self, node: TrieNode, results: List[str]):
        if node.is_end_of_word:
            results.append(node.word)
        for child in node.children.values():
            self._collect(child, results)

    # 🌳 GRAPHVIZ VISUALIZATION
    def visualize_graph(self, filename="trie"):
        try:
            dot = Digraph(comment="Trie Structure")
            dot.node("root", "ROOT")

            def dfs(node, parent_id):
                for char, child in node.children.items():
                    node_id = f"{parent_id}_{char}"
                    label = char + (" ✓" if child.is_end_of_word else "")
                    dot.node(node_id, label)
                    dot.edge(parent_id, node_id)
                    dfs(child, node_id)

            dfs(self.root, "root")
            dot.render(filename, view=True)

        except Exception:
            print("\n⚠️ Graphviz not installed or not in PATH.")
            print("➡ Skipping graphical visualization.")
