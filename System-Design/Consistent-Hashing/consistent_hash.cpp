#include <iostream>
#include <string>
#include <map>
#include <functional>
#include <cassert>

class ConsistentHash {
private:
    std::map<size_t, std::string> ring;
    int virtualNodes;

public:
    ConsistentHash(int replicas = 100) : virtualNodes(replicas) {}

    void addServer(const std::string& server) {
        std::hash<std::string> hasher;
        for (int i = 0; i < virtualNodes; ++i) {
            size_t hashVal = hasher(server + "#" + std::to_string(i));
            ring[hashVal] = server;
        }
    }

    void removeServer(const std::string& server) {
        std::hash<std::string> hasher;
        for (int i = 0; i < virtualNodes; ++i) {
            size_t hashVal = hasher(server + "#" + std::to_string(i));
            ring.erase(hashVal);
        }
    }

    std::string getServer(const std::string& key) {
        if (ring.empty()) return "";
        std::hash<std::string> hasher;
        size_t hashVal = hasher(key);
        
        auto it = ring.lower_bound(hashVal); 
        if (it == ring.end()) return ring.begin()->second; 
        return it->second;
    }
};

int main() {
    ConsistentHash ch(3); 
    ch.addServer("NodeA");
    ch.addServer("NodeB");
    
    std::string server1 = ch.getServer("User_Prasoon");
    
    ch.removeServer("NodeA");
    ch.removeServer("NodeB");
    assert(ch.getServer("User_Prasoon") == ""); 
    
    std::cout << "C++ Consistent Hashing Test Passed!\n";
    return 0;
}