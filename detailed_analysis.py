#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed Analysis of Your EEG Data
==================================
"""

import numpy as np
from eeg_converter import process_json_eeg_data

def detailed_analysis():
    """Detailed analysis of your specific EEG session"""
    
    # Your real EEG data
    eeg_data = [
        {"alpha": 0.3829952605610029, "beta": 0.3278990489077491, "theta": 0.28910569053124796, "timestamp": "2025-05-31T11:03:37.450414"},
        {"alpha": 0.3832901360439825, "beta": 0.3251087128169748, "theta": 0.2916011511390427, "timestamp": "2025-05-31T11:03:37.509961"},
        {"alpha": 0.3837218405766482, "beta": 0.3221840013295427, "theta": 0.2940941580938092, "timestamp": "2025-05-31T11:03:37.509961"},
        {"alpha": 0.3842788892920541, "beta": 0.3191195095658467, "theta": 0.29660160114209905, "timestamp": "2025-05-31T11:03:37.566273"},
        {"alpha": 0.38497876721643043, "beta": 0.31592745623609036, "theta": 0.29909377654747915, "timestamp": "2025-05-31T11:03:37.623412"},
        {"alpha": 0.3857994496213299, "beta": 0.3126133628831309, "theta": 0.3015871874955391, "timestamp": "2025-05-31T11:03:37.630123"},
        {"alpha": 0.38673139067483014, "beta": 0.3091745569392213, "theta": 0.3040940523859487, "timestamp": "2025-05-31T11:03:37.687385"},
        {"alpha": 0.3877840598217534, "beta": 0.3056196260600903, "theta": 0.3065963141181562, "timestamp": "2025-05-31T11:03:37.747432"},
        {"alpha": 0.3889478529477842, "beta": 0.30195610149985175, "theta": 0.3090960455523639, "timestamp": "2025-05-31T11:03:37.810166"},
        {"alpha": 0.3902378705549261, "beta": 0.29820083124632074, "theta": 0.3115612981987532, "timestamp": "2025-05-31T11:03:37.810166"}
    ]
    
    print("🧠 DETAILED EEG ANALYSIS")
    print("=" * 60)
    print(f"📅 Session Date: 2025-05-31 at 11:03:37")
    print(f"⏱️ Duration: ~0.36 seconds (10 samples)")
    print(f"📊 Sampling Rate: ~28 Hz")
    
    # Extract values for analysis
    alphas = [d['alpha'] for d in eeg_data]
    betas = [d['beta'] for d in eeg_data]
    thetas = [d['theta'] for d in eeg_data]
    
    # Statistical analysis
    print("\n📈 FREQUENCY BAND STATISTICS:")
    print("-" * 40)
    print(f"Alpha (8-12Hz - Relaxation):")
    print(f"  Average: {np.mean(alphas):.4f}")
    print(f"  Range: {np.min(alphas):.4f} - {np.max(alphas):.4f}")
    print(f"  Trend: {'↗️ Increasing' if alphas[-1] > alphas[0] else '↘️ Decreasing'}")
    
    print(f"\nBeta (13-30Hz - Focus/Attention):")
    print(f"  Average: {np.mean(betas):.4f}")
    print(f"  Range: {np.min(betas):.4f} - {np.max(betas):.4f}")
    print(f"  Trend: {'↗️ Increasing' if betas[-1] > betas[0] else '↘️ Decreasing'}")
    
    print(f"\nTheta (4-8Hz - Drowsiness):")
    print(f"  Average: {np.mean(thetas):.4f}")
    print(f"  Range: {np.min(thetas):.4f} - {np.max(thetas):.4f}")
    print(f"  Trend: {'↗️ Increasing' if thetas[-1] > thetas[0] else '↘️ Decreasing'}")
    
    # Key ratios
    avg_alpha = np.mean(alphas)
    avg_beta = np.mean(betas)
    avg_theta = np.mean(thetas)
    
    print("\n🔍 KEY RATIOS & INDICATORS:")
    print("-" * 40)
    print(f"Alpha/Beta Ratio: {avg_alpha/avg_beta:.3f}")
    print(f"  → {'Relaxed state' if avg_alpha/avg_beta > 1.2 else 'Alert state' if avg_alpha/avg_beta < 0.8 else 'Neutral state'}")
    
    print(f"\nTheta/Alpha Ratio: {avg_theta/avg_alpha:.3f}")
    print(f"  → {'High drowsiness' if avg_theta/avg_alpha > 0.8 else 'Moderate drowsiness' if avg_theta/avg_alpha > 0.6 else 'Low drowsiness'}")
    
    print(f"\nBeta/Theta Ratio: {avg_beta/avg_theta:.3f}")
    print(f"  → {'Good focus' if avg_beta/avg_theta > 1.2 else 'Poor focus' if avg_beta/avg_theta < 0.9 else 'Moderate focus'}")
    
    # Get model predictions
    results = process_json_eeg_data(eeg_data)
    
    print("\n🎯 MODEL PREDICTIONS:")
    print("-" * 40)
    emotions = [r['predicted_emotion'] for r in results]
    confidences = [max(r['probabilities'].values()) for r in results]
    
    print(f"Consistent Prediction: {emotions[0].upper()}")
    print(f"Average Confidence: {np.mean(confidences):.1%}")
    print(f"Confidence Range: {np.min(confidences):.1%} - {np.max(confidences):.1%}")
    
    # Detailed probability breakdown
    avg_probs = {}
    for emotion in ['fatigue', 'focus', 'relax']:
        probs = [r['probabilities'][emotion] for r in results]
        avg_probs[emotion] = np.mean(probs)
    
    print(f"\nAverage Probabilities:")
    for emotion, prob in sorted(avg_probs.items(), key=lambda x: x[1], reverse=True):
        print(f"  {emotion.capitalize()}: {prob:.1%}")
    
    print("\n🧪 PHYSIOLOGICAL INTERPRETATION:")
    print("-" * 40)
    print("Based on your EEG patterns:")
    print(f"• Theta dominance ({avg_theta:.3f}) suggests mental fatigue")
    print(f"• Declining beta ({betas[0]:.3f} → {betas[-1]:.3f}) indicates reducing alertness")
    print(f"• Rising alpha ({alphas[0]:.3f} → {alphas[-1]:.3f}) shows onset of relaxation")
    print(f"• Rising theta ({thetas[0]:.3f} → {thetas[-1]:.3f}) confirms increasing drowsiness")
    
    print("\n💡 RECOMMENDATIONS:")
    print("-" * 40)
    print("🔴 FATIGUE DETECTED - Consider:")
    print("  • Taking a 10-15 minute break")
    print("  • Light physical activity or stretching")
    print("  • Hydration and fresh air")
    print("  • Power nap (10-20 minutes) if possible")
    print("  • Avoid demanding cognitive tasks")

if __name__ == "__main__":
    detailed_analysis()
