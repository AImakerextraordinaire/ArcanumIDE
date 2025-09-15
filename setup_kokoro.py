#!/usr/bin/env python3
"""
Kokoro TTS Server Setup Script
Automatically installs dependencies and sets up the TTS server
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_system_dependencies():
    """Install system-level dependencies"""
    system = platform.system().lower()
    
    if system == "windows":
        print("🪟 Windows detected - TTS should work out of the box")
        return True
    elif system == "darwin":  # macOS
        print("🍎 macOS detected")
        return run_command("brew install espeak espeak-data", "Installing espeak via Homebrew")
    elif system == "linux":
        print("🐧 Linux detected")
        # Try different package managers
        if os.system("which apt-get > /dev/null 2>&1") == 0:
            return run_command("sudo apt-get update && sudo apt-get install -y espeak espeak-data libespeak-dev", "Installing espeak via apt")
        elif os.system("which yum > /dev/null 2>&1") == 0:
            return run_command("sudo yum install -y espeak espeak-devel", "Installing espeak via yum")
        elif os.system("which pacman > /dev/null 2>&1") == 0:
            return run_command("sudo pacman -S espeak espeak-data", "Installing espeak via pacman")
        else:
            print("⚠️ Could not detect package manager. Please install espeak manually.")
            return False
    else:
        print(f"⚠️ Unknown system: {system}")
        return False

def setup_virtual_environment():
    """Set up Python virtual environment"""
    venv_path = Path("kokoro_venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    if not run_command(f"{sys.executable} -m venv kokoro_venv", "Creating virtual environment"):
        return False
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    system = platform.system().lower()
    
    if system == "windows":
        pip_cmd = "kokoro_venv\\Scripts\\pip"
        python_cmd = "kokoro_venv\\Scripts\\python"
    else:
        pip_cmd = "kokoro_venv/bin/pip"
        python_cmd = "kokoro_venv/bin/python"
    
    # Try to upgrade pip (don't fail if this doesn't work)
    print("🔧 Attempting to upgrade pip...")
    try:
        # Use python -m pip instead of direct pip command for Windows
        upgrade_cmd = f"{python_cmd} -m pip install --upgrade pip"
        result = subprocess.run(upgrade_cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Pip upgrade completed successfully")
    except subprocess.CalledProcessError as e:
        print("⚠️ Pip upgrade failed, but continuing with installation...")
        print(f"   (This is usually fine - pip will still work)")
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r kokoro_requirements.txt", "Installing Python dependencies"):
        # Try alternative installation method
        print("🔄 Trying alternative installation method...")
        return run_command(f"{python_cmd} -m pip install -r kokoro_requirements.txt", "Installing Python dependencies (alternative method)")
    
    return True

def test_installation():
    """Test the installation"""
    system = platform.system().lower()
    
    if system == "windows":
        python_cmd = "kokoro_venv\\Scripts\\python"
    else:
        python_cmd = "kokoro_venv/bin/python"
    
    test_script = '''
import pyttsx3
import flask
import torch
print("✅ All imports successful!")

# Test TTS engine
try:
    engine = pyttsx3.init()
    print("✅ TTS engine initialized successfully!")
except Exception as e:
    print(f"⚠️ TTS engine test failed: {e}")
'''
    
    with open("test_kokoro.py", "w") as f:
        f.write(test_script)
    
    success = run_command(f"{python_cmd} test_kokoro.py", "Testing installation")
    
    # Clean up test file
    try:
        os.remove("test_kokoro.py")
    except:
        pass
    
    return success

def create_start_script():
    """Create convenient start script"""
    system = platform.system().lower()
    
    if system == "windows":
        script_content = '''@echo off
echo 🎭 Starting Kokoro TTS Server...
kokoro_venv\\Scripts\\python kokoro_tts_server.py
pause
'''
        with open("start_kokoro.bat", "w") as f:
            f.write(script_content)
        print("✅ Created start_kokoro.bat")
    else:
        script_content = '''#!/bin/bash
echo "🎭 Starting Kokoro TTS Server..."
kokoro_venv/bin/python kokoro_tts_server.py
'''
        with open("start_kokoro.sh", "w") as f:
            f.write(script_content)
        os.chmod("start_kokoro.sh", 0o755)
        print("✅ Created start_kokoro.sh")

def main():
    """Main setup function"""
    print("🎭 Kokoro TTS Server Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install system dependencies
    print("\n📦 Installing system dependencies...")
    if not install_system_dependencies():
        print("⚠️ System dependencies installation failed, but continuing...")
    
    # Set up virtual environment
    print("\n🐍 Setting up Python virtual environment...")
    if not setup_virtual_environment():
        return False
    
    # Install Python dependencies
    print("\n📚 Installing Python dependencies...")
    if not install_python_dependencies():
        return False
    
    # Test installation
    print("\n🧪 Testing installation...")
    if not test_installation():
        print("⚠️ Installation test failed, but server might still work")
    
    # Create start script
    print("\n📝 Creating start script...")
    create_start_script()
    
    print("\n🎉 Kokoro TTS Server setup complete!")
    print("\n🚀 To start the server:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   Double-click: start_kokoro.bat")
        print("   Or run: kokoro_venv\\Scripts\\python kokoro_tts_server.py")
    else:
        print("   Run: ./start_kokoro.sh")
        print("   Or run: kokoro_venv/bin/python kokoro_tts_server.py")
    
    print("\n🌟 Server will be available at: http://localhost:5002")
    print("🎭 Available magical voices:")
    print("   • Arwen (Elvish Female)")
    print("   • Legolas (Elvish Male)")
    print("   • Smaug (Draconic Male)")
    print("   • Tiamat (Draconic Female)")
    print("   • Uruk (Orcish Male)")
    print("   • Ghashak (Orcish Female)")
    print("   • Kiro (AI Assistant)")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✨ Setup successful! Ready to cast audio spells!")