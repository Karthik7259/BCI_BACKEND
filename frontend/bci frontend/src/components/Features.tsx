import React from 'react';
import { Brain, Home, Shield, Globe } from 'lucide-react';

const Features = () => {
  return (
    <div id="features" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-16 text-gray-900">
          Key Benefits
        </h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard 
            icon={<Brain className="w-12 h-12 text-blue-600" />}
            title="Emotion-Aware"
            description="Understands your emotional and physical state in real time to provide the right response when you need it."
          />
          
          <FeatureCard 
            icon={<Home className="w-12 h-12 text-blue-600" />}
            title="Smart Home Control"
            description="Seamlessly controls lights, fans, and other appliances with no physical interaction required."
          />
          
          <FeatureCard 
            icon={<Shield className="w-12 h-12 text-blue-600" />}
            title="Non-Invasive"
            description="No cameras or wearables required, respecting your privacy while providing assistance."
          />
          
          <FeatureCard 
            icon={<Globe className="w-12 h-12 text-blue-600" />}
            title="Universal Design"
            description="Designed for accessibility, inclusivity, and dignity for all users regardless of ability."
          />
        </div>
        
        <div className="mt-16 text-center">
          <p className="text-xl font-medium text-gray-700 italic">
            "Smart. Sensitive. Seamlessly Yours."
          </p>
        </div>
      </div>
    </div>
  );
};

const FeatureCard = ({ 
  icon, 
  title, 
  description 
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string 
}) => {
  return (
    <div className="bg-gray-50 p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-3 text-gray-900">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default Features;