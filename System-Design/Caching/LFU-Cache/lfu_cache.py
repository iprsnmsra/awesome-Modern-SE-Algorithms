class Node:
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def insert_head(self, node: Node):
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node
        self.size += 1

    def remove(self, node: Node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev
        self.size -= 1

    def pop_tail(self) -> Node:
        if self.size > 0:
            tail_node = self.tail.prev
            self.remove(tail_node)
            return tail_node
        return None

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_node = {}
        self.freq_to_list = {}

    def _update_freq(self, node: Node):
        # 1. Remove node from its current frequency list
        old_freq = node.freq
        self.freq_to_list[old_freq].remove(node)
        
        # 2. If the old frequency list is empty and it was the min_freq, increment min_freq
        if old_freq == self.min_freq and self.freq_to_list[old_freq].size == 0:
            self.min_freq += 1
            
        # 3. Increment node frequency and add to the new list
        node.freq += 1
        new_freq = node.freq
        if new_freq not in self.freq_to_list:
            self.freq_to_list[new_freq] = DoublyLinkedList()
        self.freq_to_list[new_freq].insert_head(node)

    def get(self, key: int) -> int:
        if key not in self.key_to_node:
            return -1
        
        node = self.key_to_node[key]
        self._update_freq(node)
        return node.val

    def put(self, key: int, value: int):
        if self.capacity == 0:
            return

        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.val = value
            self._update_freq(node)
        else:
            # Evict if at capacity
            if len(self.key_to_node) >= self.capacity:
                lru_node = self.freq_to_list[self.min_freq].pop_tail()
                del self.key_to_node[lru_node.key]

            # Insert the new node
            new_node = Node(key, value)
            self.key_to_node[key] = new_node
            self.min_freq = 1
            
            if 1 not in self.freq_to_list:
                self.freq_to_list[1] = DoublyLinkedList()
            self.freq_to_list[1].insert_head(new_node)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Initialize cache with capacity 2
    lfu = LFUCache(2)
    
    lfu.put(1, 1) # cache=[1_f1]
    lfu.put(2, 2) # cache=[2_f1, 1_f1]
    
    assert lfu.get(1) == 1 # cache=[1_f2, 2_f1] (1 increases frequency)
    
    lfu.put(3, 3) # Evicts key 2 (least frequent). cache=[3_f1, 1_f2]
    
    assert lfu.get(2) == -1 # 2 is gone
    assert lfu.get(3) == 3  # cache=[3_f2, 1_f2] (3 increases frequency)
    
    lfu.put(4, 4) # Evicts key 1 (tie in frequency, but 1 is LRU). cache=[4_f1, 3_f2]
    
    assert lfu.get(1) == -1 # 1 is gone
    assert lfu.get(3) == 3  # 3 is still here
    assert lfu.get(4) == 4  # 4 is still here
    
    print("Python LFU Cache Test Passed! O(1) frequency eviction verified.")