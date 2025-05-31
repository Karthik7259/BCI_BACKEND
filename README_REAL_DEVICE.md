# 🧠 BCI Emotion Classification with Real EEG Device

This system now supports **REAL EEG hardware** in addition to simulated data for testing!

## 🚀 Quick Start

### Option 1: Real EEG Device Mode
```bash
# Install real device dependencies (see requirements)
pip install neurosdk

# Launch the system
python start_bci.py
# Choose option 1 for real device
```

### Option 2: Simulated Data Mode (Testing)
```bash
# No additional setup required
python start_bci.py
# Choose option 2 for simulated data
```

## 📋 Real Device Setup Guide

### 1. Hardware Requirements
- **NeuroMD EEG Headband** (CallibriMX, Brainbit, or compatible)
- **Windows/Linux computer** with Bluetooth
- **Proper electrode placement** on scalp

### 2. Software Installation
```bash
# Install NeuroSDK
pip install neurosdk

# Install EmotionalMath library (contact NeuroMD)
# This library handles signal processing and emotion analysis
```

### 3. Device Preparation
1. **Power on** your EEG headband
2. **Pair device** via Bluetooth settings
3. **Clean electrode sites** on your scalp
4. **Apply conductive gel** if required by your device
5. **Position headband** properly:
   - O1, O2: Occipital regions (back of head)
   - T3, T4: Temporal regions (sides of head)

### 4. Connection Process
```bash
# Start the real device API
python bci_api.py

# The system will:
# 1. Scan for EEG devices (25 seconds)
# 2. Connect to your headband
# 3. Check electrode resistance
# 4. Calibrate signal processing (6 seconds)
# 5. Begin real-time streaming
```

## 🔧 File Structure

### Real Device Components
- `bci_api.py` - **Real EEG device API server**
- `start_bci.py` - **System launcher** (choose real/simulated)
- `requirements_real_device.txt` - **Dependencies for real device**

### Core System (Works with both real and simulated data)
- `real_time_monitor.py` - **Real-time emotion monitoring**
- `eeg_converter.py` - **Convert 3-band to 17-feature format**
- `main.py` - **Model analysis and documentation**
- `web_server.py` - **Web interface backend**
- `frontend/` - **React web interface**

### Testing/Simulation
- `test_api_server.py` - **Simulated data for testing**
- `quick_predict.py` - **Quick emotion prediction test**

## 📊 Data Flow

### Real Device Mode:
```
EEG Headband → NeuroSDK → bci_api.py → real_time_monitor.py → Emotion Prediction
                    ↓
              Signal Processing & Calibration
```

### Simulated Mode:
```
test_api_server.py → real_time_monitor.py → Emotion Prediction
       ↓
   Fake EEG Data
```

## 🎯 Emotion Detection

The system detects **3 emotional states**:

### 🎯 Focus
- **High Beta** (13-30 Hz) - Concentration
- **Low Theta** (4-8 Hz) - Alert state
- **Use case**: Study sessions, work tasks

### 😌 Relax  
- **High Alpha** (8-12 Hz) - Calm awareness
- **Moderate Beta** - Relaxed attention
- **Use case**: Meditation, rest periods

### 😴 Fatigue
- **High Theta** (4-8 Hz) - Drowsiness
- **Low Beta** - Reduced alertness
- **Use case**: Break recommendations, alertness monitoring

## 🌐 Web Interface

Access the live visualization at: **http://127.0.0.1:5001**

Features:
- **Real-time emotion display**
- **EEG band power charts**
- **Confidence metrics**
- **Session history**
- **Trend analysis**

## 🔍 Troubleshooting

### Device Not Found
```bash
# Check Bluetooth connection
# Ensure device is in pairing mode
# Verify NeuroSDK installation
```

### Poor Signal Quality
```bash
# Clean electrode sites
# Apply conductive gel
# Reposition headband
# Check resistance readings
```

### Calibration Issues
```bash
# Sit still during calibration (6 seconds)
# Minimize eye movements/blinking
# Ensure good electrode contact
```

### API Connection Failed
```bash
# Check if API server is running on port 5000
# Verify device is connected and streaming
# Check firewall settings
```

## 💡 Tips for Best Results

### Signal Quality
1. **Clean scalp** - Remove oils/lotions
2. **Proper positioning** - Follow device manual
3. **Minimize artifacts** - Avoid jaw clenching, eye movements
4. **Stable connection** - Ensure electrodes maintain contact

### Usage Scenarios
1. **Study monitoring** - Track focus during learning
2. **Meditation feedback** - Monitor relaxation states  
3. **Fatigue detection** - Get break recommendations
4. **Research applications** - Collect emotion data

## 🔄 Switching Between Modes

### To Real Device:
```bash
python start_bci.py  # Choose option 1
# OR directly:
python bci_api.py    # Start device API
python real_time_monitor.py  # Start monitoring
```

### To Simulated:
```bash
python start_bci.py  # Choose option 2  
# OR directly:
python test_api_server.py    # Start simulated API
python real_time_monitor.py  # Start monitoring
```

## 📈 Technical Details

### Signal Processing Pipeline
1. **Raw EEG** → Bipolar montage (T3-O1, T4-O2)
2. **Artifact detection** → Remove blinks, movement
3. **FFT analysis** → Extract frequency bands
4. **Feature extraction** → Alpha, Beta, Theta powers
5. **Emotion classification** → ML model prediction

### Model Features
- **Input**: Alpha, Beta, Theta band powers (3 features)
- **Processing**: Convert to 17-feature format
- **Output**: Focus/Relax/Fatigue with confidence
- **Algorithm**: Random Forest classifier

---

🎉 **You now have a complete BCI system that works with real EEG hardware!**

Need help? Check the troubleshooting section or contact support.
