"""
Prediction Module for TruthLens AI
Handles model predictions and confidence scoring
"""

import os
import joblib
import numpy as np
from preprocess import TextPreprocessor
from utils import SentimentAnalyzer


class NewsPredictor:
    """
    Make predictions on news articles
    """
    
    def __init__(self, model_name='logistic_regression', models_dir='models'):
        """
        Initialize predictor
        
        Args:
            model_name: Name of the model to use
            models_dir: Directory containing models
        """
        self.model_name = model_name
        self.models_dir = models_dir
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        self.load_model()
    
    def load_model(self):
        """Load model and vectorizer from disk"""
        # Load vectorizer
        vectorizer_path = os.path.join(self.models_dir, 'vectorizer.pkl')
        if os.path.exists(vectorizer_path):
            self.vectorizer = joblib.load(vectorizer_path)
        else:
            raise FileNotFoundError(f"Vectorizer not found at {vectorizer_path}")
        
        # Load model
        model_path = os.path.join(self.models_dir, f'{self.model_name}_model.pkl')
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            # Try alternative model names
            alt_path = os.path.join(self.models_dir, 'fake_news_model.pkl')
            if os.path.exists(alt_path):
                self.model = joblib.load(alt_path)
            else:
                raise FileNotFoundError(f"Model not found at {model_path}")
    
    def predict(self, text, return_proba=True):
        """
        Predict if article is real or fake
        
        Args:
            text: Article text
            return_proba: Return probability scores
        
        Returns:
            Dictionary with prediction and confidence
        """
        # Preprocess text
        processed_text, prep_details = self.preprocessor.preprocess_text(text)
        
        # Vectorize
        text_vector = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(text_vector)[0]
        
        # Get confidence
        if return_proba and hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(text_vector)[0]
            confidence = max(proba)
        else:
            confidence = 0.5
        
        # Sentiment analysis
        sentiment_result = self.sentiment_analyzer.analyze(text, method='vader')
        
        # Prepare result
        result = {
            'text': text,
            'processed_text': processed_text,
            'prediction': 'Real' if prediction == 1 else 'Fake',
            'prediction_code': prediction,
            'confidence': round(confidence, 4),
            'confidence_percentage': round(confidence * 100, 2),
            'sentiment': sentiment_result['sentiment'],
            'sentiment_details': sentiment_result,
            'credibility_rating': self._calculate_credibility_rating(
                confidence, sentiment_result
            ),
            'preprocessing_details': prep_details
        }
        
        return result
    
    def _calculate_credibility_rating(self, confidence, sentiment):
        """
        Calculate overall credibility rating
        
        Args:
            confidence: Model confidence score
            sentiment: Sentiment analysis result
        
        Returns:
            Credibility rating (1-5 stars)
        """
        # Base rating from confidence
        rating = confidence * 5
        
        # Adjust for sentiment (neutral is more credible)
        if sentiment['sentiment'] == 'Neutral':
            rating += 0.5
        elif sentiment['sentiment'] in ['Positive', 'Negative']:
            rating -= 0.25
        
        # Cap between 1 and 5
        rating = max(1, min(5, rating))
        
        return round(rating, 1)
    
    def batch_predict(self, texts):
        """
        Predict multiple articles
        
        Args:
            texts: List of article texts
        
        Returns:
            List of prediction dictionaries
        """
        predictions = []
        for text in texts:
            pred = self.predict(text)
            predictions.append(pred)
        
        return predictions
    
    def get_confidence_explanation(self, confidence):
        """Get explanation for confidence level"""
        if confidence >= 0.9:
            return "Very High Confidence - Model is highly certain"
        elif confidence >= 0.7:
            return "High Confidence - Model is quite sure"
        elif confidence >= 0.5:
            return "Moderate Confidence - Model has reasonable certainty"
        else:
            return "Low Confidence - Result should be verified"
    
    def get_prediction_explanation(self, prediction_result):
        """Get detailed explanation for prediction"""
        pred = prediction_result['prediction']
        conf = prediction_result['confidence']
        sentiment = prediction_result['sentiment']
        
        explanation = f"""
        **Prediction:** {pred}
        
        **Confidence:** {conf*100:.2f}%
        {self.get_confidence_explanation(conf)}
        
        **Sentiment:** {sentiment}
        
        **Credibility Rating:** {'⭐' * int(prediction_result['credibility_rating'])}
        
        This article has been analyzed using advanced NLP and Machine Learning techniques.
        The model considers text patterns, language characteristics, and contextual features
        to make this prediction.
        """
        
        return explanation


def available_models():
    """Get list of available models"""
    models_dir = 'models'
    
    model_files = [
        'logistic_regression_model.pkl',
        'naive_bayes_model.pkl',
        'random_forest_model.pkl',
        'svm_model.pkl',
        'fake_news_model.pkl'
    ]
    
    available = []
    for filename in model_files:
        filepath = os.path.join(models_dir, filename)
        if os.path.exists(filepath):
            model_name = filename.replace('_model.pkl', '')
            available.append(model_name)
    
    return available if available else ['logistic_regression']


def get_default_model():
    """Get default model name"""
    available = available_models()
    return available[0] if available else 'logistic_regression'
