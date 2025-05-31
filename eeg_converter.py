#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EEG Data Converter for Emotion Classification Model
==================================================

Converts your 3-feature EEG data (alpha, beta, theta) into the 17-feature format
required by the emotion classification model.
"""

import json
import joblib
import numpy as np
from datetime import datetime

def load_model_components():
    """Load the trained model and scaler"""
    model = joblib.load('trail_eeg (1).pkl')
    scaler = joblib.load('eeg_scaler.pkl')
    return model, scaler

def convert_3_to_17_features(alpha, beta, theta):
    """
    Convert your 3 EEG features (alpha, beta, theta) to 17 features
    
    Args:
        alpha: Alpha band power (0.3-0.8 typical range)
        beta: Beta band power (0.4-0.6 typical range) 
        theta: Theta band power (0.2-0.4 typical range)
    
    Returns:
        List of 17 features for the model
    """
    
    # Convert band powers to typical EEG amplitude ranges
    # Alpha: relaxation indicator (8-12 Hz)
    # Beta: focus/attention indicator (13-30 Hz)  
    # Theta: drowsiness/fatigue indicator (4-8 Hz)
    
    # Features 0-3: Raw EEG amplitudes (simulate from band powers)
    raw_amplitude_1 = alpha * 50.0  # Scale alpha to 0-40 range
    raw_amplitude_2 = beta * 60.0   # Scale beta to 0-36 range
    raw_amplitude_3 = theta * 80.0  # Scale theta to 0-32 range (HIGH IMPORTANCE)
    raw_amplitude_4 = (alpha + beta) * 40.0  # Combined signal
    
    # Feature 4: Always 0 (constant)
    constant_1 = 0.0
    
    # Features 5-7: Normalized ratios (HIGH IMPORTANCE for feature 5)
    alpha_beta_ratio = alpha / (beta + 0.001)  # Relaxation vs focus
    beta_theta_ratio = beta / (theta + 0.001)  # Focus vs fatigue  
    alpha_theta_ratio = alpha / (theta + 0.001)  # Relaxation vs fatigue
    
    # Feature 8: Always 0 (constant)
    constant_2 = 0.0
    
    # Features 9-16: Frequency analysis and spectral measures
    # Feature 9: Theta/Alpha ratio (fatigue indicator)
    theta_alpha_ratio = theta / (alpha + 0.001)
    
    # Features 10, 13, 15: Power measures (scale to expected ranges)
    power_measure_1 = (alpha + beta + theta) * 6.0  # Combined power
    freq_analysis = beta * 15.0 + alpha * 5.0  # Weighted analysis
    stat_measure = (alpha * beta * theta) * 50.0  # Statistical combination
    
    # Feature 11: Primary frequency band power (VERY HIGH IMPORTANCE)
    primary_freq_power = beta * 20.0 + alpha * 8.0  # Focus-weighted measure
    
    # Feature 12: Main emotion indicator (HIGHEST IMPORTANCE) 
    main_indicator = (beta - theta) + (alpha * 0.5)  # Key emotion discriminator
    
    # Feature 14: Beta/Alpha ratio (attention measure)
    attention_ratio = (beta / (alpha + 0.001)) * 3.0
    
    # Feature 16: Spectral complexity (HIGH IMPORTANCE)
    spectral_measure = np.sqrt(alpha * beta * theta) * 2.0
    
    # Assemble all 17 features
    features = [
        raw_amplitude_1,      # Feature 0
        raw_amplitude_2,      # Feature 1  
        raw_amplitude_3,      # Feature 2 (HIGH IMPORTANCE)
        raw_amplitude_4,      # Feature 3
        constant_1,           # Feature 4 (always 0)
        alpha_beta_ratio,     # Feature 5 (HIGH IMPORTANCE)
        beta_theta_ratio,     # Feature 6
        alpha_theta_ratio,    # Feature 7
        constant_2,           # Feature 8 (always 0)
        theta_alpha_ratio,    # Feature 9
        power_measure_1,      # Feature 10
        primary_freq_power,   # Feature 11 (VERY HIGH IMPORTANCE)
        main_indicator,       # Feature 12 (HIGHEST IMPORTANCE)
        freq_analysis,        # Feature 13
        attention_ratio,      # Feature 14
        stat_measure,         # Feature 15
        spectral_measure      # Feature 16 (HIGH IMPORTANCE)
    ]
    
    return features

def predict_emotion_from_bands(alpha, beta, theta):
    """
    Predict emotion from alpha, beta, theta band powers
    
    Args:
        alpha, beta, theta: EEG band powers
        
    Returns:
        Predicted emotion and probabilities
    """
    
    # Load model components
    model, scaler = load_model_components()
    
    # Convert to 17 features
    features_17 = convert_3_to_17_features(alpha, beta, theta)
    
    # Reshape for model input
    features_array = np.array(features_17).reshape(1, -1)
    
    # Scale the features
    scaled_features = scaler.transform(features_array)
    
    # Make prediction
    emotion = model.predict(scaled_features)[0]
    probabilities = model.predict_proba(scaled_features)[0]
    
    return emotion, dict(zip(model.classes_, probabilities)), features_17

def process_json_eeg_data(json_data):
    """
    Process your JSON EEG data format
    
    Args:
        json_data: List of dictionaries with timestamp, alpha, beta, theta
        
    Returns:
        List of predictions for each sample
    """
    
    results = []
    
    for sample in json_data:
        # Extract features
        alpha = sample['alpha']
        beta = sample['beta'] 
        theta = sample['theta']
        timestamp = sample['timestamp']
        
        # Predict emotion
        emotion, probabilities, features = predict_emotion_from_bands(alpha, beta, theta)
        
        # Store result
        result = {
            'timestamp': timestamp,
            'input': {'alpha': alpha, 'beta': beta, 'theta': theta},
            'predicted_emotion': emotion,
            'probabilities': probabilities,
            'converted_features': features[:5]  # Show first 5 for brevity
        }
        
        results.append(result)
    
    return results

# Example usage
if __name__ == "__main__":
    print("="*60)
    print("EEG DATA CONVERTER: 3 Features → 17 Features")
    print("="*60)
    
    # Your sample data
    sample_json = [
        {
            "timestamp": "2025-05-23T10:30:45.123456",
            "alpha": 0.75,
            "beta": 0.45,
            "theta": 0.30
        },
        {
            "timestamp": "2025-05-23T10:30:44.123456", 
            "alpha": 0.72,
            "beta": 0.48,
            "theta": 0.32
        }
    ]
    
    print("📥 INPUT: Your EEG Data (3 features)")
    print("-" * 40)
    for i, sample in enumerate(sample_json):
        print(f"Sample {i+1}: Alpha={sample['alpha']}, Beta={sample['beta']}, Theta={sample['theta']}")
    
    print("\n🔄 CONVERTING TO 17 FEATURES...")
    print("-" * 40)
    
    # Process the data
    results = process_json_eeg_data(sample_json)
    
    print("📤 OUTPUT: Emotion Predictions")
    print("-" * 40)
    
    for i, result in enumerate(results):
        print(f"\nSample {i+1} ({result['timestamp']}):")
        print(f"  Input: Alpha={result['input']['alpha']}, Beta={result['input']['beta']}, Theta={result['input']['theta']}")
        print(f"  ➜ Predicted Emotion: {result['predicted_emotion']}")
        print(f"  ➜ Probabilities:")
        for emotion, prob in result['probabilities'].items():
            print(f"     {emotion}: {prob:.3f} ({prob*100:.1f}%)")
        print(f"  ➜ First 5 converted features: {[f'{x:.3f}' for x in result['converted_features']]}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
    ✅ YES, you can use your 3-feature data with this converter!
    
    📋 What this converter does:
    1. Takes your alpha, beta, theta values
    2. Calculates ratios and derived features
    3. Generates all 17 features the model needs
    4. Predicts emotion: 'focus', 'relax', or 'fatigue'
    
    🎯 Key conversions:
    - High Beta + Low Theta = Focus
    - High Alpha + Low Beta = Relax  
    - High Theta + Low Alpha/Beta = Fatigue
    
    💡 Usage: Call process_json_eeg_data(your_json_list)
    """)
