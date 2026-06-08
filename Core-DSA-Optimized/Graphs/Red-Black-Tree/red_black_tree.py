RED = True
BLACK = False

class Node:
    def __init__(self, val: int):
        self.val = val
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        # T.NIL is the sentinel node representing NULL leaves (Rule 3: Always Black)
        self.NIL = Node(0)
        self.NIL.color = BLACK
        self.root = self.NIL

    def _left_rotate(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _insert_fixup(self, z: Node):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right # The Uncle
                if y.color == RED:
                    # Case 1: Uncle is RED
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Case 2: Uncle is BLACK, z is Right Child
                        z = z.parent
                        self._left_rotate(z)
                    # Case 3: Uncle is BLACK, z is Left Child
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left # The Uncle
                if y.color == RED:
                    # Case 1: Uncle is RED
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2: Uncle is BLACK, z is Left Child
                        z = z.parent
                        self._right_rotate(z)
                    # Case 3: Uncle is BLACK, z is Right Child
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
                    
        self.root.color = BLACK # Rule 2

    def insert(self, val: int):
        z = Node(val)
        z.left = self.NIL
        z.right = self.NIL
        
        y = self.NIL
        x = self.root
        
        # Standard BST Insert
        while x != self.NIL:
            y = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right
                
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z
            
        if z.parent == self.NIL:
            z.color = BLACK
            return
            
        if z.parent.parent == self.NIL:
            return
            
        self._insert_fixup(z)

    def search(self, val: int) -> bool:
        current = self.root
        while current != self.NIL:
            if val == current.val:
                return True
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        return False

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    rbt = RedBlackTree()
    
    # Inserting sequential data (1 to 7). 
    # In a normal BST, the root would be 1, and 7 would be at depth 7 (O(N)).
    for i in range(1, 8):
        rbt.insert(i)
        
    # Verify Search works perfectly
    assert rbt.search(4) == True, "Failed to find inserted node!"
    assert rbt.search(10) == False, "Found a hallucinated node!"
    
    # In a properly balanced Red-Black Tree with elements 1-7, 
    # the root MUST have been rotated to be 2 or 4 to maintain O(log N) height.
    assert rbt.root.val != 1, "Tree failed to rotate! It degraded into a Linked List."
    
    print(f"Python Red-Black Tree Test Passed! (Root mathematically balanced to: {rbt.root.val})")