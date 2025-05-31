#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick EEG Emotion Predictor
===========================

Simple script to predict emotions from your alpha, beta, theta EEG data.
Just paste your JSON data and get instant emotion predictions!
"""

import json
from eeg_converter import process_json_eeg_data

def quick_predict():
    """Quick emotion prediction from your EEG data"""
      # Your EEG data (real-time data from 2025-05-31)
    your_eeg_data = [
        {
            "alpha": 0.3829952605610029,
            "beta": 0.3278990489077491,
            "theta": 0.28910569053124796,
            "timestamp": "2025-05-31T11:03:37.450414"
        },
        {
            "alpha": 0.3832901360439825,
            "beta": 0.3251087128169748,
            "theta": 0.2916011511390427,
            "timestamp": "2025-05-31T11:03:37.509961"
        },
        {
            "alpha": 0.3837218405766482,
            "beta": 0.3221840013295427,
            "theta": 0.2940941580938092,
            "timestamp": "2025-05-31T11:03:37.509961"
        },
        {
            "alpha": 0.3842788892920541,
            "beta": 0.3191195095658467,
            "theta": 0.29660160114209905,
            "timestamp": "2025-05-31T11:03:37.566273"
        },
        {
            "alpha": 0.38497876721643043,
            "beta": 0.31592745623609036,
            "theta": 0.29909377654747915,
            "timestamp": "2025-05-31T11:03:37.623412"
        },
        {
            "alpha": 0.3857994496213299,
            "beta": 0.3126133628831309,
            "theta": 0.3015871874955391,
            "timestamp": "2025-05-31T11:03:37.630123"
        },
        {
            "alpha": 0.38673139067483014,
            "beta": 0.3091745569392213,
            "theta": 0.3040940523859487,
            "timestamp": "2025-05-31T11:03:37.687385"
        },
        {
            "alpha": 0.3877840598217534,
            "beta": 0.3056196260600903,
            "theta": 0.3065963141181562,
            "timestamp": "2025-05-31T11:03:37.747432"
        },
        {
            "alpha": 0.3889478529477842,
            "beta": 0.30195610149985175,
            "theta": 0.3090960455523639,
            "timestamp": "2025-05-31T11:03:37.810166"
        },
        {
            "alpha": 0.3902378705549261,
            "beta": 0.29820083124632074,
            "theta": 0.3115612981987532,
            "timestamp": "2025-05-31T11:03:37.810166"
        }
    ]
    
    print("🧠 EEG EMOTION PREDICTION")
    print("=" * 40)
    
    # Process your data
    results = process_json_eeg_data(your_eeg_data)
    
    # Display results in a clean format
    for i, result in enumerate(results, 1):
        input_data = result['input']
        emotion = result['predicted_emotion']
        probs = result['probabilities']
        
        print(f"\n📊 Sample {i}:")
        print(f"   Alpha: {input_data['alpha']:.2f} | Beta: {input_data['beta']:.2f} | Theta: {input_data['theta']:.2f}")
        print(f"   🎯 Emotion: {emotion.upper()}")
        print(f"   📈 Confidence: {max(probs.values()):.1%}")
        
        # Show interpretation
        if emotion == 'focus':
            print("   💡 Person appears to be concentrated/attentive")
        elif emotion == 'relax':
            print("   😌 Person appears to be calm/relaxed")  
        elif emotion == 'fatigue':
            print("   😴 Person appears to be tired/drowsy")
    
    return results

def analyze_patterns(results):
    """Analyze patterns in the EEG data"""
    
    print("\n" + "=" * 40)
    print("📈 PATTERN ANALYSIS")
    print("=" * 40)
    
    emotions = [r['predicted_emotion'] for r in results]
    
    # Count emotions
    emotion_counts = {}
    for emotion in emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    print(f"📊 Emotion Distribution:")
    for emotion, count in emotion_counts.items():
        percentage = (count / len(results)) * 100
        print(f"   {emotion}: {count}/{len(results)} samples ({percentage:.1f}%)")
    
    # Average confidence
    avg_confidence = sum(max(r['probabilities'].values()) for r in results) / len(results)
    print(f"\n🎯 Average Confidence: {avg_confidence:.1%}")
    
    # Trend analysis
    if len(results) > 1:
        first_emotion = results[0]['predicted_emotion']
        last_emotion = results[-1]['predicted_emotion']
        
        if first_emotion != last_emotion:
            print(f"📉 Trend: {first_emotion} → {last_emotion}")
        else:
            print(f"📊 Stable: Consistent {first_emotion} state")

if __name__ == "__main__":
    # Run the prediction
    results = quick_predict()
    
    # Analyze patterns
    analyze_patterns(results)
    
    print("\n" + "=" * 40)
    print("💡 HOW TO USE WITH YOUR DATA:")
    print("=" * 40)
    print("""
    1. Replace 'your_eeg_data' with your actual JSON data
    2. Keep the same format: timestamp, alpha, beta, theta
    3. Run this script to get instant emotion predictions!
    
    🔍 Understanding the results:
    - Focus: High beta, moderate alpha, low theta
    - Relax: High alpha, moderate beta, low theta  
    - Fatigue: High theta, low alpha/beta
    """)
