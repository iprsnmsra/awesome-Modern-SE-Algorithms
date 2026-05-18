import hashlib
import bisect

class ConsistentHash:
    def __init__(self, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_server(self, server):
        for i in range(self.virtual_nodes):
            h = self._hash(f"{server}#{i}")
            self.ring[h] = server
            bisect.insort(self.sorted_keys, h)

    def remove_server(self, server):
        for i in range(self.virtual_nodes):
            h = self._hash(f"{server}#{i}")
            if h in self.ring:
                del self.ring[h]
                self.sorted_keys.remove(h)

    def get_server(self, key):
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h)
        if idx == len(self.sorted_keys):
            idx = 0 
        return self.ring[self.sorted_keys[idx]]

if __name__ == '__main__':
    ch = ConsistentHash(virtual_nodes=5)
    ch.add_server("Server_1")
    ch.add_server("Server_2")
    
    assigned = ch.get_server("User_123")
    assert assigned in ["Server_1", "Server_2"]
    
    print("Python Consistent Hashing Test Passed!")