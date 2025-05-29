import React, { useState, useRef, useCallback } from 'react';
import { Mic, MicOff, Upload, Camera, Send, Volume2, Brain, Heart, Stethoscope, Activity } from 'lucide-react';

const AIDocterVoiceBot = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState('');
  const [speechText, setSpeechText] = useState('');
  const [doctorResponse, setDoctorResponse] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [audioResponse, setAudioResponse] = useState('');
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);

  // Enhanced floating background elements
  const FloatingElement = ({ children, className, delay = 0 }) => (
    <div className={`absolute opacity-10 animate-pulse ${className}`} 
         style={{ animationDelay: `${delay}s`, animationDuration: '4s' }}>
      {children}
    </div>
  );

  // Start/Stop recording
  const toggleRecording = useCallback(async () => {
    if (!isRecording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];

        mediaRecorderRef.current.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };

        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/mp3' });
          setAudioBlob(audioBlob);
          stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorderRef.current.start();
        setIsRecording(true);
      } catch (error) {
        console.error('Error starting recording:', error);
        alert('Failed to start recording. Please check microphone permissions.');
      }
    } else {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  // Handle image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  // Submit analysis
  const submitAnalysis = async () => {
    if (!selectedImage && !audioBlob) {
      alert('Please provide either an image or voice input.');
      return;
    }

    setIsAnalyzing(true);
    const formData = new FormData();
    
    if (audioBlob) {
      formData.append('audio', audioBlob, 'recording.mp3');
    }
    if (selectedImage) {
      formData.append('image', selectedImage);
    }

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setSpeechText(result.speech_to_text || '');
      setDoctorResponse(result.doctor_response || '');
      
      if (result.has_audio_response) {
        setAudioResponse(`/api/audio/${result.session_id}`);
      }
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Play audio response
  const playAudioResponse = () => {
    if (audioResponse) {
      const audio = new Audio(audioResponse);
      audio.play().catch(console.error);
    }
  };

  // Reset all inputs
  const resetAll = () => {
    setAudioBlob(null);
    setSelectedImage(null);
    setImagePreview('');
    setSpeechText('');
    setDoctorResponse('');
    setAudioResponse('');
    setIsRecording(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
      {/* Animated background elements */}
      <FloatingElement className="top-10 left-10" delay={0}>
        <Heart size={60} className="text-red-300" />
      </FloatingElement>
      <FloatingElement className="top-32 right-20" delay={1}>
        <Brain size={80} className="text-purple-300" />
      </FloatingElement>
      <FloatingElement className="bottom-20 left-32" delay={2}>
        <Stethoscope size={70} className="text-blue-300" />
      </FloatingElement>
      <FloatingElement className="bottom-32 right-10" delay={0.5}>
        <Activity size={90} className="text-green-300" />
      </FloatingElement>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mb-6 shadow-2xl">
            <Stethoscope size={40} className="text-white" />
          </div>
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            AI Doctor Vision
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Advanced medical analysis powered by AI. Upload an image and describe your concerns for instant professional insights.
          </p>
        </div>

        {/* Main Interface */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 mb-8">
            <div className="grid md:grid-cols-2 gap-8">
              
              {/* Voice Input Section */}
              <div className="space-y-6">
                <h3 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
                  <Mic className="mr-3 text-blue-500" size={28} />
                  Voice Input
                </h3>
                
                <div className="text-center">
                  <button
                    onClick={toggleRecording}
                    className={`relative w-32 h-32 rounded-full border-4 transition-all duration-300 ${
                      isRecording 
                        ? 'border-red-500 bg-red-500 shadow-lg shadow-red-500/30 animate-pulse' 
                        : 'border-blue-500 bg-blue-500 hover:shadow-lg hover:shadow-blue-500/30'
                    }`}
                  >
                    {isRecording ? (
                      <MicOff size={40} className="text-white mx-auto" />
                    ) : (
                      <Mic size={40} className="text-white mx-auto" />
                    )}
                  </button>
                  <p className="mt-4 text-gray-600">
                    {isRecording ? 'Recording... Click to stop' : 'Click to start recording'}
                  </p>
                </div>

                {audioBlob && (
                  <div className="p-4 bg-green-50 rounded-xl border border-green-200">
                    <p className="text-green-700 text-center">✓ Audio recorded successfully</p>
                  </div>
                )}
              </div>

              {/* Image Upload Section */}
              <div className="space-y-6">
                <h3 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
                  <Camera className="mr-3 text-purple-500" size={28} />
                  Medical Image
                </h3>

                <div className="space-y-4">
                  <div className="flex gap-4">
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="flex-1 py-3 px-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:shadow-lg transition-all duration-300 flex items-center justify-center"
                    >
                      <Upload className="mr-2" size={20} />
                      Upload Image
                    </button>
                    <button
                      onClick={() => cameraInputRef.current?.click()}
                      className="flex-1 py-3 px-6 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-xl hover:shadow-lg transition-all duration-300 flex items-center justify-center"
                    >
                      <Camera className="mr-2" size={20} />
                      Take Photo
                    </button>
                  </div>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                  <input
                    ref={cameraInputRef}
                    type="file"
                    accept="image/*"
                    capture="environment"
                    onChange={handleImageUpload}
                    className="hidden"
                  />

                  {imagePreview && (
                    <div className="relative">
                      <img
                        src={imagePreview}
                        alt="Preview"
                        className="w-full h-48 object-cover rounded-xl border-2 border-gray-200"
                      />
                      <button
                        onClick={() => {
                          setSelectedImage(null);
                          setImagePreview('');
                        }}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
                      >
                        ×
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mt-8 justify-center">
              <button
                onClick={submitAnalysis}
                disabled={isAnalyzing || (!selectedImage && !audioBlob)}
                className="px-8 py-4 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-xl hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center text-lg font-semibold"
              >
                {isAnalyzing ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Send className="mr-3" size={20} />
                    Analyze
                  </>
                )}
              </button>
              
              <button
                onClick={resetAll}
                className="px-8 py-4 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:shadow-lg transition-all duration-300 text-lg font-semibold"
              >
                Reset
              </button>
            </div>
          </div>

          {/* Results Section */}
          {(speechText || doctorResponse) && (
            <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 space-y-6">
              <h3 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
                Analysis Results
              </h3>

              {speechText && (
                <div className="p-6 bg-blue-50 rounded-xl border border-blue-200">
                  <h4 className="font-semibold text-blue-800 mb-3 flex items-center">
                    <Mic className="mr-2" size={20} />
                    Your Voice Input:
                  </h4>
                  <p className="text-blue-700">{speechText}</p>
                </div>
              )}

              {doctorResponse && (
                <div className="p-6 bg-green-50 rounded-xl border border-green-200">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-green-800 flex items-center">
                      <Stethoscope className="mr-2" size={20} />
                      Doctor's Analysis:
                    </h4>
                    {audioResponse && (
                      <button
                        onClick={playAudioResponse}
                        className="p-2 bg-green-500 text-white rounded-full hover:bg-green-600 transition-colors"
                        title="Play audio response"
                      >
                        <Volume2 size={20} />
                      </button>
                    )}
                  </div>
                  <p className="text-green-700 leading-relaxed">{doctorResponse}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p className="text-sm">
            ⚠️ This is an AI-powered tool for educational purposes only. Always consult with a qualified healthcare professional for medical advice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AIDocterVoiceBot;  