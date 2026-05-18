using System;
using System.Collections.Generic;

public class Program {
    class LRUCache {
        private int capacity;
        private Dictionary<int, LinkedListNode<(int key, int val)>> cacheMap;
        private LinkedList<(int key, int val)> cacheList;

        public LRUCache(int capacity) {
            this.capacity = capacity;
            cacheMap = new Dictionary<int, LinkedListNode<(int, int)>>(capacity);
            cacheList = new LinkedList<(int, int)>();
        }

        public int Get(int key) {
            if (!cacheMap.TryGetValue(key, out var node)) return -1;
            cacheList.Remove(node);
            cacheList.AddFirst(node);
            return node.Value.val;
        }

        public void Put(int key, int value) {
            if (cacheMap.TryGetValue(key, out var node)) {
                node.Value = (key, value);
                cacheList.Remove(node);
                cacheList.AddFirst(node);
            } else {
                if (cacheList.Count == capacity) {
                    cacheMap.Remove(cacheList.Last.Value.key);
                    cacheList.RemoveLast();
                }
                cacheMap[key] = cacheList.AddFirst((key, value));
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var lru = new LRUCache(2);
        lru.Put(1, 10);
        lru.Put(2, 20);
        bool test1 = lru.Get(1) == 10;
        lru.Put(3, 30);
        bool test2 = lru.Get(2) == -1;

        if (test1 && test2) {
            Console.WriteLine("C# LRU Cache Test Passed!");
            return 0;
        }
        return 1;
    }
}