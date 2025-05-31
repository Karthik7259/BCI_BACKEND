#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EEG Emotion Classification Model Analysis
=========================================

This script analyzes and demonstrates the usage of the trained BCI emotion classification model.
The model predicts emotional states (focus, relax, fatigue) from EEG signals.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_model_and_scaler():
    """Load the trained model and scaler"""
    try:
        model = joblib.load('trail_eeg (1).pkl')
        scaler = joblib.load('eeg_scaler.pkl')
        print("✓ Model and scaler loaded successfully!")
        return model, scaler
    except FileNotFoundError as e:
        print(f"❌ Error loading files: {e}")
        return None, None

def analyze_model(model):
    """Analyze the loaded model"""
    print("\n" + "="*50)
    print("MODEL ANALYSIS")
    print("="*50)
    
    print(f"Model Type: {type(model).__name__}")
    print(f"Algorithm: Random Forest Classifier")
    print(f"Number of Trees: {model.n_estimators}")
    print(f"Random State: {model.random_state}")
    
    print(f"\nTarget Classes: {list(model.classes_)}")
    print(f"Number of Classes: {len(model.classes_)}")
    
    print(f"\nInput Features:")
    print(f"  - Number of features expected: {model.n_features_in_}")
    print(f"  - Feature importance shape: {model.feature_importances_.shape}")
    
    # Show feature importances
    print(f"\nTop 5 Most Important Features:")
    feature_importance = model.feature_importances_
    sorted_indices = np.argsort(feature_importance)[::-1]
    
    for i in range(min(5, len(feature_importance))):
        idx = sorted_indices[i]
        print(f"  Feature {idx}: {feature_importance[idx]:.4f}")

def analyze_scaler(scaler):
    """Analyze the scaler"""
    print("\n" + "="*50)
    print("SCALER ANALYSIS")
    print("="*50)
    
    print(f"Scaler Type: {type(scaler).__name__}")
    print(f"Feature Range: {scaler.feature_range}")
    
    if hasattr(scaler, 'data_min_') and scaler.data_min_ is not None:
        print(f"Number of features scaled: {len(scaler.data_min_)}")
        print(f"Min values per feature: {scaler.data_min_[:5]}..." if len(scaler.data_min_) > 5 else f"Min values: {scaler.data_min_}")
        print(f"Max values per feature: {scaler.data_max_[:5]}..." if len(scaler.data_max_) > 5 else f"Max values: {scaler.data_max_}")

def create_sample_prediction(model, scaler):
    """Create a sample prediction to demonstrate usage"""
    print("\n" + "="*50)
    print("SAMPLE PREDICTION")
    print("="*50)
    
    # Generate random sample EEG data (17 features as expected by the model)
    np.random.seed(42)
    sample_eeg_data = np.random.rand(1, model.n_features_in_) * 100  # Random EEG-like values
    
    print("Sample EEG Input Data (17 features):")
    print(f"Raw features: {sample_eeg_data[0][:5]}... (showing first 5)")
    
    # Scale the data
    scaled_data = scaler.transform(sample_eeg_data)
    print(f"Scaled features: {scaled_data[0][:5]}... (showing first 5)")
    
    # Make prediction
    prediction = model.predict(scaled_data)[0]
    prediction_proba = model.predict_proba(scaled_data)[0]
    
    print(f"\nPredicted Emotion: {prediction}")
    print("Prediction Probabilities:")
    for i, class_name in enumerate(model.classes_):
        print(f"  {class_name}: {prediction_proba[i]:.3f} ({prediction_proba[i]*100:.1f}%)")

def show_usage_example():
    """Show how to use the model with new data"""
    print("\n" + "="*50)
    print("USAGE EXAMPLE")
    print("="*50)
    
    usage_code = '''
# How to use this model with new EEG data:

import joblib
import numpy as np

# 1. Load the model and scaler
model = joblib.load('trail_eeg (1).pkl')
scaler = joblib.load('eeg_scaler.pkl')

# 2. Prepare your EEG data (must have 17 features)
# Your EEG data should be a 2D array: (n_samples, 17_features)
new_eeg_data = np.array([[...]])  # Replace with your 17 EEG features

# 3. Scale the data (important!)
scaled_data = scaler.transform(new_eeg_data)

# 4. Make predictions
emotion_prediction = model.predict(scaled_data)
emotion_probabilities = model.predict_proba(scaled_data)

print("Predicted emotion:", emotion_prediction[0])
print("Probabilities:", dict(zip(model.classes_, emotion_probabilities[0])))
'''
    print(usage_code)
    
    # Add EEG features explanation
    explain_eeg_features()

