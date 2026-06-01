<div align="center">
  <h1>🪣 Token Bucket Rate Limiter</h1>
  <p><b>Protecting APIs from DDoS spikes while allowing legitimate burst traffic.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(Math check per request)* **Space Complexity:** O(1) *(Only stores two integers per user: token count and last refill timestamp)*

## 🚨 The Problem
If you expose a public API, malicious bots or poorly written client code can accidentally send 10,000 requests per second. This will crash your database and exhaust your server's memory. You must limit requests (e.g., "5 requests per second"). However, strict limits break user experience. If a user loads a webpage that requires 5 rapid API calls simultaneously, a strict limit will block them, even if they don't make another request for an hour. 

## 💡 The Solution
The Token Bucket algorithm balances strict limits with "burst" tolerance. 
Instead of tracking a strict window of time, we track *Tokens*.
* **Capacity (Burst Limit):** The bucket can hold a maximum of 5 tokens. This means a user can make 5 rapid requests at the exact same millisecond.
* **Refill Rate (Sustained Limit):** The bucket refills at a rate of 1 token every second.

When a request arrives, we calculate how much time has passed since their last request, mathematically add the appropriate number of tokens to their bucket, and then try to subtract 1 token for the current request.

## ⚙️ Real-World Use Cases
* **API Gateways:** Amazon AWS API Gateway and Kong use Token Buckets to protect backend microservices.
* **Payment Processors:** Stripe uses Token Buckets to ensure merchants don't spam the credit card network while allowing checkout bursts during flash sales.
* **Network Routers:** Cisco routers use Token Buckets for Traffic Shaping (throttling bandwidth to 50 Mbps while allowing short bursts).

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The CI/CD test simulates a user bursting 5 rapid requests, getting blocked on the 6th, and then waiting exactly enough time for the bucket to refill so they can request again.

* **Python:** `python3 token_bucket.py`
* **TypeScript:** `npx ts-node tokenBucket.ts`
* **C++:** `g++ -std=c++17 token_bucket.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"A good rate limiter doesn't just block traffic. It shapes traffic."*

**🤫 Secret Principal Engineer Tip:** The code here is a single-server implementation. In a distributed microservice cluster, you cannot store the bucket in local server memory (because User A might hit Server 1, and then Server 2). In production, you implement this exact math inside a **Redis Lua Script**. Redis guarantees atomic execution, meaning multiple servers can decrement the shared bucket simultaneously without race conditions.