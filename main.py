import re
import os
from collections import Counter
from itertools import combinations

class TextbookSimilarityAnalyzer:
    def __init__(self):
        # Words to exclude from frequency analysis
        self.stop_words = {"A", "AND", "AN", "OF", "IN", "THE"}
    
    def clean_text(self, text):
        """
        Clean text by keeping only alphanumeric characters and converting to uppercase
        """
        # Keep only alphanumeric characters and spaces
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Convert to uppercase
        cleaned = cleaned.upper()
        # Split into words and remove empty strings
        words = [word for word in cleaned.split() if word]
        return words

    def get_top_frequent_words(self, words, top_n=15):
        """
        Get top N frequent words excluding stop words
        """
        # Filter out stop words
        filtered_words = [word for word in words if word not in self.stop_words]
        
        # Count word frequencies
        word_count = Counter(filtered_words)
        
        # Get top N most frequent words
        top_words = word_count.most_common(top_n)
        
        return top_words, len(filtered_words)
    
    def analyze_textbook(self, filepath):
        """
        Analyze a single textbook file and return its top frequent words
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Clean the text
            words = self.clean_text(content)
            
            # Get top frequent words
            top_words, total_words = self.get_top_frequent_words(words)
            
            # Calculate normalized frequencies
            normalized_freq = {}
            for word, count in top_words:
                normalized_freq[word] = count / total_words if total_words > 0 else 0
            
            return {
                'filepath': filepath,
                'top_words': dict(top_words),
                'normalized_frequencies': normalized_freq,
                'total_words': total_words,
                'top_15_words': [word for word, _ in top_words]
            }
        
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return None
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            return None

    def calculate_similarity(self, analysis1, analysis2):
        """
        Calculate similarity between two textbook analyses
        """
        if not analysis1 or not analysis2:
            return 0
        
        words1 = set(analysis1['top_15_words'])
        words2 = set(analysis2['top_15_words'])
        
        # Find common words
        common_words = words1.intersection(words2)
        
        # Calculate similarity metrics
        common_count = len(common_words)
        jaccard_similarity = common_count / len(words1.union(words2)) if words1.union(words2) else 0
        
        return {
            'common_words': list(common_words),
            'common_count': common_count,
            'jaccard_similarity': jaccard_similarity
        }
    
    def analyze_all_textbooks(self, filepaths):
        """
        Analyze all textbook files
        """
        analyses = {}
        
        print("Analyzing textbooks...")
        print("=" * 50)
        
        for filepath in filepaths:
            analysis = self.analyze_textbook(filepath)
            if analysis:
                analyses[filepath] = analysis
                
                print(f"\nTextbook: {os.path.basename(filepath)}")
                print(f"Total words (after filtering): {analysis['total_words']}")
                print("Top 15 frequent words:")
                for i, (word, count) in enumerate(analysis['top_words'].items(), 1):
                    freq = analysis['normalized_frequencies'][word]
                    print(f"  {i:2}. {word:<15} Count: {count:3} Frequency: {freq:.4f}")
        
        return analyses
    
    def find_similar_pairs(self, analyses):
        """
        Find and rank similar pairs of textbooks
        """
        similarities = []
        
        # Compare all pairs of textbooks
        for (file1, analysis1), (file2, analysis2) in combinations(analyses.items(), 2):
            similarity = self.calculate_similarity(analysis1, analysis2)
            similarities.append({
                'file1': os.path.basename(file1),
                'file2': os.path.basename(file2),
                'similarity': similarity
            })
        
        # Sort by number of common words (descending)
        similarities.sort(key=lambda x: x['similarity']['common_count'], reverse=True)
        
        return similarities
    
    def display_similarity_results(self, similarities):
        """
        Display similarity analysis results
        """
        print("\n" + "=" * 50)
        print("SIMILARITY ANALYSIS RESULTS")
        print("=" * 50)
        
        for i, sim in enumerate(similarities, 1):
            print(f"\n{i}. {sim['file1']} vs {sim['file2']}")
            print(f"   Common words: {sim['similarity']['common_count']}")
            print(f"   Jaccard similarity: {sim['similarity']['jaccard_similarity']:.4f}")
            print(f"   Common words list: {', '.join(sim['similarity']['common_words'])}")
        
        # Identify most similar pair
        if similarities:
            most_similar = similarities[0]
            print(f"\n{'='*20} MOST SIMILAR PAIR {'='*20}")
            print(f"Most similar textbooks: {most_similar['file1']} and {most_similar['file2']}")
            print(f"Common words: {most_similar['similarity']['common_count']}")
            print(f"Jaccard similarity: {most_similar['similarity']['jaccard_similarity']:.4f}")
    
    def run_analysis(self, textbook_files):
        """
        Main method to run the complete analysis
        """

        # Analyze all textbooks
        analyses = self.analyze_all_textbooks(textbook_files)
        
        if len(analyses) < 2:
            print("Need at least 2 textbook files for similarity analysis.")
            return
        
        # Find similar pairs
        similarities = self.find_similar_pairs(analyses)
        
        # Display results
        self.display_similarity_results(similarities)

def main():
    """
    Main function to run the textbook similarity analysis
    """
    analyzer = TextbookSimilarityAnalyzer()
    
    print("Textbook Similarity Analyzer")
    print("=" * 30)
    
    textbook_files = ['mathematics_textbook.txt','physics_textbook.txt', 'chemistry_textbook.txt','advanced_mathematics.txt','biology_textbook.txt']

    # Option 1: Use sample textbooks (default)
    print("Using sample textbook files...")
    analyzer.run_analysis(textbook_files)

if __name__ == "__main__":
    main()