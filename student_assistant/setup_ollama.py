#!/usr/bin/env python3
"""
Setup script for Ollama AI integration
This script helps install and configure Ollama for the AI Learning Assistant
"""

import os
import sys
import requests
import subprocess
import time
import platform

def print_header():
    print("🚀 " + "="*60)
    print("🤖 FUTURISTIC AI LEARNING ASSISTANT SETUP")
    print("🧠 Ollama AI Integration Setup")
    print("="*64)
    print()

def check_system():
    """Check system requirements"""
    system = platform.system()
    print(f"🖥️  System: {system}")
    print(f"🐍 Python: {sys.version}")
    print()
    return system

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is already installed!")
            print(f"📋 Version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama not found")
    return False

def install_ollama():
    """Provide installation instructions for Ollama"""
    system = platform.system()
    
    print("📦 OLLAMA INSTALLATION INSTRUCTIONS")
    print("="*40)
    
    if system == "Windows":
        print("🪟 Windows Installation:")
        print("1. Go to: https://ollama.ai/download")
        print("2. Download the Windows installer")
        print("3. Run the installer")
        print("4. Restart your terminal/command prompt")
        print()
        print("Alternative (if you have winget):")
        print("   winget install Ollama.Ollama")
        
    elif system == "Darwin":  # macOS
        print("🍎 macOS Installation:")
        print("1. Go to: https://ollama.ai/download")
        print("2. Download the macOS installer")
        print("3. Install the .dmg file")
        print()
        print("Alternative (if you have Homebrew):")
        print("   brew install ollama")
        
    elif system == "Linux":
        print("🐧 Linux Installation:")
        print("Run this command:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
        print()
        
    print("⚠️  After installation, please restart your terminal!")
    return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running!")
            return True
    except:
        pass
    
    print("❌ Ollama service is not running")
    return False

def start_ollama_service():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    
    try:
        if platform.system() == "Windows":
            # On Windows, Ollama usually runs as a service
            subprocess.Popen(['ollama', 'serve'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # On Unix-like systems
            subprocess.Popen(['ollama', 'serve'])
        
        print("⏳ Waiting for service to start...")
        time.sleep(5)
        
        if check_ollama_running():
            return True
        else:
            print("❌ Failed to start Ollama service")
            print("💡 Try running 'ollama serve' manually in another terminal")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        print("💡 Try running 'ollama serve' manually in another terminal")
        return False

def install_model():
    """Install the default AI model"""
    model = "llama2"
    print(f"📥 Installing AI model: {model}")
    print("⏳ This may take several minutes depending on your internet speed...")
    
    try:
        result = subprocess.run(['ollama', 'pull', model], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Model {model} installed successfully!")
            return True
        else:
            print(f"❌ Failed to install model: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing model: {e}")
        return False

def list_available_models():
    """List available models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Installed models:")
            print(result.stdout)
            return True
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

def test_ai_response():
    """Test AI response"""
    print("🧪 Testing AI response...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "What is Python programming? Answer in one sentence.",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'No response')
            print("✅ AI Test Successful!")
            print(f"🤖 AI Response: {ai_response[:100]}...")
            return True
        else:
            print(f"❌ AI test failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI test error: {e}")
        return False

def main():
    print_header()
    
    # Check system
    system = check_system()
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        install_ollama()
        input("Press Enter after installing Ollama...")
        
        # Check again
        if not check_ollama_installed():
            print("❌ Ollama still not found. Please check installation.")
            sys.exit(1)
    
    # Check if service is running
    if not check_ollama_running():
        if not start_ollama_service():
            print("❌ Could not start Ollama service")
            print("💡 Please run 'ollama serve' in another terminal and try again")
            sys.exit(1)
    
    # Install model
    print("\n📦 INSTALLING AI MODEL")
    print("="*25)
    
    # Check if model is already installed
    list_available_models()
    
    user_input = input("\nDo you want to install/update the llama2 model? (y/N): ")
    if user_input.lower() in ['y', 'yes']:
        if not install_model():
            print("❌ Model installation failed")
            sys.exit(1)
    
    # Test AI
    print("\n🧪 TESTING AI INTEGRATION")
    print("="*26)
    if test_ai_response():
        print("✅ Setup complete! Your AI Learning Assistant is ready!")
    else:
        print("❌ AI test failed. Please check the setup.")
        sys.exit(1)
    
    print("\n🎉 SUCCESS!")
    print("="*15)
    print("Your Futuristic AI Learning Assistant is ready!")
    print("Now run: python enhanced_app.py")
    print()
    print("🌟 Features available:")
    print("   ✨ Dynamic course popups")
    print("   🧠 AI-powered recommendations")
    print("   💬 Real-time AI chat")
    print("   🎤 Voice search")
    print("   📊 Progress tracking")
    print("   🎮 Gamification")
    print("   🌓 Dark/Light mode")
    print()

if __name__ == "__main__":
    main() 