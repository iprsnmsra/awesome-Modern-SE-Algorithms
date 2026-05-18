using System;
using System.Collections.Generic;
using System.Linq;

public class Program {
    class ConsistentHash {
        private readonly int virtualNodes;
        private readonly SortedList<int, string> ring = new SortedList<int, string>();

        public ConsistentHash(int virtualNodes = 100) {
            this.virtualNodes = virtualNodes;
        }

        private int Hash(string key) {
            return key.GetHashCode();
        }

        public void AddServer(string server) {
            for (int i = 0; i < virtualNodes; i++) {
                ring[Hash($"{server}#{i}")] = server;
            }
        }

        public string GetServer(string key) {
            if (ring.Count == 0) return null;
            
            int hashVal = Hash(key);
            var keys = ring.Keys.ToList();
            
            int idx = keys.BinarySearch(hashVal);
            if (idx < 0) idx = ~idx; 
            if (idx == keys.Count) idx = 0; 
            
            return ring[keys[idx]];
        }
    }

    public static void Main() {
        var ch = new ConsistentHash(10);
        ch.AddServer("Cache_1");
        ch.AddServer("Cache_2");
        
        string assigned = ch.GetServer("Image_XYZ");
        
        if (assigned == "Cache_1" || assigned == "Cache_2") {
            Console.WriteLine("C# Consistent Hashing Test Passed!");
        } else {
            Environment.Exit(1);
        }
    }
}