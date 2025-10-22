import numpy as np
import pickle
import os
import argparse
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
import torch

def load_training_data(data_file='training_data.json'):
    """
    Load training data from JSON file
    Expected format:
    [
        {
            "text": "resume text...",
            "scores": {
                "sections": 85,
                "keywords": 75,
                "formatting": 90,
                "length": 100,
                "contact_info": 80
            },
            "overall_score": 84.5
        },
        ...
    ]
    """
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Training data file not found: {data_file}")
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    X = []
    y = []
    
    for sample in data:
        scores = sample['scores']
        X.append([
            scores['sections'],
            scores['keywords'],
            scores['formatting'],
            scores['length'],
            scores['contact_info']
        ])
        y.append(sample['overall_score'])
    
    return np.array(X), np.array(y)

def train_classifier(X, y, n_estimators=100, max_depth=10):
    """Train a Random Forest regressor for ATS scoring"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training Random Forest classifier...")
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
        verbose=1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    train_mse = mean_squared_error(y_train, train_preds)
    test_mse = mean_squared_error(y_test, test_preds)
    train_r2 = r2_score(y_train, train_preds)
    test_r2 = r2_score(y_test, test_preds)
    
    print(f"\nTraining Performance:")
    print(f"  MSE: {train_mse:.2f}")
    print(f"  R² Score: {train_r2:.4f}")
    
    print(f"\nTest Performance:")
    print(f"  MSE: {test_mse:.2f}")
    print(f"  R² Score: {test_r2:.4f}")
    
    # Feature importance
    feature_names = ['Sections', 'Keywords', 'Formatting', 'Length', 'Contact Info']
    importances = model.feature_importances_
    
    print(f"\nFeature Importances:")
    for name, importance in zip(feature_names, importances):
        print(f"  {name}: {importance:.4f}")
    
    return model

def save_model(model, output_path='models/ats_classifier.pkl'):
    """Save trained model to disk"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\nModel saved to: {output_path}")

def generate_synthetic_data(num_samples=100):
    """
    Generate synthetic training data for demonstration
    In production, replace this with real labeled data
    """
    print("Generating synthetic training data...")
    np.random.seed(42)
    
    data = []
    
    for _ in range(num_samples):
        # Generate component scores with some correlation
        section_score = np.random.uniform(50, 100)
        keyword_score = np.random.uniform(40, 100)
        formatting_score = np.random.uniform(60, 100)
        length_score = np.random.uniform(50, 100)
        contact_score = np.random.uniform(40, 100)
        
        # Calculate overall score with weighted sum plus some noise
        overall_score = (
            section_score * 0.25 +
            keyword_score * 0.30 +
            formatting_score * 0.20 +
            length_score * 0.15 +
            contact_score * 0.10
        )
        
        # Add some non-linear effects and noise
        overall_score += np.random.normal(0, 3)
        overall_score = max(0, min(100, overall_score))
        
        data.append({
            "text": f"Sample resume {_}",
            "scores": {
                "sections": round(section_score, 1),
                "keywords": round(keyword_score, 1),
                "formatting": round(formatting_score, 1),
                "length": round(length_score, 1),
                "contact_info": round(contact_score, 1)
            },
            "overall_score": round(overall_score, 1)
        })
    
    # Save synthetic data
    with open('training_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Generated {num_samples} synthetic samples")
    return data

def check_gpu():
    """Check GPU availability"""
    if torch.cuda.is_available():
        print(f"✓ GPU Available: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA Version: {torch.version.cuda}")
        print(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB\n")
        return True
    else:
        print("⚠ GPU not available, using CPU\n")
        return False

def main():
    """Main training pipeline"""
    parser = argparse.ArgumentParser(description='Train ATS ML Model')
    parser.add_argument('--data', type=str, default='training_data.json',
                       help='Path to training data JSON file')
    parser.add_argument('--n-estimators', type=int, default=100,
                       help='Number of trees in Random Forest')
    parser.add_argument('--max-depth', type=int, default=10,
                       help='Maximum depth of trees')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Training epochs (for display only with RF)')
    parser.add_argument('--use-gpu', action='store_true',
                       help='Enable GPU acceleration check')
    
    args = parser.parse_args()
    
    print("=== ATS Scorer Model Training ===\n")
    
    # Check GPU
    if args.use_gpu:
        check_gpu()
    
    # Check if training data exists, if not generate synthetic data
    if not os.path.exists(args.data):
        print(f"No training data found at {args.data}")
        print("Generating synthetic data...\n")
        generate_synthetic_data(num_samples=200)
        args.data = 'training_data.json'
    
    # Load training data
    print(f"Loading training data from {args.data}...")
    X, y = load_training_data(args.data)
    print(f"Loaded {len(X)} training samples\n")
    
    # Train model
    model = train_classifier(X, y, n_estimators=args.n_estimators, max_depth=args.max_depth)
    
    # Save model
    save_model(model)
    
    print("\n=== Training Complete ===")
    print("\nNext steps:")
    print("1. The model is saved in models/ats_classifier.pkl")
    print("2. The ML scorer will automatically load and use this model")
    print("3. To improve accuracy, collect more real labeled resume data")
    print("4. Restart the Flask server to use the trained model")

if __name__ == '__main__':
    main()
