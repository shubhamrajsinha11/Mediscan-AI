"""
Model Training Script
Trains ML models for disease prediction
"""

import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_classif

from utils.preprocessing import (
    load_datasets,
    preprocess_disease_symptoms,
    preprocess_symptom_predict,
    preprocess_combined_dataset,
    save_preprocessing_artifacts
)
from utils.prediction import DiseasePredictor


def reduce_features(X, y, max_features=200):
    """Select top features using mutual information."""
    if max_features is None or X.shape[1] <= max_features:
        print(f"   Feature selection skipped (features: {X.shape[1]})")
        return X, None

    print(f"   Selecting top {max_features} features from {X.shape[1]} using mutual information...")
    selector = SelectKBest(mutual_info_classif, k=max_features)
    X_reduced = selector.fit_transform(X, y)
    print(f"   Features reduced: {X.shape[1]} → {X_reduced.shape[1]}")
    return X_reduced, selector


def main():
    print("=" * 60)
    print("Healthcare AI - Model Training")
    print("=" * 60)

    # ── 1. Load datasets ───────────────────────────────────────────────
    print("\n1. Loading datasets...")
    datasets = load_datasets()

    X = y = le = symptom_list = None

    # Try combining Testing.csv + augmented dataset first
    if (
        'testing' in datasets and datasets['testing'] is not None and
        'disease_symptoms' in datasets and datasets['disease_symptoms'] is not None
    ):
        print("   Combining Testing.csv with Final_Augmented_dataset_Diseases_and_Symptoms.csv")
        try:
            X, y, le, symptom_list = preprocess_combined_dataset(
                datasets['testing'], datasets['disease_symptoms'], max_samples=None
            )
        except Exception as e:
            print(f"   Error combining datasets: {e}")
            X, y, le, symptom_list = None, None, None, None

    # Fall back to individual datasets if combine failed
    if X is None or len(X) == 0:
        dataset_priority = [
            ('testing',          'Testing.csv (core)',          preprocess_symptom_predict),
            ('disease_symptoms', 'Final_Augmented_dataset.csv', preprocess_disease_symptoms),
            ('symptom_predict',  'symbipredict_2022.csv',       preprocess_symptom_predict),
        ]
        for key, label, preprocess_fn in dataset_priority:
            if key not in datasets or datasets[key] is None:
                continue
            try:
                print(f"   Using {label}")
                X_tmp, y_tmp, le_tmp, cols_tmp = preprocess_fn(datasets[key], max_samples=None)
                if X_tmp is None or len(X_tmp) == 0:
                    continue
                X, y, le, symptom_list = X_tmp, y_tmp, le_tmp, cols_tmp
                break
            except Exception as e:
                print(f"   Error preprocessing {label}: {e}")

    if X is None or len(X) == 0:
        print("\nERROR: No valid dataset found or preprocessing failed!")
        print("Please check that:")
        print("  1. CSV files are in the 'data/' folder")
        print("  2. CSV files are not corrupted")
        print("  3. CSV files have the expected format")
        return

    print(f"   Dataset shape:      {X.shape}")
    print(f"   Number of diseases: {len(np.unique(y))}")
    print(f"   Number of symptoms: {len(symptom_list)}")

    # ── 2. Feature selection ───────────────────────────────────────────
    print("\n2. Applying feature selection...")
    max_features = min(int(X.shape[1] * 0.8), 200) if X.shape[1] > 50 else None
    X_reduced, selector = reduce_features(X, y, max_features=max_features)

    # Update symptom list to match selected features
    if selector is not None and symptom_list is not None:
        selected_indices = selector.get_support(indices=True)
        symptom_list = [symptom_list[i] for i in selected_indices]
        print(f"   Updated symptom list: {len(symptom_list)} symptoms")

    # ── 3. Train models ────────────────────────────────────────────────
    print("\n3. Training models...")
    predictor = DiseasePredictor()
    predictor.label_encoder = le
    predictor.symptom_list  = symptom_list

    predictor.train_models(X_reduced, y, use_pca=True, pca_variance=0.95)

    # ── 4. Save model ──────────────────────────────────────────────────
    print("\n4. Saving model...")
    predictor.save_model('models/best_model.pkl')
    save_preprocessing_artifacts(le, symptom_list, 'models')

    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)
    print(f"\nBest model : {predictor.best_model_name}")
    print(f"Saved to   : models/best_model.pkl")
    print(f"Encoder    : models/label_encoder.pkl")
    print(f"Symptoms   : models/symptom_list.pkl")
    print("\nYou can now run:  streamlit run app.py")


if __name__ == "__main__":
    main()


