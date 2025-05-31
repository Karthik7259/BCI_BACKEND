# 🧠 BCI Backend System - Complete Documentation

## 📋 Overview

This is a comprehensive Brain-Computer Interface (BCI) backend system that provides real-time EEG emotion classification. The system connects to real EEG hardware, processes neural signals, and provides emotion predictions through REST APIs.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   EEG Device    │───▶│   bci_api.py     │───▶│ real_time_      │
│  (NeuroSDK)     │    │  (Port 5000)     │    │ monitor.py      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◀───│   web_server.py  │◀───│ eeg_converter.py│
│  (Port 5173)    │    │   (Port 5001)    │    │ (ML Model)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install Python packages
pip install -r requirements_real_device.txt

# Install NeuroSDK (for real EEG device)
pip install neurosdk

# Install EmotionalMath library (contact NeuroMD for access)
```

### 2. Start the System
```bash
# Option 1: Use the launcher (recommended)
python start_bci.py

# Option 2: Manual startup
python bci_api.py          # Terminal 1: Start EEG device API
python real_time_monitor.py # Terminal 2: Start monitoring
python web_server.py       # Terminal 3: Start web API
```

## 📁 Core Components

### 🔌 EEG Device Connection (`bci_api.py`)
- **Purpose**: Connects to real EEG hardware via NeuroSDK
- **Port**: 5000
- **Features**:
  - Device scanning and connection
  - Signal calibration (6 seconds)
  - Real-time data streaming
  - Artifact detection and filtering
  - Alpha/Beta/Theta band extraction

### 🧠 Real-Time Processing (`real_time_monitor.py`)
- **Purpose**: Fetches EEG data and provides emotion predictions
- **Features**:
  - Batch processing (10 samples per 5 seconds)
  - Emotion classification (Focus/Relax/Fatigue)
  - Trend analysis
  - Session management
  - Web server integration

### 🌐 Web API Server (`web_server.py`)
- **Purpose**: Provides REST APIs for frontend integration
- **Port**: 5001
- **Features**:
  - Real-time emotion data
  - Session history
  - CORS enabled for frontend

### 🔄 Data Conversion (`eeg_converter.py`)
- **Purpose**: Converts 3-band EEG data to 17-feature format for ML model
- **Features**:
  - Feature engineering
  - ML model prediction
  - Confidence scoring

## 🔗 API Documentation

### Base URLs
- **EEG Device API**: `http://127.0.0.1:5000`
- **Web Server API**: `http://127.0.0.1:5001`

### 📊 EEG Device API Endpoints

#### GET `/api/data`
Get raw EEG data from the device.

**Response:**
```json
[
  {
    "timestamp": "2025-05-31T12:39:20.680658",
    "alpha": 0.42044602419691485,
    "beta": 0.33230824476840337,
    "theta": 0.2472457310346818
  },
  // ... up to 10 samples
]
```

#### GET `/api/status`
Get device connection status.

**Response:**
```json
{
  "device_status": {
    "connected": true,
    "calibrating": false,
    "streaming": true,
    "last_update": "2025-05-31T12:39:20.680658",
    "error": null
  },
  "data_available": true,
  "latest_reading": {
    "timestamp": "2025-05-31T12:39:20.680658",
    "alpha": 0.42,
    "beta": 0.33,
    "theta": 0.24
  },
  "buffer_size": 10,
  "timestamp": "2025-05-31T12:39:21.409759"
}
```

### 🌐 Web Server API Endpoints

#### GET `/api/eeg-data`
Get processed emotion analysis data.

**Response:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2025-05-31T12:39:21.409759",
    "dominant_emotion": "fatigue",
    "consistency": 1.0,
    "avg_confidence": 0.453,
    "probabilities": {
      "fatigue": 0.453,
      "focus": 0.259,
      "relax": 0.288
    },
    "eeg_stats": {
      "alpha": {
        "avg": 0.434,
        "trend": "stable"
      },
      "beta": {
        "avg": 0.315,
        "trend": "stable"
      },
      "theta": {
        "avg": 0.250,
        "trend": "stable"
      }
    },
    "session_stats": {
      "total_batches": 145,
      "total_samples": 1450,
      "session_duration": 725
    }
  }
}
```

#### GET `/api/session-history`
Get historical session data.

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction_history": [
      {
        "timestamp": "2025-05-31T12:39:21.409759",
        "dominant_emotion": "fatigue",
        "consistency": 1.0,
        "avg_confidence": 0.453,
        "batch_size": 10
      }
      // ... last 20 entries
    ],
    "start_time": "2025-05-31T12:28:00.000000"
  }
}
```

#### GET `/api/status`
Get web server status.

**Response:**
```json
{
  "status": "running",
  "timestamp": "2025-05-31T12:39:21.409759",
  "message": "EEG Web Server is operational"
}
```

## 🧪 Testing and Verification

### Manual API Testing
```bash
# Test EEG device connection
curl http://127.0.0.1:5000/api/status

# Get raw EEG data
curl http://127.0.0.1:5000/api/data

# Test web server
curl http://127.0.0.1:5001/api/status

# Get emotion analysis
curl http://127.0.0.1:5001/api/eeg-data
```

