import java.util.HashMap;
import java.util.Map;

public class Main {
    static class Node {
        int key, val, freq;
        Node prev, next;

        public Node(int key, int val) {
            this.key = key;
            this.val = val;
            this.freq = 1;
        }
    }

    static class DoublyLinkedList {
        Node head, tail;
        int size;

        public DoublyLinkedList() {
            head = new Node(0, 0);
            tail = new Node(0, 0);
            head.next = tail;
            tail.prev = head;
            size = 0;
        }

        public void insertHead(Node node) {
            Node nxt = head.next;
            head.next = node;
            node.prev = head;
            node.next = nxt;
            nxt.prev = node;
            size++;
        }

        public void remove(Node node) {
            Node prev = node.prev;
            Node nxt = node.next;
            prev.next = nxt;
            nxt.prev = prev;
            size--;
        }

        public Node popTail() {
            if (size > 0) {
                Node tailNode = tail.prev;
                remove(tailNode);
                return tailNode;
            }
            return null;
        }
    }

    static class LFUCache {
        private int capacity;
        private int minFreq;
        private Map<Integer, Node> keyToNode;
        private Map<Integer, DoublyLinkedList> freqToList;

        public LFUCache(int capacity) {
            this.capacity = capacity;
            this.minFreq = 0;
            this.keyToNode = new HashMap<>();
            this.freqToList = new HashMap<>();
        }

        private void updateFreq(Node node) {
            int oldFreq = node.freq;
            freqToList.get(oldFreq).remove(node);

            if (oldFreq == minFreq && freqToList.get(oldFreq).size == 0) {
                minFreq++;
            }

            node.freq++;
            int newFreq = node.freq;
            freqToList.putIfAbsent(newFreq, new DoublyLinkedList());
            freqToList.get(newFreq).insertHead(node);
        }

        public int get(int key) {
            if (!keyToNode.containsKey(key)) return -1;
            Node node = keyToNode.get(key);
            updateFreq(node);
            return node.val;
        }

        public void put(int key, int value) {
            if (capacity == 0) return;

            if (keyToNode.containsKey(key)) {
                Node node = keyToNode.get(key);
                node.val = value;
                updateFreq(node);
                return;
            }

            if (keyToNode.size() >= capacity) {
                Node lruNode = freqToList.get(minFreq).popTail();
                keyToNode.remove(lruNode.key);
            }

            Node newNode = new Node(key, value);
            keyToNode.put(key, newNode);
            minFreq = 1;
            
            freqToList.putIfAbsent(1, new DoublyLinkedList());
            freqToList.get(1).insertHead(newNode);
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        LFUCache lfu = new LFUCache(2);

        lfu.put(1, 1);
        lfu.put(2, 2);

        boolean pass = lfu.get(1) == 1;

        lfu.put(3, 3); // Evicts 2
        pass &= lfu.get(2) == -1;
        pass &= lfu.get(3) == 3;

        lfu.put(4, 4); // Evicts 1
        pass &= lfu.get(1) == -1;
        pass &= lfu.get(3) == 3;
        pass &= lfu.get(4) == 4;

        if (pass) {
            System.out.println("Java LFU Cache Test Passed!");
        } else {
            System.exit(1);
        }
    }
}