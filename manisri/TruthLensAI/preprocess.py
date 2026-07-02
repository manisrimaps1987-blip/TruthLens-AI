"""
Text Preprocessing Module for TruthLens AI
Handles all text cleaning and preprocessing operations
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from bs4 import BeautifulSoup
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')


class TextPreprocessor:
    """
    Comprehensive text preprocessing for NLP tasks
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def remove_html_tags(self, text):
        """Remove HTML tags from text"""
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    
    def remove_urls(self, text):
        """Remove URLs from text"""
        url_pattern = r'https?://\S+|www\.\S+'
        return re.sub(url_pattern, '', text)
    
    def remove_emails(self, text):
        """Remove email addresses from text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.sub(email_pattern, '', text)
    
    def remove_punctuation(self, text):
        """Remove punctuation from text"""
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_numbers(self, text):
        """Remove numbers from text"""
        return re.sub(r'\d+', '', text)
    
    def lowercase_text(self, text):
        """Convert text to lowercase"""
        return text.lower()
    
    def remove_extra_whitespace(self, text):
        """Remove extra whitespace"""
        return ' '.join(text.split())
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list"""
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def stemming(self, tokens):
        """Apply stemming to tokens"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatization(self, tokens):
        """Apply lemmatization to tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess_text(self, text, remove_stopwords=True, use_lemmatization=True):
        """
        Complete preprocessing pipeline
        
        Args:
            text: Input text to preprocess
            remove_stopwords: Whether to remove stopwords
            use_lemmatization: Whether to use lemmatization (True) or stemming (False)
        
        Returns:
            Processed text and preprocessing details
        """
        
        original_text = text
        
        # Step 1: Remove HTML tags
        text = self.remove_html_tags(text)
        
        # Step 2: Remove URLs
        text = self.remove_urls(text)
        
        # Step 3: Remove emails
        text = self.remove_emails(text)
        
        # Step 4: Lowercase
        text = self.lowercase_text(text)
        
        # Step 5: Remove punctuation
        text = self.remove_punctuation(text)
        
        # Step 6: Remove numbers
        text = self.remove_numbers(text)
        
        # Step 7: Remove extra whitespace
        text = self.remove_extra_whitespace(text)
        
        # Step 8: Tokenize
        tokens = self.tokenize(text)
        
        # Step 9: Remove stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Step 10: Apply lemmatization or stemming
        if use_lemmatization:
            tokens = self.lemmatization(tokens)
        else:
            tokens = self.stemming(tokens)
        
        processed_text = ' '.join(tokens)
        
        preprocessing_details = {
            'original_text': original_text,
            'processed_text': processed_text,
            'token_count': len(tokens),
            'unique_tokens': len(set(tokens)),
            'removed_stopwords': remove_stopwords,
            'used_lemmatization': use_lemmatization
        }
        
        return processed_text, preprocessing_details


def preprocess_batch(texts, remove_stopwords=True, use_lemmatization=True):
    """
    Preprocess a batch of texts
    
    Args:
        texts: List of texts to preprocess
        remove_stopwords: Whether to remove stopwords
        use_lemmatization: Whether to use lemmatization
    
    Returns:
        List of processed texts
    """
    preprocessor = TextPreprocessor()
    processed_texts = []
    
    for text in texts:
        processed_text, _ = preprocessor.preprocess_text(
            text, 
            remove_stopwords=remove_stopwords, 
            use_lemmatization=use_lemmatization
        )
        processed_texts.append(processed_text)
    
    return processed_texts


def preprocess_dataframe(df, text_column, remove_stopwords=True, use_lemmatization=True):
    """
    Preprocess text in a DataFrame column
    
    Args:
        df: DataFrame with text data
        text_column: Name of the column containing text
        remove_stopwords: Whether to remove stopwords
        use_lemmatization: Whether to use lemmatization
    
    Returns:
        DataFrame with additional 'processed_text' column
    """
    df_copy = df.copy()
    df_copy['processed_text'] = preprocess_batch(
        df[text_column].astype(str).tolist(),
        remove_stopwords=remove_stopwords,
        use_lemmatization=use_lemmatization
    )
    return df_copy
