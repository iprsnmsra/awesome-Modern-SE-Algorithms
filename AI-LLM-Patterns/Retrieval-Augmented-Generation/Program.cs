using System;
using System.Collections.Generic;
using System.Linq;

public class Program {
    class Document {
        public string Text { get; set; }
        public double[] Vector { get; set; }
    }

    class RAGPipeline {
        private List<Document> knowledgeBase = new List<Document> {
            new Document { Text = "The company revenue in 2025 was $50M.", Vector = new[] { 1.0, 0.1, 0.0 } },
            new Document { Text = "The CEO of the vault is Prasoon.", Vector = new[] { 0.0, 1.0, 0.1 } },
            new Document { Text = "The tech stack uses React and Node.", Vector = new[] { 0.1, 0.0, 1.0 } }
        };

        private double CosineSimilarity(double[] vec1, double[] vec2) {
            double dotProduct = 0, normA = 0, normB = 0;
            for (int i = 0; i < vec1.Length; i++) {
                dotProduct += vec1[i] * vec2[i];
                normA += vec1[i] * vec1[i];
                normB += vec2[i] * vec2[i];
            }
            if (normA == 0 || normB == 0) return 0;
            return dotProduct / (Math.Sqrt(normA) * Math.Sqrt(normB));
        }

        private string Retrieve(double[] queryVector) {
            return knowledgeBase.OrderByDescending(doc => CosineSimilarity(queryVector, doc.Vector)).First().Text;
        }

        public string Generate(string query, double[] queryVector) {
            string context = Retrieve(queryVector);
            string prompt = $"Context: '{context}'. Query: {query}. Answer:";
            if (query.Contains("CEO")) return $"{prompt} The CEO is Prasoon.";
            return $"{prompt} Information retrieved.";
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var rag = new RAGPipeline();
        string output = rag.Generate("Who is the CEO?", new double[] { 0.1, 0.9, 0.0 });

        if (output.Contains("Prasoon")) {
            Console.WriteLine("C# RAG Pipeline Test Passed!");
            return 0;
        }
        return 1;
    }
}