"""
Model Training Initialization Script
Run this script to train the fake news detection models
"""

import os
import sys
import pandas as pd
import warnings
from train_model import ModelTrainer, create_sample_dataset

warnings.filterwarnings('ignore')


def main():
    """Train and save models"""
    
    print("=" * 70)
    print("TruthLens AI - Model Training Initialization")
    print("=" * 70)
    print()
    
    # Check if models directory exists
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Create or load dataset
    print("📊 Creating training dataset...")
    print("-" * 70)
    
    # Create sample dataset
    print("Generating sample dataset with 1000 articles...")
    df = create_sample_dataset(n_samples=1000)
    
    print(f"✓ Dataset created with {len(df)} samples")
    print(f"  - Real News: {(df['label'] == 1).sum()}")
    print(f"  - Fake News: {(df['label'] == 0).sum()}")
    print()
    
    # Initialize trainer
    print("🤖 Initializing Model Trainer...")
    print("-" * 70)
    trainer = ModelTrainer(vectorizer_type='tfidf', max_features=5000)
    print("✓ Trainer initialized")
    print()
    
    # Prepare data
    print("📈 Preparing and splitting data...")
    print("-" * 70)
    data_info = trainer.prepare_data(
        df['text'].tolist(),
        df['label'].tolist(),
        test_size=0.2
    )
    
    print(f"✓ Data prepared")
    print(f"  - Training samples: {data_info['train_size']}")
    print(f"  - Test samples: {data_info['test_size']}")
    print(f"  - Features: {data_info['feature_count']}")
    print()
    
    # Train models
    print("🔄 Training models...")
    print("-" * 70)
    
    print("\n1. Training Logistic Regression...")
    trainer.train_logistic_regression()
    lr_results = trainer.results['logistic_regression']
    print(f"   ✓ Accuracy: {lr_results['accuracy']:.4f}")
    print(f"   ✓ F1 Score: {lr_results['f1_score']:.4f}")
    
    print("\n2. Training Naive Bayes...")
    trainer.train_naive_bayes()
    nb_results = trainer.results['naive_bayes']
    print(f"   ✓ Accuracy: {nb_results['accuracy']:.4f}")
    print(f"   ✓ F1 Score: {nb_results['f1_score']:.4f}")
    
    print("\n3. Training Random Forest...")
    trainer.train_random_forest()
    rf_results = trainer.results['random_forest']
    print(f"   ✓ Accuracy: {rf_results['accuracy']:.4f}")
    print(f"   ✓ F1 Score: {rf_results['f1_score']:.4f}")
    
    print("\n4. Training Linear SVM...")
    trainer.train_svm()
    svm_results = trainer.results['svm']
    print(f"   ✓ Accuracy: {svm_results['accuracy']:.4f}")
    print(f"   ✓ F1 Score: {svm_results['f1_score']:.4f}")
    
    print()
    
    # Get best model
    print("🏆 Best Model Performance")
    print("-" * 70)
    best = trainer.get_best_model()
    print(f"✓ Best Model: {best['model_name'].upper()}")
    print(f"  - Accuracy: {best['performance']['accuracy']:.4f}")
    print(f"  - Precision: {best['performance']['precision']:.4f}")
    print(f"  - Recall: {best['performance']['recall']:.4f}")
    print(f"  - F1 Score: {best['performance']['f1_score']:.4f}")
    print()
    
    # Save models
    print("💾 Saving models...")
    print("-" * 70)
    saved_paths = trainer.save_models(models_dir)
    
    for model_name, path in saved_paths.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {model_name}: {path} ({size/1024:.2f} KB)")
    
    print()
    print("=" * 70)
    print("✅ Model Training Complete!")
    print("=" * 70)
    print()
    print("Models are ready to use. Run the Streamlit app with:")
    print("  streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
