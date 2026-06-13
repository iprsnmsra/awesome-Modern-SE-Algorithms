<div align="center">
  <h1>🔄 Saga Pattern (Distributed Transactions)</h1>
  <p><b>Managing microservice rollbacks without locking global databases.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-blue?style=for-the-badge)
</div>

---

## 🚨 The Problem
In a microservices architecture, every service has its own private database. A standard user action (like booking a flight, hotel, and rental car) spans multiple services. If the flight and hotel book successfully, but the rental car fails, you cannot simply issue a SQL `ROLLBACK` command because the flight and hotel databases have already committed their changes and moved on. 

## 🧠 The Core Logic
The Saga Pattern replaces the traditional database transaction with a sequence of local transactions coordinated by a central State Machine (The Orchestrator). 

For every step that moves the system forward (`Execute`), the engineer must write a corresponding step that perfectly undoes that specific action (`Compensate`). 

1. **The Forward Path:** The Orchestrator fires `Execute` on Step 1, Step 2, and Step 3 sequentially. It keeps a log of exactly which steps succeeded.
2. **The Failure:** Step 3 throws an error (e.g., "Out of Stock" or "API Timeout").
3. **The Rollback Path:** The Orchestrator stops. It looks at its log of successful steps, reverses them, and fires the `Compensate` function for Step 2, and then Step 1. The system is cleanly restored to its original state.

## ⚙️ Real-World Use Cases
* **Uber / Lyft:** Coordinating the Rider App, Driver App, and Payment Gateway. If a driver cancels, the rider's pending payment hold is reversed via a Saga compensation.
* **Amazon / E-Commerce:** Order Processing (Order Created -> Payment Processed -> Warehouse Picked -> Shipped). If shipping fails, refunds are issued automatically.
* **Travel Booking:** Expedia booking flights, hotels, and cars. If the hotel API goes down, the flight booking is actively canceled.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The code implements a `SagaOrchestrator` simulating an E-Commerce checkout flow. We will intentionally trigger an Out-Of-Stock error to watch the orchestrator successfully refund the payment and cancel the order.

* **Python:** `python3 saga_orchestrator.py`
* **TypeScript:** `npx ts-node sagaOrchestrator.ts`
* **C++:** `g++ -std=c++17 saga_orchestrator.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not try to stop time by locking the world. Let the system move forward, and build the machinery to cleanly walk backward if you stumble."*

**🤫 Secret Principal Engineer Tip:** Compensating transactions (the undo steps) are executed over a network, which means *they can also fail or time out*. If a refund times out, the Orchestrator will automatically retry it. Therefore, every single `Compensate` function you write must be mathematically **Idempotent**. Whether you call `RefundPayment()` once or 100 times, it must only ever refund the money exactly one time!