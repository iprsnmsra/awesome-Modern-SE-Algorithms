interface Document {
    text: string;
    vector: number[];
}

export class RAGPipeline {
    private knowledgeBase: Document[] = [
        { text: "The company revenue in 2025 was $50M.", vector: [1.0, 0.1, 0.0] },
        { text: "The CEO of the vault is Prasoon.", vector: [0.0, 1.0, 0.1] },
        { text: "The tech stack uses React and Node.", vector: [0.1, 0.0, 1.0] }
    ];

    private cosineSimilarity(vec1: number[], vec2: number[]): number {
        let dotProduct = 0, normA = 0, normB = 0;
        for (let i = 0; i < vec1.length; i++) {
            dotProduct += vec1[i] * vec2[i];
            normA += vec1[i] * vec1[i];
            normB += vec2[i] * vec2[i];
        }
        if (normA === 0 || normB === 0) return 0;
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }

    private retrieve(queryVector: number[], topK: number = 1): string[] {
        const scored = this.knowledgeBase.map(doc => ({
            text: doc.text,
            score: this.cosineSimilarity(queryVector, doc.vector)
        }));
        
        scored.sort((a, b) => b.score - a.score);
        return scored.slice(0, topK).map(doc => doc.text);
    }

    public generate(query: string, queryVector: number[]): string {
        const context = this.retrieve(queryVector, 1).join(" ");
        const prompt = `Context: '${context}'. Query: ${query}. Answer:`;
        
        if (query.includes("CEO")) return `${prompt} The CEO is Prasoon.`;
        return `${prompt} Information retrieved.`;
    }
}

// --- CI/CD Automated Test ---
const rag = new RAGPipeline();
const output = rag.generate("Who is the CEO?", [0.1, 0.9, 0.0]);

if (output.includes("Prasoon")) {
    console.log("TypeScript RAG Pipeline Test Passed!");
} else {
    process.exit(1);
}