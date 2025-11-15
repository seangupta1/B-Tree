class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTree:
    def __init__(self, max_degree=3):
        self.root = BPlusTreeNode(is_leaf=True)
        self.max_degree = max_degree

    def insert(self, word):
        root = self.root
        if len(root.keys) >= self.max_degree:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, word)

    def _insert_non_full(self, node, word):
        if node.is_leaf:
            idx = 0
            while idx < len(node.keys) and word > node.keys[idx]:
                idx += 1
            node.keys.insert(idx, word)
        else:
            i = len(node.keys) - 1
            while i >= 0 and word < node.keys[i]:
                i -= 1
            i += 1
            child = node.children[i]
            if len(child.keys) >= self.max_degree:
                self._split_child(node, i)
                if word > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], word)

    def _split_child(self, parent, index):
        node = parent.children[index]
        new_node = BPlusTreeNode(is_leaf=node.is_leaf)
        mid = self.max_degree // 2

        if node.is_leaf:
            # Split keys
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]

            # Link leaves
            new_node.next = node.next
            node.next = new_node

            # Insert smallest key of new_node into parent
            parent.keys.insert(index, new_node.keys[0])
        else:
            # Promote middle key
            promote = node.keys[mid]
            new_node.keys = node.keys[mid + 1:]
            node.keys = node.keys[:mid]

            new_node.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]

            parent.keys.insert(index, promote)

        parent.children.insert(index + 1, new_node)

    def search(self, search_key):
        node = self._search(search_key, self.root)
        if node is not None:
            return node
        return

    def _search(self, search_key, node):
        if search_key is None:
            print("No search key provided.")
            return None

        if node.is_leaf:
            #print("Checking leaf node.")
            if search_key in node.keys:
                #print("Returning node found.")
                return node
            else:
                #print("Key not found.")
                return None

        #print("Starting loop")
        for i in range(len(node.keys)):
            #print(f"Checking node with keys: {node.keys} | index: {i}.")
            if search_key < node.keys[i]:
                #print(f"Recursive call less than -{node.keys[i]}-")
                return self._search(search_key, node.children[i])
        return self._search(search_key, node.children[-1])

    def print_linked_list(self):
        # Traverse down to the leftmost leaf
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        # Print all words in order using linked list of leaves
        while node:
            for word in node.keys:
                print(word, end=", ")
            node = node.next
        print()

    def get_tree_height(self):
        height = 0
        node = self.root
        while not node.is_leaf:
            height += 1
            node = node.children[0]  # Traverse to the leftmost child at each level
        return height

    def print_tree(self):
        # Print the tree starting from the root
        if self.root:
            self._print_tree(self.root, 0)
        else:
            print("Tree is empty")

    def _print_tree(self, node, level):
        # Print the current level of the tree
        print(f"Level {level}: ", end="")

        if node.is_leaf:
            # Print the words stored in the leaf node
            print("Leaf Node with words:", node.keys)
        else:
            # Print the routing keys in an internal node
            print("Internal Node with keys:", node.keys)

        # Recursively print the children
        if not node.is_leaf:
            for child in node.children:
                self._print_tree(child, level + 1)

tree = BPlusTree(3)
filepath = "1000-most-common-words.txt"
with open(filepath, 'r') as file:
    for line in file:
        tree.insert(line.strip())

to_search = ["I", "your", "test", "noword"]
for word in to_search:
    print("Searching for: ", word)
    node = tree.search(word)
    if node is not None:
        print("Found: ", node.keys)
    else:
        print("Not found: ", word)
    print()
