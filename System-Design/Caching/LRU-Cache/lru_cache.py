from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False) 

if __name__ == '__main__':
    lru = LRUCache(2)
    lru.put(1, 10)
    lru.put(2, 20)
    assert lru.get(1) == 10  
    lru.put(3, 30)          
    assert lru.get(2) == -1 
    
    print("Python LRU Cache Test Passed!")