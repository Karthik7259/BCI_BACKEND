#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real EEG Device API Server
==========================

Connects to actual EEG hardware using NeuroSDK and provides real-time data
API Endpoint: http://127.0.0.1:5000/api/data
"""

from flask import Flask, jsonify
from flask_cors import CORS
from neurosdk.scanner import Scanner
from em_st_artifacts.utils import lib_settings, support_classes
from em_st_artifacts import emotional_math
from neurosdk.cmn_types import SensorFamily, SensorCommand
from time import sleep
from datetime import datetime
import threading, csv, numpy as np
import atexit

app = Flask(__name__)
CORS(app)  # Allow React frontend to fetch data

# Global storage for latest data
latest = {
    "timestamp": None,
    "alpha": 0.0,
    "beta": 0.0,
    "theta": 0.0
}

# Store last 10 readings for API endpoint
readings_history = []

# EEG processing buffers
alpha_buffer, beta_buffer, theta_buffer = [], [], []
math = None  # Will be initialized in bci_thread
scanner = None
current_sensor = None

# Device status
device_status = {
    "connected": False,
    "calibrating": False,
    "streaming": False,
    "last_update": None,
    "error": None
}

def sensor_found(scanner, sensors):
    """Callback when sensors are discovered"""
    for index in range(len(sensors)):
        print(f'🔍 Sensor found: {sensors[index]}')

def on_sensor_state_changed(sensor, state):
    """Callback when sensor state changes"""
    print(f'📡 Sensor {sensor.name} is {state}')
    global device_status
    device_status["connected"] = True
    device_status["last_update"] = datetime.now().isoformat()

def on_battery_changed(sensor, battery):
    """Callback when battery level changes"""
    print(f'🔋 Battery: {battery}%')

def compute_apen(U, m=2, r=None):
    """
    Compute Approximate Entropy (ApEn) of a time series
    Used for signal complexity analysis
    """
    def _maxdist(xi, xj, N, m):
        return max([abs(ua - va) for ua, va in zip(xi, xj)])

    def _phi(m):
        patterns = np.array([U[i:i + m] for i in range(N - m + 1)])
        C = np.zeros(N - m + 1)
        for i in range(N - m + 1):
            template_i = patterns[i]
            C[i] = sum([1 for j in range(N - m + 1) 
                       if _maxdist(template_i, patterns[j], N, m) <= r]) / (N - m + 1.0)
        phi = (N - m + 1.0) ** (-1) * sum(np.log(C))
        return phi

    N = len(U)
    if r is None:
        r = 0.2 * np.std(U, ddof=1)
    
    return _phi(m) - _phi(m + 1)

def on_signal_received(sensor, data):
    """Callback when EEG signal data is received"""
    global latest, alpha_buffer, beta_buffer, theta_buffer, math, readings_history, device_status

    try:
        # Process the raw EEG data
        raw_channels = []
        for sample in data:
            # Create bipolar montage (T3-O1, T4-O2)
            left_bipolar = sample.T3 - sample.O1
            right_bipolar = sample.T4 - sample.O2
            raw_channels.append(support_classes.RawChannels(left_bipolar, right_bipolar))

        # Push data to emotional math processor
        math.push_data(raw_channels)
        math.process_data_arr()

        # Check calibration status
        if not math.calibration_finished():
            calibration_percent = math.get_calibration_percents()
            print(f"📊 Calibration progress: {calibration_percent}%")
            device_status["calibrating"] = True
            device_status["streaming"] = False
        else:
            device_status["calibrating"] = False
            device_status["streaming"] = True
            
            # Read processed mental and spectral data
            mental_data = math.read_mental_data_arr()
            spectral_data = math.read_spectral_data_percents_arr()

            # Process each data point
            for mind, spec in zip(mental_data, spectral_data):
                # Update rolling buffers for trend analysis
                alpha_buffer.append(spec.alpha)
                beta_buffer.append(spec.beta)
                theta_buffer.append(spec.theta)
                
                # Keep only last 20 samples for buffer
                if len(alpha_buffer) > 20:
                    alpha_buffer.pop(0)
                    beta_buffer.pop(0)
                    theta_buffer.pop(0)

                # Update latest values
                latest["timestamp"] = datetime.now().isoformat()
                latest["alpha"] = float(spec.alpha)
                latest["beta"] = float(spec.beta)
                latest["theta"] = float(spec.theta)

                # Add to readings history (keep last 10 for API)
                readings_history.append(latest.copy())
                if len(readings_history) > 10:
                    readings_history.pop(0)

                # Update device status
                device_status["last_update"] = latest["timestamp"]
                device_status["error"] = None

                print(f"🧠 EEG Data - Alpha: {spec.alpha:.3f}, Beta: {spec.beta:.3f}, Theta: {spec.theta:.3f}")

    except Exception as e:
        print(f"❌ Error processing signal data: {e}")
        device_status["error"] = str(e)

def on_resist_received(sensor, data):
    """Callback when resistance data is received"""
    print("🔌 ELECTRODE RESISTANCE CHECK:")
    print(f"   O1 (left occipital): {'✅ Good' if data.O1 < 2000000 else '❌ Poor'} ({data.O1} Ω)")
    print(f"   O2 (right occipital): {'✅ Good' if data.O2 < 2000000 else '❌ Poor'} ({data.O2} Ω)")
    print(f"   T3 (left temporal): {'✅ Good' if data.T3 < 2000000 else '❌ Poor'} ({data.T3} Ω)")
    print(f"   T4 (right temporal): {'✅ Good' if data.T4 < 2000000 else '❌ Poor'} ({data.T4} Ω)")

def cleanup():
    """Clean up device connections and resources"""
    global scanner, current_sensor, math, device_status
    
    print("🧹 Cleaning up device connections...")
    
    if current_sensor:
        try:
            current_sensor.exec_command(SensorCommand.StopSignal)
            current_sensor.disconnect()
            print("✅ Disconnected from EEG sensor")
        except Exception as e:
            print(f"⚠️ Error disconnecting sensor: {e}")
        current_sensor = None
    
    if math:
        try:
            del math
            print("✅ Cleaned up math processor")
        except:
            pass
        math = None
    
    if scanner:
        try:
            del scanner
            print("✅ Cleaned up scanner")
        except:
            pass
        scanner = None
    
    device_status["connected"] = False
    device_status["streaming"] = False

def bci_thread():
    """Background thread for EEG device communication"""
    global math, scanner, current_sensor, device_status
    
    try:
        print("🚀 STARTING REAL EEG DEVICE CONNECTION")
        print("=" * 50)
        
        # Initialize scanner for LE Headband devices
        print("🔍 Initializing scanner for LE Headband devices...")
        scanner = Scanner([SensorFamily.LEHeadband])
        scanner.sensorsChanged = sensor_found
        scanner.start()
        
        print("⏳ Searching for EEG devices (25 seconds)...")
        sleep(25)
        scanner.stop()

        # Check if any sensors were found
        sensorsInfo = scanner.sensors()
        if not sensorsInfo:
            print("❌ No EEG sensors found!")
            print("   Please check:")
            print("   • Device is powered on")
            print("   • Device is in pairing mode")
            print("   • Bluetooth is enabled")
            print("   • Device is within range")
            device_status["error"] = "No sensors found"
            return

        # Connect to the first available sensor
        current_sensor = scanner.create_sensor(sensorsInfo[0])
        print(f"✅ Connected to EEG device: {sensorsInfo[0]}")

        # Set up event callbacks
        current_sensor.sensorStateChanged = on_sensor_state_changed
        current_sensor.batteryChanged = on_battery_changed
        current_sensor.signalDataReceived = on_signal_received
        current_sensor.resistDataReceived = on_resist_received

        # Check electrode resistance
        print("\n🔌 CHECKING ELECTRODE RESISTANCE...")
        current_sensor.exec_command(SensorCommand.StartResist)
        sleep(20)
        current_sensor.exec_command(SensorCommand.StopResist)
        print("✅ Resistance check complete")

        # Initialize EmotionalMath settings for signal processing
        print("\n⚙️ INITIALIZING SIGNAL PROCESSING...")
        
        # Math library settings
        mls = lib_settings.MathLibSetting(
            sampling_rate=250,           # 250 Hz sampling rate
            process_win_freq=25,         # Process every 25 Hz
            n_first_sec_skipped=4,       # Skip first 4 seconds
            fft_window=1000,             # FFT window size
            bipolar_mode=True,           # Use bipolar montage
            squared_spectrum=True,       # Use squared spectrum
            channels_number=4,           # 4 channels (O1, O2, T3, T4)
            channel_for_analysis=0       # Use first channel for analysis
        )
        
        # Artifact detection settings
        ads = lib_settings.ArtifactDetectSetting(
            art_bord=110,                    # Artifact border
            allowed_percent_artpoints=70,    # Allowed artifact percentage
            raw_betap_limit=800_000,         # Raw beta power limit
            global_artwin_sec=4,             # Global artifact window
            num_wins_for_quality_avg=125,    # Windows for quality averaging
            hamming_win_spectrum=True,       # Use Hamming window
            hanning_win_spectrum=False,      # Don't use Hanning window
            total_pow_border=400_000_000,    # Total power border
            spect_art_by_totalp=True         # Spectral artifact by total power
        )
        
        # Short artifact detection settings
        sads = lib_settings.ShortArtifactDetectSetting(
            ampl_art_detect_win_size=200,    # Amplitude artifact detection window
            ampl_art_zerod_area=200,         # Amplitude artifact zeroed area
            ampl_art_extremum_border=25      # Amplitude artifact extremum border
        )
        
        # Mental and spectral estimation settings
        mss = lib_settings.MentalAndSpectralSetting(
            n_sec_for_averaging=2,           # Seconds for averaging
            n_sec_for_instant_estimation=4   # Seconds for instant estimation
        )

        # Initialize EmotionalMath processor
        math = emotional_math.EmotionalMath(mls, ads, sads, mss)
        math.set_calibration_length(6)           # 6 second calibration
        math.set_mental_estimation_mode(False)   # Disable mental estimation
        math.set_skip_wins_after_artifact(10)    # Skip 10 windows after artifact
        math.set_zero_spect_waves(True, 0, 1, 1, 1, 0)  # Zero spectral waves
        math.set_spect_normalization_by_bands_width(True)  # Normalize by band width

        print("✅ Signal processing initialized")

        # Start signal acquisition
        if current_sensor.is_supported_command(SensorCommand.StartSignal):
            print("\n🎯 STARTING REAL-TIME EEG ACQUISITION...")
            current_sensor.exec_command(SensorCommand.StartSignal)
            math.start_calibration()
            
            print("📊 Starting calibration phase...")
            print("🔄 Streaming EEG data... (Press Ctrl+C to stop)")
            print("=" * 50)
            
            # Keep the thread alive for continuous streaming
            while True:
                sleep(0.1)
        else:
            print("❌ Device does not support signal acquisition")
            device_status["error"] = "Signal acquisition not supported"

    except Exception as err:
        print(f"❌ Error in EEG device thread: {err}")
        device_status["error"] = str(err)
        cleanup()

# Register cleanup function for program exit
atexit.register(cleanup)

# Start EEG device thread immediately when module is imported
print("🧠 Initializing Real EEG Device Connection...")
threading.Thread(target=bci_thread, daemon=True).start()

# Flask API endpoints
@app.route("/api/data")
def get_data():
    """API endpoint to get the last 10 EEG readings"""
    try:
        if not readings_history:
            return jsonify({
                "error": "No EEG data available yet",
                "status": device_status
            }), 503
        
        return jsonify(readings_history)
    
    except Exception as e:
        return jsonify({
            "error": f"API error: {str(e)}",
            "status": device_status
        }), 500

@app.route("/api/status")
def get_status():
    """API endpoint to get device status"""
    return jsonify({
        "device_status": device_status,
        "data_available": len(readings_history) > 0,
        "latest_reading": latest if latest["timestamp"] else None,
        "buffer_size": len(readings_history),
        "timestamp": datetime.now().isoformat()
    })

@app.route("/")
def home():
    """Home endpoint with API information"""
    return f"""
    <h1>🧠 Real EEG Device API Server</h1>
    <p>Live connection to NeuroSDK EEG hardware</p>
    
    <h2>📊 Current Status:</h2>
    <ul>
        <li>Connected: {'✅' if device_status['connected'] else '❌'}</li>
        <li>Calibrating: {'🔄' if device_status['calibrating'] else '✅ Complete' if device_status['streaming'] else '⏳ Waiting'}</li>
        <li>Streaming: {'🟢' if device_status['streaming'] else '🔴'}</li>
        <li>Data Points: {len(readings_history)}</li>
        <li>Last Update: {device_status.get('last_update', 'Never')}</li>
    </ul>
    
    <h2>🔗 API Endpoints:</h2>
    <ul>
        <li><a href="/api/data">GET /api/data</a> - Get latest EEG readings</li>
        <li><a href="/api/status">GET /api/status</a> - Get device status</li>
    </ul>
    
    <h2>⚠️ Notes:</h2>
    <ul>
        <li>Ensure EEG headband is properly positioned</li>
        <li>Wait for calibration to complete (~6 seconds)</li>
        <li>Check electrode resistance for good signal quality</li>
    </ul>
    """

if __name__ == "__main__":
    try:
        print("🌐 Starting Real EEG Device API Server...")
        print("📡 Server URL: http://127.0.0.1:5000")
        print("🔗 API Endpoint: http://127.0.0.1:5000/api/data")
        print("📊 Status: http://127.0.0.1:5000/api/status")
        print("🛑 Press Ctrl+C to stop")
        
        app.run(debug=False, port=5000, host='127.0.0.1')
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        cleanup()
    except Exception as e:
        print(f"❌ Server error: {e}")
        cleanup()
