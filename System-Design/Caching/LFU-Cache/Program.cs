using System;
using System.Collections.Generic;

public class Program {
    public class Node {
        public int key, val, freq;
        public Node prev, next;

        public Node(int key, int val) {
            this.key = key;
            this.val = val;
            this.freq = 1;
        }
    }

    public class DoublyLinkedList {
        public Node head, tail;
        public int size;

        public DoublyLinkedList() {
            head = new Node(0, 0);
            tail = new Node(0, 0);
            head.next = tail;
            tail.prev = head;
            size = 0;
        }

        public void InsertHead(Node node) {
            Node nxt = head.next;
            head.next = node;
            node.prev = head;
            node.next = nxt;
            nxt.prev = node;
            size++;
        }

        public void Remove(Node node) {
            Node prev = node.prev;
            Node nxt = node.next;
            prev.next = nxt;
            nxt.prev = prev;
            size--;
        }

        public Node PopTail() {
            if (size > 0) {
                Node tailNode = tail.prev;
                Remove(tailNode);
                return tailNode;
            }
            return null;
        }
    }

    public class LFUCache {
        private int capacity;
        private int minFreq;
        private Dictionary<int, Node> keyToNode;
        private Dictionary<int, DoublyLinkedList> freqToList;

        public LFUCache(int capacity) {
            this.capacity = capacity;
            this.minFreq = 0;
            this.keyToNode = new Dictionary<int, Node>();
            this.freqToList = new Dictionary<int, DoublyLinkedList>();
        }

        private void UpdateFreq(Node node) {
            int oldFreq = node.freq;
            freqToList[oldFreq].Remove(node);

            if (oldFreq == minFreq && freqToList[oldFreq].size == 0) {
                minFreq++;
            }

            node.freq++;
            int newFreq = node.freq;

            if (!freqToList.ContainsKey(newFreq)) {
                freqToList[newFreq] = new DoublyLinkedList();
            }
            freqToList[newFreq].InsertHead(node);
        }

        public int Get(int key) {
            if (!keyToNode.ContainsKey(key)) return -1;
            
            Node node = keyToNode[key];
            UpdateFreq(node);
            return node.val;
        }

        public void Put(int key, int value) {
            if (capacity == 0) return;

            if (keyToNode.ContainsKey(key)) {
                Node node = keyToNode[key];
                node.val = value;
                UpdateFreq(node);
                return;
            }

            if (keyToNode.Count >= capacity) {
                Node lruNode = freqToList[minFreq].PopTail();
                keyToNode.Remove(lruNode.key);
            }

            Node newNode = new Node(key, value);
            keyToNode[key] = newNode;
            minFreq = 1;

            if (!freqToList.ContainsKey(1)) {
                freqToList[1] = new DoublyLinkedList();
            }
            freqToList[1].InsertHead(newNode);
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var lfu = new LFUCache(2);

        lfu.Put(1, 1);
        lfu.Put(2, 2);

        bool pass = lfu.Get(1) == 1;

        lfu.Put(3, 3); // Evicts 2
        pass &= lfu.Get(2) == -1;
        pass &= lfu.Get(3) == 3;

        lfu.Put(4, 4); // Evicts 1
        pass &= lfu.Get(1) == -1;
        pass &= lfu.Get(3) == 3;
        pass &= lfu.Get(4) == 4;

        if (pass) {
            Console.WriteLine("C# LFU Cache Test Passed!");
            return 0;
        }
        return 1;
    }
}