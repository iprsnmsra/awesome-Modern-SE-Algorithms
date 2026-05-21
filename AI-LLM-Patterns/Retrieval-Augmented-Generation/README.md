# 🧠 Retrieval-Augmented Generation (RAG)

**Time Complexity (Retrieval):** O(N),O(D) *(Where N is number of documents, D is embedding dimensions)* **Space Complexity:** O(N),O(D) *(To store the Vector space in memory)* ## 🚨 The Problem
Large Language Models (LLMs) are frozen in time after their training cuts off. They have zero knowledge of your private database, your company's API documentation, or today's news. If you want an AI to answer customer support questions based on your private manuals, relying on the model's base memory will result in dangerous, confidently incorrect hallucinations.

## 💡 The Solution
RAG separates the "Knowledge" from the "Reasoning."
1. **The Vector Database:** We convert all our private documents into dense vector embeddings (arrays of floats). 
2. **Cosine Similarity:** When a query comes in, we embed it, and calculate the angle between the query vector and all document vectors. The smallest angles (closest to 1.0) represent the most semantically relevant documents.
3. **Prompt Injection:** We pull the raw text of those top documents and feed them to the LLM alongside the user's original question. 

## ⚙️ Real-World Use Cases
* **Enterprise AI Search:** Glean, Notion AI, and Microsoft Copilot reading your private Google Drive/SharePoint files.
* **Customer Support Bots:** AI agents reading your company's Zendesk articles to answer user tickets accurately.
* **Legal Tech:** Scanning 10,000-page case law PDFs to find the exact precedent for a lawyer's query.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation.

* **Python:** `python3 rag_pipeline.py`
* **TypeScript:** `npx ts-node ragPipeline.ts`
* **C++:** `g++ -std=c++17 rag_pipeline.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"An LLM without RAG is a brilliant professor locked in a room with no internet. RAG gives them a search engine."*

**🤫 Secret Principal Engineer Tip:** Standard cosine similarity search (O(N)) fails when you have 1 Billion vectors. In production, you must use **HNSW (Hierarchical Navigable Small World)** graphs—the exact algorithm powering Pinecone and Milvus—to drop the retrieval time complexity to O(log N).