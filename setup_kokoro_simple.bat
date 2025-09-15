@echo off
echo 🎭 Kokoro TTS Server - Simple Windows Setup
echo ==========================================
cd C:\Users\Admin\source\repos\Alex_Consciousness\ArcanumIDE
REM Create virtual environment
echo 🐍 Creating virtual environment...
python -m venv kokoro_venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo Make sure Python 3.8+ is installed
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo 📚 Installing dependencies...
kokoro_venv\Scripts\python.exe -m pip install --upgrade pip
kokoro_venv\Scripts\pip.exe install -r kokoro_requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Test installation
echo 🧪 Testing installation...
kokoro_venv\Scripts\python.exe -c "import pyttsx3, flask; print('✅ All imports successful!')"
if errorlevel 1 (
    echo ⚠️ Some imports failed, but server might still work
)

REM Create start script
echo @echo off > start_kokoro.bat
echo echo 🎭 Starting Kokoro TTS Server... >> start_kokoro.bat
echo kokoro_venv\Scripts\python.exe kokoro_tts_server.py >> start_kokoro.bat
echo pause >> start_kokoro.bat

echo.
echo 🎉 Setup complete!
echo.
echo 🚀 To start the server:
echo    Double-click: start_kokoro.bat
echo    Or run: kokoro_venv\Scripts\python.exe kokoro_tts_server.py
echo.
echo 🌟 Server will be available at: http://localhost:5002
echo.
pause