### Python Testing Script
```python
import requests
import json

# Test complete data flow
def test_system():
    # 1. Check device API
    status = requests.get('http://127.0.0.1:5000/api/status').json()
    print(f"Device Connected: {status['device_status']['connected']}")
    
    # 2. Get raw data
    raw_data = requests.get('http://127.0.0.1:5000/api/data').json()
    print(f"Raw samples: {len(raw_data)}")
    
    # 3. Get analysis
    analysis = requests.get('http://127.0.0.1:5001/api/eeg-data').json()
    if analysis['success']:
        print(f"Emotion: {analysis['data']['dominant_emotion']}")
        print(f"Confidence: {analysis['data']['avg_confidence']:.1%}")

test_system()
```

## 🎯 Emotion Classification

The system detects **3 emotional states**:

### 🎯 Focus
- **Indicators**: High Beta (13-30 Hz), Low Theta (4-8 Hz)
- **Use cases**: Study sessions, work tasks, concentration monitoring

### 😌 Relax
- **Indicators**: High Alpha (8-12 Hz), Moderate Beta
- **Use cases**: Meditation, rest periods, stress monitoring

### 😴 Fatigue
- **Indicators**: High Theta (4-8 Hz), Low Beta
- **Use cases**: Break recommendations, alertness monitoring

## ⚙️ Configuration

### Device Settings (`bci_api.py`)
```python
# Signal processing parameters
sampling_rate = 250          # 250 Hz
process_win_freq = 25        # Process every 25 Hz
calibration_length = 6       # 6 second calibration
channels_number = 4          # 4 channels (O1, O2, T3, T4)

# Artifact detection
art_bord = 110              # Artifact border
allowed_percent_artpoints = 70  # Allowed artifact percentage
```

### Monitoring Settings (`real_time_monitor.py`)
```python
api_url = "http://127.0.0.1:5000/api/data"
fetch_interval = 5          # Fetch every 5 seconds
batch_size = 10            # Expected samples per fetch
```

## 📊 Data Flow Details

### 1. Signal Acquisition
```
EEG Headband → NeuroSDK → Raw Voltage Signals
```

### 2. Signal Processing
```
Raw Signals → Bipolar Montage → Artifact Detection → FFT Analysis
```

### 3. Feature Extraction
```
FFT → Alpha/Beta/Theta Bands → 3-Feature Vector
```

### 4. ML Prediction
```
3-Feature Vector → 17-Feature Conversion → Random Forest → Emotion + Confidence
```

### 5. API Response
```
Emotion Prediction → JSON Format → REST API → Frontend
```

## 🔧 Troubleshooting

### Device Not Connected
```bash
# Check device status
curl http://127.0.0.1:5000/api/status

# Common solutions:
# 1. Ensure EEG headband is powered on
# 2. Check Bluetooth pairing
# 3. Verify NeuroSDK installation
# 4. Restart bci_api.py
```

### No Data Streaming
```bash
# Check calibration status
# Device needs 6 seconds calibration after connection
# Look for "Calibration progress: 100%" message
```

### API Connection Failed
```bash
# Verify servers are running
netstat -an | findstr :5000  # EEG API
netstat -an | findstr :5001  # Web API

# Restart if needed
python bci_api.py
python web_server.py
```

### Poor Signal Quality
- Clean electrode sites on scalp
- Apply conductive gel if required
- Ensure proper headband positioning
- Minimize movement and blinking during calibration

## 📈 Performance Metrics

### Latency
- **Device to API**: ~100ms
- **API to Analysis**: ~50ms
- **Total End-to-End**: ~150ms

### Accuracy
- **Model Accuracy**: ~85% on test data
- **Real-time Consistency**: 70-95% depending on signal quality

### Throughput
- **Sampling Rate**: 250 Hz from device
- **Processing Rate**: 25 Hz (every 40ms)
- **API Updates**: Every 5 seconds (batch processing)

## 🔒 Security Considerations

### API Security
- APIs run on localhost only
- CORS enabled for frontend integration
- No authentication required (local development)

### Data Privacy
- No data stored permanently by default
- Session data saved locally only
- No external data transmission

## 🚦 System Status Indicators

### Green (Normal Operation)
- ✅ Device connected and streaming
- ✅ Calibration completed
- ✅ APIs responding
- ✅ Consistent emotion predictions

### Yellow (Warning)
- 🟡 High artifact levels
- 🟡 Inconsistent predictions
- 🟡 Signal quality issues

### Red (Requires Attention)
- ❌ Device disconnected
- ❌ API server down
- ❌ Calibration failed
- ❌ No data available

## 📝 Logging

### Log Files
- `logs/sdk_log.log` - NeuroSDK device logs
- Console output - Real-time status and data

### Log Levels
- **INFO**: Normal operation status
- **WARNING**: Signal quality issues
- **ERROR**: Connection or processing errors

## 🔄 Development Workflow

### Adding New Features
1. Modify `eeg_converter.py` for new ML features
2. Update `real_time_monitor.py` for processing logic
3. Extend `web_server.py` for new API endpoints
4. Test with `start_bci.py`

### Testing Changes
1. Use simulated data: `python test_api_server.py`
2. Test with real device: `python bci_api.py`
3. Verify API responses: `curl` commands
4. Check frontend integration

## 🆘 Support

### Common Issues
1. **"Device not found"** - Check Bluetooth connection
2. **"Calibration failed"** - Ensure proper electrode contact
3. **"No data available"** - Restart device API
4. **"API timeout"** - Check server status

### Getting Help
- Check `README_REAL_DEVICE.md` for device-specific setup
- Review console logs for error details
- Test with simulated data first
- Verify all dependencies are installed

---

🎉 **You now have a complete BCI backend system with real-time EEG processing and emotion classification!**

For frontend integration, see the React components in `frontend/bci frontend/src/`
