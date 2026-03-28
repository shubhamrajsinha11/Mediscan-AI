"""
Disease Prediction Module
Handles ML model predictions with confidence scores
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

class DiseasePredictor:
    def __init__(self):
        self.models = {}
        self.label_encoder = None
        self.symptom_list = None
        self.best_model = None
        self.best_model_name = None
        self.pca = None
        self.use_pca = True
        self.pca_components = 0.95  # Keep 95% of variance
        self.scaler = None
        self.use_scaling = True
        
    def train_models(self, X, y, test_size=0.2, random_state=42, use_pca=True, pca_variance=0.95):
        """Train multiple models and select the best one"""
        # Check if stratification is possible
        # Stratification requires at least 2 samples per class
        from collections import Counter
        class_counts = Counter(y)
        min_class_count = min(class_counts.values())
        
        # Use stratification only if all classes have at least 2 samples
        use_stratify = min_class_count >= 2
        
        if not use_stratify:
            print(f"Warning: Some classes have only 1 sample. Using non-stratified split.")
            print(f"Class distribution: {len(class_counts)} unique classes")
        
        # Create class mapping BEFORE split to ensure all classes are included
        # This keeps class labels consecutive even if some classes drop out of train/test splits
        unique_classes_all = np.unique(y)
        class_mapping = {old_class: new_class for new_class, old_class in enumerate(unique_classes_all)}
        reverse_class_mapping = {new_class: old_class for old_class, new_class in class_mapping.items()}
        
        # Remap y to consecutive integers before split
        y_remapped = np.array([class_mapping[cls] for cls in y])
        
        X_train, X_test, y_train_remapped, y_test_remapped = train_test_split(
            X, y_remapped, test_size=test_size, random_state=random_state, 
            stratify=y_remapped if use_stratify else None
        )
        
        # Apply mean centering and scaling (StandardScaler) for faster convergence
        if self.use_scaling:
            print(f"\nApplying mean centering and scaling...")
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            print(f"Mean centering and scaling applied (faster convergence)")
        
        # Apply PCA for dimensionality reduction and accuracy improvement
        # Use PCA if we have more than 20 features (lowered threshold for better accuracy)
        if use_pca and X_train.shape[1] > 20:
            print(f"\nApplying PCA (keeping {pca_variance*100}% variance)...")
            print(f"Original feature count: {X_train.shape[1]}")
            self.pca = PCA(n_components=pca_variance, random_state=random_state)
            X_train = self.pca.fit_transform(X_train)
            X_test = self.pca.transform(X_test)
            print(f"Reduced feature count: {X_train.shape[1]}")
            print(f"Explained variance: {self.pca.explained_variance_ratio_.sum():.4f}")
        else:
            self.pca = None
            if not use_pca:
                print("PCA disabled.")
            else:
                print(f"PCA skipped (feature count: {X_train.shape[1]} <= 20)")
        
        # Initialize models with optimized parameters for accuracy
        self.models = {
            'LogisticRegression': LogisticRegression(
                max_iter=1000,           # Increased for better accuracy
                C=1.0,                   # Regularization strength
                solver='lbfgs',          # Fast solver for small-medium datasets

                random_state=random_state,
                n_jobs=-1,
                verbose=0,
                tol=1e-4                 # Tighter tolerance for better accuracy
            ),
            'DecisionTree': DecisionTreeClassifier(
                max_depth=20,            # Increased depth for better accuracy
                min_samples_split=5,     # Reduced for better accuracy
                min_samples_leaf=2,      # Reduced for better accuracy
                max_features='sqrt',      # Use sqrt for faster training
                random_state=random_state
            ),
            'RandomForest': RandomForestClassifier(
                n_estimators=100,        # Increased for better accuracy
                max_depth=20,            # Increased depth
                min_samples_split=5,      # Reduced for better accuracy
                min_samples_leaf=2,       # Reduced for better accuracy
                max_features='sqrt',      # Use sqrt for faster training
                random_state=random_state,
                n_jobs=-1,
                verbose=0,
                warm_start=False
            )
        }
        
        # Train all models
        results = {}
        for name, model in self.models.items():
            print(f"Training {name}...")
            try:
                # Use remapped labels for training
                model.fit(X_train, y_train_remapped)
                
                # Evaluate
                y_pred_remapped = model.predict(X_test)
                # Convert predictions back to original class labels for accuracy calculation
                # But we need to compare with original y_test, so convert y_test_remapped back first
                y_test_original = np.array([reverse_class_mapping[pred] for pred in y_test_remapped])
                y_pred = np.array([reverse_class_mapping[pred] for pred in y_pred_remapped])
                accuracy = accuracy_score(y_test_original, y_pred)
                results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'class_mapping': reverse_class_mapping  # Store for prediction time
                }
                print(f"{name} Accuracy: {accuracy:.4f}")
            except Exception as e:
                print(f"Error training {name}: {e}")
                # Skip this model if it fails
                continue
        
        # Select best model
        if not results:
            raise ValueError("No models were successfully trained!")
            
        best_name = max(results, key=lambda x: results[x]['accuracy'])
        self.best_model = results[best_name]['model']
        self.best_model_name = best_name
        
        # Store class mapping if it exists
        if 'class_mapping' in results[best_name]:
            self.class_mapping = results[best_name]['class_mapping']
        else:
            self.class_mapping = None
            
        print(f"\nBest Model: {best_name} with accuracy {results[best_name]['accuracy']:.4f}")
        
        return results
    
    def predict(self, symptoms_vector, top_k=3):
        """Predict disease with confidence scores"""
        if self.best_model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Apply scaling if it was used during training
        if self.scaler is not None:
            symptoms_vector = self.scaler.transform(symptoms_vector.reshape(1, -1))
        else:
            symptoms_vector = symptoms_vector.reshape(1, -1)
        
        # Apply PCA transformation if it was used during training
        if self.pca is not None:
            symptoms_vector = self.pca.transform(symptoms_vector)
        
        # Get probabilities
        probabilities = self.best_model.predict_proba(symptoms_vector)[0]
        
        # Get top k predictions
        top_indices = np.argsort(probabilities)[-top_k:][::-1]
        
        # Check if we have class mapping (for XGBoost/LightGBM compatibility)
        class_mapping = getattr(self, 'class_mapping', None)
        
        predictions = []
        for idx in top_indices:
            # If class mapping exists, map back to original class
            if class_mapping:
                disease_encoded = class_mapping.get(idx, idx)
            else:
                disease_encoded = idx
                
            if self.label_encoder:
                disease_name = self.label_encoder.inverse_transform([disease_encoded])[0]
            else:
                disease_name = f"Disease_{disease_encoded}"
            
            confidence = probabilities[idx]
            predictions.append({
                'disease': disease_name,
                'confidence': float(confidence),
                'probability_percent': float(confidence * 100)
            })
        
        return predictions
    
    def calculate_risk_score(self, symptoms_vector, age=None, bmi=None, temperature=None):
        """Calculate multi-factor risk score"""
        base_risk = np.sum(symptoms_vector) / len(symptoms_vector) if len(symptoms_vector) > 0 else 0
        
        risk_factors = []
        
        # Age factor
        if age:
            if age < 18 or age > 65:
                risk_factors.append(0.1)
        
        # BMI factor
        if bmi:
            if bmi < 18.5 or bmi > 30:
                risk_factors.append(0.15)
        
        # Temperature factor
        if temperature:
            if temperature > 38.0:  # Fever
                risk_factors.append(0.2)
            elif temperature < 36.0:  # Hypothermia
                risk_factors.append(0.15)
        
        additional_risk = sum(risk_factors)
        total_risk = min(base_risk + additional_risk, 1.0)
        
        return {
            'base_risk': float(base_risk),
            'additional_risk': float(additional_risk),
            'total_risk': float(total_risk),
            'risk_level': 'High' if total_risk > 0.7 else 'Medium' if total_risk > 0.4 else 'Low'
        }
    
    def save_model(self, filepath='models/best_model.pkl'):
        """Save the best model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.best_model,
                'model_name': self.best_model_name,
                'label_encoder': self.label_encoder,
                'symptom_list': self.symptom_list,
                'pca': self.pca,
                'scaler': self.scaler,
                'class_mapping': getattr(self, 'class_mapping', None)
            }, f)
    
    def load_model(self, filepath='models/best_model.pkl'):
        """Load a saved model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.best_model = data['model']
            self.best_model_name = data['model_name']
            self.label_encoder = data.get('label_encoder')
            self.symptom_list = data.get('symptom_list')
            self.pca = data.get('pca')  # Load PCA if available
            self.scaler = data.get('scaler')  # Load scaler if available
            self.class_mapping = data.get('class_mapping')  # Load class mapping if available

