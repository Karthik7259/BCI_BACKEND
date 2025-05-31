import joblib
import numpy as np

# Load the model and scaler
model = joblib.load('trail_eeg (1).pkl')
scaler = joblib.load('eeg_scaler.pkl')

print("="*60)
print("EEG FEATURE ANALYSIS")
print("="*60)

print("\nFeature Importances (Higher = More Important):")
print("-" * 50)
feature_importances = model.feature_importances_
sorted_indices = np.argsort(feature_importances)[::-1]

for rank, idx in enumerate(sorted_indices):
    print(f"Rank {rank+1:2d}: Feature {idx:2d} - Importance: {feature_importances[idx]:.4f}")

print("\nScaler Information:")
print("-" * 50)
print(f"Number of features: {len(scaler.data_min_)}")
print("\nOriginal data ranges (before scaling):")
for i in range(len(scaler.data_min_)):
    print(f"Feature {i:2d}: Min = {scaler.data_min_[i]:.3f}, Max = {scaler.data_max_[i]:.3f}, Range = {scaler.data_max_[i] - scaler.data_min_[i]:.3f}")

print("\nScaling factors:")
for i in range(len(scaler.scale_)):
    print(f"Feature {i:2d}: Scale factor = {scaler.scale_[i]:.6f}")

# Analyze feature patterns
print("\n" + "="*60)
print("FEATURE PATTERN ANALYSIS")
print("="*60)

# Group features by their characteristics
high_importance = [i for i in range(17) if feature_importances[i] > 0.08]
medium_importance = [i for i in range(17) if 0.04 <= feature_importances[i] <= 0.08]
low_importance = [i for i in range(17) if feature_importances[i] < 0.04]

print(f"High importance features (>0.08): {high_importance}")
print(f"Medium importance features (0.04-0.08): {medium_importance}")
print(f"Low importance features (<0.04): {low_importance}")

# Analyze ranges
zero_features = [i for i in range(17) if scaler.data_max_[i] == 0]
high_range_features = [i for i in range(17) if (scaler.data_max_[i] - scaler.data_min_[i]) > 50]
low_range_features = [i for i in range(17) if 0 < (scaler.data_max_[i] - scaler.data_min_[i]) <= 10]

print(f"\nZero-range features (constant): {zero_features}")
print(f"High-range features (>50): {high_range_features}")
print(f"Low-range features (0-10): {low_range_features}")
