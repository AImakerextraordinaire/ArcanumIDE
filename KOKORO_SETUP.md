# 🎭 Kokoro TTS Server Setup Guide

Transform your ArcanumIDE with magical, character-specific voices!

## 🚀 Quick Setup

### 1. Run the Setup Script
```bash
python setup_kokoro.py
```

This will automatically:
- ✅ Check Python version (3.8+ required)
- ✅ Install system dependencies (espeak on Linux/macOS)
- ✅ Create virtual environment
- ✅ Install Python packages
- ✅ Test the installation
- ✅ Create start scripts

### 2. Start the Server

**Windows:**
```bash
start_kokoro.bat
```

**Linux/macOS:**
```bash
./start_kokoro.sh
```

**Manual start:**
```bash
# Windows
kokoro_venv\Scripts\python kokoro_tts_server.py

# Linux/macOS
kokoro_venv/bin/python kokoro_tts_server.py
```

### 3. Verify It's Working
- Open browser to: http://localhost:5002/health
- Should see: `{"status": "healthy", ...}`
- Test voices at: http://localhost:5002/test/kiro_assistant

## 🎭 Available Magical Voices

| Voice ID | Character | Language | Gender | Personality |
|----------|-----------|----------|---------|-------------|
| `elvish_female` | Arwen | Elvish | Female | Gentle, wise |
| `elvish_male` | Legolas | Elvish | Male | Noble, clear |
| `draconic_male` | Smaug | Draconic | Male | Deep, powerful |
| `draconic_female` | Tiamat | Draconic | Female | Commanding |
| `orcish_male` | Uruk | Orcish | Male | Gruff, direct |
| `orcish_female` | Ghashak | Orcish | Female | Fierce, strong |
| `kiro_assistant` | Kiro | Neutral | Female | Friendly, enthusiastic |

## 🔧 API Endpoints

### Health Check
```
GET /health
```

### Get Available Voices
```
GET /voices
```

### Synthesize Speech
```
POST /synthesize
Content-Type: application/json

{
  "text": "Mae govannen! Welcome to the magical realm!",
  "voice": "elvish_female",
  "speed": 1.0,
  "pitch": 0.0,
  "emotion": "happy"
}
```

### Test Voice
```
GET /test/{voice_id}
```

## 🐛 Troubleshooting

### Common Issues

**"TTS engine not initialized"**
- Windows: Should work out of the box
- Linux: Install espeak: `sudo apt-get install espeak espeak-data`
- macOS: Install espeak: `brew install espeak`

**"Port 5002 already in use"**
- Kill existing process: `lsof -ti:5002 | xargs kill -9`
- Or change port in `kokoro_tts_server.py`

**"Module not found" errors**
- Activate virtual environment first:
  - Windows: `kokoro_venv\Scripts\activate`
  - Linux/macOS: `source kokoro_venv/bin/activate`

### Manual Installation

If the setup script fails:

```bash
# Create virtual environment
python -m venv kokoro_venv

# Activate it
# Windows:
kokoro_venv\Scripts\activate
# Linux/macOS:
source kokoro_venv/bin/activate

# Install dependencies
pip install -r kokoro_requirements.txt

# Start server
python kokoro_tts_server.py
```

## 🎵 Testing Your Setup

1. **Start the server**
2. **Open ArcanumIDE**
3. **Enable audio in the Agentic Spell Crafter**
4. **Listen for the magical greeting!**

You should now hear Kiro's natural, friendly voice instead of robotic speech!

## 🌟 Advanced Configuration

### Custom Voice Characteristics

Edit `kokoro_tts_server.py` to modify voice characteristics:

```python
'kiro_assistant': {
    'name': 'Kiro',
    'base_voice': 'female',
    'pitch_shift': 0.1,        # Higher = more feminine
    'speed_factor': 1.0,       # 1.0 = normal speed
    'emotion': 'friendly',
    'characteristics': {
        'breathiness': 0.1,    # 0.0-1.0
        'warmth': 0.9,         # 0.0-1.0
        'clarity': 0.95,       # 0.0-1.0
        'enthusiasm': 0.7      # 0.0-1.0
    }
}
```

### Adding New Voices

Add new voice configurations to the `voice_configs` dictionary in `kokoro_tts_server.py`.

## 🎉 Success!

Once running, your ArcanumIDE will have:
- ✨ Natural, character-specific voices
- 🎭 Magical personality for each language
- 🎵 High-quality audio synthesis
- 🚀 Responsive, low-latency speech

**Ready to experience truly magical audio!** 🧙‍♂️⚡