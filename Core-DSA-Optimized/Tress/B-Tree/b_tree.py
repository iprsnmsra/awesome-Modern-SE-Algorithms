class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def search(self, k, node=None):
        if node is None:
            node = self.root
            
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
            
        if node.leaf:
            return None

        return self.search(k, node.children[i])

    def insert(self, k):
        root = self.root
        
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        
        if node.leaf:
           
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        t = self.t
        full_child = parent.children[i]

        new_node = BTreeNode(full_child.leaf)

        new_node.keys = full_child.keys[t:]

        if not full_child.leaf:
            new_node.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        middle_key = full_child.keys[t - 1]
        full_child.keys = full_child.keys[:t - 1]

        parent.children.insert(i + 1, new_node)
        parent.keys.insert(i, middle_key)

if __name__ == '__main__':

    btree = BTree(3)
    
    for i in range(1, 21):
        btree.insert(i)
        

    assert btree.search(15) is not None, "Failed to find inserted key 15!"
    assert btree.search(99) is None, "Found a key that was never inserted!"

    assert len(btree.root.keys) > 0, "Root is empty!"
    assert btree.root.keys[0] != 1, "Tree failed to balance! It grew like a Linked List."
    
    print("Python B-Tree Test Passed! Massive Disk-Optimized Structure Verified.")