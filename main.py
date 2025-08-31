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