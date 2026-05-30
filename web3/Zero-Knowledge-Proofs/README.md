<div align="center">
  <h1>👻 Zero-Knowledge Proofs (Schnorr Protocol)</h1>
  <p><b>Proving knowledge of a cryptographic secret without revealing it.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Web3_%26_Crypto-gold?style=for-the-badge)
</div>

---

**Time Complexity:** O(log E) *(Where E is the exponent in modular exponentiation)* **Space Complexity:** O(1) *(Pure in-place mathematics)*

## 🚨 The Problem
In decentralized finance (DeFi) or secure authentication systems, you often need to prove authorization. If a server asks for your password, you send it over the wire. Even if encrypted, the server decrypts it, sees it, and stores it. If the server is hacked, your secret is stolen. In Web3, sending a secret to a public Smart Contract means every node on earth immediately sees it.

## 💡 The Solution
A Zero-Knowledge Proof (ZKP) is an interactive mathematical game played between a **Prover** and a **Verifier**. 
We use the **Schnorr Protocol**, based on the Discrete Logarithm Problem.
* **Public Knowledge:** A large prime `p`, a generator `g`, and your Public Key `y = (g^x) mod p`.
* **The Secret:** Your Private Key `x`.

**The Game:**
1. The Prover picks a random number `k`, calculates `r = (g^k) mod p`, and sends `r` to the Verifier.
2. The Verifier replies with a random challenge number `c`.
3. The Prover calculates `s = k + c * x` and sends `s` to the Verifier.
4. The Verifier calculates `(g^s) mod p` and checks if it exactly equals `(r * y^c) mod p`. 

If the math matches, the Verifier is 100% certain the Prover knows `x`. But because `x` was mathematically scrambled with the random `k` and `c`, the Verifier learns absolutely nothing about `x` itself.

## ⚙️ Real-World Use Cases
* **Privacy Blockchains:** Zcash and Monero use advanced ZKPs to hide sender, receiver, and transaction amounts while still proving the transaction is mathematically valid.
* **zk-Rollups (Layer 2s):** Ethereum scaling solutions like zkSync and Starknet process 10,000 transactions off-chain, and submit a single cryptographic ZKP to the mainnet proving all 10,000 were valid.
* **Passwordless Logins:** FIDO2 and WebAuthn hardware keys use variations of this protocol to authenticate you without ever sending a password over the internet.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. 
*(Note: This uses small educational prime numbers so it compiles instantly without massive BigInt libraries, but the cryptographic logic is perfectly identical to production).*

* **Python:** `python3 zkp_schnorr.py`
* **TypeScript:** `npx ts-node zkpSchnorr.ts`
* **C++:** `g++ -std=c++17 zkp_schnorr.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"In cryptography, a secret shared is a secret compromised. Zero-Knowledge is the art of proving without sharing."*

**🤫 Secret Principal Engineer Tip:** This interactive protocol requires the Prover and Verifier to be online at the same time to send the Challenge (`c`) back and forth. In Web3 production, we use the **Fiat-Shamir Heuristic** to make it *Non-Interactive* (NIZK). We replace the Verifier's random challenge by simply hashing the Commitment `r`. This allows you to generate a proof offline and post it directly to the blockchain!

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>