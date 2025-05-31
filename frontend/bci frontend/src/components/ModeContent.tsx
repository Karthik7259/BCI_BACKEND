import React from 'react';
import { Brain, Flame, Waves, Heart } from 'lucide-react';

type ModeContentProps = {
  mode: string;
};

const modeData = {
  focus: {
    title: "Focus Mode",
    description: "Optimize your environment for concentration and productivity.",
    color: "blue",
    icon: Brain,
    benefits: [
      "Automatically dims lights to reduce distractions",
      "Adjusts room temperature for optimal cognitive performance",
      "Filters notifications based on priority",
      "Creates a calm soundscape to enhance concentration"
    ],
    bgGradient: "from-blue-900 to-blue-700",
    textColor: "text-blue-600"
  },
  anger: {
    title: "Anger Management Mode",
    description: "Calming environment adjustments to help regulate emotions.",
    color: "red",
    icon: Flame,
    benefits: [
      "Gradually shifts lighting to soothing colors",
      "Starts gentle cooling systems to reduce physical tension",
      "Plays calming music or nature sounds",
      "Suggests breathing exercises through ambient light patterns"
    ],
    bgGradient: "from-red-900 to-red-700",
    textColor: "text-red-600"
  },
  chill: {
    title: "Chill Mode",
    description: "Create a relaxing atmosphere for unwinding and comfort.",
    color: "teal",
    icon: Waves,
    benefits: [
      "Sets mood lighting with warm, gentle hues",
      "Maintains comfortable temperature settings",
      "Enables gentle background ambient sounds",
      "Minimizes all non-essential notifications"
    ],
    bgGradient: "from-teal-900 to-teal-700",
    textColor: "text-teal-600"
  },
  stress: {
    title: "Stress Relief Mode",
    description: "Environmental adjustments to help manage anxiety and tension.",
    color: "amber",
    icon: Heart,
    benefits: [
      "Creates a gentle breathing pattern with smart lights",
      "Activates aromatherapy diffusers if available",
      "Adjusts temperature for optimal comfort",
      "Plays guided meditation or relaxation prompts"
    ],
    bgGradient: "from-amber-900 to-amber-700",
    textColor: "text-amber-600"
  }
};

const ModeContent = ({ mode }: ModeContentProps) => {
  const modeInfo = modeData[mode as keyof typeof modeData] || modeData.focus;
  const IconComponent = modeInfo.icon;
  
  return (
    <div className="min-h-[calc(100vh-64px)]">
      {/* Hero Section */}
      <div className={`bg-gradient-to-br ${modeInfo.bgGradient} text-white py-16 md:py-24`}>
        <div className="container mx-auto px-4 text-center">
          <IconComponent className="w-16 h-16 mx-auto mb-6" />
          <h1 className="text-4xl md:text-5xl font-bold mb-4">{modeInfo.title}</h1>
          <p className="text-xl md:text-2xl max-w-2xl mx-auto">{modeInfo.description}</p>
        </div>
      </div>
      
      {/* Content Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8 -mt-16 relative z-10">
            <h2 className={`text-2xl font-bold mb-6 ${modeInfo.textColor}`}>
              How {modeInfo.title} Works
            </h2>
            
            <div className="space-y-6">
              {modeInfo.benefits.map((benefit, index) => (
                <div 
                  key={index}
                  className="flex items-start p-4 rounded-lg bg-gray-50"
                >
                  <div className={`flex-shrink-0 w-10 h-10 rounded-full ${modeInfo.textColor} bg-opacity-10 flex items-center justify-center mr-4`}>
                    <span className="font-bold">{index + 1}</span>
                  </div>
                  <p className="text-gray-700">{benefit}</p>
                </div>
              ))}
            </div>
            
            <div className="mt-10">
              <h3 className="text-xl font-semibold mb-4">Customize Your Experience</h3>
              <p className="text-gray-600 mb-6">
                Fine-tune how your environment responds to your emotional state with these adjustable settings.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Response Sensitivity</label>
                  <input 
                    type="range" 
                    min="1" 
                    max="10" 
                    className={`w-full h-2 rounded-lg appearance-none cursor-pointer bg-gray-200`}
                    style={{
                      backgroundImage: `linear-gradient(to right, ${modeInfo.color === 'blue' ? '#3B82F6' : 
                                                                  modeInfo.color === 'red' ? '#EF4444' : 
                                                                  modeInfo.color === 'teal' ? '#14B8A6' : 
                                                                  '#F59E0B'} 50%, #E5E7EB 50%)`
                    }}
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Subtle</span>
                    <span>Responsive</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Environmental Changes</label>
                  <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
                    <button className="border border-gray-300 rounded-lg py-2 px-3 text-sm bg-white hover:bg-gray-50 active:bg-gray-100">
                      Lighting
                    </button>
                    <button className="border border-gray-300 rounded-lg py-2 px-3 text-sm bg-white hover:bg-gray-50 active:bg-gray-100">
                      Sound
                    </button>
                    <button className="border border-gray-300 rounded-lg py-2 px-3 text-sm bg-white hover:bg-gray-50 active:bg-gray-100">
                      Temperature
                    </button>
                    <button className="border border-gray-300 rounded-lg py-2 px-3 text-sm bg-white hover:bg-gray-50 active:bg-gray-100">
                      Notifications
                    </button>
                  </div>
                </div>
              </div>
              
              <button 
                className={`mt-8 w-full py-3 px-4 rounded-lg font-medium text-white ${
                  modeInfo.color === 'blue' ? 'bg-blue-600 hover:bg-blue-700' : 
                  modeInfo.color === 'red' ? 'bg-red-600 hover:bg-red-700' : 
                  modeInfo.color === 'teal' ? 'bg-teal-600 hover:bg-teal-700' : 
                  'bg-amber-600 hover:bg-amber-700'
                } transition-colors`}
              >
                Activate {modeInfo.title}
              </button>
            </div>
          </div>
          
          <div className="mt-16 text-center">
            <h3 className="text-2xl font-semibold mb-6">Seamlessly Adapts to Your Needs</h3>
            <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
              Our emotion-aware system continuously learns from your preferences and behaviors to provide increasingly personalized responses.
            </p>
            
            <div className="inline-flex rounded-md shadow">
              <a
                href="/"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gray-800 hover:bg-gray-900"
              >
                Explore Other Modes
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModeContent;