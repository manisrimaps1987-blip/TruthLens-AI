"""
Utility Functions for TruthLens AI
Includes sentiment analysis, report generation, and helper functions
"""

import os
import json
import pandas as pd
from datetime import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import warnings

warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """
    Sentiment Analysis using TextBlob and VADER
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def textblob_sentiment(self, text):
        """
        Analyze sentiment using TextBlob
        
        Returns:
            Dictionary with polarity, subjectivity, and sentiment label
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 4),
            'subjectivity': round(subjectivity, 4),
            'method': 'TextBlob'
        }
    
    def vader_sentiment(self, text):
        """
        Analyze sentiment using VADER
        
        Returns:
            Dictionary with compound score and sentiment label
        """
        scores = self.analyzer.polarity_scores(text)
        
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'sentiment': sentiment,
            'positive': round(scores['pos'], 4),
            'negative': round(scores['neg'], 4),
            'neutral': round(scores['neu'], 4),
            'compound': round(compound, 4),
            'method': 'VADER'
        }
    
    def analyze(self, text, method='vader'):
        """
        Analyze sentiment using specified method
        
        Args:
            text: Input text
            method: 'vader' or 'textblob'
        
        Returns:
            Sentiment analysis dictionary
        """
        if method.lower() == 'vader':
            return self.vader_sentiment(text)
        else:
            return self.textblob_sentiment(text)


class PredictionHistory:
    """
    Manage prediction history storage and retrieval
    """
    
    def __init__(self, history_file='history/predictions.csv'):
        self.history_file = history_file
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        self.ensure_history_file_exists()
    
    def ensure_history_file_exists(self):
        """Create history file if it doesn't exist"""
        if not os.path.exists(self.history_file):
            df = pd.DataFrame(columns=[
                'date', 'time', 'article', 'prediction', 'confidence', 
                'sentiment', 'polarity', 'processing_time'
            ])
            df.to_csv(self.history_file, index=False)
    
    def add_prediction(self, article, prediction, confidence, sentiment, polarity, processing_time):
        """Add a new prediction to history"""
        now = datetime.now()
        
        new_record = {
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'article': article[:100],  # Store first 100 chars
            'prediction': prediction,
            'confidence': round(confidence, 4),
            'sentiment': sentiment,
            'polarity': polarity,
            'processing_time': round(processing_time, 4)
        }
        
        df = pd.read_csv(self.history_file)
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_csv(self.history_file, index=False)
    
    def get_history(self):
        """Retrieve full prediction history"""
        if os.path.exists(self.history_file):
            return pd.read_csv(self.history_file)
        return pd.DataFrame()
    
    def get_statistics(self):
        """Get prediction statistics"""
        df = self.get_history()
        
        if df.empty:
            return {}
        
        stats = {
            'total_predictions': len(df),
            'real_count': (df['prediction'] == 'Real').sum(),
            'fake_count': (df['prediction'] == 'Fake').sum(),
            'average_confidence': df['confidence'].mean(),
            'sentiment_distribution': df['sentiment'].value_counts().to_dict()
        }
        
        return stats
    
    def clear_history(self):
        """Clear all prediction history"""
        self.ensure_history_file_exists()
    
    def export_as_json(self, filename='reports/history_export.json'):
        """Export history as JSON"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = self.get_history()
        df.to_json(filename, orient='records', indent=2)
        return filename


class ReportGenerator:
    """
    Generate PDF and CSV reports
    """
    
    @staticmethod
    def generate_pdf_report(article, prediction, confidence, sentiment, filename='reports/prediction_report.pdf'):
        """
        Generate a PDF report of prediction
        
        Args:
            article: Article text
            prediction: Real or Fake
            confidence: Confidence score
            sentiment: Sentiment analysis result
            filename: Output filename
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("TruthLens AI - Prediction Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Prediction Results
        story.append(Paragraph("Prediction Results", styles['Heading2']))
        
        results_data = [
            ['Prediction', prediction],
            ['Confidence Score', f"{confidence*100:.2f}%"],
            ['Classification', 'REAL NEWS' if prediction == 'Real' else 'FAKE NEWS'],
            ['Report Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        results_table = Table(results_data, colWidths=[2*inch, 4*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Sentiment Analysis
        story.append(Paragraph("Sentiment Analysis", styles['Heading2']))
        
        sentiment_data = [
            ['Sentiment', sentiment.get('sentiment', 'N/A')],
            ['Polarity', str(sentiment.get('polarity', 'N/A'))],
            ['Confidence (VADER)', f"{sentiment.get('compound', 0):.4f}"]
        ]
        
        sentiment_table = Table(sentiment_data, colWidths=[2*inch, 4*inch])
        sentiment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(sentiment_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Article Content
        story.append(Paragraph("Article Content", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        article_text = article[:1000] + '...' if len(article) > 1000 else article
        story.append(Paragraph(article_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filename
    
    @staticmethod
    def generate_csv_report(predictions_list, filename='reports/predictions_report.csv'):
        """
        Generate a CSV report of multiple predictions
        
        Args:
            predictions_list: List of prediction dictionaries
            filename: Output filename
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df = pd.DataFrame(predictions_list)
        df.to_csv(filename, index=False)
        return filename


def get_model_info():
    """Get information about trained models"""
    models_dir = 'models'
    
    model_files = {
        'vectorizer': 'vectorizer.pkl',
        'fake_news_model': 'fake_news_model.pkl',
        'logistic_regression': 'logistic_regression_model.pkl',
        'naive_bayes': 'naive_bayes_model.pkl'
    }
    
    available_models = {}
    for name, filename in model_files.items():
        filepath = os.path.join(models_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            available_models[name] = {
                'path': filepath,
                'size': f"{size/1024:.2f} KB",
                'exists': True
            }
    
    return available_models


def format_bytes(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"


def get_system_info():
    """Get system and application information"""
    return {
        'app_name': 'TruthLens AI',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'models': get_model_info()
    }
