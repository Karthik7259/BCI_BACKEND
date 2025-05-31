#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-Time EEG Emotion Monitoring System
=======================================

Fetches EEG data from API every 5 seconds and provides continuous emotion predictions.
API Endpoint: http://127.0.0.1:5000/api/data
"""

import requests
import time
import json
import numpy as np
from datetime import datetime
from eeg_converter import process_json_eeg_data
import threading
import sys
import subprocess
import os

class EEGMonitor:
    def __init__(self, api_url="http://127.0.0.1:5000/api/data", enable_web_server=True):
        self.api_url = api_url
        self.running = False
        self.session_data = []
        self.current_batch = []
        self.prediction_history = []
        self.enable_web_server = enable_web_server
        self.web_server_process = None
          # Start web server if enabled
        if self.enable_web_server:
            self.start_web_server()
        
    def fetch_eeg_data(self):
        """Fetch EEG data from the API"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check if response contains error (for real device API)
            if isinstance(data, dict) and 'error' in data:
                print(f"🔴 Device Error: {data['error']}")
                if 'status' in data:
                    status = data['status']
                    if not status.get('connected', False):
                        print("   📡 Device not connected - check EEG headband")
                    elif status.get('calibrating', False):
                        print("   🔄 Device is calibrating - please wait...")
                    elif not status.get('streaming', False):
                        print("   ⏳ Device not streaming yet")
                return None
            
            # Validate data format
            if isinstance(data, list) and len(data) > 0:
                # Check if first item has required fields
                if all(key in data[0] for key in ['alpha', 'beta', 'theta', 'timestamp']):
                    return data
                else:
                    print("⚠️ API data missing required fields (alpha, beta, theta, timestamp)")
                    return None
            else:
                print("⚠️ API returned empty or invalid data")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API Request failed: {e}")
            print("   💡 Make sure the EEG device API server is running on port 5000")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def analyze_batch(self, eeg_batch):
        """Analyze a batch of EEG data"""
        if not eeg_batch:
            return None
            
        try:
            # Get predictions for the batch
            results = process_json_eeg_data(eeg_batch)
            
            # Calculate batch statistics
            emotions = [r['predicted_emotion'] for r in results]
            confidences = [max(r['probabilities'].values()) for r in results]
            
            # Get dominant emotion
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            dominant_emotion = max(emotion_counts.keys(), key=lambda x: emotion_counts[x])
            consistency = emotion_counts[dominant_emotion] / len(emotions)
            avg_confidence = np.mean(confidences)
            
            # Calculate average probabilities
            avg_probs = {}
            for emotion in ['fatigue', 'focus', 'relax']:
                probs = [r['probabilities'][emotion] for r in results]
                avg_probs[emotion] = np.mean(probs)
            
            # EEG band analysis
            alphas = [sample['alpha'] for sample in eeg_batch]
            betas = [sample['beta'] for sample in eeg_batch]
            thetas = [sample['theta'] for sample in eeg_batch]
            
            batch_analysis = {
                'timestamp': datetime.now().isoformat(),
                'batch_size': len(eeg_batch),
                'dominant_emotion': dominant_emotion,
                'consistency': consistency,
                'avg_confidence': avg_confidence,
                'avg_probabilities': avg_probs,                'eeg_stats': {
                    'alpha': {'avg': np.mean(alphas), 'trend': 'stable'},
                    'beta': {'avg': np.mean(betas), 'trend': 'stable'},
                    'theta': {'avg': np.mean(thetas), 'trend': 'stable'}
                },
                'raw_results': results
            }
            
            # Calculate trends if we have previous data
            if len(self.prediction_history) > 0:
                prev_alpha = np.mean([s['alpha'] for s in self.current_batch[-10:]] if self.current_batch else alphas)
                prev_beta = np.mean([s['beta'] for s in self.current_batch[-10:]] if self.current_batch else betas)
                prev_theta = np.mean([s['theta'] for s in self.current_batch[-10:]] if self.current_batch else thetas)
                batch_analysis['eeg_stats']['alpha']['trend'] = self._get_trend(prev_alpha, np.mean(alphas))
                batch_analysis['eeg_stats']['beta']['trend'] = self._get_trend(prev_beta, np.mean(betas))
                batch_analysis['eeg_stats']['theta']['trend'] = self._get_trend(prev_theta, np.mean(thetas))
            
            return batch_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing batch: {e}")
            return None

    def start_web_server(self):
        """Start the web server in a separate process"""
        try:
            print("🌐 Starting web server for frontend...")
            self.web_server_process = subprocess.Popen([
                sys.executable, 'web_server.py'
            ], cwd=os.getcwd())
            time.sleep(2)  # Give server time to start
            print("✅ Web server started! Open http://127.0.0.1:5001 in your browser")
        except Exception as e:
            print(f"⚠️ Failed to start web server: {e}")
            print("You can start it manually: python web_server.py")
    
    def update_web_data(self, analysis):
        """Send data to web server"""
        if not self.enable_web_server:
            return
            
        try:
            # Try to update web server data via file (simpler approach)
            session_data = {
                'prediction_history': self.prediction_history,
                'session_data': self.session_data
            }
            
            # Write data to a temp file that web server can read
            web_data = {
                'analysis': analysis,
                'session': session_data,
                'timestamp': datetime.now().isoformat()
            }
            
            with open('web_data.json', 'w') as f:
                json.dump(web_data, f, indent=2)
                
        except Exception as e:
            # Silently fail if cannot write data
            pass
    
    def _get_trend(self, prev_val, curr_val):
        """Determine trend direction"""
        diff = curr_val - prev_val
        if abs(diff) < 0.01:
            return 'stable'
        elif diff > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def display_results(self, analysis):
        """Display real-time analysis results"""
        if not analysis:
            return
            
        print("\n" + "="*60)
        print(f"🧠 REAL-TIME EEG ANALYSIS - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        # Main prediction
        emotion = analysis['dominant_emotion']
        consistency = analysis['consistency']
        confidence = analysis['avg_confidence']
        
        emotion_emoji = {'focus': '🎯', 'relax': '😌', 'fatigue': '😴'}
        
        print(f"🎯 CURRENT STATE: {emotion_emoji.get(emotion, '🧠')} {emotion.upper()}")
        print(f"📊 Consistency: {consistency:.1%} ({int(consistency * analysis['batch_size'])}/{analysis['batch_size']} samples)")
        print(f"🎪 Confidence: {confidence:.1%}")
        
        # Probability breakdown
        print(f"\n📈 PROBABILITY BREAKDOWN:")
        probs = analysis['avg_probabilities']
        for emotion_name, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            bar_length = int(prob * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"   {emotion_name.capitalize():8s}: {bar} {prob:.1%}")
        
        # EEG band analysis
        print(f"\n🌊 EEG BAND ANALYSIS:")
        stats = analysis['eeg_stats']
        trend_emoji = {'increasing': '↗️', 'decreasing': '↘️', 'stable': '➡️'}
        
        print(f"   Alpha (Relaxation): {stats['alpha']['avg']:.3f} {trend_emoji[stats['alpha']['trend']]}")
        print(f"   Beta (Focus):       {stats['beta']['avg']:.3f} {trend_emoji[stats['beta']['trend']]}")
        print(f"   Theta (Drowsiness): {stats['theta']['avg']:.3f} {trend_emoji[stats['theta']['trend']]}")
        
        # Recommendations
        self.show_recommendations(emotion, confidence, stats)
        
        # Session stats
        print(f"\n📊 SESSION STATS:")
        print(f"   Total Batches: {len(self.prediction_history) + 1}")
        print(f"   Total Samples: {len(self.session_data) + analysis['batch_size']}")
        print(f"   Session Duration: {len(self.prediction_history) * 5} seconds")
    
    def show_recommendations(self, emotion, confidence, eeg_stats):
        """Show contextual recommendations"""
        print(f"\n💡 RECOMMENDATIONS:")
        
        if emotion == 'fatigue':
            if confidence > 0.5:
                print("   🔴 HIGH FATIGUE - Take immediate action:")
                print("      • Stop current tasks and take a break")
                print("      • Consider a 15-20 minute power nap")
                print("      • Hydrate and get fresh air")
            else:
                print("   🟡 MODERATE FATIGUE - Consider:")
                print("      • Light stretching or movement")
                print("      • Stay hydrated")
                print("      • Monitor your state")
                
        elif emotion == 'focus':
            print("   🟢 GOOD FOCUS STATE:")
            print("      • Continue with cognitive tasks")
            print("      • Maintain current environment")
            print("      • Stay hydrated")
            
        elif emotion == 'relax':
            if eeg_stats['theta']['avg'] > 0.35:
                print("   🟡 RELAXED BUT DROWSY:")
                print("      • Light activity to maintain alertness")
                print("      • Consider if rest is needed")
            else:
                print("   🟢 CALM AND ALERT:")
                print("      • Good state for learning or creativity")
                print("      • Maintain current conditions")
    
    def save_session_data(self):
        """Save session data to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"eeg_session_{timestamp}.json"
        
        session_summary = {
            'session_start': self.prediction_history[0]['timestamp'] if self.prediction_history else datetime.now().isoformat(),
            'session_end': datetime.now().isoformat(),
            'total_batches': len(self.prediction_history),
            'total_samples': len(self.session_data),
            'batch_history': self.prediction_history,
            'raw_data': self.session_data
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_summary, f, indent=2)
            print(f"💾 Session data saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save session data: {e}")
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        print("🚀 STARTING REAL-TIME EEG MONITORING")
        print("="*60)
        print(f"📡 API Endpoint: {self.api_url}")
        print(f"⏱️ Fetch Interval: 5 seconds")
        print(f"📊 Batch Size: Expected 10 samples per fetch")
        print("🛑 Press Ctrl+C to stop monitoring")
        print("="*60)
        
        self.running = True
        batch_count = 0
        
        try:
            while self.running:
                batch_count += 1
                print(f"\n🔄 Fetching batch #{batch_count}...")
                
                # Fetch data from API
                eeg_data = self.fetch_eeg_data()
                
                if eeg_data:
                    print(f"✅ Received {len(eeg_data)} samples")
                    
                    # Store data
                    self.current_batch = eeg_data
                    self.session_data.extend(eeg_data)
                      # Analyze batch
                    analysis = self.analyze_batch(eeg_data)
                    
                    if analysis:
                        # Store analysis
                        self.prediction_history.append(analysis)
                        
                        # Update web server data
                        self.update_web_data(analysis)
                        
                        # Display results
                        self.display_results(analysis)
                    else:
                        print("❌ Failed to analyze batch")
                else:
                    print("❌ No data received from API")
                
                # Wait 5 seconds before next fetch
                print(f"\n⏳ Waiting 5 seconds before next fetch...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            self.running = False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            self.running = False
        finally:
            # Save session data
            if self.session_data:
                print("\n💾 Saving session data...")
                self.save_session_data()
            
            print("\n👋 EEG monitoring session ended")

def main():
    """Main function"""
    print("🧠 REAL-TIME EEG EMOTION MONITORING")
    print("=" * 50)
    print("📋 SETUP CHECKLIST:")
    print("   1. ✅ EEG headband is powered on")
    print("   2. ✅ Electrodes are properly positioned")
    print("   3. ✅ Real EEG API server is running (bci_api.py)")
    print("   4. ✅ Device is connected and calibrated")
    print("=" * 50)
    
    # You can change the API URL here if needed
    api_url = "http://127.0.0.1:5000/api/data"
    
    # Create monitor instance
    monitor = EEGMonitor(api_url)
    
    # Test API connection first
    print("🔍 Testing connection to real EEG device API...")
    test_data = monitor.fetch_eeg_data()
    
    if test_data:
        print(f"✅ Real EEG device connection successful! Received {len(test_data)} samples")
        print("📊 Sample data from your EEG device:")
        if test_data:
            sample = test_data[0]
            print(f"   Alpha: {sample.get('alpha', 'N/A'):.3f}")
            print(f"   Beta: {sample.get('beta', 'N/A'):.3f}")
            print(f"   Theta: {sample.get('theta', 'N/A'):.3f}")
            print(f"   Timestamp: {sample.get('timestamp', 'N/A')}")
        
        print("\n🎯 Starting real-time emotion monitoring...")
        # Start monitoring
        monitor.start_monitoring()
    else:
        print("❌ Failed to connect to real EEG device API.")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure the real EEG API server is running:")
        print("      python bci_api.py")
        print("   2. Check that your EEG headband is:")
        print("      • Powered on and paired")
        print("      • Properly positioned on your head")
        print("      • Connected to the NeuroSDK")
        print("   3. Ensure electrodes have good contact:")
        print("      • Clean electrode sites")
        print("      • Use conductive gel if needed")
        print("      • Check resistance readings")
        print("   4. Wait for device calibration to complete")
        print("\n💡 Alternative: Use simulated data for testing:")
        print("   python test_api_server.py")
        print("   (Run this in another terminal for demo mode)")
        
        print(f"\n📊 API Status Check: http://127.0.0.1:5000/api/status")
        print(f"🌐 Web Interface: http://127.0.0.1:5001")

if __name__ == "__main__":
    main()
