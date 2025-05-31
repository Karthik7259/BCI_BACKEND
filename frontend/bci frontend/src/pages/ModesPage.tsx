import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import ModeContent from '../components/ModeContent';

const ModesPage = () => {
  const { mode } = useParams<{ mode: string }>();
  
  useEffect(() => {
    document.title = `${mode?.charAt(0).toUpperCase()}${mode?.slice(1)} Mode | EmotionControl`;
  }, [mode]);

  return (
    <div className="min-h-screen">
      <header className="bg-white shadow-sm p-4">
        <div className="container mx-auto flex items-center">
          <Link 
            to="/" 
            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
          >
            <ArrowLeft size={20} className="mr-2" />
            <span>Back to Home</span>
          </Link>
        </div>
      </header>
      <ModeContent mode={mode || 'focus'} />
    </div>
  );
};

export default ModesPage;