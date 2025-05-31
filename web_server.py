#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Server for Real-Time EEG Data
=================================

Serves real-time EEG emotion analysis data to the frontend
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables to store latest data
latest_analysis = None
session_data = {
    'prediction_history': [],
    'session_data': [],
    'start_time': datetime.now().isoformat()
}

@app.route('/api/eeg-data', methods=['GET'])
def get_eeg_data():
    """Get the latest EEG analysis data"""
    global latest_analysis, session_data
    
    try:
        # Try to read from the data file that real_time_monitor.py writes
        if os.path.exists('web_data.json'):
            with open('web_data.json', 'r') as f:
                data = json.load(f)
                latest_analysis = data.get('analysis')
                session_data = data.get('session', session_data)
        
        if latest_analysis:
            # Format data for frontend
            response_data = {
                'timestamp': latest_analysis.get('timestamp', datetime.now().isoformat()),
                'dominant_emotion': latest_analysis.get('dominant_emotion', 'unknown'),
                'consistency': latest_analysis.get('consistency', 0),
                'avg_confidence': latest_analysis.get('avg_confidence', 0),
                'probabilities': latest_analysis.get('avg_probabilities', {
                    'fatigue': 0,
                    'relax': 0,
                    'focus': 0
                }),
                'eeg_stats': latest_analysis.get('eeg_stats', {
                    'alpha': {'avg': 0, 'trend': 'stable'},
                    'beta': {'avg': 0, 'trend': 'stable'},
                    'theta': {'avg': 0, 'trend': 'stable'}
                }),
                'session_stats': {
                    'total_batches': len(session_data.get('prediction_history', [])),
                    'total_samples': len(session_data.get('session_data', [])),
                    'session_duration': len(session_data.get('prediction_history', [])) * 5
                }
            }
            
            return jsonify({
                'success': True,
                'data': response_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No data available yet',
                'data': None
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reading data: {str(e)}',
            'data': None
        }), 500

@app.route('/api/session-history', methods=['GET'])
def get_session_history():
    """Get session history data"""
    global session_data
    
    try:
        return jsonify({
            'success': True,
            'data': {
                'prediction_history': session_data.get('prediction_history', [])[-20:],  # Last 20 entries
                'start_time': session_data.get('start_time', datetime.now().isoformat())
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'message': 'EEG Web Server is operational'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return """
    <h1>EEG Real-Time Web Server</h1>
    <p>Backend server for BCI emotion classification frontend</p>
    <ul>
        <li><a href="/api/eeg-data">GET /api/eeg-data</a> - Get current EEG analysis</li>
        <li><a href="/api/session-history">GET /api/session-history</a> - Get session history</li>
        <li><a href="/api/status">GET /api/status</a> - Server status</li>
    </ul>
    <p>Frontend should be running on port 5173 (Vite dev server)</p>
    """

if __name__ == '__main__':
    print("🌐 Starting EEG Web Server")
    print("=" * 40)
    print("🔗 Server URL: http://127.0.0.1:5001")
    print("📊 API Endpoints:")
    print("   - GET /api/eeg-data - Real-time EEG analysis")
    print("   - GET /api/session-history - Session history")
    print("   - GET /api/status - Server status")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 40)
    
    app.run(host='127.0.0.1', port=5001, debug=False)