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