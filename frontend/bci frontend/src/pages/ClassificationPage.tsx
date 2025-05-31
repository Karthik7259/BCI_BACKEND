import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

// Interface for EEG data from backend
interface EEGData {
  timestamp: string;
  dominant_emotion: string;
  consistency: number;
  avg_confidence: number;
  probabilities: {
    fatigue: number;
    relax: number;
    focus: number;
  };
  eeg_stats: {
    alpha: { avg: number; trend: string };
    beta: { avg: number; trend: string };
    theta: { avg: number; trend: string };
  };
  session_stats: {
    total_batches: number;
    total_samples: number;
    session_duration: number;
  };
}

const ClassificationPage = () => {
  const [emotionData, setEmotionData] = useState([
    { name: 'Focus', value: 0, key: 'focus' },
    { name: 'Relax', value: 0, key: 'relax' },
    { name: 'Fatigue', value: 0, key: 'fatigue' }
  ]);
  const [selectedMode, setSelectedMode] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [sessionStats, setSessionStats] = useState({
    total_batches: 0,
    total_samples: 0,
    session_duration: 0
  });
  const [eegStats, setEegStats] = useState({
    alpha: { avg: 0, trend: 'stable' },
    beta: { avg: 0, trend: 'stable' },
    theta: { avg: 0, trend: 'stable' }
  });

  // Fetch real-time EEG data from backend
  const fetchEEGData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5001/api/eeg-data');
      const result = await response.json();
      
      if (result.success && result.data) {
        const data: EEGData = result.data;
        
        // Update emotion data with real probabilities
        const newEmotionData = emotionData.map(emotion => ({
          ...emotion,
          value: (data.probabilities[emotion.key as keyof typeof data.probabilities] || 0) * 100
        }));
        
        setEmotionData(newEmotionData);
        setSelectedMode(data.dominant_emotion);
        setLastUpdate(new Date(data.timestamp).toLocaleTimeString());
        setSessionStats(data.session_stats);
        setEegStats(data.eeg_stats);
        setIsConnected(true);
      } else {
        setIsConnected(false);
      }
    } catch (error) {
      console.error('Failed to fetch EEG data:', error);
      setIsConnected(false);
    }
  };

  useEffect(() => {
    // Fetch data immediately
    fetchEEGData();
    
    // Set up interval to fetch data every 2 seconds
    const interval = setInterval(fetchEEGData, 2000);
    
    return () => clearInterval(interval);
  }, []);

  const getEmotionColor = (name: string) => {
    switch (name.toLowerCase()) {
      case 'focus': return 'from-blue-500 to-blue-600 border-blue-400';
      case 'relax': return 'from-teal-500 to-teal-600 border-teal-400';
      case 'fatigue': return 'from-amber-500 to-amber-600 border-amber-400';
      default: return 'from-blue-500 to-blue-600 border-blue-400';
    }
  };

  const getEmotionIconColor = (name: string) => {
    switch (name.toLowerCase()) {
      case 'focus': return '#3B82F6';
      case 'relax': return '#14B8A6';
      case 'fatigue': return '#F59E0B';
      default: return '#3B82F6';
    }
  };

  const getEmotionEmoji = (name: string) => {
    switch (name.toLowerCase()) {
      case 'focus': return '🎯';
      case 'relax': return '😌';
      case 'fatigue': return '😴';
      default: return '🧠';
    }
  };

  const getTrendEmoji = (trend: string) => {
    switch (trend) {
      case 'increasing': return '↗️';
      case 'decreasing': return '↘️';
      default: return '➡️';
    }
  };

  // Create progress bar visualization like the terminal output
  const createProgressBar = (value: number) => {
    const filledBlocks = Math.floor(value / 5); // 20 blocks total, each represents 5%
    const emptyBlocks = 20 - filledBlocks;
    return '█'.repeat(filledBlocks) + '░'.repeat(emptyBlocks);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white p-2 sm:p-8">
      <div className="max-w-lg mx-auto sm:max-w-6xl">
        {/* Header */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xl sm:text-4xl font-bold text-center mb-4 sm:mb-12 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400 px-2"
        >
          Real-Time EEG Emotion Analysis
        </motion.h1>

        {/* Connection Status */}
        <div className="text-center mb-6">
          <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm ${
            isConnected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
          }`}>
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
            {isConnected ? 'Connected to EEG Monitor' : 'Disconnected - Check if EEG monitor is running'}
          </div>
          {lastUpdate && (
            <p className="text-gray-400 text-sm mt-1">Last update: {lastUpdate}</p>
          )}
        </div>

        {/* Current Dominant Emotion */}
        {selectedMode && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <div className={`inline-block rounded-xl px-6 py-4 mb-4 bg-gradient-to-r ${getEmotionColor(selectedMode)} bg-opacity-20 border border-white/10`}>
              <div className="text-4xl mb-2">{getEmotionEmoji(selectedMode)}</div>
              <h2 className="text-2xl sm:text-3xl font-bold capitalize">
                {selectedMode}
              </h2>
              <p className="text-sm sm:text-base text-white/80">
                Dominant emotional state
              </p>
            </div>
          </motion.div>
        )}

        {/* Probability Breakdown - Terminal Style */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-white/10 mb-6">
          <h3 className="text-xl font-bold mb-4 text-center">📈 PROBABILITY BREAKDOWN</h3>
          <div className="space-y-3">
            {emotionData
              .sort((a, b) => b.value - a.value)
              .map((emotion, index) => (
                <motion.div
                  key={emotion.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center gap-4"
                >
                  <div className="flex items-center gap-2 min-w-[80px]">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: getEmotionIconColor(emotion.name) }}
                    />
                    <span className="font-medium capitalize text-sm">
                      {emotion.name}:
                    </span>
                  </div>
                  
                  {/* Terminal-style progress bar */}
                  <div className="flex-1 font-mono text-sm">
                    <span className="text-gray-300">
                      {createProgressBar(emotion.value)}
                    </span>
                  </div>
                  
                  <div className="min-w-[50px] text-right font-semibold">
                    {emotion.value.toFixed(1)}%
                  </div>
                </motion.div>
              ))}
          </div>
        </div>

        {/* EEG Band Analysis */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-white/10 mb-6">
          <h3 className="text-xl font-bold mb-4 text-center">🌊 EEG BAND ANALYSIS</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-white/5 rounded-lg">
              <div className="text-blue-400 font-semibold mb-2">Alpha (Relaxation)</div>
              <div className="text-2xl font-mono">{eegStats.alpha.avg.toFixed(3)}</div>
              <div className="text-sm text-gray-400 flex items-center justify-center gap-1">
                {getTrendEmoji(eegStats.alpha.trend)} {eegStats.alpha.trend}
              </div>
            </div>
            
            <div className="text-center p-4 bg-white/5 rounded-lg">
              <div className="text-green-400 font-semibold mb-2">Beta (Focus)</div>
              <div className="text-2xl font-mono">{eegStats.beta.avg.toFixed(3)}</div>
              <div className="text-sm text-gray-400 flex items-center justify-center gap-1">
                {getTrendEmoji(eegStats.beta.trend)} {eegStats.beta.trend}
              </div>
            </div>
            
            <div className="text-center p-4 bg-white/5 rounded-lg">
              <div className="text-yellow-400 font-semibold mb-2">Theta (Drowsiness)</div>
              <div className="text-2xl font-mono">{eegStats.theta.avg.toFixed(3)}</div>
              <div className="text-sm text-gray-400 flex items-center justify-center gap-1">
                {getTrendEmoji(eegStats.theta.trend)} {eegStats.theta.trend}
              </div>
            </div>
          </div>
        </div>

        {/* Session Statistics */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 className="text-xl font-bold mb-4 text-center">📊 SESSION STATS</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-400">{sessionStats.total_batches}</div>
              <div className="text-sm text-gray-400">Total Batches</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-teal-400">{sessionStats.total_samples}</div>
              <div className="text-sm text-gray-400">Total Samples</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-amber-400">{sessionStats.session_duration}s</div>
              <div className="text-sm text-gray-400">Session Duration</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClassificationPage;