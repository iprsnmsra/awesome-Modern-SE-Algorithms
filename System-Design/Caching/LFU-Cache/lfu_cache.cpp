#include <iostream>
#include <unordered_map>
#include <cassert>

using namespace std;

struct Node {
    int key, val, freq;
    Node* prev;
    Node* next;
    Node(int k, int v) : key(k), val(v), freq(1), prev(nullptr), next(nullptr) {}
};

class DoublyLinkedList {
public:
    Node* head;
    Node* tail;
    int size;

    DoublyLinkedList() {
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head->next = tail;
        tail->prev = head;
        size = 0;
    }

    ~DoublyLinkedList() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* nxt = curr->next;
            delete curr;
            curr = nxt;
        }
    }

    void insertHead(Node* node) {
        Node* nxt = head->next;
        head->next = node;
        node->prev = head;
        node->next = nxt;
        nxt->prev = node;
        size++;
    }

    void remove(Node* node) {
        Node* prev = node->prev;
        Node* nxt = node->next;
        prev->next = nxt;
        nxt->prev = prev;
        size--;
    }

    Node* popTail() {
        if (size > 0) {
            Node* tailNode = tail->prev;
            remove(tailNode);
            return tailNode;
        }
        return nullptr;
    }
};

class LFUCache {
private:
    int capacity;
    int minFreq;
    unordered_map<int, Node*> keyToNode;
    unordered_map<int, DoublyLinkedList*> freqToList;

    void updateFreq(Node* node) {
        int oldFreq = node->freq;
        freqToList[oldFreq]->remove(node);

        if (oldFreq == minFreq && freqToList[oldFreq]->size == 0) {
            minFreq++;
        }

        node->freq++;
        int newFreq = node->freq;

        if (freqToList.find(newFreq) == freqToList.end()) {
            freqToList[newFreq] = new DoublyLinkedList();
        }
        freqToList[newFreq]->insertHead(node);
    }

public:
    LFUCache(int cap) : capacity(cap), minFreq(0) {}

    ~LFUCache() {
        for (auto& pair : freqToList) {
            delete pair.second;
        }
        // Nodes inside are deleted by DoublyLinkedList destructor
    }

    int get(int key) {
        if (keyToNode.find(key) == keyToNode.end()) return -1;
        
        Node* node = keyToNode[key];
        updateFreq(node);
        return node->val;
    }

    void put(int key, int value) {
        if (capacity == 0) return;

        if (keyToNode.find(key) != keyToNode.end()) {
            Node* node = keyToNode[key];
            node->val = value;
            updateFreq(node);
            return;
        }

        if (keyToNode.size() >= capacity) {
            Node* lruNode = freqToList[minFreq]->popTail();
            keyToNode.erase(lruNode->key);
            delete lruNode;
        }

        Node* newNode = new Node(key, value);
        keyToNode[key] = newNode;
        minFreq = 1;

        if (freqToList.find(1) == freqToList.end()) {
            freqToList[1] = new DoublyLinkedList();
        }
        freqToList[1]->insertHead(newNode);
    }
};

// --- CI/CD Automated Test ---
int main() {
    LFUCache lfu(2);

    lfu.put(1, 1);
    lfu.put(2, 2);

    assert(lfu.get(1) == 1);

    lfu.put(3, 3); // Evicts 2
    assert(lfu.get(2) == -1);
    assert(lfu.get(3) == 3);

    lfu.put(4, 4); // Evicts 1
    assert(lfu.get(1) == -1);
    assert(lfu.get(3) == 3);
    assert(lfu.get(4) == 4);

    cout << "C++ LFU Cache Test Passed!\n";
    return 0;
}