def explain_eeg_features():
    """Explain what the 17 EEG features represent based on model analysis"""
    print("\n" + "="*60)
    print("17 EEG FEATURES EXPLANATION")
    print("="*60)
    
    print("""
Based on the model analysis, here are the 17 EEG features your model expects:

📊 FEATURE GROUPS BY IMPORTANCE:
================================

🔥 HIGH IMPORTANCE FEATURES (Most Critical):
   Feature 12: Power/Amplitude measure (Range: -0.66 to 2.47) - MOST IMPORTANT
   Feature 11: Frequency band power (Range: 0.18 to 28.88) - 2nd MOST IMPORTANT  
   Feature 16: Spectral feature (Range: 0.03 to 4.70) - 3rd MOST IMPORTANT
   Feature 2:  Raw EEG amplitude (Range: 0 to 62.24)
   Feature 5:  Normalized ratio/index (Range: 0.02 to 0.80)

⚡ MEDIUM IMPORTANCE FEATURES:
   Feature 6:  Normalized metric (Range: 0.17 to 0.93)
   Feature 3:  Raw EEG signal (Range: 0 to 94.29) 
   Feature 7:  Computed ratio (Range: 0.03 to 0.67)
   Feature 14: Power band ratio (Range: 0.04 to 12.42)
   Feature 13: Frequency analysis (Range: 0.31 to 19.11)
   Feature 9:  Band power ratio (Range: 0.05 to 2.47)
   Feature 15: Statistical measure (Range: 0.41 to 19.73)
   Feature 10: Computed index (Range: 0.41 to 19.73)

📉 LOW IMPORTANCE FEATURES:
   Feature 0:  Raw EEG channel (Range: 0 to 58.42)
   Feature 1:  Raw EEG channel (Range: 0 to 60.79)
   Feature 4:  CONSTANT (Always 0) - Not used
   Feature 8:  CONSTANT (Always 0) - Not used

🧠 LIKELY EEG FEATURE TYPES:
============================

Based on typical EEG analysis, your 17 features likely include:

1. RAW EEG SIGNALS (Features 0-3):
   - Raw voltage readings from EEG electrodes
   - Range: 0-94 microvolts (typical EEG amplitudes)

2. FREQUENCY BAND POWERS (Features 5-7, 9):
   - Alpha band (8-12 Hz): Associated with relaxation
   - Beta band (13-30 Hz): Associated with focus/concentration  
   - Theta band (4-8 Hz): Associated with drowsiness/fatigue
   - Gamma band (30+ Hz): Associated with high cognitive load

3. SPECTRAL RATIOS (Features 10-16):
   - Alpha/Beta ratio: Focus vs relaxation indicator
   - Theta/Alpha ratio: Fatigue indicator
   - Band power ratios: Emotional state indicators
   - Spectral entropy: Mental complexity measure

4. STATISTICAL FEATURES:
   - Mean, variance, skewness of EEG signals
   - Power spectral density measures
   - Coherence between channels

💡 FOR YOUR EEG DATA INPUT:
===========================

Your input should be a numpy array/list with exactly 17 values:

example_eeg_input = [
    # Features 0-3: Raw EEG amplitudes (0-94 range)
    25.5, 30.2, 45.1, 60.8,
    
    # Feature 4: Always 0 (not used)
    0.0,
    
    # Features 5-7: Normalized ratios (0-1 range)
    0.45, 0.62, 0.38,
    
    # Feature 8: Always 0 (not used) 
    0.0,
    
    # Features 9-16: Power ratios and spectral measures
    1.2, 8.5, 15.3, 1.8, 12.1, 6.7, 10.2, 2.1
]

🎯 MOST IMPORTANT FOR EMOTION DETECTION:
========================================
Focus on getting accurate values for:
- Feature 12: Primary emotion indicator
- Feature 11: Secondary emotion indicator  
- Feature 16: Tertiary emotion indicator
- Features 2, 5: Supporting indicators

These top 5 features account for ~45% of the model's decision making!
""")

def main():
    """Main function to run the analysis"""
    print("EEG Emotion Classification Model Analysis")
    print("="*50)
    
    # Load model and scaler
    model, scaler = load_model_and_scaler()
    
    if model is None or scaler is None:
        return
    
    # Analyze model
    analyze_model(model)
    
    # Analyze scaler
    analyze_scaler(scaler)
    
    # Create sample prediction
    create_sample_prediction(model, scaler)
    
    # Show usage example
    show_usage_example()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("This is a Random Forest model for EEG-based emotion classification.")
    print("INPUT: 17 EEG features (must be scaled using the provided scaler)")
    print("OUTPUT: One of three emotions - 'focus', 'relax', or 'fatigue'")
    print("USAGE: Scale input → model.predict() → get emotion prediction")

if __name__ == "__main__":
    main()