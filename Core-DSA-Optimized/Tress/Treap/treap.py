import random

class TreapNode:
    def __init__(self, key: int):
        self.key = key
        # Random priority determines heap structure
        self.priority = random.random()
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def _right_rotate(self, y: TreapNode) -> TreapNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        return x

    def _left_rotate(self, x: TreapNode) -> TreapNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        return y

    def _insert(self, root: TreapNode, key: int) -> TreapNode:
        if root is None:
            return TreapNode(key)

        # Standard BST Insert
        if key < root.key:
            root.left = self._insert(root.left, key)
            # Fix Heap property if violated
            if root.left.priority > root.priority:
                root = self._right_rotate(root)
        elif key > root.key:
            root.right = self._insert(root.right, key)
            # Fix Heap property if violated
            if root.right.priority > root.priority:
                root = self._left_rotate(root)
        
        return root

    def insert(self, key: int):
        self.root = self._insert(self.root, key)

    def _delete(self, root: TreapNode, key: int) -> TreapNode:
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            # Node found. If it's a leaf, simply drop it.
            if root.left is None and root.right is None:
                return None
            
            # If one child is empty, return the other
            elif root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            
            # If both children exist, rotate the child with higher priority UP
            elif root.left.priority < root.right.priority:
                root = self._left_rotate(root)
                root.left = self._delete(root.left, key)
            else:
                root = self._right_rotate(root)
                root.right = self._delete(root.right, key)

        return root

    def delete(self, key: int):
        self.root = self._delete(self.root, key)

    def search(self, key: int) -> bool:
        curr = self.root
        while curr:
            if curr.key == key:
                return True
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Fix the random seed to ensure deterministic CI/CD testing
    random.seed(42)
    
    treap = Treap()
    
    # Inserting sequential data. A normal BST would degrade to a straight line.
    for i in range(1, 8):
        treap.insert(i)
        
    assert treap.search(4) == True, "Failed to find inserted node!"
    assert treap.search(10) == False, "Found hallucinated node!"
    
    # Because of random priorities, the root should not be 1 (which would indicate a linked list)
    assert treap.root.key != 1, "Treap degraded into a linked list!"
    
    treap.delete(4)
    assert treap.search(4) == False, "Failed to delete node!"
    
    print(f"Python Treap Test Passed! (Root naturally balanced to: {treap.root.key})")