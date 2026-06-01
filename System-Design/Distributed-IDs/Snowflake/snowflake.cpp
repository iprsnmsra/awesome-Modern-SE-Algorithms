#include <iostream>
#include <stdexcept>
#include <chrono>
#include <mutex>
#include <cassert>

using namespace std;

class SnowflakeGenerator {
private:
    const uint64_t EPOCH = 1609459200000ULL;
    const int WORKER_ID_BITS = 5;
    const int DATACENTER_ID_BITS = 5;
    const int SEQUENCE_BITS = 12;

    const uint64_t MAX_WORKER_ID = -1ULL ^ (-1ULL << WORKER_ID_BITS);
    const uint64_t MAX_DATACENTER_ID = -1ULL ^ (-1ULL << DATACENTER_ID_BITS);

    const int WORKER_SHIFT = SEQUENCE_BITS;
    const int DATACENTER_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS;
    const int TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS;

    const uint64_t SEQUENCE_MASK = -1ULL ^ (-1ULL << SEQUENCE_BITS);

    uint64_t datacenterId;
    uint64_t workerId;
    uint64_t sequence = 0;
    uint64_t lastTimestamp = 0;
    
    mutex mtx;

    uint64_t currentTimeMillis() {
        auto now = chrono::system_clock::now();
        auto duration = now.time_since_epoch();
        return chrono::duration_cast<chrono::milliseconds>(duration).count();
    }

public:
    SnowflakeGenerator(uint64_t dcId, uint64_t wId) : datacenterId(dcId), workerId(wId) {
        if (datacenterId > MAX_DATACENTER_ID) {
            throw invalid_argument("Invalid Datacenter ID");
        }
        if (workerId > MAX_WORKER_ID) {
            throw invalid_argument("Invalid Worker ID");
        }
    }

    uint64_t nextId() {
        lock_guard<mutex> lock(mtx);
        uint64_t timestamp = currentTimeMillis();

        if (timestamp < lastTimestamp) {
            throw runtime_error("Clock moved backwards.");
        }

        if (timestamp == lastTimestamp) {
            sequence = (sequence + 1) & SEQUENCE_MASK;
            if (sequence == 0) {
                while (timestamp <= lastTimestamp) {
                    timestamp = currentTimeMillis();
                }
            }
        } else {
            sequence = 0;
        }

        lastTimestamp = timestamp;

        return ((timestamp - EPOCH) << TIMESTAMP_SHIFT) |
               (datacenterId << DATACENTER_SHIFT) |
               (workerId << WORKER_SHIFT) |
               sequence;
    }
};

// --- CI/CD Automated Test ---
int main() {
    SnowflakeGenerator generator(1, 1);
    
    uint64_t id1 = generator.nextId();
    uint64_t id2 = generator.nextId();
    
    assert(id1 != id2);
    assert(id2 > id1);
    
    cout << "C++ Snowflake ID Test Passed!\n";
    cout << "Generated ID 1: " << id1 << "\n";
    cout << "Generated ID 2: " << id2 << "\n";
    
    return 0;
}