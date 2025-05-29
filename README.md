# AI Doctor VoiceBot 🩺🤖

An intelligent voice-enabled chatbot designed to provide medical consultations and health-related assistance. Built with FastAPI backend and React frontend, featuring advanced speech recognition and text-to-speech capabilities.

## ✨ Features

- **Voice Interaction** - Natural speech input and audio responses
- **AI-Powered Consultations** - Powered by Groq AI for intelligent medical conversations
- **Multiple TTS Options** - ElevenLabs and Google Text-to-Speech integration
- **Real-time Processing** - Fast response times for seamless conversation
- **Modern Web Interface** - Responsive React frontend with intuitive design
- **Cross-Platform** - Works on desktop and mobile browsers

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Groq** - AI language model for medical consultations
- **ElevenLabs** - Premium text-to-speech service
- **Google TTS (gTTS)** - Alternative text-to-speech
- **SpeechRecognition** - Voice input processing
- **Pydub** - Audio file manipulation
- **Uvicorn** - ASGI server

### Frontend
- **React** - Modern JavaScript library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Responsive design
- **Web Audio API** - Browser-based audio handling

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn package manager

## 🚀 Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/yourusername/ai-doctor-voicebot.git
cd ai-doctor-voicebot
```

### 2. Backend Setup
```
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 3. Frontend Setup
```
# Navigate to frontend directory
cd ../frontend

# Install Node dependencies
npm install
```

### 4. Environment Configuration

Create a `.env` file in the backend directory with your API keys:

```env
# AI Service
GROQ_API_KEY=your_groq_api_key_here

# Text-to-Speech Services
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional Configuration
ENVIRONMENT=development
DEBUG=True
```

### 5. API Keys Setup

#### Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login and create an API key
3. Add to your `.env` file

#### ElevenLabs API Key (Optional)
1. Visit [ElevenLabs](https://elevenlabs.io/)
2. Sign up and get your API key
3. Add to your `.env` file

## 🏃‍♂️ Running the Application

### Development Mode

#### Start Backend Server
```
cd backend
python main.py
# Server runs on http://localhost:8000
```

#### Start Frontend Development Server
```
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### Production Build

#### Build Frontend
```
cd frontend
npm run build
```

#### Run Production Server
```
cd backend
python main.py
# Serves both API and built frontend
```

## 📁 Project Structure

```
ai-doctor-voicebot/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── response.py             # TTS response handlers
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   └── dist/                   # Built frontend files
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Application pages
│   │   ├── utils/              # Utility functions
│   │   └── App.jsx             # Main App component
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── index.html              # HTML template
├── README.md
└── .gitignore
```

## 🌐 API Endpoints

### Health Check
```
GET /api/health
```

### Process Audio
```
POST /api/process-audio
Content-Type: multipart/form-data
Body: audio file
```

### Text Chat
```
POST /api/chat
Content-Type: application/json
Body: {"message": "your message here"}
```

## 🚀 Deployment

### Deploy to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [Render.com](https://render.com)
   - Connect your GitHub repository
   - Configure as Web Service

3. **Build Settings**
   - **Build Command**: `cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Root Directory**: `backend`

4. **Environment Variables**
   Add your API keys in Render dashboard:
   - `GROQ_API_KEY`
   - `ELEVENLABS_API_KEY`

### Deploy to Other Platforms

The application can be deployed to:
- **Heroku** - Add Procfile: `web: cd backend && python main.py`
- **Railway** - Connect GitHub repo and configure build settings
- **DigitalOcean App Platform** - Use the same build configuration
- **AWS/GCP/Azure** - Deploy using container services

## 🔧 Configuration

### Customizing TTS Services

Edit `response.py` to configure text-to-speech preferences:

```
# Prefer ElevenLabs for premium quality
USE_ELEVENLABS = True

# Fallback to Google TTS
USE_GTTS = True

# Voice settings
ELEVENLABS_VOICE_ID = "your_preferred_voice_id"
```

### Adjusting AI Behavior

Modify the system prompt in your main application logic to customize the AI doctor's personality and responses.

## 🐛 Troubleshooting

### Common Issues

1. **PyAudio Installation Error**
   - Remove PyAudio from requirements.txt for cloud deployment
   - Use web-based audio recording instead

2. **API Key Errors**
   - Verify all API keys are correctly set in environment variables
   - Check API key permissions and quotas

3. **Audio Not Playing**
   - Ensure browser permissions for microphone/audio
   - Check network connectivity for TTS services
   - Verify audio file formats are supported

4. **Build Failures**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js and Python versions
   - Verify all dependencies are listed in requirements.txt

### Getting Help

- Check the [Issues](https://github.com/yourusername/ai-doctor-voicebot/issues) page
- Review deployment logs for specific error messages
- Ensure all environment variables are properly configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This AI Doctor VoiceBot is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: theshayarguyjaani@example.com
- Documentation: [Project Wiki](https://github.com/JaaniCoder/AI-Doctor-Voicebot/wiki)

---

**Made with ❤️ for better healthcare accessibility**
