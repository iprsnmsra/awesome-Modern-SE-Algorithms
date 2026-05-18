import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    static class LRUCache<K, V> extends LinkedHashMap<K, V> {
        private final int capacity;

        public LRUCache(int capacity) {
            super(capacity, 0.75f, true); 
            this.capacity = capacity;
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() > capacity; 
        }
    }
    public static void main(String[] args) {
        LRUCache<Integer, Integer> lru = new LRUCache<>(2);
        lru.put(1, 10);
        lru.put(2, 20);
        
        boolean test1 = lru.get(1) == 10; 
        lru.put(3, 30); // Evicts 2
        boolean test2 = lru.get(2) == null; 
        
        if (test1 && test2) {
            System.out.println("Java LRU Cache Test Passed!");
        } else {
            System.exit(1);
        }
    }
}