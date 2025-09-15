# 🛠️ Manual Kokoro TTS Setup (Windows)

If the automated setup fails, follow these manual steps:

## 🚀 Quick Manual Setup

### 1. Create Virtual Environment
```cmd
python -m venv kokoro_venv
```

### 2. Activate Virtual Environment
```cmd
kokoro_venv\Scripts\activate
```

### 3. Install Dependencies
```cmd
python -m pip install --upgrade pip
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install pyttsx3==2.90
pip install torch==2.0.1
pip install torchaudio==2.0.2
pip install numpy==1.24.3
```

### 4. Test Installation
```cmd
python -c "import pyttsx3, flask; print('✅ Ready!')"
```

### 5. Start Server
```cmd
python kokoro_tts_server.py
```

## 🎯 Alternative: Use Simple Batch File

Just double-click: **`setup_kokoro_simple.bat`**

This will do all the steps above automatically.

## 🐛 Common Issues

### **"pip upgrade failed"**
- **Solution**: Ignore this error, it's just a permission issue
- **Alternative**: Run as Administrator

### **"torch installation failed"**
- **Solution**: Install CPU-only version:
  ```cmd
  pip install torch==2.0.1+cpu torchaudio==2.0.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
  ```

### **"pyttsx3 not working"**
- **Windows**: Should work out of the box
- **Alternative**: Try `pip install pyttsx3==2.71` (older version)

### **"Module not found"**
- **Solution**: Make sure virtual environment is activated:
  ```cmd
  kokoro_venv\Scripts\activate
  ```

## ✅ Verify Setup

1. **Start server**: `python kokoro_tts_server.py`
2. **Check health**: Open http://localhost:5002/health
3. **Test voice**: Open http://localhost:5002/test/kiro_assistant

## 🎉 Success!

Once running, your ArcanumIDE will automatically detect the Kokoro server and use beautiful, natural voices instead of robotic speech!

**The magical audio experience awaits!** 🎭✨