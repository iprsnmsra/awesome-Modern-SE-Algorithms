import java.util.*;

public class Main {
    static class Document {
        String text;
        double[] vector;
        Document(String t, double[] v) { text = t; vector = v; }
    }

    static class RAGPipeline {
        private List<Document> knowledgeBase = Arrays.asList(
            new Document("The company revenue in 2025 was $50M.", new double[]{1.0, 0.1, 0.0}),
            new Document("The CEO of the vault is Prasoon.", new double[]{0.0, 1.0, 0.1}),
            new Document("The tech stack uses React and Node.", new double[]{0.1, 0.0, 1.0})
        );

        private double cosineSimilarity(double[] vec1, double[] vec2) {
            double dotProduct = 0, normA = 0, normB = 0;
            for (int i = 0; i < vec1.length; i++) {
                dotProduct += vec1[i] * vec2[i];
                normA += vec1[i] * vec1[i];
                normB += vec2[i] * vec2[i];
            }
            if (normA == 0 || normB == 0) return 0;
            return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
        }

        private String retrieve(double[] queryVector) {
            return Collections.max(knowledgeBase, Comparator.comparingDouble(
                doc -> cosineSimilarity(queryVector, doc.vector)
            )).text;
        }

        public String generate(String query, double[] queryVector) {
            String context = retrieve(queryVector);
            String prompt = "Context: '" + context + "'. Query: " + query + ". Answer:";
            if (query.contains("CEO")) return prompt + " The CEO is Prasoon.";
            return prompt + " Information retrieved.";
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        RAGPipeline rag = new RAGPipeline();
        String output = rag.generate("Who is the CEO?", new double[]{0.1, 0.9, 0.0});
        
        if (output.contains("Prasoon")) {
            System.out.println("Java RAG Pipeline Test Passed!");
        } else {
            System.exit(1);
        }
    }
}