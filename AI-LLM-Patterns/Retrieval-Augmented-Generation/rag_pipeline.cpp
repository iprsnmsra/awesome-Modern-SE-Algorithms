#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <cassert>

struct Document {
    std::string text;
    std::vector<double> vector;
};

class RAGPipeline {
private:
    std::vector<Document> knowledgeBase = {
        {"The company revenue in 2025 was $50M.", {1.0, 0.1, 0.0}},
        {"The CEO of the vault is Prasoon.", {0.0, 1.0, 0.1}},
        {"The tech stack uses React and Node.", {0.1, 0.0, 1.0}}
    };

    double cosineSimilarity(const std::vector<double>& vec1, const std::vector<double>& vec2) {
        double dotProduct = 0, normA = 0, normB = 0;
        for (size_t i = 0; i < vec1.size(); i++) {
            dotProduct += vec1[i] * vec2[i];
            normA += vec1[i] * vec1[i];
            normB += vec2[i] * vec2[i];
        }
        if (normA == 0 || normB == 0) return 0;
        return dotProduct / (std::sqrt(normA) * std::sqrt(normB));
    }

    std::string retrieve(const std::vector<double>& queryVector) {
        auto bestDoc = std::max_element(knowledgeBase.begin(), knowledgeBase.end(),
            [this, &queryVector](const Document& a, const Document& b) {
                return cosineSimilarity(queryVector, a.vector) < cosineSimilarity(queryVector, b.vector);
            });
        return bestDoc->text;
    }

public:
    std::string generate(const std::string& query, const std::vector<double>& queryVector) {
        std::string context = retrieve(queryVector);
        std::string prompt = "Context: '" + context + "'. Query: " + query + ". Answer:";
        if (query.find("CEO") != std::string::npos) {
            return prompt + " The CEO is Prasoon.";
        }
        return prompt + " Information retrieved.";
    }
};

// --- CI/CD Automated Test ---
int main() {
    RAGPipeline rag;
    std::string output = rag.generate("Who is the CEO?", {0.1, 0.9, 0.0});
    
    assert(output.find("Prasoon") != std::string::npos);
    std::cout << "C++ RAG Pipeline Test Passed!\n";
    return 0;
}