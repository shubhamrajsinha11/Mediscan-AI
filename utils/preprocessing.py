"""
Data Preprocessing Utilities
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def load_datasets():
    """Load all CSV datasets"""
    datasets = {}
    
    # Core disease prediction dataset
    try:
        datasets['testing'] = pd.read_csv('data/Testing.csv')
    except:
        pass
    
    # Load additional disease-symptom dataset (for extended coverage)
    try:
        datasets['disease_symptoms'] = pd.read_csv('data/Final_Augmented_dataset_Diseases_and_Symptoms.csv')
    except:
        pass
    
    # Load health dataset
    try:
        datasets['health'] = pd.read_csv('data/health_dataset.csv')
    except:
        pass
    
    # Load medical data
    try:
        datasets['medical'] = pd.read_csv('data/medical data.csv')
    except:
        pass
    
    # Load community drug reviews for medicine mapping
    try:
        datasets['drug_reviews'] = pd.read_csv('data/drugsComTest_raw.csv')
    except:
        pass
    
    # Load symptom prediction dataset (legacy)
    try:
        datasets['symptom_predict'] = pd.read_csv('data/symbipredict_2022.csv')
    except:
        pass
    
    # Load symptom severity
    try:
        datasets['symptom_severity'] = pd.read_csv('data/Symptom-severity.csv')
    except:
        pass
    
    return datasets

def preprocess_disease_symptoms(df, min_samples_per_class=2, max_samples=None):
    """Preprocess the main disease-symptom dataset"""
    if df is None or df.empty:
        return None, None, None, None
    
    # First column is disease, rest are symptoms
    disease_col = df.columns[0]
    symptom_cols = df.columns[1:]
    
    # Extract features and target
    X = df[symptom_cols].fillna(0).astype(int)
    y = df[disease_col]
    
    # Filter out classes with too few samples
    from collections import Counter
    class_counts = Counter(y)
    valid_classes = {cls for cls, count in class_counts.items() if count >= min_samples_per_class}
    
    if len(valid_classes) < len(class_counts):
        print(f"Filtering out {len(class_counts) - len(valid_classes)} classes with < {min_samples_per_class} samples")
        mask = y.isin(valid_classes)
        X = X[mask]
        y = y[mask]
        print(f"Remaining samples: {len(X)}, Remaining classes: {len(valid_classes)}")
    
    if len(X) == 0:
        return None, None, None, None
    
    # Sample data to reduce size for faster execution (only if max_samples is specified)
    if max_samples is not None and len(X) > max_samples:
        print(f"Sampling {max_samples} samples from {len(X)} for faster execution...")
        # Stratified sampling to maintain class distribution
        from sklearn.model_selection import train_test_split
        X, _, y, _ = train_test_split(
            X, y, train_size=max_samples, 
            stratify=y, random_state=42
        )
        print(f"Using {len(X)} samples for training")
    elif max_samples is None:
        print(f"Using full dataset: {len(X)} samples for maximum accuracy")
    
    # Encode disease labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    return X, y_encoded, le, symptom_cols.tolist()

def preprocess_symptom_predict(df, min_samples_per_class=2, max_samples=None):
    """Preprocess the symptom prediction dataset"""
    if df is None or df.empty:
        return None, None, None, None
    
    # Last column is prognosis (disease)
    feature_cols = df.columns[:-1]
    target_col = df.columns[-1]
    
    X = df[feature_cols].fillna(0).astype(int)
    y = df[target_col]
    
    # Filter out classes with too few samples
    from collections import Counter
    class_counts = Counter(y)
    valid_classes = {cls for cls, count in class_counts.items() if count >= min_samples_per_class}
    
    if len(valid_classes) < len(class_counts):
        print(f"Filtering out {len(class_counts) - len(valid_classes)} classes with < {min_samples_per_class} samples")
        mask = y.isin(valid_classes)
        X = X[mask]
        y = y[mask]
        print(f"Remaining samples: {len(X)}, Remaining classes: {len(valid_classes)}")
    
    if len(X) == 0:
        return None, None, None, None
    
    # Sample data to reduce size for faster execution (only if max_samples is specified)
    if max_samples is not None and len(X) > max_samples:
        print(f"Sampling {max_samples} samples from {len(X)} for faster execution...")
        # Stratified sampling to maintain class distribution
        from sklearn.model_selection import train_test_split
        X, _, y, _ = train_test_split(
            X, y, train_size=max_samples, 
            stratify=y, random_state=42
        )
        print(f"Using {len(X)} samples for training")
    elif max_samples is None:
        print(f"Using full dataset: {len(X)} samples for maximum accuracy")
    
    # Encode disease labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    return X, y_encoded, le, feature_cols.tolist()

def preprocess_combined_dataset(test_df, aug_df, min_samples_per_class=2, max_samples=None):
    """Merge Testing.csv (core) with augmented dataset for richer coverage"""
    if test_df is None or test_df.empty:
        return preprocess_disease_symptoms(aug_df, min_samples_per_class, max_samples)
    if aug_df is None or aug_df.empty:
        return preprocess_symptom_predict(test_df, min_samples_per_class, max_samples)
    
    test_df = test_df.copy()
    aug_df = aug_df.copy()
    
    test_df.columns = [col.strip() for col in test_df.columns]
    aug_df.columns = [col.strip() for col in aug_df.columns]
    
    test_target_col = 'prognosis' if 'prognosis' in test_df.columns else test_df.columns[-1]
    test_symptom_cols = [col for col in test_df.columns if col != test_target_col]
    
    aug_df = aug_df.rename(columns={aug_df.columns[0]: 'prognosis'})
    aug_symptom_cols = [col for col in aug_df.columns if col != 'prognosis']
    
    symptom_union = sorted(list(set(test_symptom_cols) | set(aug_symptom_cols)))
    
    X_test = test_df[test_symptom_cols].fillna(0).astype(int)
    X_test = X_test.reindex(columns=symptom_union, fill_value=0)
    y_test = test_df[test_target_col].astype(str)
    
    X_aug = aug_df[aug_symptom_cols].fillna(0).astype(int)
    X_aug = X_aug.reindex(columns=symptom_union, fill_value=0)
    y_aug = aug_df['prognosis'].astype(str)
    
    X = pd.concat([X_test, X_aug], axis=0, ignore_index=True)
    y = pd.concat([y_test, y_aug], axis=0, ignore_index=True)
    
    from collections import Counter
    class_counts = Counter(y)
    valid_classes = {cls for cls, count in class_counts.items() if count >= min_samples_per_class}
    
    if len(valid_classes) < len(class_counts):
        print(f"Filtering out {len(class_counts) - len(valid_classes)} classes with < {min_samples_per_class} samples")
        valid_mask = y.isin(valid_classes)
        X = X[valid_mask]
        y = y[valid_mask]
        print(f"Remaining samples: {len(X)}, Remaining classes: {len(valid_classes)}")
    
    if len(X) == 0:
        return None, None, None, None
    
    if max_samples is not None and len(X) > max_samples:
        from sklearn.model_selection import train_test_split
        X, _, y, _ = train_test_split(
            X, y, train_size=max_samples,
            stratify=y if len(set(y)) > 1 else None,
            random_state=42
        )
        print(f"Using {len(X)} samples for training")
    elif max_samples is None:
        print(f"Using full combined dataset: {len(X)} samples for maximum accuracy")
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    return X, y_encoded, le, symptom_union

def merge_datasets(datasets):
    """Merge multiple datasets for comprehensive training"""
    all_X = []
    all_y = []
    all_symptoms = []
    
    # Process disease-symptom dataset
    if 'disease_symptoms' in datasets and datasets['disease_symptoms'] is not None:
        X1, y1, le1, symptoms1 = preprocess_disease_symptoms(datasets['disease_symptoms'])
        if X1 is not None:
            all_X.append(X1)
            all_y.append(y1)
            all_symptoms.append(symptoms1)
    
    # Process symptom predict dataset
    if 'symptom_predict' in datasets and datasets['symptom_predict'] is not None:
        X2, y2, le2, symptoms2 = preprocess_symptom_predict(datasets['symptom_predict'])
        if X2 is not None:
            all_X.append(X2)
            all_y.append(y2)
            all_symptoms.append(symptoms2)
    
    if not all_X:
        return None, None, None, None
    
    # For now, use the largest dataset
    # In production, you'd want to properly merge and align features
    max_idx = np.argmax([len(x) for x in all_X])
    
    return all_X[max_idx], all_y[max_idx], all_symptoms[max_idx], None

def get_symptom_severity_mapping():
    """Get symptom severity weights"""
    try:
        severity_df = pd.read_csv('data/Symptom-severity.csv')
        return dict(zip(severity_df['Symptom'], severity_df['weight']))
    except:
        return {}

def calculate_symptom_score(symptoms, severity_map):
    """Calculate weighted symptom score"""
    score = 0
    for symptom in symptoms:
        if symptom in severity_map:
            score += severity_map[symptom]
    return score

def get_medicine_mapping():
    """Extract medicine-disease mapping from medical data"""
    try:
        medical_df = pd.read_csv('data/medical data.csv')
        medicine_map = {}
        
        for _, row in medical_df.iterrows():
            disease = str(row.get('Disease', '')).strip()
            medicine = str(row.get('Medicine', '')).strip()
            
            if disease and medicine and disease != 'nan' and medicine != 'nan':
                if disease not in medicine_map:
                    medicine_map[disease] = []
                if medicine not in medicine_map[disease]:
                    medicine_map[disease].append(medicine)
        
        return medicine_map
    except:
        return {}

def save_preprocessing_artifacts(le, symptom_list, output_dir='models'):
    """Save preprocessing artifacts"""
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    
    with open(f'{output_dir}/symptom_list.pkl', 'wb') as f:
        pickle.dump(symptom_list, f)

def load_preprocessing_artifacts(input_dir='models'):
    """Load preprocessing artifacts"""
    le = None
    symptom_list = None
    
    try:
        with open(f'{input_dir}/label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)
    except:
        pass
    
    try:
        with open(f'{input_dir}/symptom_list.pkl', 'rb') as f:
            symptom_list = pickle.load(f)
    except:
        pass
    
    return le, symptom_list

