"""
Machine Learning Model Training Module for TruthLens AI
Trains and evaluates multiple models for fake news detection
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    roc_auc_score
)
import warnings

warnings.filterwarnings('ignore')


class ModelTrainer:
    """
    Train and evaluate multiple fake news detection models
    """
    
    def __init__(self, vectorizer_type='tfidf', max_features=5000):
        """
        Initialize model trainer
        
        Args:
            vectorizer_type: 'tfidf' or 'count'
            max_features: Maximum number of features
        """
        self.vectorizer_type = vectorizer_type
        self.max_features = max_features
        self.vectorizer = None
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def create_vectorizer(self):
        """Create TF-IDF or Count vectorizer"""
        if self.vectorizer_type.lower() == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=5,
                max_df=0.8
            )
        else:
            self.vectorizer = CountVectorizer(
                max_features=self.max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=5,
                max_df=0.8
            )
        
        return self.vectorizer
    
    def prepare_data(self, texts, labels, test_size=0.2, random_state=42):
        """
        Prepare and split data
        
        Args:
            texts: List of text samples
            labels: List of labels (0 for Fake, 1 for Real)
            test_size: Test set size
            random_state: Random seed
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        # Create and fit vectorizer
        self.create_vectorizer()
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        self.X_train = X_train_vec
        self.X_test = X_test_vec
        self.y_train = y_train
        self.y_test = y_test
        
        return {
            'train_size': len(X_train),
            'test_size': len(X_test),
            'feature_count': X_train_vec.shape[1],
            'label_distribution': pd.Series(labels).value_counts().to_dict()
        }
    
    def train_logistic_regression(self):
        """Train Logistic Regression model"""
        model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1,
            solver='lbfgs'
        )
        model.fit(self.X_train, self.y_train)
        self.models['logistic_regression'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_proba = model.predict_proba(self.X_test)
        
        self.results['logistic_regression'] = self._evaluate_model(
            self.y_test, y_pred, y_proba, 'Logistic Regression'
        )
        
        return model
    
    def train_naive_bayes(self):
        """Train Multinomial Naive Bayes model"""
        model = MultinomialNB(alpha=1.0)
        model.fit(self.X_train, self.y_train)
        self.models['naive_bayes'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_proba = model.predict_proba(self.X_test)
        
        self.results['naive_bayes'] = self._evaluate_model(
            self.y_test, y_pred, y_proba, 'Multinomial Naive Bayes'
        )
        
        return model
    
    def train_random_forest(self, n_estimators=100):
        """Train Random Forest model"""
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42,
            n_jobs=-1,
            max_depth=20
        )
        model.fit(self.X_train, self.y_train)
        self.models['random_forest'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_proba = model.predict_proba(self.X_test)
        
        self.results['random_forest'] = self._evaluate_model(
            self.y_test, y_pred, y_proba, 'Random Forest'
        )
        
        return model
    
    def train_svm(self):
        """Train Linear SVM model"""
        model = LinearSVC(max_iter=2000, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['svm'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        
        self.results['svm'] = self._evaluate_model(
            self.y_test, y_pred, None, 'Linear SVM'
        )
        
        return model
    
    def _evaluate_model(self, y_true, y_pred, y_proba, model_name):
        """Evaluate model performance"""
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        cm = confusion_matrix(y_true, y_pred)
        
        results = {
            'model_name': model_name,
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1, 4),
            'confusion_matrix': cm.tolist(),
            'classification_report': classification_report(y_true, y_pred, output_dict=True)
        }
        
        if y_proba is not None:
            try:
                roc_auc = roc_auc_score(y_true, y_proba[:, 1])
                results['roc_auc'] = round(roc_auc, 4)
            except:
                results['roc_auc'] = None
        
        return results
    
    def train_all_models(self):
        """Train all available models"""
        self.train_logistic_regression()
        self.train_naive_bayes()
        self.train_random_forest()
        self.train_svm()
        
        return self.results
    
    def get_best_model(self):
        """Get best performing model"""
        if not self.results:
            return None
        
        best_model = max(self.results.items(), key=lambda x: x[1]['f1_score'])
        return {
            'model_name': best_model[0],
            'performance': best_model[1]
        }
    
    def save_models(self, models_dir='models'):
        """Save trained models to disk"""
        os.makedirs(models_dir, exist_ok=True)
        
        # Save vectorizer
        vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
        joblib.dump(self.vectorizer, vectorizer_path)
        
        # Save models
        saved_paths = {'vectorizer': vectorizer_path}
        for model_name, model in self.models.items():
            filepath = os.path.join(models_dir, f'{model_name}_model.pkl')
            joblib.dump(model, filepath)
            saved_paths[model_name] = filepath
        
        return saved_paths
    
    def load_models(self, models_dir='models'):
        """Load trained models from disk"""
        # Load vectorizer
        vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
        if os.path.exists(vectorizer_path):
            self.vectorizer = joblib.load(vectorizer_path)
        
        # Load models
        model_files = [
            'logistic_regression_model.pkl',
            'naive_bayes_model.pkl',
            'random_forest_model.pkl',
            'svm_model.pkl',
            'fake_news_model.pkl'
        ]
        
        for filename in model_files:
            filepath = os.path.join(models_dir, filename)
            if os.path.exists(filepath):
                model_name = filename.replace('_model.pkl', '')
                self.models[model_name] = joblib.load(filepath)
        
        return self.models


def create_sample_dataset(n_samples=1000):
    """
    Create a sample dataset for training
    
    Returns:
        DataFrame with 'text' and 'label' columns
    """
    sample_real_news = [
        "Scientists discover new treatment for cancer patients",
        "World leaders meet to discuss climate change",
        "Economy grows by 2.5% in latest quarter",
        "New vaccine approved by health authorities",
        "Tech company announces major investment in renewable energy",
        "Study shows benefits of regular exercise",
        "Government releases annual budget report",
        "University launches groundbreaking research program",
        "Stock market reaches historic high",
        "Breakthrough in renewable energy technology"
    ]
    
    sample_fake_news = [
        "Celebrities secretly control world governments",
        "Miracles cure proven to eliminate all diseases",
        "Hidden evidence reveals shocking truth",
        "This one weird trick will change your life",
        "Conspiracy theorists prove earth is flat",
        "Government hides secret alien technology",
        "Billionaire reveals shocking truth",
        "Medical doctors hate this simple cure",
        "Click here to see what celebrities don't want known",
        "Shocking discovery that changes everything"
    ]
    
    # Create balanced dataset
    real_texts = (sample_real_news * (n_samples // 20)) + sample_real_news[:n_samples % 20]
    fake_texts = (sample_fake_news * (n_samples // 20)) + sample_fake_news[:n_samples % 20]
    
    np.random.seed(42)
    real_indices = np.random.permutation(len(real_texts))[:n_samples // 2]
    fake_indices = np.random.permutation(len(fake_texts))[:n_samples // 2]
    
    texts = list(np.array(real_texts)[real_indices]) + list(np.array(fake_texts)[fake_indices])
    labels = [1] * (n_samples // 2) + [0] * (n_samples // 2)
    
    # Shuffle
    shuffle_indices = np.random.permutation(len(texts))
    texts = [texts[i] for i in shuffle_indices]
    labels = [labels[i] for i in shuffle_indices]
    
    return pd.DataFrame({'text': texts, 'label': labels})
