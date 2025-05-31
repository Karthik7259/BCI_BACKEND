#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EEG Feature Template for Emotion Classification
===============================================

This template shows you exactly what 17 EEG features your model needs.
Use this as a guide to extract the correct features from your EEG device.
"""

import joblib
import numpy as np

def create_eeg_feature_template():
    """
    Template for the 17 EEG features your model expects.
    Replace the example values with your actual EEG data.
    """
    
    # FEATURE TEMPLATE WITH EXPECTED RANGES
    eeg_features = {
        # RAW EEG AMPLITUDES (microvolts) - Features 0-3
        'feature_0_raw_eeg_1': 25.5,      # Range: 0-58.4 μV
        'feature_1_raw_eeg_2': 30.2,      # Range: 0-60.8 μV  
        'feature_2_raw_eeg_3': 45.1,      # Range: 0-62.2 μV (HIGH IMPORTANCE)
        'feature_3_raw_eeg_4': 60.8,      # Range: 0-94.3 μV
        
        # CONSTANT FEATURES (always 0)
        'feature_4_constant': 0.0,        # Always 0 (not used by model)
        
        # NORMALIZED RATIOS/INDICES - Features 5-7
        'feature_5_norm_ratio_1': 0.45,   # Range: 0.02-0.80 (HIGH IMPORTANCE)
        'feature_6_norm_ratio_2': 0.62,   # Range: 0.17-0.93
        'feature_7_norm_ratio_3': 0.38,   # Range: 0.03-0.67
        
        # CONSTANT FEATURE
        'feature_8_constant': 0.0,        # Always 0 (not used by model)
        
        # FREQUENCY BAND POWERS & RATIOS - Features 9-16
        'feature_9_band_power_1': 1.2,    # Range: 0.05-2.47
        'feature_10_power_index': 8.5,    # Range: 0.41-19.73
        'feature_11_freq_power': 15.3,    # Range: 0.18-28.88 (VERY HIGH IMPORTANCE)
        'feature_12_main_indicator': 1.8, # Range: -0.66-2.47 (HIGHEST IMPORTANCE)
        'feature_13_freq_analysis': 12.1, # Range: 0.31-19.11
        'feature_14_band_ratio': 6.7,     # Range: 0.04-12.42
        'feature_15_stat_measure': 10.2,  # Range: 0.41-19.73
        'feature_16_spectral': 2.1,       # Range: 0.03-4.70 (HIGH IMPORTANCE)
    }
    
    return list(eeg_features.values())

def typical_eeg_feature_mapping():
    """
    What these features likely represent in typical EEG analysis
    """
    
    feature_meanings = {
        'Features 0-3': 'Raw EEG electrode readings (Fp1, Fp2, C3, C4, etc.)',
        'Features 5-7': 'Alpha/Beta/Theta power ratios (relaxation vs focus indicators)', 
        'Feature 9': 'Theta/Alpha ratio (fatigue indicator)',
        'Features 10,13,15': 'Frequency band power measures',
        'Feature 11': 'Primary frequency band power (critical for emotion detection)',
        'Feature 12': 'Main emotional state indicator (most important feature)',
        'Feature 14': 'Beta/Alpha ratio (attention/focus measure)',
        'Feature 16': 'Spectral entropy or complexity measure'
    }
    
    return feature_meanings

def predict_emotion_from_eeg(eeg_data):
    """
    Predict emotion from your EEG data
    
    Args:
        eeg_data: List or array of 17 EEG features
    
    Returns:
        Predicted emotion and probabilities
    """
    
    # Load model and scaler
    model = joblib.load('trail_eeg (1).pkl')
    scaler = joblib.load('eeg_scaler.pkl')
    
    # Ensure correct format
    eeg_array = np.array(eeg_data).reshape(1, -1)
    
    if eeg_array.shape[1] != 17:
        raise ValueError(f"Expected 17 features, got {eeg_array.shape[1]}")
    
    # Scale the data
    scaled_data = scaler.transform(eeg_array)
    
    # Predict
    emotion = model.predict(scaled_data)[0]
    probabilities = model.predict_proba(scaled_data)[0]
    
    return emotion, dict(zip(model.classes_, probabilities))

# EXAMPLE USAGE
if __name__ == "__main__":
    print("="*60)
    print("EEG FEATURE TEMPLATE FOR EMOTION CLASSIFICATION")
    print("="*60)
    
    # Get template features
    template_features = create_eeg_feature_template()
    
    print("\n📋 TEMPLATE EEG FEATURES (Replace with your data):")
    print("-" * 50)
    for i, value in enumerate(template_features):
        if i in [4, 8]:  # Constant features
            print(f"Feature {i:2d}: {value:8.3f} (CONSTANT - always 0)")
        elif i in [2, 5, 11, 12, 16]:  # High importance
            print(f"Feature {i:2d}: {value:8.3f} ⭐ HIGH IMPORTANCE")
        else:
            print(f"Feature {i:2d}: {value:8.3f}")
    
    print("\n🧠 FEATURE MEANINGS:")
    print("-" * 50)
    meanings = typical_eeg_feature_mapping()
    for feature_group, meaning in meanings.items():
        print(f"{feature_group}: {meaning}")
    
    print("\n🔮 SAMPLE PREDICTION:")
    print("-" * 50)
    try:
        emotion, probs = predict_emotion_from_eeg(template_features)
        print(f"Predicted Emotion: {emotion}")
        print("Probabilities:")
        for emotion_class, prob in probs.items():
            print(f"  {emotion_class}: {prob:.3f} ({prob*100:.1f}%)")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n💡 HOW TO USE WITH YOUR EEG DEVICE:")
    print("-" * 50)
    print("""
    1. Extract these 17 features from your EEG signals:
       - Raw amplitudes from 4 channels
       - Alpha, Beta, Theta band powers  
       - Frequency ratios and spectral measures
       
    2. Replace template values with your actual data
    
    3. Call predict_emotion_from_eeg(your_features)
    
    4. Get emotion prediction: 'focus', 'relax', or 'fatigue'
    
    📚 Key tip: Features 11, 12, and 16 are most important!
    """)
