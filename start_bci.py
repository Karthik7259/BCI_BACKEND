#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BCI System Launcher
==================

Real-time EEG device launcher for brain-computer interface system
"""

import subprocess
import sys
import os
import time

def run_real_device():
    """Launch the real EEG device API"""
    print("🧠 LAUNCHING REAL EEG DEVICE MODE")
    print("=" * 40)
    print("📋 Prerequisites:")
    print("   • NeuroSDK installed")
    print("   • EEG headband powered on")
    print("   • Electrodes properly positioned")
    print("   • Device paired via Bluetooth")
    print("=" * 40)
    
    try:
        print("🚀 Starting real EEG device API server...")
        # Start the real device API
        process = subprocess.Popen([sys.executable, 'bci_api.py'])
        print("✅ Real EEG device API started!")
        print("📡 Device connection process initiated...")
        print("🔄 Please wait for device calibration...")
        return process
    except Exception as e:
        print(f"❌ Failed to start real device API: {e}")
        return None

def main():
    """Main launcher function"""
    print("🧠 BCI EMOTION CLASSIFICATION SYSTEM")
    print("=" * 50)
    print("🔴 Real EEG Device Mode")
    print("   - Connect to actual EEG headband")
    print("   - Requires hardware setup")
    print("   - Real brain activity data")
    print("=" * 50)
    
    try:
        print("Do you want to start the BCI system? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice in ['y', 'yes']:
            # Real device mode
            api_process = run_real_device()
            if api_process:
                print("\n⏳ Waiting for device initialization (30 seconds)...")
                time.sleep(30)  # Give device time to connect and calibrate
            else:
                print("❌ Failed to start real device mode")
                return
                
        elif choice in ['n', 'no']:
            print("👋 Exiting...")
            return
        else:
            print("❌ Invalid choice. Please enter y or n.")
            return
                
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        return
    
    # Now start the monitoring system
    print("\n🎯 STARTING REAL-TIME MONITORING...")
    print("=" * 50)
    
    try:
        # Start the monitoring system
        subprocess.run([sys.executable, 'real_time_monitor.py'])
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error running monitor: {e}")
    finally:
        # Clean up API process
        if 'api_process' in locals() and api_process:
            print("🧹 Cleaning up API server...")
            api_process.terminate()
            print("✅ Cleanup complete")

if __name__ == "__main__":
    main()
